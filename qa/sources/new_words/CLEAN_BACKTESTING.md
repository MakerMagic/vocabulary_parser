# CLEAN Stage Backtesting Report (`CLEAN_BACKTESTING.md`)

> **Source:** `new_words`  
> **Generated deterministically from:** `data/clean/sources/new_words/validation.json`  
> **Stage Status:** `completed`

## 1. Stage Execution Summary

- **What was processed:** CLEAN normalization of 159 records (156 eligible, 3 excluded A1/A2) with token-ledger verification.
- **Input artifact:** `data/raw/sources/new_words/entries.raw.json` (SHA-256: `4fb56c9b4a453adae704296482f1c2f57f477e7aa0b6d3f2e0b70f380831c9ee`)
- **Output artifact:** `data/clean/sources/new_words/entries.clean.json` (SHA-256: `f0c131505ce6d5c31f2368aeef0b7f9ed4c2c031cd088534e352443aad1c73e8`)

| Metric | Count |
|---|---|
| **Records Entered Stage** | `159` |
| **Successfully Processed (Clean/Validated)** | `156` |
| **Excluded from Eligible Dataset (e.g. A1/A2)** | `3` |
| **Flagged for Review (`review_pending`)** | `0` |
| **Unresolved Blocking Errors (`error`)** | `0` |
| **Total Distinct Issue Occurrences** | `7` |
| **Unique Affected Records** | `7` |

## 2. Primary-Reason Partition (Disjoint Record Counts)

| Primary State / Reason | Unique Record Count |
|---|---|
| `clean_eligible` | `156` |
| `excluded_elementary_a1_a2` | `3` |

## 3. Automated Invariant Checks

| Check Name | Status | Details |
|---|---|---|
| `token_ledger_conservation` | **PASS** | 100% of 159 records strictly preserve non-whitespace raw tokens. |
| `elementary_a1_a2_exclusion_gate` | **PASS** | 3 elementary A1/A2 entries reliably identified and marked as excluded. |
| `difficulty_field_unset_guard` | **PASS** | Reserved field 'difficulty' remains explicitly null across all records. |
| `type_field_integrity` | **PASS** | Type field cleanly preserved and uncorrupted. |

## 4. Reproducible Backtesting Commands

Run the following commands from the repository root:

```powershell
.\.venv\Scripts\python.exe -m processors.normalization.cleaner_new_words
.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Repair"
.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Nearly"
.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Several"
```

## 5. Verification Procedure

1. Inspect `data/clean/sources/new_words/entries.clean.json` and confirm 156 eligible clean records and 3 excluded records.
2. Verify that elementary words (`Repair`, `Nearly`, `Several`) have `status == 'excluded'`.
3. Verify that token-ledger conservation is True across 100% of records.
4. Inspect `qa/sources/new_words/CLEAN_ISSUES.md` for categorized findings.
