# DIFFICULTY Stage Backtesting Report (`DIFFICULTY_BACKTESTING.md`)

> **Source:** `new_words`  
> **Generated deterministically from:** `data/difficulty/sources/new_words/validation.json`  
> **Stage Status:** `completed`

## 1. Stage Execution Summary

- **What was processed:** CEFR-based difficulty classification and preset assignment for new_words.
- **Input artifact:** `data/enriched/sources/new_words/entries.enriched.json` (SHA-256: `1ac35dbc00cbb1e120923501bc342bc3d793726f78d95eda96ffeeb3e249a0ee`)
- **Output artifact:** `data/difficulty/sources/new_words/entries.difficulty.json` (SHA-256: `d71bc4f913a3ea66c63eff173b01fd4940d8bce886d3db076582785a585acc8b`)

| Metric | Count |
|---|---|
| **Records Entered Stage** | `159` |
| **Successfully Processed (Clean/Validated)** | `154` |
| **Excluded from Eligible Dataset (e.g. A1/A2)** | `5` |
| **Flagged for Review (`review_pending`)** | `0` |
| **Unresolved Blocking Errors (`error`)** | `0` |
| **Total Distinct Issue Occurrences** | `0` |
| **Unique Affected Records** | `0` |

## 4. Reproducible Backtesting Commands

Run the following commands from the repository root:

```powershell
.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Impact"
.\.venv\Scripts\pytest.exe tests/test_vocabulary_pipeline.py
```

## 5. Verification Procedure

1. Verify all 159 records have preset='Basics'.
2. Verify difficulty tier counts: {'Easy': 31, 'Medium': 60, 'Hard': 68, 'Unset': 0}.
3. Verify final_output_eligible: 154 eligible, 5 blocked/excluded.
