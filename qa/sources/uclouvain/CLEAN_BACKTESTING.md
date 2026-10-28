# CLEAN Stage Backtesting Report (`CLEAN_BACKTESTING.md`)

> **Source:** `uclouvain`  
> **Generated deterministically from:** `data/clean/sources/uclouvain/validation.json`  
> **Stage Status:** `completed`

## 1. Stage Execution Summary

- **What was processed:** CLEAN normalization of 413 records (384 eligible, 29 excluded A1/A2) with slash-splitting and token-ledger verification.
- **Input artifact:** `data/raw/sources/uclouvain/entries.raw.json` (SHA-256: `a6c041bcd5b7118f0cb99f209982b36b28a13037d0395866dc174347cf53f325`)
- **Output artifact:** `data/clean/sources/uclouvain/entries.clean.json` (SHA-256: `73de5d5ebeeb14fc7a93a338ec448b5b4c0fd62132a1800cc1a4f87b632365d6`)

| Metric | Count |
|---|---|
| **Records Entered Stage** | `413` |
| **Successfully Processed (Clean/Validated)** | `384` |
| **Excluded from Eligible Dataset (e.g. A1/A2)** | `29` |
| **Flagged for Review (`review_pending`)** | `0` |
| **Unresolved Blocking Errors (`error`)** | `0` |
| **Total Distinct Issue Occurrences** | `36` |
| **Unique Affected Records** | `36` |

## 2. Primary-Reason Partition (Disjoint Record Counts)

| Primary State / Reason | Unique Record Count |
|---|---|
| `eligible_clean_vocabulary` | `384` |
| `excluded_elementary_a1_a2` | `29` |

## 3. Automated Invariant Checks

| Check Name | Status | Details |
|---|---|---|
| `non_whitespace_token_ledger_equality` | **PASS** | All non-whitespace token ledgers verified (0 lost or mutated tokens). |
| `elementary_a1_a2_exclusion_gate` | **PASS** | 29 elementary A1/A2 entries reliably identified and marked as excluded. |
| `raw_snapshot_and_json_pointer_lock` | **PASS** | All cleaned records embed an immutable raw_record snapshot and RFC 6901 pointer. |
| `difficulty_field_unset_guard` | **PASS** | Reserved field 'difficulty' is strictly null across all records. |

## 4. Reproducible Backtesting Commands

Run the following commands from the repository root:

```powershell
.\.venv\Scripts\python.exe -m processors.normalization.cleaner
.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "sure"
.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "particular"
```

## 5. Verification Procedure

1. Inspect `data/clean/sources/uclouvain/entries.clean.json` and confirm `summary.excluded_count == 29`.
2. Verify that elementary words like `sure`, `be`, `can`, `use` have `status == 'excluded'`.
3. Check `qa/CLEAN_ISSUES.md` to confirm all findings are grouped by error category.
