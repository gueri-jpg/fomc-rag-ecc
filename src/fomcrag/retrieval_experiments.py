"""Guarded phase-3 orchestration. Labels enter evaluation, never the retrievers."""
from __future__ import annotations

from collections import defaultdict
import json
from pathlib import Path
import platform
import time

from .dense import DenseEncoder
from .indexing import lexical_views, load_baseline, save_lexical_cache
from .retrieval import BM25Index, reciprocal_rank_fusion, stable_ranking
from .retrieval_evaluation import choose_configuration, objective, page_diagnostics
from .selection import load_selection_inputs, phase3_questions, require_tuning_eligible
from .storage import file_hash, fingerprint, write_json, write_jsonl


def memory_snapshot() -> dict:
    """Windows process working-set counters; explicit unavailable fallback."""
    try:
        import ctypes
        from ctypes import wintypes
        class Counters(ctypes.Structure):
            _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD)] + [(name, ctypes.c_size_t) for name in
                ("PeakWorkingSetSize", "WorkingSetSize", "QuotaPeakPagedPoolUsage", "QuotaPagedPoolUsage",
                 "QuotaPeakNonPagedPoolUsage", "QuotaNonPagedPoolUsage", "PagefileUsage", "PeakPagefileUsage")]
        counters = Counters()
        counters.cb = ctypes.sizeof(counters)
        function = ctypes.windll.psapi.GetProcessMemoryInfo
        function.argtypes = [ctypes.c_void_p, ctypes.POINTER(Counters), wintypes.DWORD]
        if not function(ctypes.c_void_p(-1), ctypes.byref(counters), counters.cb):
            raise OSError("Process memory query unavailable")
        return dict(peak_working_set_bytes=counters.PeakWorkingSetSize, current_working_set_bytes=counters.WorkingSetSize,
                    logical_cpus=__import__("os").cpu_count(), measurement="Windows GetProcessMemoryInfo")
    except (OSError, AttributeError):
        return dict(measurement="unavailable")


def read_grades(root: Path, question_ids: set[str]) -> dict:
    """Evaluation-only view: never returns labels for test/embargo questions."""
    rows = defaultdict(dict)
    for line in (root / "evaluation/benchmark/qrels_group_confirmed_PAGES.trec").read_text(encoding="utf-8").splitlines():
        qid, _, page, grade = line.split()
        if qid in question_ids:
            rows[qid][page] = int(grade)
    return dict(rows)


def score_lexical(chunks, tokens, queries, parameters):
    import numpy as np
    started = time.perf_counter()
    ids = [c["chunk_id"] for c in chunks]
    index = BM25Index(tokens, ids, **parameters)
    construction = time.perf_counter() - started
    scores, ranks, times, repeat_times = [], [], [], []
    for query in queries:
        started = time.perf_counter()
        values = index.scores(query["question"])
        ranked = stable_ranking(values, ids)
        times.append((time.perf_counter() - started) * 1000)
        started = time.perf_counter()
        assert stable_ranking(index.scores(query["question"]), ids) == ranked
        repeat_times.append((time.perf_counter() - started) * 1000)
        scores.append(values)
        ranks.append(ranked)
    return dict(scores=np.asarray(scores), ranks=np.asarray(ranks), retrieval_ms=times,
                repeat_ms=repeat_times, construction_seconds=construction)


def score_dense(chunks, documents, queries, encoder):
    import numpy as np
    ids = [c["chunk_id"] for c in chunks]
    scores, ranks, times, repeat, tokenization = [], [], [], [], []
    for query in queries:
        started = time.perf_counter()
        vector, tokens = encoder.query(query["question"])
        values = documents @ vector
        ranked = stable_ranking(values, ids)
        times.append((time.perf_counter() - started) * 1000)
        started = time.perf_counter()
        repeated, _ = encoder.query(query["question"])
        if stable_ranking(documents @ repeated, ids) != ranked:
            raise ValueError("Non-deterministic repeated dense ranking")
        repeat.append((time.perf_counter() - started) * 1000)
        scores.append(values)
        ranks.append(ranked)
        tokenization.append(dict(question_id=query["question_id"], **tokens))
    return dict(scores=np.asarray(scores), ranks=np.asarray(ranks), retrieval_ms=times, repeat_ms=repeat,
                query_tokenization=tokenization)


