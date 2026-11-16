"""Separate fixed 3B experiment. Original files are read-only references."""
from __future__ import annotations
import json
from pathlib import Path
import subprocess

from .dense_windowed import WindowedEncoder
from .indexing import load_baseline
from .retrieval_evaluation import choose_configuration
from .retrieval_experiments import score_dense, fuse, export_run, tuning_rows, objective, read_grades, memory_snapshot
from .retrieval_reporting import validate_saved_run
from .selection import phase3_questions
from .storage import file_hash, fingerprint, read_jsonl, write_json, write_jsonl

ARCHIVED = {"BM25_L0": "BM25", "Dense128": "Dense", "Hybrid128": "Hybrid"}
METHODS = ("BM25_L0", "Dense128", "DenseWindowMean", "Hybrid128", "HybridWindowMean")


def verify_history(root: Path) -> dict:
    path = root / "artifacts/phase3_extension/historical_snapshot.json"
    if not path.exists():
        paths = [p for directory in ("artifacts/phase3", "reports/retrieval_phase3", "data/processed")
                 for p in (root/directory).rglob("*") if p.is_file()]
        paths += list((root/"reports/figures").glob("phase3_*.png"))
        paths += [root/"evaluation/benchmark"/name for name in ("qrels_group_confirmed_PAGES.csv", "qrels_group_confirmed_PAGES.trec")]
        if not (root/"artifacts/phase3/validation/completed.json").exists():
            raise ValueError("Restore completed original phase-3 artifacts first")
        write_json(path, {p.relative_to(root).as_posix(): file_hash(p) for p in paths})
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    changed = [name for name, digest in snapshot.items() if file_hash(root/name) != digest]
    if changed:
        raise ValueError("Historical artifacts changed: " + ", ".join(changed))
    return dict(status="PASS", files=len(snapshot), snapshot_sha256=fingerprint(snapshot))


def source_hashes(root: Path):
    return {name: file_hash(root/name) for name in ("configs/retrieval_phase3_extension.json", "configs/dense_model_lock.json",
        "src/fomcrag/dense.py", "src/fomcrag/dense_windowed.py", "src/fomcrag/retrieval.py",
        "src/fomcrag/phase3_extension.py", "src/fomcrag/retrieval_experiments.py")}


def historical_run(root, split, method, queries, chunks, identity):
    import numpy as np
    config = json.loads((root/"configs/retrieval_phase3.json").read_text(encoding="utf-8"))
    directory = root/"artifacts/phase3"/split
    records = read_jsonl(directory/(method+".jsonl"))
    validate_saved_run(records, queries, {c["chunk_id"]:c for c in chunks}, identity, fingerprint(config), method)
    with np.load(directory/(method+"_complete.npz"), allow_pickle=False) as data:
        if (data["chunk_ids"].tolist() != [c["chunk_id"] for c in chunks]
                or data["question_ids"].tolist() != [q["question_id"] for q in queries]):
            raise ValueError("Historical full ranking identities differ")
        scored = dict(scores=data["scores"].copy(), ranks=data["ranks"].copy(),
            retrieval_ms=[r["retrieval_ms"] for r in records], repeat_ms=[r["repeat_ms"] for r in records])
    return scored, records


