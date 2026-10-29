# RAW Stage Backtesting Report (`RAW_BACKTESTING.md`)

> **Source:** `math_basics`  
> **Generated deterministically from:** `data/raw/sources/math_basics/validation.json`  
> **Stage Status:** `completed`

## 1. Stage Execution Summary

- **What was processed:** RAW extraction of mathematical vocabulary from math_basics.txt
- **Input artifact:** `acquisition/sources/math_basics/math_basics.txt` (SHA-256: `N/A`)
- **Output artifact:** `data/raw/sources/math_basics/entries.raw.json` (SHA-256: `N/A`)

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
.\.venv\Scripts\python.exe -c "from parsers.math_basics.parser import run_raw_extraction; run_raw_extraction()"
Get-Content data/raw/sources/math_basics/validation.json | ConvertFrom-Json
```

## 5. Verification Procedure

1. Verify all 274 records are present in data/raw/sources/math_basics/entries.raw.json.
2. Verify exact slice coordinate matching against source text.
3. Check validation summary: entered_count == 274, succeeded_count == 274, error_count == 0.
