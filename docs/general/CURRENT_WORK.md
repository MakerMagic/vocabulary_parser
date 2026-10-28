# Current Operational State (`CURRENT_WORK.md`)

> **Last Updated:** 2026-10-28  
> **Status:** Initial Architecture, Documentation Framework, Project Skills & PDF Tooling Installed and Verified

---

## Current milestone

Establish the initial repository foundation, architectural contracts, documentation system (`docs/general/`), project skills (`.agents/skills/`), and verified PDF-processing/testing environment (`.venv/`, `requirements.txt`) for the Vocabulary Document-Parsing Pipeline.

---

## Already completed

1. **Codex Handover Preservation:** Preserved [`PARSING_KNOWLEDGE_TRANSFER.md`](file:///c:/Users/user/Desktop/vocabulary_parser/PARSING_KNOWLEDGE_TRANSFER.md) and [`DOCUMENTATION_ARCHITECTURE_HANDOVER.md`](file:///c:/Users/user/Desktop/vocabulary_parser/DOCUMENTATION_ARCHITECTURE_HANDOVER.md) as immutable historical reference material.
2. **Repository Foundation:**
   - Initialized drop zone for source documents in [`acquisition/local/`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/local).
   - Established pre-parsing profiling registry in [`inspections/SOURCE_PROFILES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/inspections/SOURCE_PROFILES.md).
   - Created immutable extraction storage directory [`data/raw/`](file:///c:/Users/user/Desktop/vocabulary_parser/data/raw) with strict data contracts.
   - Initialized QA defect ledger [`qa/ISSUE_LOG.md`](file:///c:/Users/user/Desktop/vocabulary_parser/qa/ISSUE_LOG.md) and stage reporting rules.
   - Defined automated testing standards in [`tests/README.md`](file:///c:/Users/user/Desktop/vocabulary_parser/tests/README.md).
   - Created root [`.gitignore`](file:///c:/Users/user/Desktop/vocabulary_parser/.gitignore) and [`requirements.txt`](file:///c:/Users/user/Desktop/vocabulary_parser/requirements.txt).
3. **Documentation Architecture (`docs/general/`):**
   - [`PROJECT_CONTEXT.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/PROJECT_CONTEXT.md), [`ARCHITECTURE.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/ARCHITECTURE.md), [`DATA_SCHEMA.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/DATA_SCHEMA.md), [`PROCESSING_RULES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/PROCESSING_RULES.md), [`DEVELOPMENT_RULES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/DEVELOPMENT_RULES.md), [`CODEX_SKILLS_USAGE.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/CODEX_SKILLS_USAGE.md), and [`CURRENT_WORK.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/CURRENT_WORK.md).
4. **Installed Project Skills (`.agents/skills/`):**
   - Installed and adapted all 7 project skills under [`.agents/skills/`](file:///c:/Users/user/Desktop/vocabulary_parser/.agents/skills): `project-architecture-guardrails`, `processing-raw-preservation`, `testing-validation-expectations`, `data-schema-consistency`, `safe-development-workflow`, `token-efficient-context-routing`, and `token-saver-codex` (with [`skills-lock.json`](file:///c:/Users/user/Desktop/vocabulary_parser/skills-lock.json)).
5. **Installed & Verified Python / PDF / CLI Environment:**
   - Configured [`.venv/`](file:///c:/Users/user/Desktop/vocabulary_parser/.venv) (Python `3.13.16`) and installed `pdfplumber==0.11.10`, `pdfminer.six==20260107`, `pypdfium2==5.14.0`, `pillow==12.3.0`, `pytest==9.1.1`, and `ruff==0.16.10` in both `.venv` and system Python.
   - Installed `ripgrep` (`rg` `15.2.0`) via `winget` alongside `git`, `node`, and `PowerShell`.

---

## In progress

- Awaiting intake of first Vocabulary source documents into `acquisition/local/`.

---

## Next task

1. Ingest initial Vocabulary source document(s) (PDF, DOCX, HTML, TXT, etc.) into [`acquisition/local/`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/local).
2. Generate SHA-256 manifest and document role metadata in `acquisition/`.
3. Perform source layout, font/IPA encoding, and boundary inspection using `pdfplumber` / `pdfminer.six` / `pypdfium2`, recording findings in [`inspections/SOURCE_PROFILES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/inspections/SOURCE_PROFILES.md).

---

## Do not work on yet

- **Do NOT write parsers or extraction code** before source documents are ingested and profiled.
- **Do NOT create downstream directories** (`data/clean/`, `data/pre_final/`, `processors/`) prematurely.
- **Do NOT install conditional OCR packages** (`tesseract.js`, `pix2text`, `cnocr`) unless source inspection proves scanned/raster PDFs exist.
- **Do NOT hand-edit generated JSON or stage reports.**
