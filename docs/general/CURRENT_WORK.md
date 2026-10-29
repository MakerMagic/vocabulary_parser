# Current Operational State (`CURRENT_WORK.md`)

> **Last Updated:** 2026-10-29  
> **Active Milestone:** Vocabulary Rendering for `math_basics` Executed & Validated

---

## 1. Absolute Rule for All Future Work

> [!IMPORTANT]
> **EXECUTE ONLY THE EXPLICITLY REQUESTED STAGES.**
> 
> - A request for Stage $X$ authorizes Stage $X$ **ONLY**.
> - Do not automatically proceed to Stage $X+1$.
> - After completing the authorized stage: 1) Save outputs, 2) Validate stage results, 3) Document issues, 4) Document backtesting, 5) Update `CURRENT_WORK.md`, 6) **STOP**.
> - **DO NOT INTEGRATE INTO LIVE WEBSITE CODEBASE WITHOUT AUTHORIZATION.**

---

## 2. Completed in Current Session (Vocabulary Rendering for `math_basics`)

1. **Upstream Audit & Verification:**
   - Audited all 274 records of `math_basics` in [`data/pre_final/sources/math_basics/vocabulary.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/pre_final/sources/math_basics/vocabulary.json).
   - Zero validation errors, zero unassigned fields, 100% mathematical context preserved.
2. **Admission & Exclusion Evaluation:**
   - Admitted to website card presentation: **183 unique mathematical terms** (`status: "validated"`, `final_output_eligible: true`, 0 errors, 0 review notes).
   - Blocked from website card presentation: **91 duplicate records** (`status: "excluded"`, `exclusion_reason: "duplicate_term"`). These receive the diagnostic notification banner identifying them as policy-excluded duplicate occurrences.
3. **Rendering Artifact Generation:**
   - Emitted display-ready dataset: [`data/rendered/sources/math_basics/display_ready.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/rendered/sources/math_basics/display_ready.json) (274 records: 183 admitted, 91 blocked).
   - Emitted rendering validation report: [`data/rendered/sources/math_basics/validation.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/rendered/sources/math_basics/validation.json) (100% verified, 0 errors).
   - Emitted stage QA documentation: [`qa/sources/math_basics/RENDERING_ISSUES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/qa/sources/math_basics/RENDERING_ISSUES.md) and [`qa/sources/math_basics/RENDERING_BACKTESTING.md`](file:///c:/Users/user/Desktop/vocabulary_parser/qa/sources/math_basics/RENDERING_BACKTESTING.md).
4. **Automated Verification:**
   - 20 unit and regression tests passing in [`tests/test_vocabulary_pipeline.py`](file:///c:/Users/user/Desktop/vocabulary_parser/tests/test_vocabulary_pipeline.py).
   - Linter clean (`ruff check .` 0 errors).
5. **CLI Backtesting Tested:**
   - Verified with PowerShell CLI: `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source math_basics --word "altitude"`.
   - Verified duplicate term presentation: `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source math_basics --word "decimal"`.

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
| **Acquisition (`nature`)** | **Executed & Validated** | [`acquisition/sources/nature/`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/sources/nature) | SHA-256 locked (`215bdb89...`, 170 lines, 169 words across 7 topics). |
| **Inspection (`nature`)** | **Executed & Validated** | [`inspections/sources/nature/profile.json`](file:///c:/Users/user/Desktop/vocabulary_parser/inspections/sources/nature/profile.json) | Profiled 169 items, 7 topics, paired singular/plural variants logged. |
| **RAW Extraction (`nature`)** | **Executed & Validated** | [`data/raw/sources/nature/entries.raw.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/raw/sources/nature/entries.raw.json) | 169 records with exact character and line spans; preset: nature assigned. |
| **Cleaning (`nature`)** | **Executed & Validated** | [`data/clean/sources/nature/entries.clean.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/clean/sources/nature/entries.clean.json) | 142 eligible, 27 elementary A1/A2 excluded (12 approved A2 words restored); 100% token-ledger match. |
| **Enrichment (`nature`)** | **Executed & Validated** | [`data/enriched/sources/nature/entries.enriched.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/enriched/sources/nature/entries.enriched.json) | <=2 translation alternatives rule enforced; 131 redundant second translations pruned (e.g. `whales → киты`). |
| **Difficulty (`nature`)** | **Executed & Validated** | [`data/difficulty/sources/nature/entries.difficulty.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/difficulty/sources/nature/entries.difficulty.json) | Easy: 82, Medium: 75, Hard: 12, Unset: 0; preset: nature (169/169); eligible: 142, excluded: 27. |
| **Validation & PRE-FINAL (`nature`)** | **Executed & Validated** | [`data/pre_final/sources/nature/vocabulary.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/pre_final/sources/nature/vocabulary.json) | 142 validated & website-eligible, 27 excluded, 0 errors; preset: nature locked. |
| **Acquisition (`math_basics`)** | **Executed & Validated** | [`acquisition/sources/math_basics/`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/sources/math_basics) | SHA-256 locked (`eb6ea47d...`, 274 lines, 183 unique terms). |
| **Inspection (`math_basics`)** | **Executed & Validated** | [`inspections/sources/math_basics/profile.json`](file:///c:/Users/user/Desktop/vocabulary_parser/inspections/sources/math_basics/profile.json) | Profiled 274 lines, 183 unique terms, 52 duplicated terms (91 redundant occurrences). |
| **RAW Extraction (`math_basics`)** | **Executed & Validated** | [`data/raw/sources/math_basics/entries.raw.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/raw/sources/math_basics/entries.raw.json) | 274 records with exact character and line spans; preset: math_basics assigned. |
| **Cleaning (`math_basics`)** | **Executed & Validated** | [`data/clean/sources/math_basics/entries.clean.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/clean/sources/math_basics/entries.clean.json) | 183 eligible unique, 91 duplicates excluded; 100% token ledger match. |
| **Enrichment (`math_basics`)** | **Executed & Validated** | [`data/enriched/sources/math_basics/entries.enriched.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/enriched/sources/math_basics/entries.enriched.json) | 100% mathematical context translations (<=2 alts), non-circular explanations, mathematical POS. |
| **Difficulty (`math_basics`)** | **Executed & Validated** | [`data/difficulty/sources/math_basics/entries.difficulty.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/difficulty/sources/math_basics/entries.difficulty.json) | Eligible: Easy: 110, Medium: 63, Hard: 10; Total: Easy: 184, Medium: 80, Hard: 10. |
| **Validation & PRE-FINAL (`math_basics`)** | **Executed & Validated** | [`data/pre_final/sources/math_basics/vocabulary.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/pre_final/sources/math_basics/vocabulary.json) | 183 validated & eligible, 91 duplicate excluded, 0 errors; preset: math_basics locked. |
| **Vocabulary Rendering (`math_basics`)** | **Executed & Validated** | [`data/rendered/sources/math_basics/display_ready.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/rendered/sources/math_basics/display_ready.json) | 183 admitted (website card preview), 91 blocked duplicates (diagnostic notice), 0 errors. |
| **Repository Rendering Audit** | **Executed & Validated** | [`docs/general/VOCABULARY_RENDERING.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/VOCABULARY_RENDERING.md) | 1,015 total records audited: 858 admitted, 157 blocked (150 policy exclusions, 7 review pending, 0 errors). |

---

## 4. Next Task (Awaiting Explicit User Authorization)

1. Awaiting explicit user authorization before executing any subsequent processing stage or modifying datasets.
