# ENRICHMENT Stage Backtesting Report (`ENRICHMENT_BACKTESTING.md`)

> **Source:** `nature`  
> **Generated deterministically from:** `data/enriched/sources/nature/validation.json`  
> **Stage Status:** `completed`

## 1. Stage Execution Summary

- **What was processed:** Vocabulary enrichment, Russian translation rule, and POS normalization audit for nature.
- **Input artifact:** `data/clean/sources/nature/entries.clean.json` (SHA-256: `e1a5498d9d8221cb2a7c224b22236d4405e77d2186c3fd8e9e5fdadf1ea6efb3`)
- **Output artifact:** `data/enriched/sources/nature/entries.enriched.json` (SHA-256: `b069cef7a6064135e29a63be9eac2753c70764220967e4fec588ca6152c5701e`)

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
| `enriched_successfully` | `169` |

## 3. Automated Invariant Checks

| Check Name | Status | Details |
|---|---|---|
| `russian_translation_two_alternatives_cap` | **PASS** | All 169 records processed with valid Russian translation alternatives (<=2 alternatives). |
| `pos_normalization_integrity` | **PASS** | All parts of speech normalized to valid platform categories. |
| `english_explanation_integrity` | **PASS** | All English explanations verified >=15 chars and non-circular. |
| `preset_and_difficulty_contract` | **PASS** | Contract invariant: preset == 'nature' and difficulty == null across all enriched records. |

## 4. Reproducible Backtesting Commands

Run the following commands from the repository root:

```powershell
.\.venv\Scripts\python.exe -c "from processors.enrichment.enricher_nature import run_enrichment; run_enrichment()"
Get-Content data/enriched/sources/nature/validation.json | ConvertFrom-Json
```

## 5. Verification Procedure

1. Confirm all records have <= 2 Russian translation alternatives.
2. Verify all parts of speech belong to standard lowercase categories.
3. Confirm preset is 'nature' and difficulty is null.
