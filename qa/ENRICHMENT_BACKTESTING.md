# ENRICHMENT Stage Backtesting Report (`ENRICHMENT_BACKTESTING.md`)

> **Source:** `uclouvain`  
> **Generated deterministically from:** `data/enriched/sources/uclouvain/validation.json`  
> **Stage Status:** `completed`

## 1. Stage Execution Summary

- **What was processed:** Vocabulary enrichment of 413 records (POS, Russian translation with <=2 alternatives [406 1-alt, 7 2-alt], multiword support, and contextual English explanations; 29 A1/A2 records tracked as excluded).
- **Input artifact:** `data/clean/sources/uclouvain/entries.clean.json` (SHA-256: `73de5d5ebeeb14fc7a93a338ec448b5b4c0fd62132a1800cc1a4f87b632365d6`)
- **Output artifact:** `data/enriched/sources/uclouvain/entries.enriched.json` (SHA-256: `e582975bc6c8488e20c33e0820c4df4dc1f4b081114c958305a00ed8041dc3e0`)

| Metric | Count |
|---|---|
| **Records Entered Stage** | `413` |
| **Successfully Processed (Clean/Validated)** | `379` |
| **Excluded from Eligible Dataset (e.g. A1/A2)** | `29` |
| **Flagged for Review (`review_pending`)** | `5` |
| **Unresolved Blocking Errors (`error`)** | `0` |
| **Total Distinct Issue Occurrences** | `5` |
| **Unique Affected Records** | `5` |

## 2. Primary-Reason Partition (Disjoint Record Counts)

| Primary State / Reason | Unique Record Count |
|---|---|
| `eligible_clean_enriched` | `379` |
| `enrichment_sense_or_morphology_review` | `5` |
| `excluded_elementary_a1_a2` | `29` |

## 3. Automated Invariant Checks

| Check Name | Status | Details |
|---|---|---|
| `russian_translation_max_two_alternatives_and_cyrillic` | **PASS** | All 413 records have Cyrillic Russian translations with 1-2 alternatives (406 1-alt, 7 2-alt; 0 >2-alt). |
| `english_explanation_completeness_and_clarity` | **PASS** | All 413 records have non-empty, contextual English explanations. |
| `section_scoped_pos_consistency` | **PASS** | All 233 verbs and 180 adjectives enriched according to their section-scoped grammatical category. |
| `difficulty_field_unset_guard` | **PASS** | Reserved field 'difficulty' remains explicitly null across all 413 enriched records. |
| `elementary_a1_a2_exclusion_preservation` | **PASS** | Elementary A1/A2 excluded records (29) cleanly preserved with enrichment_status='excluded'. |

## 4. Reproducible Backtesting Commands

Run the following commands from the repository root:

```powershell
.\.venv\Scripts\python.exe -m processors.enrichment.enricher
.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "account for"
.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "different from"
.\.venv\Scripts\python.exe -m pytest -q tests/test_vocabulary_pipeline.py -k enrichment
```

## 5. Verification Procedure

1. Inspect `data/enriched/sources/uclouvain/entries.enriched.json` and confirm all 413 records have `russian_alternatives_count <= 2`.
2. Confirm multiword alternatives (e.g. 'объяснять; являться причиной' for 'account for', 'составлять часть чего-то' for 'constitute', 'отличающийся; непохожий на' for 'different') pass validation.
3. Review the 5 `review_pending` records in `qa/ENRICHMENT_ISSUES.md`.
4. Verify that 29 elementary A1/A2 records have `status == 'excluded'`.
