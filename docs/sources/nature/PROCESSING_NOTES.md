# Nature Processing Notes (`PROCESSING_NOTES.md`)

> **Source ID:** `nature`  
> **Source Document:** [`acquisition/sources/nature/Nature_Vocabulary_Simplified.csv`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/sources/nature/Nature_Vocabulary_Simplified.csv)  
> **Document Role:** Introductory & Intermediate Nature and Environmental Science Vocabulary

---

## 1. Pipeline Execution Architecture

1. **Acquisition Stage:**
   - Source preserved in [`acquisition/local/Nature_Vocabulary_Simplified.csv`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/local/Nature_Vocabulary_Simplified.csv) and mirrored to [`acquisition/sources/nature/Nature_Vocabulary_Simplified.csv`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/sources/nature/Nature_Vocabulary_Simplified.csv).
   - SHA-256 lock: `215bdb89ad6910d4edeeddebf980523bd2ad55616c651cf908cbdf713d0809bc`.
   - Manifest: [`acquisition/sources/nature/manifest.json`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/sources/nature/manifest.json).
2. **RAW Extraction Stage:**
   - Implemented in [`parsers/nature/parser.py`](file:///c:/Users/user/Desktop/vocabulary_parser/parsers/nature/parser.py).
   - Extracts all 169 records with exact character offset coordinates indexing into the source CSV.
   - Assigns `preset: "nature"` and `difficulty: null`.
3. **Cleaning Stage:**
   - Implemented in [`processors/normalization/cleaner_nature.py`](file:///c:/Users/user/Desktop/vocabulary_parser/processors/normalization/cleaner_nature.py).
   - Verified 100% token-ledger conservation across all 169 entries.
   - Partitioned dataset into 142 eligible records and 27 excluded elementary A1/A2 records (restoring 12 approved A2 terms: `wind`, `oil`, `lake`, `salt`, `whales`, `stomach`, `seed`, `bone`, `farming`, `roots`, `flies`, `bugs`).
4. **Enrichment Stage:**
   - Implemented in [`processors/enrichment/enricher_nature.py`](file:///c:/Users/user/Desktop/vocabulary_parser/processors/enrichment/enricher_nature.py).
   - Normalized parts of speech to lowercase categories: `noun`, `adjective`, `noun (plural)`, `proper noun`, `noun (abbreviation)`.
   - Curated Russian translations: 1 translation preferred when fully sufficient; 2 translation alternatives permitted ONLY when contributing distinct, useful lexical meaning. Pruned 131 redundant descriptive paraphrases (e.g. `whales → киты`).
   - Verified non-circular English explanations (`#165 Cone` enhanced to avoid circular `cone-shaped` reference).
5. **Difficulty Classification Stage:**
   - Authoritative CEFR mapping in [`processors/difficulty/cefr_registry.py`](file:///c:/Users/user/Desktop/vocabulary_parser/processors/difficulty/cefr_registry.py):
     - `A1/A2/B1 -> Easy` (82 records)
     - `B2 -> Medium` (75 records)
     - `C1 -> Hard` (12 records)
     - `Unset: 0`
   - Final-output eligibility:
     - 142 eligible records (`final_output_eligible: true`).
     - 27 excluded records (`final_output_eligible: false`).
6. **Validation & PRE-FINAL Assembly:**
   - Implemented in [`processors/validation/validator_nature.py`](file:///c:/Users/user/Desktop/vocabulary_parser/processors/validation/validator_nature.py).
   - Assembled [`data/pre_final/sources/nature/vocabulary.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/pre_final/sources/nature/vocabulary.json) with full provenance chain (142 eligible, 27 excluded, 0 errors).
7. **HTML Backtesting:**
   - Verified via [`tools/vocabulary_review.py`](file:///c:/Users/user/Desktop/vocabulary_parser/tools/vocabulary_review.py) with `--source nature`.
