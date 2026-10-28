# RAW Stage Backtesting Report (`RAW_BACKTESTING.md`)

> **Source:** `new_words`  
> **Generated deterministically from:** `data/raw/sources/new_words/validation.json`  
> **Stage Status:** `completed`

## 1. Stage Execution Summary

- **What was processed:** RAW extraction of 159 records across 56 semantic clusters from acquisition/sources/new_words/new_words.md.
- **Input artifact:** `acquisition/sources/new_words/new_words.md` (SHA-256: `6aac09b4631462c239e49c6bbbbebf0a2d30ee88acddfbb16debb780ce163ec7`)
- **Output artifact:** `data/raw/sources/new_words/entries.raw.json` (SHA-256: `4fb56c9b4a453adae704296482f1c2f57f477e7aa0b6d3f2e0b70f380831c9ee`)

| Metric | Count |
|---|---|
| **Records Entered Stage** | `159` |
| **Successfully Processed (Clean/Validated)** | `159` |
| **Excluded from Eligible Dataset (e.g. A1/A2)** | `0` |
| **Flagged for Review (`review_pending`)** | `0` |
| **Unresolved Blocking Errors (`error`)** | `0` |
| **Total Distinct Issue Occurrences** | `17` |
| **Unique Affected Records** | `17` |

## 2. Primary-Reason Partition (Disjoint Record Counts)

| Primary State / Reason | Unique Record Count |
|---|---|
| `clean_raw_entries` | `159` |

## 3. Automated Invariant Checks

| Check Name | Status | Details |
|---|---|---|
| `exact_source_span_reconstruction` | **PASS** | All 159 entries reconstructed from source file byte slices without drift. |
| `raw_metadata_completeness` | **PASS** | 100% of records have non-empty declared POS, Russian translation, and English explanation. |
| `difficulty_field_unset_guard` | **PASS** | Reserved field 'difficulty' is explicitly null across all records. |
| `type_field_extensibility` | **PASS** | Type field cleanly supported (0 Essential questions detected; schema prepared). |

## 4. Reproducible Backtesting Commands

Run the following commands from the repository root:

```powershell
.\.venv\Scripts\python.exe -m parsers.new_words.parser
.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Impact"
.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Give rise to"
.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "negligible"
```

## 5. Verification Procedure

1. Inspect `data/raw/sources/new_words/entries.raw.json` and confirm 159 records with exact character and line spans.
2. Verify that multiword expressions ('Give rise to', 'Lead to', 'Be capable of') are intact.
3. Inspect `qa/sources/new_words/RAW_ISSUES.md` for duplicate and multiword entries.
