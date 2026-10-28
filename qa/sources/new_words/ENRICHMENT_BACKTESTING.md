# ENRICHMENT Stage Backtesting Report (`ENRICHMENT_BACKTESTING.md`)

> **Source:** `new_words`  
> **Generated deterministically from:** `data/enriched/sources/new_words/validation.json`  
> **Stage Status:** `completed`

## 1. Stage Execution Summary

- **What was processed:** Vocabulary enrichment of 159 records for new_words (POS, Russian translation with <=2 alternatives [27 1-alt, 132 2-alt], multiword support, and contextual English explanations; 3 A1/A2 records tracked as excluded, 0 Essential questions).
- **Input artifact:** `data/clean/sources/new_words/entries.clean.json` (SHA-256: `f0c131505ce6d5c31f2368aeef0b7f9ed4c2c031cd088534e352443aad1c73e8`)
- **Output artifact:** `data/enriched/sources/new_words/entries.enriched.json` (SHA-256: `1ac35dbc00cbb1e120923501bc342bc3d793726f78d95eda96ffeeb3e249a0ee`)

| Metric | Count |
|---|---|
| **Records Entered Stage** | `159` |
| **Successfully Processed (Clean/Validated)** | `154` |
| **Excluded from Eligible Dataset (e.g. A1/A2)** | `3` |
| **Flagged for Review (`review_pending`)** | `2` |
| **Unresolved Blocking Errors (`error`)** | `0` |
| **Total Distinct Issue Occurrences** | `2` |
| **Unique Affected Records** | `2` |

## 2. Primary-Reason Partition (Disjoint Record Counts)

| Primary State / Reason | Unique Record Count |
|---|---|
| `eligible_clean_enriched` | `154` |
| `enrichment_sense_or_morphology_review` | `2` |
| `excluded_elementary_a1_a2` | `3` |

## 3. Automated Invariant Checks

| Check Name | Status | Details |
|---|---|---|
| `russian_translation_max_two_alternatives_and_cyrillic` | **PASS** | All 159 records have Cyrillic Russian translations with 1-2 alternatives (27 1-alt, 132 2-alt; 0 >2-alt). |
| `english_explanation_completeness_and_clarity` | **PASS** | All 159 records have non-empty, contextual English explanations (>= 15 chars). |
| `difficulty_field_unset_guard` | **PASS** | Reserved field 'difficulty' remains explicitly null across all 159 enriched records. |
| `elementary_a1_a2_exclusion_preservation` | **PASS** | Elementary A1/A2 excluded records (3) cleanly preserved with enrichment_status='excluded'. |
| `type_field_integrity` | **PASS** | Type field correctly tracked (Essential count: 0). |

## 4. Reproducible Backtesting Commands

Run the following commands from the repository root:

```powershell
.\.venv\Scripts\python.exe -m processors.enrichment.enricher_new_words
.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Necessitates"
.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Opulent"
.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Give rise to"
```

## 5. Verification Procedure

1. Inspect `data/enriched/sources/new_words/entries.enriched.json` and confirm all 159 records have `russian_alternatives_count <= 2`.
2. Confirm multiword alternatives (e.g. 'приводить к', 'порождать, вызывать') pass Cyrillic validation.
3. Review the 2 `review_pending` records in `qa/sources/new_words/ENRICHMENT_ISSUES.md`.
4. Verify that 3 elementary A1/A2 records have `status == 'excluded'`.
