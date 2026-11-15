# Data restoration, attribution and publication boundaries

The public repository contains code, project-authored protocol documentation,
benchmark questions/judgments, source metadata, descriptive outputs and generated
charts. Original PDFs, page screenshots, extracted corpus, private course
materials, individual annotator sheets, credentials and model weights stay local.

## Restore the source corpus

`evaluation/benchmark/MANIFESTE_CORPUS_93.csv` describes the exact snapshot:
46 Minutes and 47 Statements, 838 pages, 2021–2026. Each row provides filename,
type, year, page count and SHA256. Paths starting `TextsData/` are relative to
`utils/TxtExtraction/`, for example:

```text
utils/TxtExtraction/TextsData/minutes/fomcminutes20210127.pdf
utils/TxtExtraction/TextsData/statements/monetary20210127a1.pdf
```

Use the team's preserved snapshot for exact byte-for-byte reproduction.
Alternatively locate named documents through the official
[FOMC calendars](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm)
and [historical materials](https://www.federalreserve.gov/monetarypolicy/fomc_historical.htm).
Usual official PDF locations are:

```text
https://www.federalreserve.gov/monetarypolicy/files/<minutes-filename.pdf>
https://www.federalreserve.gov/newsevents/pressreleases/files/<statement-filename.pdf>
```

These are location conventions, not a claim that all 93 URLs were fetched or
that current bytes match. No bulk PDF download was performed for publication.
Unavailable documents must be restored from the team's preserved snapshot;
do not manufacture replacements or silently change hashes/page counts.
Availability/authenticity of each remote document is not independently certified.

```powershell
& .venv\Scripts\python.exe scripts/preflight_codex.py --hash-pdfs
& .venv\Scripts\python.exe scripts/ingest.py
& .venv\Scripts\python.exe scripts/eda.py
& .venv\Scripts\python.exe scripts/verify_phase1.py --rebuild --eda-rebuild
```

## Rights and provenance review

The Federal Reserve Board's [website disclaimer](https://www.federalreserve.gov/disclaimer.htm)
states that Board website information is in the public domain unless otherwise
indicated, with exceptions for third-party material. This policy was checked
when preparing publication. Selected evidence consists of attributed FOMC text
excerpts; EDA tables contain filenames, counts, short recurring text and derived
statistics. No private course slides or individual reviewer identities are
included. The owner's publication instruction covers the team's project code,
questions, judgments and technical documentation. This does not assign a
software/benchmark reuse license; that decision remains with the owners.

Original page images, including logos, remain excluded regardless of source
rights. Private course material stays in `references_local_only/`.
Dependency-resolution JSON reports with workstation paths remain unpublished;
scripts and locks provide reproduction. Unnecessary workstation identifiers
were removed from phase reports while preserving measured results and limits.
