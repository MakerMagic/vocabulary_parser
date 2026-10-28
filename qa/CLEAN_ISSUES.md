# CLEAN Stage Issues Report (`CLEAN_ISSUES.md`)

> **Source:** `new_words`  
> **Generated deterministically from:** `data/clean/sources/new_words/validation.json`  
> **Total Issue Occurrences:** `7`  
> **Unique Affected Records:** `7`

```text
ISSUE SUMMARY — NEW_WORDS / CLEAN
Cross-cluster duplicate entries: 4
Vocabulary below A1/A2 exclusion threshold: 3
TOTAL DISTINCT ISSUES: 7
UNIQUE AFFECTED RECORDS: 7
```

---

## 1. Issue Summary by Error Category

| Error Category | Issue Occurrences | Unique Records | Primary Severity |
|---|---|---|---|
| `Cross-cluster duplicate entries` | `4` | `4` | `review_notice` |
| `Vocabulary below A1/A2 exclusion threshold` | `3` | `3` | `review_notice` |
| **TOTAL DISTINCT ISSUES** | **`7`** | **`7`** | |

---

## 2. Itemized Issues Grouped by Error Category

### Category: Cross-cluster duplicate entries (Count: 4)

- **Affected Vocabulary Entries:** `Negligible` (#72), `Negligible` (#94), `Augment` (#99), `Augment` (#112)

#### [CROS-001] `#72` (`new_words_vocab_072`) — `Negligible`

- **Problem Description:** Preserved distinct cluster occurrence of 'Negligible' (#72, Cluster 28).
- **Actual Observed Output:** `Clean record #72 'Negligible' under Cluster 28 ('Small: Negligible, Minimal, Slight')`
- **Expected Output:** `Individually addressable record for 'Negligible'`
- **Root Cause:** Term belongs legitimately to multiple semantic clusters ('Small: Negligible, Minimal, Slight').
- **Corrective Action:** Preserve distinct addressable record with semantic cluster attribution.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Negligible"`
- **Resolution Status:** `distinct_record_maintained`

#### [CROS-002] `#94` (`new_words_vocab_094`) — `Negligible`

- **Problem Description:** Preserved distinct cluster occurrence of 'Negligible' (#94, Cluster 36).
- **Actual Observed Output:** `Clean record #94 'Negligible' under Cluster 36 ('Unimportant: Negligible, Trivial, Inconsequential, Trifling')`
- **Expected Output:** `Individually addressable record for 'Negligible'`
- **Root Cause:** Term belongs legitimately to multiple semantic clusters ('Unimportant: Negligible, Trivial, Inconsequential, Trifling').
- **Corrective Action:** Preserve distinct addressable record with semantic cluster attribution.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Negligible"`
- **Resolution Status:** `distinct_record_maintained`

#### [CROS-003] `#99` (`new_words_vocab_099`) — `Augment`

- **Problem Description:** Preserved distinct cluster occurrence of 'Augment' (#99, Cluster 37).
- **Actual Observed Output:** `Clean record #99 'Augment' under Cluster 37 ('Increase: Proliferate, Augment, Intensify, Amplify')`
- **Expected Output:** `Individually addressable record for 'Augment'`
- **Root Cause:** Term belongs legitimately to multiple semantic clusters ('Increase: Proliferate, Augment, Intensify, Amplify').
- **Corrective Action:** Preserve distinct addressable record with semantic cluster attribution.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Augment"`
- **Resolution Status:** `distinct_record_maintained`

#### [CROS-004] `#112` (`new_words_vocab_112`) — `Augment`

- **Problem Description:** Preserved distinct cluster occurrence of 'Augment' (#112, Cluster 41).
- **Actual Observed Output:** `Clean record #112 'Augment' under Cluster 41 ('Improve: Enhance, Augment, Ameliorate')`
- **Expected Output:** `Individually addressable record for 'Augment'`
- **Root Cause:** Term belongs legitimately to multiple semantic clusters ('Improve: Enhance, Augment, Ameliorate').
- **Corrective Action:** Preserve distinct addressable record with semantic cluster attribution.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Augment"`
- **Resolution Status:** `distinct_record_maintained`

### Category: Vocabulary below A1/A2 exclusion threshold (Count: 3)

- **Affected Vocabulary Entries:** `Repair` (#35), `Several` (#44), `Nearly` (#49)

#### [VOCA-001] `#35` (`new_words_vocab_035`) — `Repair`

- **Problem Description:** Excluded elementary vocabulary entry 'Repair' (Elementary maintenance verb (Cambridge EVP A2: to restore something damaged or broken to good condition)).
- **Actual Observed Output:** `status='excluded' (CEFR A2)`
- **Expected Output:** `Excluded record with documented CEFR A2 evidence`
- **Root Cause:** Vocabulary entry verified as CEFR A2 elementary level.
- **Corrective Action:** Exclude 'Repair' from eligible learning dataset per CEFR benchmark; preserve full record and provenance in RAW and CLEAN datasets.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Repair"`
- **Resolution Status:** `excluded_from_curriculum`

#### [VOCA-002] `#44` (`new_words_vocab_044`) — `Several`

- **Problem Description:** Excluded elementary vocabulary entry 'Several' (Elementary quantifier/determiner (Cambridge EVP A2: more than two but not many)).
- **Actual Observed Output:** `status='excluded' (CEFR A2)`
- **Expected Output:** `Excluded record with documented CEFR A2 evidence`
- **Root Cause:** Vocabulary entry verified as CEFR A2 elementary level.
- **Corrective Action:** Exclude 'Several' from eligible learning dataset per CEFR benchmark; preserve full record and provenance in RAW and CLEAN datasets.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Several"`
- **Resolution Status:** `excluded_from_curriculum`

#### [VOCA-003] `#49` (`new_words_vocab_049`) — `Nearly`

- **Problem Description:** Excluded elementary vocabulary entry 'Nearly' (Elementary degree adverb (Cambridge EVP A2: almost, but not completely)).
- **Actual Observed Output:** `status='excluded' (CEFR A2)`
- **Expected Output:** `Excluded record with documented CEFR A2 evidence`
- **Root Cause:** Vocabulary entry verified as CEFR A2 elementary level.
- **Corrective Action:** Exclude 'Nearly' from eligible learning dataset per CEFR benchmark; preserve full record and provenance in RAW and CLEAN datasets.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Nearly"`
- **Resolution Status:** `excluded_from_curriculum`