def fuse(chunks, lexical, dense, rrf_k, depth):
    import numpy as np
    ids = [c["chunk_id"] for c in chunks]
    values, ranks, contributions, times = [], [], [], []
    for i in range(len(lexical["ranks"])):
        started = time.perf_counter()
        scores, details = reciprocal_rank_fusion({"BM25": [ids[j] for j in lexical["ranks"][i][:depth]],
                                                  "Dense": [ids[j] for j in dense["ranks"][i][:depth]]}, rrf_k=rrf_k, depth=depth)
        vector = [scores.get(cid, 0.) for cid in ids]
        ranks.append(stable_ranking(vector, ids))
        values.append(vector)
        contributions.append(details)
        times.append((time.perf_counter() - started) * 1000)
    # Serial composition of measured source and fusion costs, not parallel E2E.
    return dict(scores=np.asarray(values), ranks=np.asarray(ranks), contributions=contributions, fusion_ms=times,
                retrieval_ms=[a + b + c for a, b, c in zip(lexical["retrieval_ms"], dense["retrieval_ms"], times)],
                repeat_ms=[a + b + c for a, b, c in zip(lexical["repeat_ms"], dense["repeat_ms"], times)])


def tuning_rows(chunks, queries, scored, grades):
    return [page_diagnostics([chunks[j] for j in scored["ranks"][i][:100]], grades[q["question_id"]],
                             5, "page-coverage-from-chunk@k") for i, q in enumerate(queries)]


def export_run(output, method, chunks, identity, queries, selection, scored, config_id, parameters):
    import numpy as np
    output.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(output / f"{method}_complete.npz", ranks=scored["ranks"], scores=scored["scores"],
                        chunk_ids=np.asarray([c["chunk_id"] for c in chunks]),
                        question_ids=np.asarray([q["question_id"] for q in queries]))
    records = []
    fields = ("chunk_id", "document_id", "document", "source_pdf", "page_id", "page", "year", "doc_type", "meeting_date", "text", "char_start", "char_end")
    for i, query in enumerate(queries):
        retrieved = []
        for rank, j in enumerate(scored["ranks"][i][:100], 1):
            hit = {key: chunks[j][key] for key in fields}
            hit.update(rank=rank, score=float(scored["scores"][i][j]))
            if "contributions" in scored:
                hit["rrf_contributions"] = scored["contributions"][i].get(chunks[j]["chunk_id"], {})
            retrieved.append(hit)
        record = dict(question_id=query["question_id"], question=query["question"], split=selection["split"], method=method,
            retrieved=retrieved, retrieval_ms=scored["retrieval_ms"][i], repeat_ms=scored["repeat_ms"][i],
            latency_kind="serial_sum_of_measured_sources_and_fusion" if method == "Hybrid" else "measured_uncached_query_inference_and_ranking",
            corpus_identity=identity, config_id=config_id, parameters=parameters,
            selection_policy_sha256=selection["policy_sha256"], reranking=False)
        records.append(record)
    write_jsonl(output / (method + ".jsonl"), records)
    write_json(output / (method + "_metadata.json"), dict(selection=selection, corpus=identity, config_id=config_id,
               parameters=parameters, complete_rankings_file=method + "_complete.npz", top_text_records=100,
               timing={k: scored[k] for k in ("construction_seconds", "query_tokenization", "fusion_ms") if k in scored}))
    return records


