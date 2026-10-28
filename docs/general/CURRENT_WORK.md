# Current Operational State (`CURRENT_WORK.md`)

> **Last Updated:** 2026-10-28  
> **Active Milestone:** Reprocessing, Linguistic Correction, Categorized Issue Reporting & Stage-Level HTML Backtesting Tool

---

## 1. Absolute Rule for All Future Work

> [!IMPORTANT]
> **EXECUTE ONLY THE EXPLICITLY REQUESTED STAGES.**
> 
> - A request for Stage $X$ authorizes Stage $X$ **ONLY**.
> - Do not automatically proceed to Stage $X+1$.
> - After completing the authorized stage: 1) Save outputs, 2) Validate stage results, 3) Document issues, 4) Document backtesting, 5) Update `CURRENT_WORK.md`, 6) **STOP**.

---

## 2. Completed in Current Session (Reprocessing & Quality Hardening)

1. **Reprocessed RAW Extraction (`uclouvain`):**
   - Verified 413 records extracted from [`acquisition/sources/uclouvain/uclouvain_vocabulary_list.txt`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/sources/uclouvain/uclouvain_vocabulary_list.txt) (SHA-256: `e1b15633...`).
   - Categorized issues generated using structured error types (`Cross-section homograph distinction`, `Parenthetical or phrasal modifier syntax`).
2. **Reprocessed Cleaning & Normalization (`uclouvain`):**
   - Implemented generic slash-separated alternative entry splitting architecture.
   - Implemented systematic exclusion of elementary A1/A2 vocabulary with defensible CEFR linguistic evidence (29 records excluded, 384 eligible).
   - Preserved genuine multiword expressions (`account for`) and parentheticals without destructive fragmentation.
   - Verified 100% token-ledger match for all regular and split records.
3. **Reprocessed Vocabulary Enrichment (`uclouvain`):**
   - Corrected Russian translation engine: repealed obsolete 2-word cap; enforced maximum TWO alternatives with multiword support.
   - Updated linguistic data in [`processors/enrichment/lexicon_data.py`](file:///c:/Users/user/Desktop/vocabulary_parser/processors/enrichment/lexicon_data.py):
     - `different from` / `different`: `отличающийся; непохожий на` (NOT `в отличие от`).
     - `current`: `настоящий` (temporal sense, NOT fluid/electrical flow).
     - `present` (adjective): `настоящий; присутствующий` (cross-section homograph with `#167 present` verb).
     - `particular` / `specific`: distinct entries (`particular` -> `определённый; особый`; `specific` -> `определённый; конкретный`).
     - `account for`: `объяснять; являться причиной` (causal/explanatory English explanation).
     - `constitute`: `составлять часть чего-то` (single multiword alternative).
     - `confident`: `уверенный`.
     - `sure`: benchmarked as elementary A1/A2 exclusion (`уверенный; точный`).
   - Dual-written to [`data/enriched/sources/uclouvain/`](file:///c:/Users/user/Desktop/vocabulary_parser/data/enriched/sources/uclouvain) and legacy paths.
4. **Validation & PRE-FINAL Assembly:**
   - 379 validated, 5 review_pending, 29 excluded (A1/A2), 0 blocking errors.
   - Enforced `difficulty: null` placeholder across all 413 records.
   - Updated [`data/pre_final/vocabulary.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/pre_final/vocabulary.json) and validation docs.
5. **Categorized Issue Reporting Engine:**
   - Upfront `ISSUE SUMMARY — <SOURCE> / <STAGE>` block with error categories and counts.
   - Itemized reports grouped by error category with structured problem, expected/actual output, root cause, corrective action, reproduction command, and status.
   - Emitted to `qa/` and `qa/sources/uclouvain/`.
6. **Reusable Backtesting Review Tool (`tools/vocabulary_review.py`):**
   - CLI interface: `--source <source>`, `--word "<word>"`, `--open`.
   - Supports single words, multiword expressions (`different from`, `account for`), and slash queries (`particular / specific`).
   - Deterministically generates standalone HTML inspection views: `inspections/review/backtest_<source>_<slug>.html`.
7. **Passing Automated Verification Suite:**
   - 10 automated test cases passing in [`tests/test_vocabulary_pipeline.py`](file:///c:/Users/user/Desktop/vocabulary_parser/tests/test_vocabulary_pipeline.py).
   - Clean linter check with `ruff`.

---

## 3. Actual Operational Status of Pipeline Stages

| Stage | Operational State | Location | Evidence / Findings |
|---|---|---|---|
| **Acquisition (`uclouvain`)** | **Executed & Validated** | [`acquisition/sources/uclouvain/`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/sources/uclouvain) | SHA-256 locked (`e1b15633...`). |
| **Inspection (`uclouvain`)** | **Executed & Validated** | [`inspections/sources/uclouvain/profile.json`](file:///c:/Users/user/Desktop/vocabulary_parser/inspections/sources/uclouvain/profile.json) | Profiled 233 verbs + 180 adjectives = 413 items; homographs (`present`, `separate`) and parenthetical (`account (for)`) logged. |
| **RAW Extraction (`uclouvain`)** | **Executed & Validated** | [`data/raw/sources/uclouvain/entries.raw.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/raw/sources/uclouvain/entries.raw.json) | 413 records with exact character/line slice coordinates; categorized issues emitted. |
| **Cleaning (`uclouvain`)** | **Executed & Validated** | [`data/clean/sources/uclouvain/entries.clean.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/clean/sources/uclouvain/entries.clean.json) | 384 eligible, 29 elementary A1/A2 excluded; 100% token-ledger match; `"difficulty": null` set. |
| **Enrichment (`uclouvain`)** | **Executed & Validated** | [`data/enriched/sources/uclouvain/entries.enriched.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/enriched/sources/uclouvain/entries.enriched.json) | <=2 translation alternatives rule enforced; multiword alternatives supported; 379 clean, 5 review_pending, 29 excluded. |
| **Future: Difficulty Stage** | **Architecture Prepared Only (NOT IMPLEMENTED)** | [`processors/difficulty/contract.py`](file:///c:/Users/user/Desktop/vocabulary_parser/processors/difficulty/contract.py) | Contract prepared for `Easy`/`Medium`/`Hard`; `"difficulty": null` enforced across all records. |
| **Validation & PRE-FINAL** | **Executed & Validated** | [`data/pre_final/vocabulary.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/pre_final/vocabulary.json) | 379 validated, 5 review_pending, 29 excluded, 0 errors. |
| **Backtesting & Review UI** | **Implemented & Verified** | [`tools/vocabulary_review.py`](file:///c:/Users/user/Desktop/vocabulary_parser/tools/vocabulary_review.py), [`inspections/review/vocabulary_review.html`](file:///c:/Users/user/Desktop/vocabulary_parser/inspections/review/vocabulary_review.html) | PowerShell CLI tool generating stage-level HTML reports; comprehensive review interface. |

---

## 4. Next Task (Awaiting Explicit User Authorization)

1. Awaiting user instruction before executing any further processing.
2. If Difficulty Classification is authorized:
   - Implement `processors/difficulty/classifier.py` adhering strictly to contract `ALLOWED_DIFFICULTY_LABELS = ("Easy", "Medium", "Hard")`.
   - Run Difficulty stage **ONLY**, validate results, update reports, and stop.
