# Acquisition (`acquisition/`)

## 1. Intended Responsibility

The `acquisition/` directory manages **incoming original Vocabulary source documents** and their **origin/identity metadata**. Its sole job is to preserve untouched source files and establish authoritative file-level provenance before any inspection or extraction occurs.

---

## 2. Directory Structure

- `acquisition/local/` — Storage for original, unmodified local source files (e.g., PDF, DOCX, HTML, TXT, CSV, images). If multiple distinct source families are added later, group them into clear subdirectories by source family (`acquisition/local/<source_family>/`).
- `acquisition/manifest.json` *(to be created/updated when files are ingested)* — Canonical registry mapping each file in `acquisition/local/` to its SHA-256 hash, origin, source family, document role (e.g., `wordlist`, `glossary`, `exercise_paper`, `answer_key`, `explanations`), and acquisition date.

---

## 3. What Belongs Here

- Original, byte-for-byte unmodified Vocabulary source documents inside `acquisition/local/`.
- Provenance manifests, download/import logs, and source-identification metadata.
- Approved, explicitly provenance-tagged manual source supplements (if a missing key or errata sheet is supplied externally), kept clearly separated from original primary documents.

---

## 4. What Must NOT Be Stored Here

- **No extracted or parsed data:** RAW JSON, cleaned records, cropped assets, and intermediate text dumps belong in `data/raw/` or downstream `data/` subdirectories.
- **No parser or normalization code:** Extraction scripts belong in `parsers/` once source inspection is complete.
- **No destructively modified sources:** Never hand-edit, re-save, or OCR-overwrite an original PDF/document in `acquisition/local/`.
- **No inspection notes or QA reports:** Document layout analyses belong in `inspections/`, and extraction defects belong in `qa/`.

---

## 5. Relationship to Other Parts of the Project

1. **Feeds [`inspections/`](file:///c:/Users/user/Desktop/vocabulary_parser/inspections):** Every new source family added to `acquisition/local/` must first be examined and profiled in [`inspections/SOURCE_PROFILES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/inspections/SOURCE_PROFILES.md).
2. **Feeds Future `parsers/` & [`data/raw/`](file:///c:/Users/user/Desktop/vocabulary_parser/data/raw):** RAW parsers read strictly from `acquisition/local/` (read-only) and embed each file's `source_sha256` and identity metadata into `data/raw/` outputs.
3. **Protects Downstream Integrity:** Changing or replacing a file in `acquisition/local/` changes its SHA-256 hash, which automatically invalidates downstream RAW, CLEAN, and PRE-FINAL bindings (see [`docs/PROVENANCE_AND_CONTRACTS.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/PROVENANCE_AND_CONTRACTS.md)).
