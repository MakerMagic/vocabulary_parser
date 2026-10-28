# DIFFICULTY Stage Backtesting Report (`DIFFICULTY_BACKTESTING.md`)

> **Source:** `uclouvain`  
> **Generated deterministically from:** `data/difficulty/sources/uclouvain/validation.json`  
> **Stage Status:** `completed`

## 1. Stage Execution Summary

- **What was processed:** CEFR-based difficulty classification and preset assignment for uclouvain.
- **Input artifact:** `data/enriched/sources/uclouvain/entries.enriched.json` (SHA-256: `e582975bc6c8488e20c33e0820c4df4dc1f4b081114c958305a00ed8041dc3e0`)
- **Output artifact:** `data/difficulty/sources/uclouvain/entries.difficulty.json` (SHA-256: `44d0fc02bbe6bf56080090603f6c5da844cf9362156b8b610572858155c3d46b`)

| Metric | Count |
|---|---|
| **Records Entered Stage** | `413` |
| **Successfully Processed (Clean/Validated)** | `379` |
| **Excluded from Eligible Dataset (e.g. A1/A2)** | `34` |
| **Flagged for Review (`review_pending`)** | `0` |
| **Unresolved Blocking Errors (`error`)** | `0` |
| **Total Distinct Issue Occurrences** | `0` |
| **Unique Affected Records** | `0` |

## 4. Reproducible Backtesting Commands

Run the following commands from the repository root:

```powershell
.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "accept"
.\.venv\Scripts\pytest.exe tests/test_vocabulary_pipeline.py
```

## 5. Verification Procedure

1. Verify all 413 records have preset='Basics'.
2. Verify difficulty tier counts: {'Easy': 220, 'Medium': 175, 'Hard': 18, 'Unset': 0}.
3. Verify final_output_eligible: 379 eligible, 34 blocked/excluded.
