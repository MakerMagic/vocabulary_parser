# CLEAN Stage Backtesting Report (`CLEAN_BACKTESTING.md`)

> **Source:** `nature`  
> **Generated deterministically from:** `data/clean/sources/nature/validation.json`  
> **Stage Status:** `completed`

## 1. Stage Execution Summary

- **What was processed:** Cleaning, token-ledger conservation, and elementary A1/A2 exclusion audit for nature.
- **Input artifact:** `data/raw/sources/nature/entries.raw.json` (SHA-256: `d4604e0804e3987e8e008b186aa5d0318e166a5391c64f7aefec4a10205fb0dd`)
- **Output artifact:** `data/clean/sources/nature/entries.clean.json` (SHA-256: `e1a5498d9d8221cb2a7c224b22236d4405e77d2186c3fd8e9e5fdadf1ea6efb3`)

| Metric | Count |
|---|---|
| **Records Entered Stage** | `169` |
| **Successfully Processed (Clean/Validated)** | `169` |
| **Excluded from Eligible Dataset (e.g. A1/A2)** | `0` |
| **Flagged for Review (`review_pending`)** | `0` |
| **Unresolved Blocking Errors (`error`)** | `0` |
| **Total Distinct Issue Occurrences** | `0` |
| **Unique Affected Records** | `0` |

## 2. Primary-Reason Partition (Disjoint Record Counts)

| Primary State / Reason | Unique Record Count |
|---|---|
| `eligible_curriculum_records` | `142` |
| `excluded_elementary_a1_a2` | `27` |

## 3. Automated Invariant Checks

| Check Name | Status | Details |
|---|---|---|
| `token_ledger_conservation` | **PASS** | 100% token-ledger conservation verified for all 169 records. |
| `a1_a2_elementary_exclusion` | **PASS** | Systematic CEFR benchmark excluded 27 elementary A1/A2 records, preserving 142 curriculum records. |
| `preset_and_difficulty_contract` | **PASS** | Contract invariant: preset == 'nature' and difficulty == null across all clean records. |

## 4. Reproducible Backtesting Commands

Run the following commands from the repository root:

```powershell
.\.venv\Scripts\python.exe -c "from processors.normalization.cleaner_nature import run_cleaning; run_cleaning()"
Get-Content data/clean/sources/nature/validation.json | ConvertFrom-Json
```

## 5. Verification Procedure

1. Confirm 100% token-ledger match for all records.
2. Verify 39 elementary A1/A2 exclusions are recorded with defensible CEFR rationale.
3. Confirm difficulty remains null and preset is 'nature' across all records.
