"""Offline conservative secret scan. Report paths/counts only, never matched text."""
from pathlib import Path
import argparse
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{32,}\b"),
    re.compile(r"(?:postgres(?:ql)?|https?)://[^\s/:]+:[^\s/@]+@", re.I),
    re.compile(r'''(?:password|api_key|secret|token)\s*=\s*["'][^"'\s]{12,}["']''', re.I),
]


def audit_staged():
    """Inspect actual index blobs, including CSV/TREC and hidden text files."""
    names = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"], cwd=ROOT, capture_output=True, check=True).stdout.decode("utf-8").split("\0")
    findings = []
    total_bytes = 0
    files = []
    denied_parts = {".venv", "venv", "references_local_only", "artifacts", "models", "cache", "_cache", ".aws", ".git", "__pycache__", ".vscode"}
    personal_path = re.compile(r"[A-Za-z]:[\\/](?:Users|Documents and Settings)[\\/]", re.I)
    for name in filter(None, names):
        parts = Path(name).parts
        suffix = Path(name).suffix.lower()
        if (denied_parts.intersection(parts) or name.startswith(("data/processed/", "reports/figures/source_checks/"))
                or (Path(name).name.startswith(".env") and Path(name).name != ".env.example")
                or suffix in {".pdf", ".pem", ".key", ".p12", ".pfx", ".zip", ".bin", ".pt", ".ckpt", ".safetensors", ".db", ".sqlite3", ".log"}
                or name == ".streamlit/secrets.toml"):
            findings.append({"path": name, "reason": "forbidden_path"})
            continue
        data = subprocess.run(["git", "show", ":" + name], cwd=ROOT, capture_output=True, check=True).stdout
        total_bytes += len(data)
        files.append({"path": name, "bytes": len(data)})
        if len(data) > 5 * 1024 * 1024:
            findings.append({"path": name, "reason": "blob_over_5_MiB"})
        if data.startswith(b"%PDF"):
            findings.append({"path": name, "reason": "pdf_content"})
        if suffix == ".png":
            if not data.startswith(b"\x89PNG\r\n\x1a\n") or not name.startswith(("reports/figures/phase1_", "reports/figures/phase3_")):
                findings.append({"path": name, "reason": "unapproved_image"})
            continue
        try:
            content = data.decode("utf-8-sig")
        except UnicodeDecodeError:
            findings.append({"path": name, "reason": "unapproved_binary"})
            continue
        matches = sum(len(pattern.findall(content)) for pattern in PATTERNS)
        if matches:
            findings.append({"path": name, "reason": "secret_pattern", "matches": matches})
        if personal_path.search(content):
            findings.append({"path": name, "reason": "personal_windows_path"})
    result = {"status": "FAIL" if findings else "PASS", "scope": "actual staged blobs; heuristic scan",
              "files": files, "total_bytes": total_bytes, "findings": findings}
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 1 if findings else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--staged", action="store_true")
    if parser.parse_args().staged:
        return audit_staged()
    listing = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT, capture_output=True, check=True,
    ).stdout.decode("utf-8").split("\0")
    findings = []
    scanned = 0
    for name in sorted(set(filter(None, listing))):
        path = ROOT / name
        if path.suffix.lower() not in {".py", ".md", ".json", ".toml", ".txt", ".yaml", ".yml", ".example"}:
            continue
        content = path.read_text(encoding="utf-8", errors="replace")
        scanned += 1
        count = sum(len(pattern.findall(content)) for pattern in PATTERNS)
        if count:
            findings.append({"path": name, "matches": count})
    tracked_env = subprocess.run(["git", "ls-files", ".env", ".env.*"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.splitlines()
    tracked_secrets = [name for name in tracked_env if name != ".env.example"]
    result = {"scanned_text_files": scanned, "findings": findings,
              "tracked_secret_paths": tracked_secrets,
              "scope": "Git-eligible text only; ignored secrets not opened; heuristic, not a guarantee",
              "status": "FAIL" if findings or tracked_secrets else "PASS"}
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 1 if findings or tracked_secrets else 0


if __name__ == "__main__":
    raise SystemExit(main())