def run_phase3(root: Path, stage: str) -> dict:
    """Dev before validation. Never accepts test, all, paraphrases or embargo."""
    import numpy as np
    if stage not in {"dev", "validation"}:
        raise ValueError("Phase 3 only accepts dev or validation")
    config = json.loads((root / "configs/retrieval_phase3.json").read_text(encoding="utf-8"))
    if config["test_authorized"] or config["paraphrases_enabled"] or config["reranking"] or config["scope"] != "ALL_DOCUMENTS_ALL_YEARS":
        raise ValueError("Unsafe phase-3 configuration")
    output = root / "artifacts/phase3" / stage
    selected_path = root / "artifacts/phase3/dev_selection.json"
    # Refuse any validation execution until dev selection is persisted and bound.
    config_id = fingerprint(config)
    if stage == "validation":
        if not selected_path.is_file():
            raise ValueError("Dev selection artifact required before validation")
        selected = json.loads(selected_path.read_text(encoding="utf-8"))
        if selected["config_id"] != config_id or selected["test_authorized"] is not False:
            raise ValueError("Dev configuration changed; no silent validation iteration")
        if output.exists() and (output / "completed.json").exists():
            raise ValueError("Validation already completed: do not tune/repeat silently")
    queries, selection = phase3_questions(root, stage)
    _, policy = load_selection_inputs(root)
    require_tuning_eligible(selection, policy, queries=None)
    chunks, identity = load_baseline(root, config)
    views = lexical_views(root, chunks)
    cache_dir = root / "artifacts/phase3/indexes"
    caches = {variant: save_lexical_cache(cache_dir, tokens, identity, variant) for variant, tokens in views.items()}
    encoder = DenseEncoder(root, config["dense"], config["seed"])
    if stage == "validation" and encoder.descriptor != selected["dense_encoder"]:
        raise ValueError("Dense checkpoint/environment differs from locked dev selection")
    documents, dense_cache = encoder.encode([c["text"] for c in chunks], [c["chunk_id"] for c in chunks], cache_dir)
    dense = score_dense(chunks, documents, queries, encoder)
    grades = read_grades(root, {q["question_id"] for q in queries})
    candidates, rrf_candidates = [], []
    if stage == "dev":
        lexical_runs = []
        for parameters in config["bm25_grid"]:
            run = score_lexical(chunks, views["L0"], queries, parameters)
            lexical_runs.append(run)
            candidates.append(dict(parameters=parameters, objective=objective(tuning_rows(chunks, queries, run, grades))))
        winner = choose_configuration(candidates)
        best = candidates.index(winner)
        lexical = lexical_runs[best]
        parameters = winner["parameters"]
        for constant in config["rrf_grid"]:
            run = fuse(chunks, lexical, dense, constant, config["candidate_depth"])
            rrf_candidates.append(dict(rrf_k=constant, objective=objective(tuning_rows(chunks, queries, run, grades))))
        rrf_k = choose_configuration(rrf_candidates)["rrf_k"]
    else:
        parameters, rrf_k = selected["bm25_parameters"], selected["rrf_k"]
        if selected["policy_sha256"] != selection["policy_sha256"] or selected["corpus_identity"] != identity:
            raise ValueError("Policy or corpus differs from dev selection")
        lexical = score_lexical(chunks, views["L0"], queries, parameters)
    hybrid = fuse(chunks, lexical, dense, rrf_k, config["candidate_depth"])
    alternative = score_lexical(chunks, views["L1"], queries, parameters)
    methods = dict(BM25=lexical, Dense=dense, Hybrid=hybrid, BM25_L1=alternative)
    params = dict(BM25=dict(parameters, lexical="L0"), Dense=encoder.descriptor,
                  Hybrid=dict(rrf_k=rrf_k, depth=config["candidate_depth"], lexical="L0"),
                  BM25_L1=dict(parameters, lexical="L1"))
    for method, run in methods.items():
        export_run(output, method, chunks, identity, queries, selection, run, config_id, params[method])
    objectives = {name: objective(tuning_rows(chunks, queries, run, grades)) for name, run in methods.items()}
    if stage == "dev":
        chosen_method = choose_configuration([dict(method=name, objective=objectives[name]) for name in ("BM25", "Dense", "Hybrid")])["method"]
        selected = dict(config_id=config_id, config_sha256=file_hash(root / "configs/retrieval_phase3.json"),
            corpus_identity=identity, policy_sha256=selection["policy_sha256"],
            selection=selection, dense_encoder=encoder.descriptor, bm25_parameters=parameters, rrf_k=rrf_k, recommended_method=chosen_method,
            bm25_grid_results=candidates, rrf_grid_results=rrf_candidates, objectives=objectives,
            lexical_ablation_preference=choose_configuration([dict(variant=name, objective=objectives[method]) for name, method in (("L0", "BM25"), ("L1", "BM25_L1"))])["variant"],
            human_validated=False, test_authorized=False, validation_consulted=False)
        write_json(selected_path, selected)
    write_json(output / "resources.json", dict(platform=platform.platform(), python=platform.python_version(), memory=memory_snapshot(),
        model_load_seconds=encoder.load_seconds, dense_document_cache=dense_cache, lexical_caches=caches,
        dense_encoder=encoder.descriptor, device=config["dense"]["device"], seed=config["seed"]))
    write_json(output / "completed.json", dict(stage=stage, queries=len(queries), config_id=config_id,
        selection=selection, corpus_identity=identity, objectives=objectives, test_executed=False))
    return dict(stage=stage, queries=len(queries), objectives=objectives, bm25_parameters=parameters, rrf_k=rrf_k,
                recommended_method=selected["recommended_method"], model_revision=encoder.lock["revision"])
