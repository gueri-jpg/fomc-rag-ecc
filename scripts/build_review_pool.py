"""Consume *existing* ranked outputs; never calls a retriever or model."""
import argparse
from pathlib import Path

from fomcrag.benchmark import export_csv, load_benchmark
from fomcrag.pooling import build_pool
from fomcrag.storage import read_jsonl


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="append", required=True, help="METHOD=ranked.jsonl")
    parser.add_argument("--top-k", type=int, default=20)
    parser.add_argument("--unit", choices=["page", "chunk"], default="chunk")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    queries, _, judgments = load_benchmark(root)
    runs = {}
    for specification in args.run:
        method, path = specification.split("=", 1)
        if method in runs:
            parser.error("Duplicate method")
        runs[method] = read_jsonl(Path(path))
        if any(r["question_id"] not in {q["question_id"] for q in queries} for r in runs[method]):
            parser.error("Unknown question in run")
    chunks = {c["chunk_id"]: c for c in read_jsonl(root / "data/processed/chunks_256.jsonl")}
    pool = build_pool(runs, chunks, judgments, top_k=args.top_k, unit=args.unit)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    export_csv(args.output, pool, ["question_id", "candidate_id", "unit", "page_id", "candidate_chunk_ids", "returned_by", "page_judgment", "review_status", "relevance_grade", "notes"])
    print(f"Exported {len(pool)} candidates; no human decisions inferred")


if __name__ == "__main__":
    main()
