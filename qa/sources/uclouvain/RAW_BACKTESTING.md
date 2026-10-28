# RAW Stage Backtesting Report (`RAW_BACKTESTING.md`)

> **Source:** `uclouvain`  
> **Generated deterministically from:** `data/raw/sources/uclouvain/validation.json`  
> **Stage Status:** `completed`

## 1. Stage Execution Summary

- **What was processed:** RAW extraction of 413 vocabulary items with exact character/line slice spans for uclouvain.
- **Input artifact:** `acquisition/sources/uclouvain/uclouvain_vocabulary_list.txt` (SHA-256: `e1b15633f274f58f093a3e1950dd1f368aad83fd54fb67ca9f682344d5628d7e`)
- **Output artifact:** `data/raw/sources/uclouvain/entries.raw.json` (SHA-256: `a6c041bcd5b7118f0cb99f209982b36b28a13037d0395866dc174347cf53f325`)

| Metric | Count |
|---|---|
| **Records Entered Stage** | `413` |
| **Successfully Processed (Clean/Validated)** | `413` |
| **Excluded from Eligible Dataset (e.g. A1/A2)** | `0` |
| **Flagged for Review (`review_pending`)** | `5` |
| **Unresolved Blocking Errors (`error`)** | `0` |
| **Total Distinct Issue Occurrences** | `5` |
| **Unique Affected Records** | `5` |

## 2. Primary-Reason Partition (Disjoint Record Counts)

| Primary State / Reason | Unique Record Count |
|---|---|
| `clean_single_word_extraction` | `408` |
| `cross_section_homograph` | `4` |
| `parenthetical_phrasal_token` | `1` |

## 3. Automated Invariant Checks

| Check Name | Status | Details |
|---|---|---|
| `exact_source_span_reconstruction` | **PASS** | All 413 records reconstructed byte-for-byte from source_text[file_char_start:file_char_end]. |
| `exact_line_span_reconstruction` | **PASS** | All 413 records reconstructed from source_lines[line_number-1][line_char_start:line_char_end]. |
| `adjacent_entry_boundary_non_contamination` | **PASS** | Adjacent entries (N-1, N, N+1) verified non-overlapping and strictly increasing in file offsets. |
| `deterministic_id_and_count_completeness` | **PASS** | 233 verbs + 180 adjectives = 413 unique deterministic IDs. |

## 4. Reproducible Backtesting Commands

Run the following commands from the repository root:

```powershell
.\.venv\Scripts\python.exe -m parsers.justprepy_wordlist.parser
.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "account (for)"
```

## 5. Verification Procedure

1. Inspect `data/raw/sources/uclouvain/entries.raw.json` and confirm `record_count == 413`.
2. Verify that `source_text[file_char_start:file_char_end] == raw_text` for every record.
3. Check `qa/RAW_ISSUES.md` to confirm the issues are grouped by error category.
