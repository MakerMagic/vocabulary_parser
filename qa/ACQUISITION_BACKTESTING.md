# ACQUISITION Stage Backtesting Report (`ACQUISITION_BACKTESTING.md`)

> **Generated deterministically from:** `data/acquisition/validation.json`
> **Stage Status:** `completed`

## 1. Stage Execution Summary

- **What was processed:** Acquisition and SHA-256 provenance registration of supplied justprepy vocabulary list.
- **Input artifact:** `acquisition/local/justprepy_vocabulary_list.txt` (SHA-256: `e1b15633f274f58f093a3e1950dd1f368aad83fd54fb67ca9f682344d5628d7e`)
- **Output artifact:** `acquisition/manifest.json` (SHA-256: `0cfb02fa0dacd998611ee47dcfa7f6ee76daf20b619db3c3d246325c71ee612a`)

| Metric | Count |
|---|---|
| **Records Entered Stage** | `1` |
| **Successfully Processed (Clean/Validated)** | `1` |
| **Flagged for Review (`review_pending`)** | `0` |
| **Unresolved Blocking Errors (`error`)** | `0` |
| **Total Affected Records with Findings** | `0` |
| **Total Structured Findings Logged** | `0` |

## 2. Primary-Reason Partition (Disjoint Record Counts)

| Primary State / Reason | Unique Record Count |
|---|---|
| `registered_clean` | `1` |

## 3. Automated Invariant Checks

| Check Name | Status | Details |
|---|---|---|
| `source_file_exists_and_nonempty` | **PASS** | Source file present at acquisition/local/justprepy_vocabulary_list.txt (3823 bytes). |
| `utf8_encoding_integrity` | **PASS** | UTF-8 decoding verified without replacement characters (4 non-empty lines). |
| `sha256_provenance_recorded` | **PASS** | SHA-256 lock recorded in acquisition/manifest.json: e1b15633f274f58f... |

## 4. Reproducible Backtesting Commands

Run the following commands from the repository root (`c:\Users\user\Desktop\vocabulary_parser`):

```powershell
.\.venv\Scripts\python.exe -m processors.acquisition
.\.venv\Scripts\python.exe -m pytest -q tests/test_vocabulary_pipeline.py -k acquisition
```

## 5. Verification Procedure

1. Confirm `acquisition/local/justprepy_vocabulary_list.txt` exists and matches the SHA-256 recorded in `acquisition/manifest.json`.
2. Inspect `data/acquisition/validation.json` and verify `error_count == 0`.
3. Run the acquisition pytest check to confirm byte-for-byte source preservation.
