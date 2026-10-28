# RAW Stage Issues Report (`RAW_ISSUES.md`)

> **Source:** `uclouvain`  
> **Generated deterministically from:** `data/raw/sources/uclouvain/validation.json`  
> **Total Issue Occurrences:** `5`  
> **Unique Affected Records:** `5`

```text
ISSUE SUMMARY — UCLOUVAIN / RAW
Cross-section homograph distinction: 4
Parenthetical or phrasal modifier syntax: 1
TOTAL DISTINCT ISSUES: 5
UNIQUE AFFECTED RECORDS: 5
```

---

## 1. Issue Summary by Error Category

| Error Category | Issue Occurrences | Unique Records | Primary Severity |
|---|---|---|---|
| `Cross-section homograph distinction` | `4` | `4` | `review_notice` |
| `Parenthetical or phrasal modifier syntax` | `1` | `1` | `review_notice` |
| **TOTAL DISTINCT ISSUES** | **`5`** | **`5`** | |

---

## 2. Itemized Issues Grouped by Error Category

### Category: Cross-section homograph distinction (Count: 4)

- **Affected Vocabulary Entries:** `present` (#167), `separate` (#205), `present` (#347), `separate` (#373)

#### [CROS-001] `#167` (`uclouvain_vocab_167`) — `present`

- **Problem Description:** Homograph 'present' extracted in section '233 verbs' (#167); also occurs at #347.
- **Actual Observed Output:** `#167 'present' in 233 verbs`
- **Expected Output:** `Separate records for #167 and #347`
- **Root Cause:** Word 'present' legitimately belongs to both '233 verbs' and '180 adjectives'.
- **Corrective Action:** Keep distinct section-scoped record ID uclouvain_vocab_167 (verb); do not deduplicate across sections.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe -m parsers.justprepy_wordlist.parser`
- **Resolution Status:** `section_scoped`

#### [CROS-002] `#205` (`uclouvain_vocab_205`) — `separate`

- **Problem Description:** Homograph 'separate' extracted in section '233 verbs' (#205); also occurs at #373.
- **Actual Observed Output:** `#205 'separate' in 233 verbs`
- **Expected Output:** `Separate records for #205 and #373`
- **Root Cause:** Word 'separate' legitimately belongs to both '233 verbs' and '180 adjectives'.
- **Corrective Action:** Keep distinct section-scoped record ID uclouvain_vocab_205 (verb); do not deduplicate across sections.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe -m parsers.justprepy_wordlist.parser`
- **Resolution Status:** `section_scoped`

#### [CROS-003] `#347` (`uclouvain_vocab_347`) — `present`

- **Problem Description:** Homograph 'present' extracted in section '180 adjectives' (#347); also occurs at #167.
- **Actual Observed Output:** `#347 'present' in 180 adjectives`
- **Expected Output:** `Separate records for #347 and #167`
- **Root Cause:** Word 'present' legitimately belongs to both '233 verbs' and '180 adjectives'.
- **Corrective Action:** Keep distinct section-scoped record ID uclouvain_vocab_347 (adjective); do not deduplicate across sections.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe -m parsers.justprepy_wordlist.parser`
- **Resolution Status:** `section_scoped`

#### [CROS-004] `#373` (`uclouvain_vocab_373`) — `separate`

- **Problem Description:** Homograph 'separate' extracted in section '180 adjectives' (#373); also occurs at #205.
- **Actual Observed Output:** `#373 'separate' in 180 adjectives`
- **Expected Output:** `Separate records for #373 and #205`
- **Root Cause:** Word 'separate' legitimately belongs to both '233 verbs' and '180 adjectives'.
- **Corrective Action:** Keep distinct section-scoped record ID uclouvain_vocab_373 (adjective); do not deduplicate across sections.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe -m parsers.justprepy_wordlist.parser`
- **Resolution Status:** `section_scoped`

### Category: Parenthetical or phrasal modifier syntax (Count: 1)

- **Affected Vocabulary Entries:** `account (for)` (#2)

#### [PARE-001] `#2` (`uclouvain_vocab_002`) — `account (for)`

- **Problem Description:** Preserved parenthetical particle in raw_text='account (for)' at span [18:31].
- **Actual Observed Output:** `raw_text='account (for)'`
- **Expected Output:** `Exact raw token preserved in RAW; structured separation in CLEAN`
- **Root Cause:** Source specifies optional/required preposition in parentheses for 'account (for)'.
- **Corrective Action:** Retain exact raw_text='account (for)' in RAW; separate lemma 'account' and particle '(for)' non-destructively in CLEAN.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe -m parsers.justprepy_wordlist.parser`
- **Resolution Status:** `preserved_in_raw`
