# VALIDATION Stage Backtesting Report (`VALIDATION_BACKTESTING.md`)

> **Source:** `uclouvain`  
> **Generated deterministically from:** `data/pre_final/validation.json`  
> **Stage Status:** `completed`

## 1. Stage Execution Summary

- **What was processed:** End-to-end validation and PRE-FINAL assembly of 413 vocabulary records (379 validated, 5 review_pending, 29 excluded A1/A2, 0 errors).
- **Input artifact:** `data/enriched/sources/uclouvain/entries.enriched.json` (SHA-256: `e582975bc6c8488e20c33e0820c4df4dc1f4b081114c958305a00ed8041dc3e0`)
- **Output artifact:** `data/pre_final/vocabulary.json` (SHA-256: `02baee4d7f8e511f0e18817fd6b41087345459cc6be1a1aa76b3553c324a97c7`)

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
| `error` | `0` |
| `excluded_elementary_a1_a2` | `29` |
| `review_pending` | `5` |
| `validated` | `379` |

## 3. Automated Invariant Checks

| Check Name | Status | Details |
|---|---|---|
| `end_to_end_provenance_and_hash_chain` | **PASS** | All 413 records traced through Enriched -> CLEAN -> RAW -> Source SHA-256 and JSON pointers. |
| `russian_translation_max_two_alternatives_and_script` | **PASS** | All 413 records satisfy Russian translation <= 2 alternatives and Cyrillic script checks. |
| `non_circular_english_explanations` | **PASS** | All 413 records have clear, non-circular English explanations (>= 15 chars, headword lemma excluded). |
| `difficulty_architecture_unset_invariant` | **PASS** | All 413 records have 'difficulty: null' (Difficulty Classification stage not executed). |
| `elementary_a1_a2_exclusion_partition` | **PASS** | Elementary A1/A2 records (29) cleanly preserved with validation_status='excluded'. |

## 4. Reproducible Backtesting Commands

Run the following commands from the repository root:

```powershell
.\.venv\Scripts\python.exe -m processors.validation.validator
.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "account for"
.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "different from"
.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "sure"
.\.venv\Scripts\python.exe -m pytest -q tests/test_vocabulary_pipeline.py
```

## 5. Verification Procedure

1. Inspect `data/pre_final/vocabulary.json` and verify `summary.total_records == 413`, `validated_count == 379`, `review_pending_count == 5`, `excluded_count == 29`, `error_count == 0`.
2. Inspect `qa/VALIDATION_ISSUES.md` and `qa/ISSUE_LOG.md` for categorized review records and root causes.
3. Use `tools/vocabulary_review.py` to inspect progression of individual words and edge cases.
