# Current Operational State (`CURRENT_WORK.md`)

> **Last Updated:** 2026-10-29  
> **Active Milestone:** Vocabulary Rendering Stage Implementation & Multi-Source Audit

---

## 1. Absolute Rule for All Future Work

> [!IMPORTANT]
> **EXECUTE ONLY THE EXPLICITLY REQUESTED STAGES.**
> 
> - A request for Stage $X$ authorizes Stage $X$ **ONLY**.
> - Do not automatically proceed to Stage $X+1$.
> - After completing the authorized stage: 1) Save outputs, 2) Validate stage results, 3) Document issues, 4) Document backtesting, 5) Update `CURRENT_WORK.md`, 6) **STOP**.

---

## 2. Completed in Current Session (Vocabulary Rendering Stage Implementation)

1. **Read-Only Multi-Source Audit:**
   - Performed systematic read-only audit across all 741 records in the repository (`uclouvain`: 413, `new_words`: 159, `nature`: 169) without re-running earlier stages.
   - Verified that all earlier stages (Acquisition, Inspection, RAW, Cleaning, Enrichment, Difficulty, Validation) were verifiably complete with `error_count: 0`.
2. **Dedicated Rendering Package (`processors/rendering/`):**
   - Implemented [`processors/rendering/contract.py`](file:///c:/Users/user/Desktop/vocabulary_parser/processors/rendering/contract.py) defining strict ZERO UNRESOLVED ISSUES admission gate.
   - Implemented [`processors/rendering/template.py`](file:///c:/Users/user/Desktop/vocabulary_parser/processors/rendering/template.py) providing ONE reusable HTML template with Area A (website card reproduction: 640px card, 24px border radius, bold headword, italic POS, bookmark SVG, large bold Cyrillic headline, English explanation) and Area B (technical QA metadata and upstream audit panes).
   - Implemented [`processors/rendering/renderer.py`](file:///c:/Users/user/Desktop/vocabulary_parser/processors/rendering/renderer.py) providing single-record and batch audit functions.
3. **Strict Zero-Unresolved-Issues Gate Results:**
   - Total repo records: **741**
   - Admitted (eligible for website rendering): **675 records**
   - Blocked (ineligible): **66 records total**
     - 59 policy exclusions (elementary A1/A2: UCL 29, NW 3, Nature 27).
     - 7 pending review (UCL 5: `#2 account (for)`, `#206 should`, `#252 certain`, `#347 present`, `#402 unlike`; NW 2: `#27 Necessitates`, `#126 Opulent`).
     - 0 active errors.
4. **PowerShell Backtesting CLI Integration:**
   - Updated [`tools/vocabulary_review.py`](file:///c:/Users/user/Desktop/vocabulary_parser/tools/vocabulary_review.py) to render Area A website preview (or diagnostic blocked card) and Area B metadata for any inspected word.
5. **Documentation & Test Verification:**
   - Created [`docs/general/VOCABULARY_RENDERING.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/VOCABULARY_RENDERING.md).
   - Added automated tests in [`tests/test_vocabulary_pipeline.py`](file:///c:/Users/user/Desktop/vocabulary_parser/tests/test_vocabulary_pipeline.py); all 17 tests passing.
   - Clean lint status (`ruff check .` 0 errors).

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
| **Vocabulary Rendering (All Sources)** | **Executed & Validated** | [`processors/rendering/`](file:///c:/Users/user/Desktop/vocabulary_parser/processors/rendering), [`docs/general/VOCABULARY_RENDERING.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/VOCABULARY_RENDERING.md) | Zero unresolved issues gate: 675 admitted, 66 blocked (59 excluded, 7 review pending, 0 errors). One reusable template with Area A (card) and Area B (QA metadata). |
| **Backtesting & Review UI** | **Implemented & Verified** | [`tools/vocabulary_review.py`](file:///c:/Users/user/Desktop/vocabulary_parser/tools/vocabulary_review.py) | CLI review rendering website flashcard (Area A) for eligible records and diagnostic blocked notices for ineligible records. |

---

## 4. Next Task (Awaiting Explicit User Authorization)

1. Awaiting explicit user authorization before executing any subsequent processing stage or modifying datasets.
