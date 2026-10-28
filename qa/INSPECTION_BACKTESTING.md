# INSPECTION Stage Backtesting Report (`INSPECTION_BACKTESTING.md`)

> **Generated deterministically from:** `data/inspection/validation.json`
> **Stage Status:** `completed`

## 1. Stage Execution Summary

- **What was processed:** Pre-parser structural and lexical inspection of the 413-item justprepy vocabulary list.
- **Input artifact:** `acquisition/local/justprepy_vocabulary_list.txt` (SHA-256: `e1b15633f274f58f093a3e1950dd1f368aad83fd54fb67ca9f682344d5628d7e`)
- **Output artifact:** `data/inspection/profile.json` (SHA-256: `4bdab7cf386c3640b7e2f54dcd32c28b9733333a46124025feb772a51ae30f17`)

| Metric | Count |
|---|---|
| **Records Entered Stage** | `413` |
| **Successfully Processed (Clean/Validated)** | `413` |
| **Flagged for Review (`review_pending`)** | `5` |
| **Unresolved Blocking Errors (`error`)** | `0` |
| **Total Affected Records with Findings** | `9` |
| **Total Structured Findings Logged** | `9` |

## 2. Primary-Reason Partition (Disjoint Record Counts)

| Primary State / Reason | Unique Record Count |
|---|---|
| `cross_section_homograph` | `4` |
| `hyphenated_compound_token` | `1` |
| `modal_auxiliary_in_verbs` | `3` |
| `parenthetical_phrasal_token` | `1` |
| `standard_single_word_item` | `404` |

## 3. Automated Invariant Checks

| Check Name | Status | Details |
|---|---|---|
| `section_1_verbs_count_matches` | **PASS** | Section 1 header declares 233 verbs and line 2 contains exactly 233 comma-separated items. |
| `section_2_adjectives_count_matches` | **PASS** | Section 2 header declares 180 adjectives and line 4 contains exactly 180 comma-separated items. |
| `zero_within_section_duplicates` | **PASS** | 0 duplicate entries within '233 verbs' and 0 duplicate entries within '180 adjectives'. |
| `cross_section_homographs_identified` | **PASS** | Detected 2 cross-section homograph pairs (present, separate) requiring section-scoped identity. |

## 4. Reproducible Backtesting Commands

Run the following commands from the repository root (`c:\Users\user\Desktop\vocabulary_parser`):

```powershell
.\.venv\Scripts\python.exe -m processors.inspection
.\.venv\Scripts\python.exe -m pytest -q tests/test_vocabulary_pipeline.py -k inspection
```

## 5. Verification Procedure

1. Inspect `data/inspection/profile.json` and `inspections/SOURCE_PROFILES.md` to verify section counts (233 + 180 = 413).
2. Confirm the 2 cross-section homographs (`present`, `separate`) and `account (for)` are logged in `qa/INSPECTION_ISSUES.md`.
3. Run the inspection pytest suite to confirm structural profile invariants.
