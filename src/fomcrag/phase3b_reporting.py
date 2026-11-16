"""Read-only 3B diagnostics on seed qrels; no inference or human-label synthesis."""
from __future__ import annotations
from collections import Counter
import json
from pathlib import Path
import statistics

from .annotation_review import read_csv
from .indexing import load_baseline
from .phase3_extension import ARCHIVED, METHODS, historical_run, verify_history
from .pooling import build_pool
from .retrieval import stable_ranking
from .retrieval_evaluation import page_diagnostics
from .retrieval_experiments import read_grades
from .retrieval_reporting import CONVENTIONS, bootstrap_interval, review_queue, validate_saved_run, write_csv
from .selection import phase3_questions
from .storage import file_hash, read_jsonl, write_json, write_jsonl


def report_extension(root: Path):
    import numpy as np
    history = verify_history(root)
    base = root/"artifacts/phase3_extension"
    output = root/"reports/retrieval_phase3_extension"
    seal = json.loads((base/"dev_seal.json").read_text(encoding="utf-8"))
    config = seal["config"]
    old = json.loads((root/"configs/retrieval_phase3.json").read_text(encoding="utf-8"))
    chunks, identity = load_baseline(root, old)
    by_id = {c["chunk_id"]:c for c in chunks}
    old_pairs = {(r["question_id"], r["page_id"]) for r in read_csv(root/"reports/retrieval_phase3/new_pages_review_queue.csv")}
    metrics, aggregate, latency, paired, resources, pools, all_queries, delta_rows = [], [], [], [], {}, {}, {}, []
    new_review = []
    for split in ("dev", "validation"):
        queries, selection = phase3_questions(root, split)
        all_queries.update({q["question_id"]:q for q in queries})
        completed = json.loads((base/split/"completed.json").read_text(encoding="utf-8"))
        if completed["config_id"] != seal["config_id"] or completed["test_executed"] or not completed["seed_qrels_only"]:
            raise ValueError("Unexpected extension completion state")
        grades = read_grades(root, set(selection["selected_question_ids"]))
        runs = {}
        for method in METHODS:
            if method in ARCHIVED:
                _, records = historical_run(root, split, ARCHIVED[method], queries, chunks, identity)
            else:
                path = base/split/(method+".jsonl")
                records = read_jsonl(path)
                validate_saved_run(records, queries, by_id, identity, seal["config_id"], method)
                with np.load(base/split/(method+"_complete.npz"), allow_pickle=False) as data:
                    ids = data["chunk_ids"].tolist()
                    scores, ranks = data["scores"], data["ranks"]
                    if ids != [c["chunk_id"] for c in chunks] or data["question_ids"].tolist() != [q["question_id"] for q in queries]:
                        raise ValueError("New full matrices differ from common identities")
                    for i, row in enumerate(records):
                        rank = stable_ranking(scores[i], ids)
                        if ranks[i].tolist() != rank:
                            raise ValueError("New rankings not deterministic")
                        for j, hit in zip(rank, row["retrieved"]):
                            if hit["chunk_id"] != chunks[j]["chunk_id"] or hit["score"] != float(scores[i][j]):
                                raise ValueError("NPZ and JSONL scores/IDs differ")
                            if method == "HybridWindowMean" and abs(sum(x["contribution"] for x in hit["rrf_contributions"].values())-hit["score"]) > 1e-12:
                                raise ValueError("Incorrect new RRF contributions")
            runs[method] = records
            for row in records:
                for convention in CONVENTIONS:
                    for k in config["budgets"]:
                        metrics.append(dict(split=split, method=method, question_id=row["question_id"],
                            convention=convention, k=k, reference="ORIGINAL_SEED", **page_diagnostics(row["retrieved"], grades[row["question_id"]], k, convention)))
            latency.append(dict(split=split, method=method, source="archived phase3" if method in ARCHIVED else "new phase3B",
                kind=records[0]["latency_kind"],
                p50_ms=float(np.percentile([r["retrieval_ms"] for r in records],50)),
                p95_ms=float(np.percentile([r["retrieval_ms"] for r in records],95)),
                repeat_p50_ms=float(np.percentile([r["repeat_ms"] for r in records],50)),
                repeat_p95_ms=float(np.percentile([r["repeat_ms"] for r in records],95))))
        for method in METHODS:
            for convention in CONVENTIONS:
                for k in config["budgets"]:
                    subset = [r for r in metrics if (r["split"], r["method"], r["convention"], r["k"]) == (split, method, convention, k)]
                    numeric = ("known_positive_coverage", "known_positive_hit", "known_positive_page_rr", "seed_ndcg",
                        "unjudged_fraction", "unjudged_pages", "unique_pages", "unique_documents", "consumed_chunks")
                    low, high = bootstrap_interval([r["known_positive_coverage"] for r in subset], config["seed"])
                    aggregate.append(dict(split=split, method=method, convention=convention, k=k, queries=len(subset), reference="ORIGINAL_SEED",
                        **{name:statistics.mean(r[name] for r in subset) for name in numeric}, ci_low=low, ci_high=high))
        for new, reference in (("DenseWindowMean", "Dense128"), ("HybridWindowMean", "Hybrid128"), ("DenseWindowMean", "BM25_L0"), ("HybridWindowMean", "BM25_L0")):
            values = {m:{r["question_id"]:r["known_positive_coverage"] for r in metrics if r["split"] == split and r["method"] == m and r["k"] == 5 and r["convention"] == CONVENTIONS[0]} for m in (new, reference)}
            differences = [values[new][q["question_id"]]-values[reference][q["question_id"]] for q in queries]
            low, high = bootstrap_interval(differences, config["seed"])
            paired.append(dict(split=split, comparison=new+" minus "+reference, metric="strict known coverage@5", difference=statistics.mean(differences),
                ci_low=low, ci_high=high, improved=sum(d>0 for d in differences), worsened=sum(d<0 for d in differences), unchanged=sum(d==0 for d in differences)))
            for query, difference in zip(queries, differences):
                qid = query["question_id"]
                records = {m:next(r for r in runs[m] if r["question_id"] == qid) for m in (new, reference)}
                delta_rows.append(dict(split=split, question_id=qid, method=new, reference=reference, coverage_delta_at5=difference,
                    first_source_new=records[new]["retrieved"][0]["page_id"], first_source_reference=records[reference]["retrieved"][0]["page_id"],
                    first_positive_chunk_rank_new=next((r["rank"] for r in records[new]["retrieved"] if r["page_id"] in grades[qid]), "NOT_IN_TOP100"),
                    first_positive_chunk_rank_reference=next((r["rank"] for r in records[reference]["retrieved"] if r["page_id"] in grades[qid]), "NOT_IN_TOP100")))
        page_grades = {(q,p):g for q,pages in grades.items() for p,g in pages.items()}
        new_runs = {m:runs[m] for m in ("DenseWindowMean", "HybridWindowMean")}
        page_pool = build_pool(new_runs, by_id, page_grades, top_k=20, unit="page")
        chunk_pool = build_pool(new_runs, by_id, page_grades, top_k=20, unit="chunk")
        write_jsonl(base/split/"new_methods_top20_chunk_pool.jsonl", chunk_pool)
        write_jsonl(base/split/"new_methods_top20_page_pool.jsonl", page_pool)
        novel = [r for r in page_pool if (r["question_id"],r["page_id"]) not in old_pairs and r["page_judgment"] is None]
        new_review.extend(review_queue(novel, by_id, all_queries))
        pools[split] = dict(page_candidates=len(page_pool), chunk_candidates=len(chunk_pool), outside_original_pool_and_seed=len(novel),
            already_seed_judged=sum(r["page_judgment"] is not None for r in page_pool), original_pool_retained=2756 if split=="dev" else 975)
        resource = json.loads((base/split/"resources.json").read_text(encoding="utf-8"))
        coverage = resource["dense_cache"].pop("coverage")
        counts = [len(r["windows"]) for r in coverage]
        resource["window_stats"] = dict(chunks=len(coverage), total=sum(counts), mean=statistics.mean(counts), p95=float(np.percentile(counts,95)),
            maximum=max(counts), content_tokens=sum(r["content_tokens"] for r in coverage),
            lost_content_tokens=sum(r["lost_content_tokens"] for r in coverage), fully_covered_chunks=sum(r["covered_content_tokens"]==r["content_tokens"] for r in coverage))
        resource["window_count_histogram"] = dict(Counter(counts))
        resources[split] = resource
    write_csv(output/"seed_metrics_aggregate.csv", aggregate)
    write_csv(output/"seed_metrics_per_question.csv", metrics)
    write_csv(output/"paired_bootstrap.csv", paired)
    write_csv(output/"latencies.csv", latency)
    write_csv(output/"question_deltas.csv", delta_rows)
    new_review.sort(key=lambda r:(-r["priority"],r["question_id"],r["page_id"]))
    # Preserve headers even in the possible zero-new-candidate case.
    if new_review:
        write_csv(output/"additional_UNJUDGED_review_queue.csv", new_review)
    write_json(output/"dev_seal.json", seal)
    summary = dict(status="COMPLETED_SEED_ONLY", historical_integrity=history, resources=resources, pools=pools,
        new_unjudged_pairs=len(new_review), test_executed=False, validation_independent=False,
        augmented_metrics_status="NOT_RUN_NO_HUMAN_LABELS", human_import_status="WAITING_FOR_HUMAN_VALIDATION",
        judgments_exhaustive=False, bootstrap_repeats=2000, seed_qrels_sha256=file_hash(root/"evaluation/benchmark/qrels_group_confirmed_PAGES.trec"))
    summary["new_run_files_sha256"] = {p.relative_to(root).as_posix():file_hash(p)
        for split in ("dev", "validation") for p in sorted((base/split).glob("*")) if p.is_file()}
    write_json(output/"summary.json", summary)
    draw(output, aggregate, paired, latency, resources["dev"]["window_count_histogram"])
    return dict(new_unjudged_pairs=len(new_review), pools=pools, windows=resources["dev"]["window_stats"], history=history)


