# PROCESSING_NOTES.md — `new_words` Source Processing Architecture

> **Source ID:** `new_words`  
> **Source Document:** [`acquisition/sources/new_words/new_words.md`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/sources/new_words/new_words.md)  
> **Pipeline Implementation:** Isolated profile parser, cleaner, enricher, and validator under `processors/` and `parsers/new_words/`.

---

## 1. Pipeline Routing & Stage Separation

Following the multi-source architecture in [`docs/general/ARCHITECTURE.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/ARCHITECTURE.md):

1. **Acquisition:**
   - Locked in `acquisition/sources/new_words/new_words.md` (SHA-256: `6aac09b4631462c239e49c6bbbbebf0a2d30ee88acddfbb16debb780ce163ec7`).
   - Manifest: `acquisition/sources/new_words/manifest.json`.
2. **RAW Extraction:**
   - Implemented in [`parsers/new_words/parser.py`](file:///c:/Users/user/Desktop/vocabulary_parser/parsers/new_words/parser.py).
   - Generates exact byte-slice coordinates (`file_char_start`, `file_char_end`, `line_number`, `line_char_start`, `line_char_end`).
   - Output: `data/raw/sources/new_words/entries.raw.json` (159 records).
3. **Cleaning & Normalization:**
   - Implemented in [`processors/normalization/cleaner_new_words.py`](file:///c:/Users/user/Desktop/vocabulary_parser/processors/normalization/cleaner_new_words.py).
   - Verifies 100% token-ledger conservation.
   - Partitions dataset into 156 eligible records and 3 excluded elementary A2 records (`Repair`, `Several`, `Nearly`).
   - Output: `data/clean/sources/new_words/entries.clean.json`.
4. **Vocabulary Enrichment:**
   - Implemented in [`processors/enrichment/enricher_new_words.py`](file:///c:/Users/user/Desktop/vocabulary_parser/processors/enrichment/enricher_new_words.py).
   - Strictly enforces the rule: maximum TWO translation alternatives per entry; multiword alternatives permitted.
   - Normalizes POS into standard categories (`noun`, `verb`, `adjective`, `adverb`, `verb (phrasal)`, `verb phrase`, `adjective phrase`, `quantifier phrase`, `adverbial phrase`, `determiner`).
   - Output: `data/enriched/sources/new_words/entries.enriched.json`.
5. **Validation & PRE-FINAL Assembly:**
   - Implemented in [`processors/validation/validator_new_words.py`](file:///c:/Users/user/Desktop/vocabulary_parser/processors/validation/validator_new_words.py).
   - Verifies full provenance chain, non-circular explanations, Cyrillic script, and unset `difficulty: null`.
   - Output: `data/pre_final/sources/new_words/vocabulary.json`.
6. **HTML Backtesting & Review:**
   - Accessible via [`tools/vocabulary_review.py`](file:///c:/Users/user/Desktop/vocabulary_parser/tools/vocabulary_review.py) (`--source new_words`).
   - Displays `Type: Essential` or `Type: null`.
