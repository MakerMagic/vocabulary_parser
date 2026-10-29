# VALIDATION Stage Backtesting Report (`VALIDATION_BACKTESTING.md`)

> **Source:** `math_basics`  
> **Generated deterministically from:** `data/pre_final/sources/math_basics/validation.json`  
> **Stage Status:** `completed`

## 1. Stage Execution Summary

- **What was processed:** Validation and PRE-FINAL assembly for math_basics vocabulary
- **Input artifact:** `data/difficulty/sources/math_basics/entries.difficulty.json` (SHA-256: `f4585c65d7955b3877f82e4d9843ad88f3da46987bea57810bd59198d7edc823`)
- **Output artifact:** `data/pre_final/sources/math_basics/vocabulary.json` (SHA-256: `N/A`)

| Metric | Count |
|---|---|
| **Records Entered Stage** | `274` |
| **Successfully Processed (Clean/Validated)** | `274` |
| **Excluded from Eligible Dataset (e.g. A1/A2)** | `91` |
| **Flagged for Review (`review_pending`)** | `0` |
| **Unresolved Blocking Errors (`error`)** | `0` |
| **Total Distinct Issue Occurrences** | `91` |
| **Unique Affected Records** | `91` |

## 4. Reproducible Backtesting Commands

Run the following commands from the repository root:

```powershell
.\.venv\Scripts\python.exe -c "from processors.validation.validator_math import run_validation; run_validation()"
Get-Content data/pre_final/sources/math_basics/validation.json | ConvertFrom-Json
```

## 5. Verification Procedure

1. Verify all 274 records exist in data/pre_final/sources/math_basics/vocabulary.json.
2. Verify exactly 183 validated eligible terms (zero errors, zero unresolved review notes).
3. Verify exactly 91 duplicate records marked excluded (final_output_eligible=False).
4. Verify preset='math_basics' across 100% of records.
5. Verify 0 validation errors across the dataset.
