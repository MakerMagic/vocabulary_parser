# Pipeline Data Artifacts (`data/`)

## 1. Intended Responsibility

The `data/` directory holds **canonical, structured pipeline outputs** organized strictly by processing stage. Canonical JSON files in `data/` are the single source of truth for inspecting pipeline state and validating downstream readiness (Codex Section 13.2).

---

## 2. Current Stage Directories

- **[`data/raw/`](file:///c:/Users/user/Desktop/vocabulary_parser/data/raw)** — **Initialized (Empty Placeholder).** Preserves original extraction outputs, exact source spans, layout coordinates, extracted visual assets, and RAW-stage findings once RAW extraction is implemented.

### Deferred Stage Directories (Do NOT Create Prematurely)

Future subdirectories under `data/` (`data/clean/`, `data/merged/`, `data/categorized/`, `data/pre_final/`) are **intentionally omitted** until their corresponding upstream stages and schemas are designed and verified.

---

## 3. What Belongs Here

- Deterministic, schema-validated JSON artifacts produced by pipeline stages (starting with `data/raw/`).
- Extracted and derived visual/table assets referenced by canonical JSON records (with SHA-256 integrity hashes).
- Stage validation metadata (`validation.json`) recording input/output counts, file hashes, and structured issue summaries.

---

## 4. What Must NOT Be Stored Here

- **No original source documents:** Unmodified PDFs, DOCX, HTML, or text sources belong in [`acquisition/local/`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/local).
- **No parser or processor code:** Python modules and scripts belong in stage code directories (`parsers/`, `processors/`).
- **No undocumented manual edits:** Never hand-edit generated JSON or overwrite asset files inside `data/`. Manual corrections must be supplied via explicit, provenance-tracked overlay files (see [`docs/PROVENANCE_AND_CONTRACTS.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/PROVENANCE_AND_CONTRACTS.md)).
- **No disposable HTML previews or narrative reports:** Diagnostic HTML previews belong in [`inspections/`](file:///c:/Users/user/Desktop/vocabulary_parser/inspections), and Markdown QA reports (`<STAGE>_BACKTESTING.md`, `<STAGE>_ISSUES.md`) belong in [`qa/`](file:///c:/Users/user/Desktop/vocabulary_parser/qa).

---

## 5. Relationship to Other Parts of the Project

1. **Derived from [`acquisition/local/`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/local):** Every record in `data/raw/` locks to a source file in `acquisition/local/` via `source_sha256`.
2. **Audited by [`qa/`](file:///c:/Users/user/Desktop/vocabulary_parser/qa) and [`tests/`](file:///c:/Users/user/Desktop/vocabulary_parser/tests):** Automated tests and QA stage reports verify the integrity, source reconstruction, and issue counts of `data/` artifacts.
3. **Strict Upstream Immutability:** Downstream stages read upstream `data/` directories as **read-only** inputs and write to their own stage directory, embedding upstream file and record hashes to detect dependency drift (Codex Section 12.1–12.2).