def run_extension(root: Path, stage: str):
    if stage not in {"dev", "validation"}:
        raise ValueError("3B prohibits test/all/paraphrases/embargo diagnostics")
    config = json.loads((root/"configs/retrieval_phase3_extension.json").read_text(encoding="utf-8"))
    if (config["test_authorized"] or config["reranking"] or config["paraphrases_enabled"]
            or config["scope"] != "ALL_DOCUMENTS_ALL_YEARS" or config["qrels"] != "ORIGINAL_279_SEED_ONLY"
            or config["rrf_k"] != 10 or config["candidate_depth"] != 100):
        raise ValueError("Unsafe/unregistered extension settings")
    history = verify_history(root)
    directory = root/"artifacts/phase3_extension"
    output = directory/stage
    seal_path = directory/"dev_seal.json"
    code = source_hashes(root)
    config_id = fingerprint(dict(config=config, source_hashes=code))
    if (directory/"validation/started.json").exists() and stage == "dev":
        raise ValueError("Validation started: dev selection closed")
    if (output/"completed.json").exists() or (stage == "validation" and (output/"started.json").exists()):
        raise ValueError("Stage already executed/started: no silent validation repetition")
    if stage == "validation":
        if not seal_path.exists():
            raise ValueError("Dev seal required before validation")
        seal = json.loads(seal_path.read_text(encoding="utf-8"))
        if seal["config_id"] != config_id or seal["history"] != history or seal["test_authorized"]:
            raise ValueError("Experiment changed after dev seal")
    old = json.loads((root/"configs/retrieval_phase3.json").read_text(encoding="utf-8"))
    chosen = json.loads((root/"reports/retrieval_phase3/dev_selection.json").read_text(encoding="utf-8"))
    if config["bm25"]["k1"] != chosen["bm25_parameters"]["k1"] or config["bm25"]["b"] != chosen["bm25_parameters"]["b"]:
        raise ValueError("BM25 cannot be retuned in extension")
    chunks, identity = load_baseline(root, old)
    queries, selection = phase3_questions(root, stage)
    if len(queries) != config[stage+"_questions"]:
        raise ValueError("Unexpected selected partition")
    encoder = WindowedEncoder(root, old["dense"], config["seed"], config["window"])
    if stage == "validation" and encoder.descriptor != seal["encoder"]:
        raise ValueError("Encoder changed after dev seal")
    write_json(output/"started.json", dict(config_id=config_id, queries=len(queries), descriptive_validation=stage=="validation"))
    documents, cache = encoder.encode([c["text"] for c in chunks], [c["chunk_id"] for c in chunks], directory/"indexes")
    dense = score_dense(chunks, documents, queries, encoder)
    lexical, _ = historical_run(root, stage, "BM25", queries, chunks, identity)
    hybrid = fuse(chunks, lexical, dense, config["rrf_k"], config["candidate_depth"])
    for method, run in (("DenseWindowMean", dense), ("HybridWindowMean", hybrid)):
        records = export_run(output, method, chunks, identity, queries, selection, run, config_id,
            dict(encoder=encoder.descriptor) if method == "DenseWindowMean" else dict(rrf_k=10, depth=100, lexical="historical BM25 L0"))
        for record in records:
            record["experiment"] = "phase3b"
            if method == "HybridWindowMean":
                record["latency_kind"] = "serial_sum_new_dense_fusion_and_archived_BM25_component"
        write_jsonl(output/(method+".jsonl"), records)
    # Labels are used only here, after retrieval, restricted to this split.
    grades = read_grades(root, set(selection["selected_question_ids"]))
    runs = {"DenseWindowMean":dense, "HybridWindowMean":hybrid}
    for name, archive_name in ARCHIVED.items():
        runs[name] = historical_run(root, stage, archive_name, queries, chunks, identity)[0]
    objectives = {name: objective(tuning_rows(chunks, queries, runs[name], grades)) for name in METHODS}
    if stage == "dev":
        recommended = choose_configuration([dict(method=name, objective=objectives[name]) for name in METHODS])["method"]
        seal = dict(config_id=config_id, source_hashes=code, config=config, encoder=encoder.descriptor,
            history=history, identity=identity, selection=selection, objectives=objectives, recommended_method=recommended,
            test_authorized=False, human_validated=False, augmented_metrics_status="NOT_RUN_NO_HUMAN_LABELS",
            validation_previously_observed=True, validation_consulted_for_this_selection=False,
            preregistration_commit=subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True, check=True).stdout.strip())
        write_json(seal_path, seal)
    write_json(output/"resources.json", dict(encoder=encoder.descriptor, dense_cache=cache, memory=memory_snapshot(),
        model_load_seconds=encoder.load_seconds, historical_bm25_latency_reused=True))
    write_json(output/"completed.json", dict(stage=stage, config_id=config_id, selection=selection, identity=identity,
        objectives=objectives, test_executed=False, seed_qrels_only=True, history=verify_history(root)))
    return dict(stage=stage, queries=len(queries), objectives=objectives, recommended_on_dev=seal["recommended_method"], history=history)
