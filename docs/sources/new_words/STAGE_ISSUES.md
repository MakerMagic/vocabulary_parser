# new_words Stage Issues & Backtesting Registry (`STAGE_ISSUES.md`)

> **Source Identifier:** `new_words`  
> **Source Document:** [`acquisition/sources/new_words/new_words.md`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/sources/new_words/new_words.md)  
> **SHA-256 Lock:** `6aac09b4631462c239e49c6bbbbebf0a2d30ee88acddfbb16debb780ce163ec7`  
> **Authority:** Tracks source-specific issues across `new_words` pipeline stages.

---

## 1. Stage Findings Summary for `new_words`

| Stage | Input Records | Validated | Review Pending | Excluded (A1/A2) | Blocking Errors | Core Findings |
|---|---|---|---|---|---|---|
| **Acquisition** | `1` file | `1` | `0` | `0` | `0` | SHA-256 locked (`6aac09b4...`); UTF-8 verified (30,161 bytes). |
| **Inspection** | `159` | `159` | `0` | `0` | `0` | 56 semantic clusters, 159 lexical items; 2 cross-cluster duplicates (`negligible`, `augment`); 0 general questions present at end of file. |
| **RAW Extraction** | `159` | `159` | `0` | `0` | `0` | 100% exact character/line span reconstruction; multiword expressions tagged; 0 questions audited. |
| **Cleaning** | `159` | `156` | `0` | `3` | `0` | 100% token-ledger match; 3 elementary A2 items systematically excluded per CEFR benchmark (`Repair`, `Nearly`, `Several`); `"difficulty": null` set. |
| **Enrichment** | `159` | `154` | `2` | `3` | `0` | <=2 translation alternatives rule strictly verified; multiword translations supported; 2 items flagged for linguistic review (`Necessitates`, `Opulent`). |
| **Validation / PRE-FINAL** | `159` | `154` | `2` | `3` | `0` | End-to-end provenance verified; 0 blocking errors; `Type` field schema-validated. |

---

## 2. Active Review Pending Items (`new_words`)

### [NEW_WORDS-001] Record `#27` (`new_words_vocab_027`) — `Necessitates`
- **Stage:** ENRICHMENT / VALIDATION
- **Observation:** Ingested as third-person singular inflected form `necessitates` under Cluster 10 (`Need: Require, Necessitates`). The base lemma is `necessitate`.
- **Handling:** Preserved exact source representation `Necessitates`; mapped POS to `verb`; contextual translation `делать необходимым; требовать` and explanation provided. Flagged `review_pending` for curriculum decision whether to lemmatize to `necessitate`.
- **Verification Command:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Necessitates"`

### [NEW_WORDS-002] Record `#126` (`new_words_vocab_126`) — `Opulent`
- **Stage:** ENRICHMENT / VALIDATION
- **Observation:** Denotes extreme wealth and luxury (`богатый, роскошный`), but appears in Cluster 46 (`Unwealthy: Impoverished, Destitute, Opulent`) as an antonymous/contrasting term in the source document.
- **Handling:** Preserved exact definition and translation; flagged `review_pending` to record the contrastive placement relative to cluster title.
- **Verification Command:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Opulent"`

---

## 3. Systematic A1/A2 Exclusions (`new_words`)

| Record | Word | Declared POS | Cluster | CEFR Level | Evidence / Reason |
|---|---|---|---|---|---|
| `#33` | `Repair` | Verb | 13 (`Fix`) | **A2** | Elementary maintenance verb (Cambridge EVP A2: to restore something damaged or broken to good condition) |
| `#42` | `Several` | Determiner | 17 (`Some`) | **A2** | Elementary quantifier/determiner (Cambridge EVP A2: more than two but not many) |
| `#47` | `Nearly` | Adverb | 19 (`Almost`) | **A2** | Elementary degree adverb (Cambridge EVP A2: almost, but not completely) |

---

## 4. `Type: Essential` Audit

- **Audit Result:** `0` questions present in `new_words.md`.
- **Architecture:** The `type` field is fully implemented and validated across all pipeline stages (`data/clean/`, `data/enriched/`, `data/pre_final/`, and `tools/vocabulary_review.py`).
- **Rule Verification:** Any entry matching question syntax or designated in a question cluster receives `Type: Essential` and is exempt from elementary A1/A2 exclusion.
