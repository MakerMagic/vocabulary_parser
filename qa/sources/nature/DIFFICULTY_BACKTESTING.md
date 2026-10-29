# DIFFICULTY Stage Backtesting Report (`DIFFICULTY_BACKTESTING.md`)

> **Source:** `nature`  
> **Generated deterministically from:** `data/difficulty/sources/nature/validation.json`  
> **Stage Status:** `completed`

## 1. Stage Execution Summary

- **What was processed:** CEFR-based difficulty classification and preset assignment for nature.
- **Input artifact:** `data/enriched/sources/nature/entries.enriched.json` (SHA-256: `b069cef7a6064135e29a63be9eac2753c70764220967e4fec588ca6152c5701e`)
- **Output artifact:** `data/difficulty/sources/nature/entries.difficulty.json` (SHA-256: `3778b32c76738fbd1e7f71ca443197aa67dffe6c4713c0c48e5b8fa47914f7c8`)

| Metric | Count |
|---|---|
| **Records Entered Stage** | `169` |
| **Successfully Processed (Clean/Validated)** | `142` |
| **Excluded from Eligible Dataset (e.g. A1/A2)** | `27` |
| **Flagged for Review (`review_pending`)** | `0` |
| **Unresolved Blocking Errors (`error`)** | `0` |
| **Total Distinct Issue Occurrences** | `0` |
| **Unique Affected Records** | `0` |

## 4. Reproducible Backtesting Commands

Run the following commands from the repository root:

```powershell
.\.venv\Scripts\python.exe tools/vocabulary_review.py --source nature --word "Energy"
.\.venv\Scripts\pytest.exe tests/test_vocabulary_pipeline.py
```

## 5. Verification Procedure

1. Verify all 169 records have preset='nature'.
2. Verify difficulty tier counts: {'Easy': 82, 'Medium': 75, 'Hard': 12, 'Unset': 0}.
3. Verify final_output_eligible: 142 eligible, 27 blocked/excluded.
