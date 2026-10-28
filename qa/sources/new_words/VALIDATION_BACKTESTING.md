# VALIDATION Stage Backtesting Report (`VALIDATION_BACKTESTING.md`)

> **Source:** `new_words`  
> **Generated deterministically from:** `data/pre_final/sources/new_words/validation.json`  
> **Stage Status:** `completed`

## 1. Stage Execution Summary

- **What was processed:** End-to-end validation and PRE-FINAL assembly of 159 vocabulary records for new_words (154 validated, 2 review_pending, 3 excluded A1/A2, 0 errors).
- **Input artifact:** `data/enriched/sources/new_words/entries.enriched.json` (SHA-256: `1ac35dbc00cbb1e120923501bc342bc3d793726f78d95eda96ffeeb3e249a0ee`)
- **Output artifact:** `data/pre_final/sources/new_words/vocabulary.json` (SHA-256: `677b55269cf8c0b66015cccbf09ff195007133b0d8b8ed77e2dd343969a9bf4b`)

| Metric | Count |
|---|---|
| **Records Entered Stage** | `159` |
| **Successfully Processed (Clean/Validated)** | `154` |
| **Excluded from Eligible Dataset (e.g. A1/A2)** | `3` |
| **Flagged for Review (`review_pending`)** | `2` |
| **Unresolved Blocking Errors (`error`)** | `0` |
| **Total Distinct Issue Occurrences** | `2` |
| **Unique Affected Records** | `2` |

## 2. Primary-Reason Partition (Disjoint Record Counts)

| Primary State / Reason | Unique Record Count |
|---|---|
| `error` | `0` |
| `excluded_elementary_a1_a2` | `3` |
| `review_pending` | `2` |
| `validated` | `154` |

## 3. Automated Invariant Checks

| Check Name | Status | Details |
|---|---|---|
| `end_to_end_provenance_and_hash_chain` | **PASS** | All 159 records traced through Enriched -> CLEAN -> RAW -> Source SHA-256 and JSON pointers. |
| `russian_translation_max_two_alternatives_and_script` | **PASS** | All 159 records satisfy Russian translation <= 2 alternatives and Cyrillic script checks. |
| `non_circular_english_explanations` | **PASS** | All 159 records have clear, non-circular English explanations (>= 15 chars). |
| `difficulty_classification_valid_tiers` | **PASS** | All 159 records have valid CEFR-based difficulty tier in ('Easy', 'Medium', 'Hard'). |
| `preset_basics_assigned` | **PASS** | All 159 records have preset='Basics' assigned. |
| `final_output_eligibility_enforced` | **PASS** | Final output eligibility correctly enforced (154 eligible, 5 blocked/excluded). |
| `elementary_a1_a2_exclusion_partition` | **PASS** | Elementary A1/A2 records (3) cleanly preserved with validation_status='excluded'. |
| `type_field_validation` | **PASS** | Type field verified across dataset (Essential questions count: 0). |

## 4. Reproducible Backtesting Commands

Run the following commands from the repository root:

```powershell
.\.venv\Scripts\python.exe -m processors.validation.validator_new_words
.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Necessitates"
.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Repair"
.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Give rise to"
```

## 5. Verification Procedure

1. Inspect `data/pre_final/sources/new_words/vocabulary.json` and verify total_records == 159, validated_count == 154, review_pending_count == 2, excluded_count == 3, error_count == 0.
2. Inspect `qa/sources/new_words/VALIDATION_ISSUES.md` for categorized review records and root causes.
3. Use `tools/vocabulary_review.py` to inspect progression of individual words and edge cases for source 'new_words'.
