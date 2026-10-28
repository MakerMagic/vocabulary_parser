# ACQUISITION Stage Backtesting Report (`ACQUISITION_BACKTESTING.md`)

> **Source:** `new_words`  
> **Generated deterministically from:** `data/acquisition/sources/new_words/validation.json`  
> **Stage Status:** `completed`

## 1. Stage Execution Summary

- **What was processed:** Cryptographic lock and byte-level acquisition audit of new_words.md.
- **Input artifact:** `acquisition/local/new_words.md` (SHA-256: `6aac09b4631462c239e49c6bbbbebf0a2d30ee88acddfbb16debb780ce163ec7`)
- **Output artifact:** `acquisition/sources/new_words/new_words.md` (SHA-256: `6aac09b4631462c239e49c6bbbbebf0a2d30ee88acddfbb16debb780ce163ec7`)

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
| `sha256_immutable_lock` | **PASS** | SHA-256 matches cryptographic lock 6aac09b4631462c239e49c6bbbbebf0a2d30ee88acddfbb16debb780ce163ec7 exactly. |
| `utf8_decodability` | **PASS** | File size 30161 bytes decoded successfully under UTF-8 encoding. |

## 4. Reproducible Backtesting Commands

Run the following commands from the repository root:

```powershell
Get-FileHash acquisition/sources/new_words/new_words.md -Algorithm SHA256
```

## 5. Verification Procedure

1. Verify SHA-256 matches manifest.json (6aac09b4631462c239e49c6bbbbebf0a2d30ee88acddfbb16debb780ce163ec7).
2. Verify UTF-8 decoding without errors.
