# RAW Stage Backtesting Report (`RAW_BACKTESTING.md`)

> **Source:** `nature`  
> **Generated deterministically from:** `data/raw/sources/nature/validation.json`  
> **Stage Status:** `completed`

## 1. Stage Execution Summary

- **What was processed:** RAW extraction and span coordinate verification for Nature_Vocabulary_Simplified.csv.
- **Input artifact:** `acquisition/sources/nature/Nature_Vocabulary_Simplified.csv` (SHA-256: `215bdb89ad6910d4edeeddebf980523bd2ad55616c651cf908cbdf713d0809bc`)
- **Output artifact:** `data/raw/sources/nature/entries.raw.json` (SHA-256: `d4604e0804e3987e8e008b186aa5d0318e166a5391c64f7aefec4a10205fb0dd`)

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
| `clean_extraction` | `169` |

## 3. Automated Invariant Checks

| Check Name | Status | Details |
|---|---|---|
| `full_record_extraction` | **PASS** | All 169 rows faithfully extracted with 0 omissions. |
| `source_span_integrity` | **PASS** | Every record has exact line_number, file_char_start, and file_char_end indexing. |
| `preset_and_difficulty_contract` | **PASS** | All records carry preset: 'nature' and difficulty: null. |

## 4. Reproducible Backtesting Commands

Run the following commands from the repository root:

```powershell
.\.venv\Scripts\python.exe -c "from parsers.nature.parser import run_raw_extraction; run_raw_extraction()"
Get-Content data/raw/sources/nature/validation.json | ConvertFrom-Json
```

## 5. Verification Procedure

1. Verify all 169 records are present in data/raw/sources/nature/entries.raw.json.
2. Verify exact slice coordinate matching against source text.
3. Check validation summary: entered_count == 169, succeeded_count == 169, error_count == 0.
