"""Descriptive, unsupervised corpus audit; never reads benchmark questions."""
from __future__ import annotations

from collections import Counter, defaultdict
import csv
from itertools import combinations
import json
import os
from pathlib import Path
import re

from .preprocessing import HYPHEN_BREAK, WORD, lexical_tokens
from .storage import file_hash, fingerprint, read_jsonl, write_json

# For one descriptive frequency table only; never applied to BM25 input.
EDA_STOPWORDS = set("a an the and or of to in for on at by with as is are was were be been being that this these those it its from had has have would could should will may might their they than which also more most some over all not no".split())
ECONOMIC_TERMS = ("inflation", "federal funds rate", "labor market", "unemployment", "monetary policy",
                  "balance sheet", "economic activity", "interest rates", "basis points", "percent",
                  "financial conditions", "price stability", "maximum employment", "treasury", "uncertainty")


def write_csv(path: Path, rows: list[dict], fields: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields or list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def distribution(values: list[int]) -> dict:
    import numpy as np
    if not values:
        return {key: 0 for key in ("count", "min", "p05", "p25", "median", "p75", "p95", "max", "mean", "sum")}
    return dict(count=len(values), min=min(values), p05=float(np.percentile(values, 5)),
                p25=float(np.percentile(values, 25)), median=float(np.median(values)),
                p75=float(np.percentile(values, 75)), p95=float(np.percentile(values, 95)),
                max=max(values), mean=float(np.mean(values)), sum=sum(values))


def audit_corpus(processed: Path, report: Path, figures: Path) -> dict:
    """Produce CSV/JSON and deterministic plots from verified extraction files."""
    cache = report.resolve() / "_cache/matplotlib"
    cache.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(cache))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    manifest = json.loads((processed / "manifest.json").read_text(encoding="utf-8"))
    if manifest["status"] != "PASS":
        raise ValueError("Cannot audit incomplete corpus")
    for name, metadata in manifest["files"].items():
        if file_hash(processed / name) != metadata["sha256"]:
            raise ValueError(f"Export checksum mismatch: {name}")
    pages = read_jsonl(processed / "pages.jsonl")
    docs = read_jsonl(processed / "documents.jsonl")
    report.mkdir(parents=True, exist_ok=True)
    figures.mkdir(parents=True, exist_ok=True)
    groups: dict[tuple, dict] = {}
    for doc in docs:
        key = (doc["year"], doc["doc_type"])
        group = groups.setdefault(key, dict(year=key[0], document_type=key[1], documents=0, pages=0, words=0))
        group["documents"] += 1
        group["pages"] += doc["physical_pages"]
        group["words"] += doc["word_count"]
    write_csv(report / "by_year_type.csv", list(groups.values()))
    write_csv(report / "documents.csv", [{k: d[k] for k in ("document", "meeting_date", "year", "doc_type", "physical_pages", "word_count", "char_count", "pdf_sha256")} for d in docs])
    monthly = Counter((d["meeting_date"][:7], d["doc_type"]) for d in docs)
    write_csv(report / "chronology.csv", [dict(month=month, document_type=kind, documents=count) for (month, kind), count in sorted(monthly.items())])
    page_stats, anomaly_rows = [], []
    frequencies: Counter = Counter()
    doc_frequencies: dict[str, set] = defaultdict(set)
    recurring: dict[str, set] = defaultdict(set)
    grams: Counter = Counter()
    gram_pages: dict[str, set] = defaultdict(set)
    exact: dict[str, list] = defaultdict(list)
    token_sets = []
    term_rows = []
    for page in pages:
        tokens = lexical_tokens(page["text"])
        frequencies.update(tokens)
        for token in set(tokens):
            doc_frequencies[token].add(page["document"])
        page_grams = [" ".join(tokens[i:i + 5]) for i in range(len(tokens) - 4)]
        grams.update(page_grams)
        for gram in set(page_grams):
            gram_pages[gram].add(page["page_id"])
        token_sets.append(set(page_grams))
        for line in page["raw_text"].splitlines():
            line = " ".join(line.split())
            if len(line) >= 20:
                recurring[line].add(page["page_id"])
        # Exact normalized text, excluding blank pages.
        if page["text"]:
            exact[fingerprint(page["text"])].append(page["page_id"])
        suspicious = sum(0xE000 <= ord(c) <= 0xF8FF for c in page["text"])
        row = {k: page[k] for k in ("document", "page_id", "page", "year", "doc_type", "word_count", "char_count", "raw_char_count")}
        row.update(hyphen_line_breaks=len(HYPHEN_BREAK.findall(page["raw_text"])),
                   replacement_chars=page["text"].count("\ufffd"), private_use_chars=suspicious,
                   layout_rules=sum(len(w) >= 50 and not any(c.isalnum() for c in w) for w in WORD.findall(page["text"])),
                   long_words=sum(len(w) >= 50 and any(c.isalnum() for c in w) for w in WORD.findall(page["text"])))
        page_stats.append(row)
        kinds = []
        if not page["word_count"]:
            kinds.append("empty")
        elif page["word_count"] < manifest["config"]["short_page_words"]:
            kinds.append("short_page")
        if row["replacement_chars"] or row["private_use_chars"]:
            kinds.append("encoding_suspect")
        if row["long_words"]:
            kinds.append("long_word")
        if row["layout_rules"]:
            kinds.append("layout_rule")
        for kind in kinds:
            anomaly_rows.append(dict(page_id=page["page_id"], kind=kind, word_count=page["word_count"]))
        joined = " " + " ".join(tokens) + " "
        for term in ECONOMIC_TERMS:
            count = len(re.findall(r"(?<!\S)" + re.escape(term) + r"(?!\S)", joined))
            if count:
                term_rows.append(dict(term=term, page_id=page["page_id"], document=page["document"], year=page["year"], document_type=page["doc_type"], occurrences=count))
    write_csv(report / "pages.csv", page_stats)
    write_csv(report / "anomalies.csv", anomaly_rows, ["page_id", "kind", "word_count"])
    word_rows = [dict(term=token, occurrences=count, document_frequency=len(doc_frequencies[token])) for token, count in sorted(frequencies.items(), key=lambda item: (-item[1], item[0]))]
    write_csv(report / "word_frequencies.csv", word_rows)
    content_words = [row for row in word_rows if row["term"] not in EDA_STOPWORDS and row["term"].isalpha()]
    write_csv(report / "content_word_frequencies.csv", content_words)
    write_json(report / "eda_stopwords.json", sorted(EDA_STOPWORDS))
    write_csv(report / "economic_terms_by_page.csv", term_rows, ["term", "page_id", "document", "year", "document_type", "occurrences"])
    term_totals = [dict(term=term, occurrences=sum(r["occurrences"] for r in term_rows if r["term"] == term),
                        pages=len({r["page_id"] for r in term_rows if r["term"] == term})) for term in ECONOMIC_TERMS]
    write_csv(report / "economic_terms.csv", term_totals)
    repeated = [dict(line=line, pages=len(ids), page_ids="|".join(sorted(ids))) for line, ids in recurring.items() if len(ids) >= 3]
    repeated.sort(key=lambda row: (-row["pages"], row["line"]))
    write_csv(report / "recurrent_lines.csv", repeated, ["line", "pages", "page_ids"])
    phrases = [dict(phrase=gram, occurrences=count, pages=len(gram_pages[gram])) for gram, count in grams.most_common(100)]
    write_csv(report / "recurrent_5grams.csv", phrases)
    duplicate_rows = [dict(text_sha256=h, page_ids="|".join(ids), pages=len(ids)) for h, ids in exact.items() if len(ids) > 1]
    write_csv(report / "exact_duplicate_pages.csv", duplicate_rows, ["text_sha256", "page_ids", "pages"])
    duplicate_pdfs: dict[str, list] = defaultdict(list)
    for doc in docs:
        duplicate_pdfs[doc["pdf_sha256"]].append(doc["document"])
    write_csv(report / "exact_duplicate_pdfs.csv", [dict(pdf_sha256=h, documents="|".join(ids), count=len(ids)) for h, ids in duplicate_pdfs.items() if len(ids) > 1], ["pdf_sha256", "documents", "count"])
    near = []
    threshold = manifest["config"]["near_duplicate_jaccard"]
    for i, j in combinations(range(len(pages)), 2):
        a, b = token_sets[i], token_sets[j]
        if not a or not b or min(len(a), len(b)) / max(len(a), len(b)) < threshold:
            continue
        intersection = len(a.intersection(b))
        similarity = intersection / (len(a) + len(b) - intersection)
        if similarity >= threshold:
            near.append(dict(page_a=pages[i]["page_id"], page_b=pages[j]["page_id"], jaccard_5grams=round(similarity, 6),
                             same_document=pages[i]["document"] == pages[j]["document"]))
    write_csv(report / "near_duplicate_pages.csv", near, ["page_a", "page_b", "jaccard_5grams", "same_document"])
    chunk_stats, chunk_dist, chunk_by_group = [], {}, []
    for size, entry in manifest["chunks"].items():
        chunks = read_jsonl(processed / entry["file"])
        chunk_dist[size] = distribution([c["word_count"] for c in chunks])
        chunk_dist[size]["short_chunks"] = sum(c["word_count"] < manifest["config"]["short_chunk_words"] for c in chunks)
        chunk_dist[size]["overlap_expansion"] = sum(c["word_count"] for c in chunks) / sum(p["word_count"] for p in pages)
        for chunk in chunks:
            chunk_stats.append(dict(window_words=int(size), **{key: chunk[key] for key in ("chunk_id", "page_id", "document", "year", "doc_type", "word_count", "char_start", "char_end")},
                                    short_fragment=chunk["word_count"] < manifest["config"]["short_chunk_words"]))
        counts = Counter((c["year"], c["doc_type"]) for c in chunks)
        chunk_by_group.extend(dict(window_words=int(size), year=y, document_type=t, chunks=count) for (y, t), count in sorted(counts.items()))
    write_csv(report / "chunks.csv", chunk_stats)
    write_csv(report / "chunks_by_year_type.csv", chunk_by_group)
    distributions = []
    for kind in ("minutes", "statements"):
        for unit, values in (("document_words", [d["word_count"] for d in docs if d["doc_type"] == kind]),
                             ("page_words", [p["word_count"] for p in pages if p["doc_type"] == kind]),
                             ("document_pages", [d["physical_pages"] for d in docs if d["doc_type"] == kind])):
            distributions.append(dict(document_type=kind, unit=unit, **distribution(values)))
        for size in manifest["chunks"]:
            distributions.append(dict(document_type=kind, unit=f"chunk{size}_words", **distribution([c["word_count"] for c in chunk_stats if c["doc_type"] == kind and c["window_words"] == int(size)])))
    write_csv(report / "distributions_by_type.csv", distributions)
    glyphs = Counter(c for p in pages for c in p["text"] if 0xE000 <= ord(c) <= 0xF8FF or c == "\ufffd")
    write_csv(report / "suspect_glyphs.csv", [dict(codepoint=f"U+{ord(c):04X}", occurrences=n) for c, n in sorted(glyphs.items())], ["codepoint", "occurrences"])
    stats = {"corpus_version": manifest["corpus_version"], "documents": len(docs), "physical_pages": len(pages),
             "years": sorted({p["year"] for p in pages}), "first_meeting": min(d["meeting_date"] for d in docs),
             "last_meeting": max(d["meeting_date"] for d in docs),
             "by_year_type": list(groups.values()),
             "document_words": distribution([d["word_count"] for d in docs]),
             "document_pages": distribution([d["physical_pages"] for d in docs]),
             "page_words": distribution([p["word_count"] for p in pages]),
             "page_chars": distribution([p["char_count"] for p in pages]),
             "chunks": chunk_dist, "anomalies": dict(Counter(row["kind"] for row in anomaly_rows)),
             "empty_pages": sum(not p["text"] for p in pages), "extraction_errors": sum(p["extraction_status"] != "ok" for p in pages),
             "replacement_characters": sum(row["replacement_chars"] for row in page_stats),
             "private_use_characters": sum(row["private_use_chars"] for row in page_stats),
             "exact_duplicate_pdf_groups": sum(len(ids) > 1 for ids in duplicate_pdfs.values()),
             "hyphen_breaks": sum(row["hyphen_line_breaks"] for row in page_stats),
             "pages_with_hyphen_breaks": sum(row["hyphen_line_breaks"] > 0 for row in page_stats),
             "exact_duplicate_page_groups": len(duplicate_rows), "near_duplicate_pairs": len(near),
             "recurrent_lines_ge3_pages": len(repeated), "lexical_vocabulary": len(frequencies),
             "near_duplicate_method": "all-pairs Jaccard of sets of 5 lexical token shingles, threshold " + str(threshold)}
    write_json(report / "summary.json", stats)

    plt.rcParams.update({"font.size": 10, "figure.dpi": 120})
    def save(fig, name):
        fig.tight_layout()
        fig.savefig(figures / name, dpi=160, metadata={"Software": "fomcrag phase1"})
        plt.close(fig)

    years = stats["years"]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    for ax, field, title, unit in zip(axes, ("documents", "pages"), ("Documents par année et type", "Pages physiques par année et type"), ("Documents (nombre)", "Pages (nombre)")):
        for k, kind in enumerate(("minutes", "statements")):
            ax.bar(np.arange(len(years)) + (k - 0.5) * 0.36, [groups.get((year, kind), {}).get(field, 0) for year in years], width=0.36, label=kind)
        ax.set(xticks=np.arange(len(years)), xticklabels=years, xlabel="Année (2026 partielle)", ylabel=unit, title=title)
        ax.legend()
    save(fig, "phase1_year_type.png")
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    for ax, values, title, unit in zip(axes, ([d["word_count"] for d in docs], [p["word_count"] for p in pages], [d["physical_pages"] for d in docs]),
                                      ("Longueur des documents", "Longueur des pages", "Pagination des documents"), ("Mots par document", "Mots par page", "Pages par document")):
        ax.hist(values, bins=30, edgecolor="white")
        ax.set(xlabel=unit, ylabel="Fréquence (nombre)", title=title)
    save(fig, "phase1_lengths.png")
    fig, ax = plt.subplots(figsize=(10, 6))
    top = content_words[:20][::-1]
    ax.barh([r["term"] for r in top], [r["occurrences"] for r in top])
    ax.set(xlabel="Occurrences lexicales (sans stopwords EDA)", ylabel="Terme", title="20 mots fréquents — corpus complet")
    save(fig, "phase1_frequent_words.png")
    fig, ax = plt.subplots(figsize=(10, 6))
    terms = sorted(term_totals, key=lambda r: r["occurrences"])
    ax.barh([r["term"] for r in terms], [r["occurrences"] for r in terms], color="#237c72")
    ax.set(xlabel="Occurrences (expression exacte normalisée)", ylabel="Expression économique", title="Termes économiques — corpus complet")
    save(fig, "phase1_economic_terms.png")
    fig, axes = plt.subplots(1, len(manifest["chunks"]), figsize=(15, 4))
    for ax, size in zip(np.atleast_1d(axes), manifest["chunks"]):
        values = [c["word_count"] for c in chunk_stats if c["window_words"] == int(size)]
        ax.hist(values, bins=25, edgecolor="white")
        ax.axvline(manifest["config"]["short_chunk_words"], color="red", linestyle="--", label="Fragment court <40 mots")
        ax.set(xlabel="Mots par chunk", ylabel="Chunks (nombre)", title=f"Fenêtre {size}, overlap {manifest['config']['overlap_words']}")
        ax.legend(fontsize=8)
    save(fig, "phase1_chunks.png")
    fig, ax = plt.subplots(figsize=(14, 3.5))
    months = [f"{year}-{month:02d}" for year in years for month in range(1, 13)]
    for k, kind in enumerate(("minutes", "statements")):
        ax.bar(np.arange(len(months)) + (k - 0.5) * 0.4, [monthly[(month, kind)] for month in months], width=0.4, label=kind)
    ax.set(xticks=np.arange(0, len(months), 3), xticklabels=months[::3], xlabel="Mois de fin de réunion", ylabel="Documents (nombre)", title="Couverture chronologique — absence ≠ donnée négative")
    ax.tick_params(axis="x", rotation=60)
    ax.legend()
    save(fig, "phase1_chronology.png")
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    kinds = ["minutes", "statements"]
    axes[0].boxplot([[p["word_count"] for p in pages if p["doc_type"] == kind] for kind in kinds], tick_labels=kinds)
    axes[0].set(xlabel="Type de document", ylabel="Mots par page", title="Longueurs de pages par type")
    baseline = manifest["config"]["baseline_words"]
    selected = [r for r in chunk_by_group if r["window_words"] == baseline]
    for k, kind in enumerate(kinds):
        axes[1].bar(np.arange(len(years)) + (k - 0.5) * 0.36,
                    [sum(r["chunks"] for r in selected if r["year"] == year and r["document_type"] == kind) for year in years],
                    width=0.36, label=kind)
    axes[1].set(xticks=np.arange(len(years)), xticklabels=years, xlabel="Année (2026 partielle)", ylabel="Chunks (nombre)", title=f"Répartition du baseline {baseline} mots")
    axes[1].legend()
    save(fig, "phase1_type_and_chunks.png")
    write_json(report / "manifest.json", {
        "corpus_version": manifest["corpus_version"],
        "input_manifest_sha256": file_hash(processed / "manifest.json"),
        "eda_code_sha256": file_hash(Path(__file__)),
        "numpy": np.__version__, "matplotlib": matplotlib.__version__,
        "tables": {p.name: file_hash(p) for p in sorted(report.glob("*.csv"))},
        "figures": {p.name: file_hash(p) for p in sorted(figures.glob("phase1_*.png"))},
    })
    return stats
