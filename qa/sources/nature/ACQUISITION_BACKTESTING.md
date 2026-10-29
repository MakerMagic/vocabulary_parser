# ACQUISITION Stage Backtesting Report (`ACQUISITION_BACKTESTING.md`)

> **Source:** `nature`  
> **Generated deterministically from:** `data/acquisition/sources/nature/validation.json`  
> **Stage Status:** `completed`

## 1. Stage Execution Summary

- **What was processed:** Cryptographic lock and byte-level acquisition audit of Nature_Vocabulary_Simplified.csv.
- **Input artifact:** `acquisition/local/Nature_Vocabulary_Simplified.csv` (SHA-256: `215bdb89ad6910d4edeeddebf980523bd2ad55616c651cf908cbdf713d0809bc`)
- **Output artifact:** `acquisition/sources/nature/Nature_Vocabulary_Simplified.csv` (SHA-256: `215bdb89ad6910d4edeeddebf980523bd2ad55616c651cf908cbdf713d0809bc`)

| Metric | Count |
|---|---|
| **Records Entered Stage** | `1` |
| **Successfully Processed (Clean/Validated)** | `1` |
| **Excluded from Eligible Dataset (e.g. A1/A2)** | `0` |
| **Flagged for Review (`review_pending`)** | `0` |
| **Unresolved Blocking Errors (`error`)** | `0` |
| **Total Distinct Issue Occurrences** | `0` |
| **Unique Affected Records** | `0` |

## 2. Primary-Reason Partition (Disjoint Record Counts)

| Primary State / Reason | Unique Record Count |
|---|---|
| `clean_acquisition` | `1` |

## 3. Automated Invariant Checks

| Check Name | Status | Details |
|---|---|---|
| `sha256_immutable_lock` | **PASS** | SHA-256 matches cryptographic lock 215bdb89ad6910d4edeeddebf980523bd2ad55616c651cf908cbdf713d0809bc exactly. |
| `utf8_decodability` | **PASS** | File size 23138 bytes decoded successfully under UTF-8 (with BOM) encoding. |
| `line_count_integrity` | **PASS** | 170 lines / 169 data rows verified without truncation or replacement characters. |

## 4. Reproducible Backtesting Commands

Run the following commands from the repository root:

```powershell
Get-FileHash -Algorithm SHA256 acquisition/sources/nature/Nature_Vocabulary_Simplified.csv
Get-Content data/acquisition/sources/nature/validation.json | ConvertFrom-Json
```

## 5. Verification Procedure

1. Verify SHA-256 matches 215bdb89ad6910d4edeeddebf980523bd2ad55616c651cf908cbdf713d0809bc.
2. Verify 170 lines / 169 records byte-for-byte fidelity.
