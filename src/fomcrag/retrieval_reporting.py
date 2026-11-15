"""Read saved dev/validation rankings; never run or tune a retriever."""
from __future__ import annotations

from collections import Counter, defaultdict
import csv
import json
from pathlib import Path
import re
import statistics

from .indexing import load_baseline
from .hyphen_diagnostics import BREAK, PROTECTED, lexical_ablation_candidate
from .metrics import select_budget
from .preprocessing import lexical_tokens, normalize_text
from .pooling import build_pool
from .retrieval_evaluation import page_diagnostics
from .retrieval_experiments import read_grades
from .selection import phase3_questions
from .storage import file_hash, fingerprint, read_jsonl, write_json, write_jsonl

METHODS = ("BM25", "Dense", "Hybrid", "BM25_L1")
CONVENTIONS = ("page-coverage-from-chunk@k", "unique-page@k")
ERROR_CASE_IDS = tuple("FOMC_" + n for n in ("003", "004", "007", "009", "013", "014", "015", "018", "032", "048", "120",
    "005", "008", "051", "058", "084", "102", "104", "106", "132"))


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise ValueError("Cannot export empty table")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def validate_saved_run(records: list[dict], queries: list[dict], chunks: dict[str, dict],
                       identity: dict, config_id: str, method: str) -> None:
    expected = {q["question_id"]: q for q in queries}
    if len(records) != len(expected) or {r["question_id"] for r in records} != set(expected):
        raise ValueError("Saved query IDs differ from exact authorized partition")
    for record in records:
        query = expected[record["question_id"]]
        if (record["question"] != query["question"] or record["split"] != query["split"]
                or record["method"] != method or record["corpus_identity"] != identity
                or record["config_id"] != config_id or record["reranking"] is not False):
            raise ValueError("Changed query, configuration or corpus in saved run")
        hits = record["retrieved"]
        if len(hits) != 100 or len({h["chunk_id"] for h in hits}) != 100:
            raise ValueError("Exactly 100 unique saved candidates required")
        for rank, hit in enumerate(hits, 1):
            chunk = chunks.get(hit["chunk_id"])
            if chunk is None or hit["rank"] != rank:
                raise ValueError("Unknown chunk or incorrect rank")
            for field in ("page_id", "document_id", "source_pdf", "year", "doc_type", "text", "char_start", "char_end"):
                if hit[field] != chunk[field]:
                    raise ValueError("Incorrect saved provenance: " + field)
            if method == "Hybrid":
                details = hit["rrf_contributions"]
                if not details or abs(sum(d["contribution"] for d in details.values()) - hit["score"]) > 1e-12:
                    raise ValueError("Invalid RRF contributions")
        if len(select_budget(hits, 20, "unique-page@k")["pages"]) != 20:
            raise ValueError("Saved depth insufficient for unique-page@20")


def bootstrap_interval(values: list[float], seed: int, repeats: int = 2000) -> tuple[float, float]:
    import numpy as np
    if not values:
        raise ValueError("No query needs for bootstrap")
    array = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    means = array[rng.integers(0, len(array), size=(repeats, len(array)))].mean(axis=1)
    return tuple(float(x) for x in np.quantile(means, [0.025, 0.975]))


def review_queue(pool: list[dict], chunks: dict[str, dict], questions: dict[str, dict]) -> list[dict]:
    """New pages only; date flag is a review hint, never a search filter."""
    rows = []
    for row in pool:
        if row["page_judgment"] is not None:
            continue
        chunk = chunks[row["candidate_chunk_ids"][0]]
        explicit_years = {int(y) for y in re.findall(r"\b20(?:21|22|23|24|25|26)\b", questions[row["question_id"]]["question"])}
        cross_year = bool(explicit_years and chunk["year"] not in explicit_years)
        minimum = min(h["rank"] for h in row["returned_by"])
        rows.append(dict(question_id=row["question_id"], split=questions[row["question_id"]]["split"],
            page_id=row["page_id"], source_pdf=chunk["source_pdf"], year=chunk["year"], doc_type=chunk["doc_type"],
            chunk_ids="|".join(sorted(row["candidate_chunk_ids"])),
            proposed_by="|".join(sorted({h["method"] for h in row["returned_by"]})),
            method_ranks=json.dumps(row["returned_by"], separators=(",", ":")), best_rank=minimum,
            cross_explicit_question_year=cross_year, priority=round(100 / (minimum + 1) + 5 * cross_year, 6),
            review_status="UNJUDGED", relevance_grade="", notes=""))
    return sorted(rows, key=lambda r: (-r["priority"], r["question_id"], r["page_id"]))