def draw(output, metrics, pairs, latency, histogram):
    import os
    cache = output.parents[1]/"artifacts/matplotlib"
    cache.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR",str(cache))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    fig, axes = plt.subplots(1,2,figsize=(12,4.8),sharey=True)
    for axis, split in zip(axes,("dev","validation")):
        for method in METHODS:
            rows = [r for r in metrics if r["split"]==split and r["method"]==method and r["convention"]==CONVENTIONS[0]]
            axis.plot([r["k"] for r in rows],[r["known_positive_coverage"] for r in rows],marker="o",label=method)
        axis.set(title=split+ (" — descriptive, déjà observée" if split=="validation" else " — 83 besoins"),xlabel="Budget strict de chunks",xticks=[1,3,5,10,20],ylim=(0,1))
        axis.grid(alpha=.2)
    axes[0].set_ylabel("Couverture moyenne des pages positives connues")
    axes[1].legend(fontsize=8)
    fig.suptitle("Extension 3B — seed incomplet, aucune annotation automatique utilisée")
    fig.tight_layout(); fig.savefig(output/"phase3b_coverage.png",dpi=160); plt.close(fig)
    fig, axes = plt.subplots(1,2,figsize=(13,4.8))
    for axis, split in zip(axes,("dev","validation")):
        rows=[r for r in pairs if r["split"]==split]
        values=np.array([r["difference"] for r in rows])
        axis.errorbar(values,range(len(rows)),xerr=[values-[r["ci_low"] for r in rows],[r["ci_high"] for r in rows]-values],fmt="o",capsize=4)
        axis.axvline(0,color="grey",linestyle="--")
        axis.set(title=split,yticks=range(len(rows)),yticklabels=[r["comparison"] for r in rows],xlabel="Différence de couverture connue @5")
    fig.suptitle("Bootstrap apparié 95 % descriptif — jugements incomplets")
    fig.tight_layout();fig.savefig(output/"phase3b_paired.png",dpi=160);plt.close(fig)
    fig, axis=plt.subplots(figsize=(8,4))
    keys=sorted(int(k) for k in histogram)
    axis.bar(keys,[histogram.get(k,histogram.get(str(k))) for k in keys])
    axis.set(title="Couverture intégrale des 2 127 chunks — fenêtres de 126 tokens, overlap 32",xlabel="Fenêtres par chunk historique",ylabel="Nombre de chunks",xticks=keys)
    fig.tight_layout();fig.savefig(output/"phase3b_windows.png",dpi=160);plt.close(fig)
    fig, axes=plt.subplots(1,2,figsize=(13,5),sharey=True)
    for axis, split in zip(axes,("dev","validation")):
        rows=[r for r in latency if r["split"]==split]
        x=np.arange(5)
        axis.bar(x-.18,[r["p50_ms"] for r in rows],width=.36,label="p50")
        axis.bar(x+.18,[r["p95_ms"] for r in rows],width=.36,label="p95")
        axis.set(title=split,xticks=x,xticklabels=METHODS,yscale="log")
        axis.tick_params(axis="x",rotation=30)
    axes[0].set_ylabel("Latence (ms, échelle log)");axes[1].legend()
    fig.suptitle("CPU : historiques archivés ; HybridWindow = composant BM25 archivé + Dense/fusion nouveaux")
    fig.tight_layout();fig.savefig(output/"phase3b_latency.png",dpi=160);plt.close(fig)
