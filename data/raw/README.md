# RAW Extraction Outputs (`data/raw/`)

> **Status:** Initialized foundation only. **No RAW extraction has been executed yet.**

## 1. Intended Responsibility

`data/raw/` stores the **immutable initial extraction outputs** produced directly from source documents in [`acquisition/local/`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/local).

Its core purpose is **source-faithful preservation**: capturing exact text, layout coordinates, component boundaries, visual assets, and extraction warnings/issues so that downstream stages (`CLEAN`, `Matching`, `Categorization`) never have to guess what the original document contained or re-parse the raw file.

---

## 2. Mandatory RAW Preservation Principles (From Codex Section 5)

When RAW parsers are implemented and write to `data/raw/<source_profile>/`, they must keep five concepts strictly distinct:

1. **Exact Extracted Source Text & Spans:**
   - Store the full unmodified page/source text alongside exact slice offsets (`start`, `end`) for every extracted entry, line, and component.
   - It must be possible to reconstruct every extracted entry's raw text directly from unchanged source slices (`validate_raw` invariant).
2. **Readable Text Interpretation:**
   - When font decoding (e.g., verified CID mappings, ligature expansion, phonetic symbol normalization) or spatial reading-order repair is applied, store the readable projection **alongside** the exact original string—never overwrite the original text or confuse decoded string lengths with original span offsets.
3. **Semantic Component Ownership:**
   - Explicitly record which entry and sub-component (e.g., headword, pronunciation, part of speech, definition, example, stem, option, excluded header/footer) owns each text span or visual object.
4. **Focused Genuine Assets vs. Diagnostic Previews:**
   - Separate genuine content assets (tables, illustrations, diagrams required by an entry) from broad page/entry debugging previews. Store coordinate frames, bounding boxes, and SHA-256 hashes for all assets.
5. **Honest Extraction Issues:**
   - Emit structured RAW findings whenever segmentation, encoding, visual ownership, or raster/OCR fidelity is uncertain. Never mask uncertain extraction via destructive cleanup in RAW.

---

## 3. What Belongs Here

- Per-profile or per-document `.raw.json` files containing extracted records, page texts, spans, geometry, and structured RAW issues.
- Extracted raw visual assets (e.g., PNG crops) organized under the corresponding source profile directory.
- RAW-stage validation summary JSON (`validation.json`).

---

## 4. What Must NOT Be Stored Here

- **No original source files:** Keep PDFs, DOCX, and HTML inputs in [`acquisition/local/`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/local).
- **No cleaned/normalized projections:** Line-wrap reflow, punctuation normalization, and derived clean crops belong in a separate future `data/clean/` directory so defects introduced during cleaning can always be distinguished from RAW extraction defects (Codex Section 6.1).
- **No manual text patches:** Never hand-edit `.raw.json` files to fix a broken extraction; fix the parser or register a provenance-tracked manual override downstream.
- **No narrative Markdown reports:** Human-readable backtesting and issue reports (`RAW_BACKTESTING.md`, `RAW_ISSUES.md`) belong in [`qa/`](file:///c:/Users/user/Desktop/vocabulary_parser/qa).

---

## 5. Relationship to Other Parts of the Project

1. **Produced from [`acquisition/local/`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/local):** Locked to source files via `source_sha256`.
2. **Consumed by Future `CLEAN` Stage:** Future normalization processors will read `data/raw/` (read-only) and embed both a `raw_record` snapshot and the RAW file SHA-256 + JSON pointer.
3. **Verified by [`qa/`](file:///c:/Users/user/Desktop/vocabulary_parser/qa) and [`tests/`](file:///c:/Users/user/Desktop/vocabulary_parser/tests):** Subject to span-reconstruction tests, adjacent-entry boundary checks, and `RAW_BACKTESTING.md` / `RAW_ISSUES.md` generation.