def hyphen_counts(root: Path, chunks: list[dict]) -> dict:
    pages = {p["page_id"]: p for p in read_jsonl(root / "data/processed/pages.jsonl")}
    changed = joined = protected = 0
    for chunk in chunks:
        raw = pages[chunk["page_id"]]["raw_text"][chunk["raw_char_start"]:chunk["raw_char_end"]]
        if lexical_tokens(normalize_text(raw).text) != chunk["bm25_tokens"] or "\u00ad" in raw:
            raise ValueError("L1 raw span differs from baseline beyond attested line hyphens")
        changed += lexical_ablation_candidate(raw) != chunk["bm25_tokens"]
        for match in BREAK.finditer(raw):
            if (match[1] + "-" + match[2]).casefold() in PROTECTED:
                protected += 1
            else:
                joined += 1
    return dict(changed_chunks=changed, joined_occurrences_with_overlap=joined,
                protected_occurrences_with_overlap=protected, baseline_reconstruction_mismatches=0,
                note="Occurrences in chunk windows include overlap; not unique page counts")


def summarize(root: Path) -> dict:
    """Deterministic postprocessing only, safe to regenerate without validation inference."""
    import numpy as np
    config = json.loads((root / "configs/retrieval_phase3.json").read_text(encoding="utf-8"))
    immutable = {
        "evaluation/benchmark/qrels_group_confirmed_PAGES.csv": "d550fdf524af81111504efad0c44dc25ad36b48d4f32007f1808953d16d187cb",
        "evaluation/benchmark/qrels_group_confirmed_PAGES.trec": "9c6080cf08a34361162ffcd57ec187f2e20118ceca19c4e226f742ac7e8e8682",
        "data/processed/chunks_256.jsonl": "0489ac8494e25d06b282548f55a4c845c1be2a64f1dbf45a9987145ab049cbb5",
    }
    if any(file_hash(root / name) != digest for name, digest in immutable.items()):
        raise ValueError("Original qrels or baseline chunks changed")
    chunks, identity = load_baseline(root, config)
    by_id = {c["chunk_id"]: c for c in chunks}
    by_page = {c["page_id"]: c for c in chunks}
    output = root / "reports/retrieval_phase3"
    local = root / "artifacts/phase3"
    summaries, detailed, latencies, source_rows, intervals, pools = [], [], [], [], [], {}
    integrity, resources, all_queries, all_grades = {}, {}, {}, {}
    run_by_split = {}
    source_coverage = defaultdict(list)
    for split in ("dev", "validation"):
        queries, selection = phase3_questions(root, split)
        all_queries.update({q["question_id"]: q for q in queries})
        grades = read_grades(root, set(selection["selected_question_ids"]))
        all_grades.update({(qid, p): grade for qid, pages in grades.items() for p, grade in pages.items()})
        completed = json.loads((local / split / "completed.json").read_text(encoding="utf-8"))
        if completed["test_executed"] is not False or completed["config_id"] != fingerprint(config):
            raise ValueError("Unsafe or mismatched completed artifact")
        resources[split] = json.loads((local / split / "resources.json").read_text(encoding="utf-8"))
        runs = {}
        per_method = {}
        for method in METHODS:
            path = local / split / (method + ".jsonl")
            records = read_jsonl(path)
            validate_saved_run(records, queries, by_id, identity, fingerprint(config), method)
            # Check every full ranking and raw score, not just the exported top-100.
            with np.load(local / split / (method + "_complete.npz"), allow_pickle=False) as matrix:
                ids = matrix["chunk_ids"].tolist()
                if ids != [c["chunk_id"] for c in chunks] or matrix["question_ids"].tolist() != [q["question_id"] for q in queries]:
                    raise ValueError("Full matrix identities differ from common corpus/questions")
                scores, ranks = matrix["scores"], matrix["ranks"]
                from .retrieval import stable_ranking
                for i, record in enumerate(records):
                    if ranks[i].tolist() != stable_ranking(scores[i], ids):
                        raise ValueError("Full ranking fails deterministic score ordering")
                    for rank, hit in enumerate(record["retrieved"]):
                        j = ranks[i][rank]
                        if hit["chunk_id"] != ids[j] or hit["score"] != float(scores[i][j]):
                            raise ValueError("Full matrix and JSONL disagree")
            integrity[f"{split}/{method}"] = dict(jsonl_sha256=file_hash(path), queries=len(records),
                full_ranking_chunks=2127, top_text_records=100, shared_scope_verified=True)
            runs[method] = records
            per_method[method] = {}
            for record in records:
                qid = record["question_id"]
                for k in config["budgets"]:
                    retrieved_pages = set(select_budget(record["retrieved"], k, CONVENTIONS[0])["pages"])
                    positive_groups = defaultdict(set)
                    for page, grade in grades[qid].items():
                        if grade > 0:
                            source = by_page[page]
                            positive_groups[(source["year"], source["doc_type"])].add(page)
                    for (year, doc_type), positive_pages in positive_groups.items():
                        source_coverage[(split, method, k, year, doc_type)].append(
                            (len(retrieved_pages.intersection(positive_pages)), len(positive_pages)))
                for convention in CONVENTIONS:
                    for k in config["budgets"]:
                        row = dict(split=split, method=method, question_id=qid, convention=convention, k=k,
                            **page_diagnostics(record["retrieved"], grades[qid], k, convention))
                        detailed.append(row)
                        if k == 5 and convention == CONVENTIONS[0]:
                            per_method[method][qid] = row["known_positive_coverage"]
                for hit in record["retrieved"][:20]:
                    source_rows.append(dict(split=split, method=method, year=hit["year"], doc_type=hit["doc_type"]))
            meta = json.loads((local / split / (method + "_metadata.json")).read_text(encoding="utf-8"))
            latencies.append(dict(split=split, method=method, queries=len(records),
                first_ms_p50=float(np.percentile([r["retrieval_ms"] for r in records], 50)),
                first_ms_p95=float(np.percentile([r["retrieval_ms"] for r in records], 95)),
                repeat_ms_p50=float(np.percentile([r["repeat_ms"] for r in records], 50)),
                repeat_ms_p95=float(np.percentile([r["repeat_ms"] for r in records], 95)),
                construction_seconds=meta["timing"].get("construction_seconds", ""),
                latency_kind=records[0]["latency_kind"]))
        for method in METHODS:
            for convention in CONVENTIONS:
                for k in config["budgets"]:
                    subset = [r for r in detailed if (r["split"], r["method"], r["convention"], r["k"]) == (split, method, convention, k)]
                    numeric = ("known_positive_coverage", "known_positive_hit", "known_positive_page_rr", "seed_ndcg",
                        "unjudged_pages", "unjudged_fraction", "unique_pages", "unique_documents", "consumed_chunks")
                    low, high = bootstrap_interval([r["known_positive_coverage"] for r in subset], config["seed"])
                    summaries.append(dict(split=split, method=method, convention=convention, k=k, queries=len(subset),
                        **{key: statistics.mean(r[key] for r in subset) for key in numeric},
                        coverage_ci_low=low, coverage_ci_high=high,
                        first_positive_rank_mean_among_hits=statistics.mean([r["first_known_positive_page_rank"] for r in subset if r["first_known_positive_page_rank"] is not None])
                            if any(r["first_known_positive_page_rank"] is not None for r in subset) else ""))
        for left, right in (("Hybrid", "BM25"), ("Dense", "BM25"), ("Hybrid", "Dense"), ("BM25_L1", "BM25")):
            differences = [per_method[left][q["question_id"]] - per_method[right][q["question_id"]] for q in queries]
            low, high = bootstrap_interval(differences, config["seed"])
            intervals.append(dict(split=split, comparison=f"{left} minus {right}", metric="strict known_positive_coverage@5",
                queries=len(queries), difference=statistics.mean(differences), ci_low=low, ci_high=high,
                improved=sum(d > 0 for d in differences), worsened=sum(d < 0 for d in differences), unchanged=sum(d == 0 for d in differences)))
        primary = {m: runs[m] for m in METHODS[:3]}
        chunk_pool = build_pool(primary, by_id, all_grades, top_k=20, unit="chunk")
        page_pool = build_pool(primary, by_id, all_grades, top_k=20, unit="page")
        write_jsonl(local / split / "top20_chunk_pool.jsonl", chunk_pool)
        write_jsonl(local / split / "top20_page_pool.jsonl", page_pool)
        pools[split] = dict(chunk_candidates=len(chunk_pool), page_candidates=len(page_pool),
            new_unjudged_pages=sum(r["page_judgment"] is None for r in page_pool),
            existing_page_judgments=sum(r["page_judgment"] is not None for r in page_pool))
        pools[split]["review_rows"] = review_queue(page_pool, by_id, all_queries)
        run_by_split[split] = runs
    write_csv(output / "metrics_aggregate.csv", summaries)
    write_csv(output / "metrics_per_question.csv", detailed)
    write_csv(output / "latencies.csv", latencies)
    write_csv(output / "paired_bootstrap.csv", intervals)
    source_counts = Counter((r["split"], r["method"], r["year"], r["doc_type"]) for r in source_rows)
    write_csv(output / "sources_top20.csv", [dict(split=s, method=m, year=y, doc_type=t, retrieved_chunks=n)
        for (s, m, y, t), n in sorted(source_counts.items())])
    write_csv(output / "known_coverage_by_source.csv", [dict(split=s, method=m, k=k, source_year=y, doc_type=t,
        query_needs_with_known_positive=len(values), known_positive_pages=sum(n for hit, n in values),
        matched_known_pages=sum(hit for hit, n in values), macro_known_coverage=statistics.mean(hit/n for hit, n in values),
        micro_known_coverage=sum(hit for hit, n in values)/sum(n for hit, n in values))
        for (s, m, k, y, t), values in sorted(source_coverage.items())])
    review = [r for split in pools.values() for r in split.pop("review_rows")]
    review.sort(key=lambda r: (-r["priority"], r["question_id"], r["page_id"]))
    write_csv(output / "new_pages_review_queue.csv", review)
    errors = []
    if not set(ERROR_CASE_IDS) <= set(all_queries):
        raise ValueError("Qualitative cases must belong to authorized dev/validation only")
    for qid in ERROR_CASE_IDS:
        split = all_queries[qid]["split"]
        known = {p for (q, p) in all_grades if q == qid}
        row = dict(question_id=qid, split=split, known_pages="|".join(sorted(known)))
        for method in METHODS:
            record = next(r for r in run_by_split[split][method] if r["question_id"] == qid)
            row[method + "_first_positive_chunk_rank_top100"] = next((h["rank"] for h in record["retrieved"] if h["page_id"] in known), "NOT_IN_TOP100")
            row[method + "_first_source"] = record["retrieved"][0]["page_id"]
        errors.append(row)
    write_csv(output / "error_cases.csv", errors)
    selection = json.loads((local / "dev_selection.json").read_text(encoding="utf-8"))
    write_json(output / "dev_selection.json", selection)
    # Keep per-chunk token diagnostics local, expose complete aggregate statistics.
    tokens = resources["dev"]["dense_document_cache"].pop("tokenization")
    resources["validation"]["dense_document_cache"].pop("tokenization")
    for split in resources:
        query_tokens = json.loads((local / split / "Dense_metadata.json").read_text(encoding="utf-8"))["timing"]["query_tokenization"]
        resources[split]["query_tokens"] = dict(queries=len(query_tokens), truncated=sum(t["truncated"] for t in query_tokens),
            maximum=max(t["input_tokens"] for t in query_tokens), minimum=min(t["input_tokens"] for t in query_tokens))
        for name, cache in resources[split]["lexical_caches"].items():
            cache["note"] = "Serialized token view; postings rebuilt in memory"
    truncation = dict(chunks=len(tokens), truncated_chunks=sum(t["truncated"] for t in tokens),
        fraction_truncated=statistics.mean(t["truncated"] for t in tokens),
        input_tokens_min=min(t["input_tokens"] for t in tokens), input_tokens_max=max(t["input_tokens"] for t in tokens),
        input_tokens_p50=float(np.percentile([t["input_tokens"] for t in tokens], 50)),
        input_tokens_p95=float(np.percentile([t["input_tokens"] for t in tokens], 95)),
        total_input_tokens=sum(t["input_tokens"] for t in tokens), total_discarded_tokens=sum(t["discarded_tokens"] for t in tokens))
    model_lock = json.loads((root / "configs/dense_model_lock.json").read_text(encoding="utf-8"))
    weights = root / "models/minilm" / model_lock["revision"]
    summary = dict(config_id=fingerprint(config), corpus_identity=identity, pools=pools, resources=resources,
        hyphen_ablation=hyphen_counts(root, chunks),
        truncation=truncation, model_files_bytes=sum((weights / name).stat().st_size for name in model_lock["files"]),
        run_integrity=integrity, test_executed=False, judgments_exhaustive=False, bootstrap_repeats=2000,
        bootstrap_unit="query need; percentile 95%; descriptive, no multiplicity correction, missing labels unchanged",
        review_priority="100/(1+best chunk rank) + 5 if source year differs from explicit question year; otherwise no year inference",
        immutable_files_verified=immutable,
        qrels_sha256=file_hash(root / "evaluation/benchmark/qrels_group_confirmed_PAGES.trec"))
    write_json(output / "summary.json", summary)
    draw_figures(root, summaries, latencies, intervals, source_counts, tokens, resources["dev"]["dense_encoder"]["max_seq_length"])
    return dict(config_id=summary["config_id"], pools=pools, truncation=truncation,
                aggregate_rows=len(summaries), per_question_rows=len(detailed), test_executed=False)


