# Current Operational State (`CURRENT_WORK.md`)

> **Last Updated:** 2026-10-28  
> **Active Milestone:** CEFR-Based Difficulty Classification & Vocabulary Presets Implementation

---

## 1. Absolute Rule for All Future Work

> [!IMPORTANT]
> **EXECUTE ONLY THE EXPLICITLY REQUESTED STAGES.**
> 
> - A request for Stage $X$ authorizes Stage $X$ **ONLY**.
> - Do not automatically proceed to Stage $X+1$.
> - After completing the authorized stage: 1) Save outputs, 2) Validate stage results, 3) Document issues, 4) Document backtesting, 5) Update `CURRENT_WORK.md`, 6) **STOP**.

---

## 2. Completed in Current Session (Presets & CEFR Difficulty Implementation)

1. **Preset Architecture & Assignment:**
   - Added `preset` field to canonical data schema ([`docs/general/DATA_SCHEMA.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/DATA_SCHEMA.md)) with default `null` for future records.
   - Explicitly assigned `preset: "Basics"` across all 572 existing records (413 `uclouvain`, 159 `new_words`).
2. **Authoritative CEFR Level Mapping & Difficulty Tiers:**
   - Implemented [`processors/difficulty/cefr_registry.py`](file:///c:/Users/user/Desktop/vocabulary_parser/processors/difficulty/cefr_registry.py) mapping all 572 records against CEFR EVP / Oxford benchmarks (0 missing terms).
   - Implemented [`processors/difficulty/classifier.py`](file:///c:/Users/user/Desktop/vocabulary_parser/processors/difficulty/classifier.py) adhering to strict contract `A1/A2/B1 -> Easy`, `B2 -> Medium`, `C1/C2 -> Hard`.
   - Classification distribution:
     - `uclouvain` (413 records): Easy = 220, Medium = 175, Hard = 18, Unset = 0.
     - `new_words` (159 records): Easy = 31, Medium = 60, Hard = 68, Unset = 0.
     - Combined (572 records): Easy = 251, Medium = 235, Hard = 86, Unset = 0.
3. **Preserved A1/A2 Exclusions & Blocked Records Guard:**
   - Preserved all 32 elementary A1/A2 exclusions (29 in `uclouvain`, 3 in `new_words`) without reincluding them.
   - Enforced website eligibility rule: records with `review_pending`, `excluded`, or `error` have `final_output_eligible = false`.
   - Results: **533 records eligible for final output**; **39 records blocked / excluded** (32 A1/A2 exclusions + 7 review_pending: 5 UCL + 2 NW).
4. **Validation & PRE-FINAL Assembly:**
   - Updated validators ([`processors/validation/validator.py`](file:///c:/Users/user/Desktop/vocabulary_parser/processors/validation/validator.py), [`processors/validation/validator_new_words.py`](file:///c:/Users/user/Desktop/vocabulary_parser/processors/validation/validator_new_words.py)) to assert difficulty contract, preset presence, and provenance integrity.
   - Reassembled `data/pre_final/` datasets.
5. **Backtesting & HTML Review UI:**
   - Updated [`tools/vocabulary_review.py`](file:///c:/Users/user/Desktop/vocabulary_parser/tools/vocabulary_review.py) CLI summary and HTML generator to visibly display Preset, CEFR Level, Difficulty Tier, and Final Output Eligibility badge.
   - Updated [`inspections/review/vocabulary_review.html`](file:///c:/Users/user/Desktop/vocabulary_parser/inspections/review/vocabulary_review.html) review UI.
6. **Automated Verification:**
   - 12 automated test cases passing in [`tests/test_vocabulary_pipeline.py`](file:///c:/Users/user/Desktop/vocabulary_parser/tests/test_vocabulary_pipeline.py).
   - Clean linter check with `ruff`.

---

## 3. Actual Operational Status of Pipeline Stages

| Stage | Operational State | Location | Evidence / Findings |
|---|---|---|---|
| **Acquisition (`uclouvain`)** | **Executed & Validated** | [`acquisition/sources/uclouvain/`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/sources/uclouvain) | SHA-256 locked (`e1b15633...`). |
| **Inspection (`uclouvain`)** | **Executed & Validated** | [`inspections/sources/uclouvain/profile.json`](file:///c:/Users/user/Desktop/vocabulary_parser/inspections/sources/uclouvain/profile.json) | Profiled 233 verbs + 180 adjectives = 413 items. |
| **RAW Extraction (`uclouvain`)** | **Executed & Validated** | [`data/raw/sources/uclouvain/entries.raw.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/raw/sources/uclouvain/entries.raw.json) | 413 records with exact character/line slice coordinates. |
| **Cleaning (`uclouvain`)** | **Executed & Validated** | [`data/clean/sources/uclouvain/entries.clean.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/clean/sources/uclouvain/entries.clean.json) | 384 eligible, 29 elementary A1/A2 excluded; 100% token-ledger match. |
| **Enrichment (`uclouvain`)** | **Executed & Validated** | [`data/enriched/sources/uclouvain/entries.enriched.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/enriched/sources/uclouvain/entries.enriched.json) | <=2 translation alternatives rule enforced; multiword alternatives supported. |
| **Difficulty (`uclouvain`)** | **Executed & Validated** | [`data/difficulty/sources/uclouvain/entries.difficulty.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/difficulty/sources/uclouvain/entries.difficulty.json) | Easy: 220, Medium: 175, Hard: 18, Unset: 0; preset: Basics (413/413); eligible: 379, blocked/excluded: 34. |
| **Validation & PRE-FINAL (`uclouvain`)** | **Executed & Validated** | [`data/pre_final/vocabulary.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/pre_final/vocabulary.json) | 379 validated & website-eligible, 5 review_pending (blocked), 29 excluded, 0 errors. |
| **Acquisition (`new_words`)** | **Executed & Validated** | [`acquisition/sources/new_words/`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/sources/new_words) | SHA-256 locked (`6aac09b4...`, 159 words in 56 clusters). |
| **Inspection (`new_words`)** | **Executed & Validated** | [`inspections/sources/new_words/profile.json`](file:///c:/Users/user/Desktop/vocabulary_parser/inspections/sources/new_words/profile.json) | Profiled 56 clusters, 159 lexical items. |
| **RAW Extraction (`new_words`)** | **Executed & Validated** | [`data/raw/sources/new_words/entries.raw.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/raw/sources/new_words/entries.raw.json) | 159 records with exact character and line spans. |
| **Cleaning (`new_words`)** | **Executed & Validated** | [`data/clean/sources/new_words/entries.clean.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/clean/sources/new_words/entries.clean.json) | 156 eligible, 3 elementary A2 excluded (`Repair`, `Several`, `Nearly`); 100% token ledger match. |
| **Enrichment (`new_words`)** | **Executed & Validated** | [`data/enriched/sources/new_words/entries.enriched.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/enriched/sources/new_words/entries.enriched.json) | <=2 translation alternatives rule enforced; multiword alternatives supported. |
| **Difficulty (`new_words`)** | **Executed & Validated** | [`data/difficulty/sources/new_words/entries.difficulty.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/difficulty/sources/new_words/entries.difficulty.json) | Easy: 31, Medium: 60, Hard: 68, Unset: 0; preset: Basics (159/159); eligible: 154, blocked/excluded: 5. |
| **Validation & PRE-FINAL (`new_words`)** | **Executed & Validated** | [`data/pre_final/sources/new_words/vocabulary.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/pre_final/sources/new_words/vocabulary.json) | 154 validated & website-eligible, 2 review_pending (blocked), 3 excluded, 0 errors. |
| **Backtesting & Review UI** | **Implemented & Verified** | [`tools/vocabulary_review.py`](file:///c:/Users/user/Desktop/vocabulary_parser/tools/vocabulary_review.py), [`inspections/review/vocabulary_review.html`](file:///c:/Users/user/Desktop/vocabulary_parser/inspections/review/vocabulary_review.html) | Multi-source backtesting CLI and visual review UI displaying Preset, CEFR, Difficulty, and Final Output Eligibility. |

---

## 4. Next Task (Awaiting Explicit User Authorization)

1. Awaiting explicit user authorization before executing any subsequent processing stage or modifying datasets.
