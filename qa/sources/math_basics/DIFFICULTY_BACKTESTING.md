# DIFFICULTY Stage Backtesting Report (`DIFFICULTY_BACKTESTING.md`)

> **Source:** `math_basics`  
> **Generated deterministically from:** `data/difficulty/sources/math_basics/validation.json`  
> **Stage Status:** `completed`

## 1. Stage Execution Summary

- **What was processed:** CEFR-based difficulty classification for math_basics vocabulary
- **Input artifact:** `data/enriched/sources/math_basics/entries.enriched.json` (SHA-256: `b99b969560371dc84f2f8241f0935c97c9406f6b5fc88205957e3ca9943ece9c`)
- **Output artifact:** `data/difficulty/sources/math_basics/entries.difficulty.json` (SHA-256: `N/A`)

| Metric | Count |
|---|---|
| **Records Entered Stage** | `274` |
| **Successfully Processed (Clean/Validated)** | `274` |
| **Excluded from Eligible Dataset (e.g. A1/A2)** | `0` |
| **Flagged for Review (`review_pending`)** | `0` |
| **Unresolved Blocking Errors (`error`)** | `0` |
| **Total Distinct Issue Occurrences** | `0` |
| **Unique Affected Records** | `0` |

## 4. Reproducible Backtesting Commands

Run the following commands from the repository root:

```powershell
.\.venv\Scripts\python.exe -c "from processors.difficulty.classifier_math import run_difficulty_classification; run_difficulty_classification()"
Get-Content data/difficulty/sources/math_basics/validation.json | ConvertFrom-Json
```

## 5. Verification Procedure

1. Verify all 274 records have difficulty in ('Easy', 'Medium', 'Hard').
2. Verify CEFR mapping contract: A1/A2/B1 -> Easy, B2 -> Medium, C1/C2 -> Hard.
3. Verify preset='math_basics' on 100% of records.
