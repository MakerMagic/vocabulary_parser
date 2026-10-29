# CLEAN Stage Backtesting Report (`CLEAN_BACKTESTING.md`)

> **Source:** `math_basics`  
> **Generated deterministically from:** `data/clean/sources/math_basics/validation.json`  
> **Stage Status:** `completed`

## 1. Stage Execution Summary

- **What was processed:** Cleaned and deduplicated mathematical vocabulary records from math_basics
- **Input artifact:** `data/raw/sources/math_basics/entries.raw.json` (SHA-256: `23ac7ec94f8b8cba90d22b489799442f21d197a3baa6e7ddeb1b68ab7dc6b7c4`)
- **Output artifact:** `data/clean/sources/math_basics/entries.clean.json` (SHA-256: `N/A`)

| Metric | Count |
|---|---|
| **Records Entered Stage** | `274` |
| **Successfully Processed (Clean/Validated)** | `274` |
| **Excluded from Eligible Dataset (e.g. A1/A2)** | `0` |
| **Flagged for Review (`review_pending`)** | `0` |
| **Unresolved Blocking Errors (`error`)** | `0` |
| **Total Distinct Issue Occurrences** | `91` |
| **Unique Affected Records** | `91` |

## 4. Reproducible Backtesting Commands

Run the following commands from the repository root:

```powershell
.\.venv\Scripts\python.exe -c "from processors.normalization.cleaner_math import run_cleaning_and_deduplication; run_cleaning_and_deduplication()"
Get-Content data/clean/sources/math_basics/validation.json | ConvertFrom-Json
```

## 5. Verification Procedure

1. Verify all 274 records are present in data/clean/sources/math_basics/entries.clean.json.
2. Verify exactly 183 records have status='clean' and final_output_eligible=True.
3. Verify exactly 91 records have status='excluded', exclusion_reason='duplicate_term', and final_output_eligible=False.
4. Check 100% token ledger conservation across all records.
5. Check preset='math_basics' on 100% of records.
