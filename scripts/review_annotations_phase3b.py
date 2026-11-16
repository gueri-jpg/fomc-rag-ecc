"""Audit local aids; optionally consolidate genuinely attested human decisions."""
import argparse
import json
from pathlib import Path
from fomcrag.annotation_review import audit_pack, consolidate


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pack", type=Path, default=root / "references_local_only/annotations/phase3b_pack_v2")
    parser.add_argument("--sheet", type=Path)
    parser.add_argument("--attestation", type=Path)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    result = audit_pack(root, args.pack) if args.sheet is None else consolidate(root, args.pack, args.sheet, args.attestation, args.require_complete)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
