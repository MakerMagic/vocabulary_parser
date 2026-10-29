# VALIDATION Stage Backtesting Report (`VALIDATION_BACKTESTING.md`)

> **Source:** `nature`  
> **Generated deterministically from:** `data/pre_final/sources/nature/validation.json`  
> **Stage Status:** `completed`

## 1. Stage Execution Summary

- **What was processed:** Validation and PRE-FINAL assembly audit for nature.
- **Input artifact:** `data/enriched/sources/nature/entries.enriched.json` (SHA-256: `b069cef7a6064135e29a63be9eac2753c70764220967e4fec588ca6152c5701e`)
- **Output artifact:** `data/pre_final/sources/nature/vocabulary.json` (SHA-256: `5249b1fe7a43d195874be48491e293769f0f689592df969a0e1cd31415aa5b88`)

| Metric | Count |
|---|---|
| **Records Entered Stage** | `169` |
| **Successfully Processed (Clean/Validated)** | `142` |
| **Excluded from Eligible Dataset (e.g. A1/A2)** | `27` |
| **Flagged for Review (`review_pending`)** | `0` |
| **Unresolved Blocking Errors (`error`)** | `0` |
| **Total Distinct Issue Occurrences** | `0` |
| **Unique Affected Records** | `0` |

## 2. Primary-Reason Partition (Disjoint Record Counts)

| Primary State / Reason | Unique Record Count |
|---|---|
| `eligible_for_final_output` | `142` |
| `excluded_elementary_a1_a2` | `27` |

## 3. Automated Invariant Checks

| Check Name | Status | Details |
|---|---|---|
| `byte_level_source_slice_reconstruction` | **PASS** | All 169 records reconstructed byte-for-byte from raw source slices. |
| `zero_blocking_validation_errors` | **PASS** | Full dataset validated: 142 eligible, 27 excluded, 0 errors. |
| `preset_and_difficulty_contract` | **PASS** | Contract invariant: 100% records carry preset: 'nature' and defensible difficulty (Easy/Medium/Hard). |

## 4. Reproducible Backtesting Commands

Run the following commands from the repository root:

```powershell
.\.venv\Scripts\python.exe -c "from processors.validation.validator_nature import run_validation; run_validation()"
Get-Content data/pre_final/sources/nature/validation.json | ConvertFrom-Json
```

## 5. Verification Procedure

1. Confirm data/pre_final/sources/nature/vocabulary.json contains 169 records.
2. Verify exactly 130 records have final_output_eligible == True and 39 have final_output_eligible == False.
3. Verify error_count == 0.