def draw_figures(root, summaries, latencies, intervals, source_counts, tokens, max_seq_length):
    import os
    cache_directory = root / "artifacts/matplotlib"
    cache_directory.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(cache_directory))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    directory = root / "reports/figures"
    directory.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 10})
    colors = dict(BM25="#3366aa", Dense="#c66b20", Hybrid="#28845a")
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), sharey=True)
    for axis, split in zip(axes, ("dev", "validation")):
        for method in METHODS[:3]:
            rows = [r for r in summaries if r["split"] == split and r["method"] == method and r["convention"] == CONVENTIONS[0]]
            y = np.array([r["known_positive_coverage"] for r in rows])
            axis.errorbar([r["k"] for r in rows], y, yerr=[y - [r["coverage_ci_low"] for r in rows], [r["coverage_ci_high"] for r in rows] - y],
                label=method, color=colors[method], marker="o", capsize=3)
        axis.set(title=f"{split} ({83 if split == 'dev' else 30} questions)", xlabel="Budget strict de chunks k", xticks=[1, 3, 5, 10, 20], ylim=(0, 1))
        axis.grid(alpha=.2)
    axes[0].set_ylabel("Couverture moyenne des pages positives connues")
    axes[1].legend()
    fig.suptitle("Jugements incomplets — IC bootstrap descriptifs 95 %")
    fig.tight_layout()
    fig.savefig(directory / "phase3_known_coverage.png", dpi=160)
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True)
    for axis, split in zip(axes, ("dev", "validation")):
        rows = [next(r for r in latencies if r["split"] == split and r["method"] == method) for method in METHODS[:3]]
        x = np.arange(3)
        axis.bar(x-.18, [r["first_ms_p50"] for r in rows], width=.36, label="p50")
        axis.bar(x+.18, [r["first_ms_p95"] for r in rows], width=.36, label="p95")
        axis.set(title=split, xticks=x, xticklabels=METHODS[:3], yscale="log")
        axis.grid(axis="y", alpha=.2)
    axes[0].set_ylabel("Millisecondes (échelle logarithmique)")
    axes[1].legend()
    fig.suptitle("CPU, modèle chargé, requêtes sans cache — Hybrid : somme sérielle")
    fig.tight_layout()
    fig.savefig(directory / "phase3_latency.png", dpi=160)
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    for axis, split in zip(axes, ("dev", "validation")):
        rows = [r for r in intervals if r["split"] == split]
        y = np.arange(len(rows))
        means = np.array([r["difference"] for r in rows])
        axis.errorbar(means, y, xerr=[means-[r["ci_low"] for r in rows], [r["ci_high"] for r in rows]-means], fmt="o", capsize=4)
        axis.axvline(0, color="grey", linestyle="--")
        axis.set(title=split, yticks=y, yticklabels=[r["comparison"] for r in rows], xlabel="Différence de couverture connue @5")
    fig.suptitle("IC appariés 95 % par question — ne corrigent pas les qrels incomplets")
    fig.tight_layout()
    fig.savefig(directory / "phase3_paired_differences.png", dpi=160)
    plt.close(fig)
    fig, axis = plt.subplots(figsize=(9, 4))
    axis.hist([t["input_tokens"] for t in tokens], bins=35, color="#3366aa", label="Longueur avant troncature")
    axis.axvline(max_seq_length, color="#b52f32", linestyle="--", label=f"Limite du checkpoint : {max_seq_length} tokens")
    axis.set(title="2 127 chunks de 256 mots : longueur réelle MiniLM", xlabel="Tokens avec tokens spéciaux", ylabel="Nombre de chunks")
    axis.legend()
    fig.tight_layout()
    fig.savefig(directory / "phase3_truncation.png", dpi=160)
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True)
    for axis, split in zip(axes, ("dev", "validation")):
        for i, method in enumerate(METHODS[:3]):
            counts = [sum(n for (s, m, yr, t), n in source_counts.items() if (s, m, yr) == (split, method, year)) for year in range(2021, 2027)]
            axis.bar(np.arange(6)+(i-1)*.25, counts, width=.25, label=method, color=colors[method])
        axis.set(title=split, xticks=np.arange(6), xticklabels=list(range(2021, 2027)), xlabel="Année de la source")
    axes[0].set_ylabel("Occurrences de chunks dans les top-20")
    axes[1].legend()
    fig.suptitle("Distribution des sources retrouvées — aucun filtre temporel")
    fig.tight_layout()
    fig.savefig(directory / "phase3_source_years.png", dpi=160)
    plt.close(fig)
