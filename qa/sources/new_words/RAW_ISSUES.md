# RAW Stage Issues Report (`RAW_ISSUES.md`)

> **Source:** `new_words`  
> **Generated deterministically from:** `data/raw/sources/new_words/validation.json`  
> **Total Issue Occurrences:** `17`  
> **Unique Affected Records:** `17`

```text
ISSUE SUMMARY — NEW_WORDS / RAW
Cross-cluster duplicate entries: 4
Essential question group verification: 1
Phrasal and multiword expressions: 12
TOTAL DISTINCT ISSUES: 17
UNIQUE AFFECTED RECORDS: 17
```

---

## 1. Issue Summary by Error Category

| Error Category | Issue Occurrences | Unique Records | Primary Severity |
|---|---|---|---|
| `Cross-cluster duplicate entries` | `4` | `4` | `review_notice` |
| `Essential question group verification` | `1` | `1` | `review_notice` |
| `Phrasal and multiword expressions` | `12` | `12` | `review_notice` |
| **TOTAL DISTINCT ISSUES** | **`17`** | **`17`** | |

---

## 2. Itemized Issues Grouped by Error Category

### Category: Cross-cluster duplicate entries (Count: 4)

- **Affected Vocabulary Entries:** `Negligible` (#72), `Negligible` (#94), `Augment` (#99), `Augment` (#112)

#### [CROS-001] `#72` (`new_words_vocab_072`) — `Negligible`

- **Problem Description:** Headword 'Negligible' appears in multiple clusters (also at #94).
- **Actual Observed Output:** `Record #72 'Negligible' in Cluster 28 ('Small: Negligible, Minimal, Slight')`
- **Expected Output:** `Multiple semantic cluster occurrences preserved ([94])`
- **Root Cause:** Source text intentionally reuses term under distinct semantic clusters with tailored explanations.
- **Corrective Action:** Preserve distinct addressable record with cross-cluster reference and nuanced definition.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Negligible"`
- **Resolution Status:** `distinct_cluster_record_preserved`

#### [CROS-002] `#94` (`new_words_vocab_094`) — `Negligible`

- **Problem Description:** Headword 'Negligible' appears in multiple clusters (also at #72).
- **Actual Observed Output:** `Record #94 'Negligible' in Cluster 36 ('Unimportant: Negligible, Trivial, Inconsequential, Trifling')`
- **Expected Output:** `Multiple semantic cluster occurrences preserved ([72])`
- **Root Cause:** Source text intentionally reuses term under distinct semantic clusters with tailored explanations.
- **Corrective Action:** Preserve distinct addressable record with cross-cluster reference and nuanced definition.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Negligible"`
- **Resolution Status:** `distinct_cluster_record_preserved`

#### [CROS-003] `#99` (`new_words_vocab_099`) — `Augment`

- **Problem Description:** Headword 'Augment' appears in multiple clusters (also at #112).
- **Actual Observed Output:** `Record #99 'Augment' in Cluster 37 ('Increase: Proliferate, Augment, Intensify, Amplify')`
- **Expected Output:** `Multiple semantic cluster occurrences preserved ([112])`
- **Root Cause:** Source text intentionally reuses term under distinct semantic clusters with tailored explanations.
- **Corrective Action:** Preserve distinct addressable record with cross-cluster reference and nuanced definition.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Augment"`
- **Resolution Status:** `distinct_cluster_record_preserved`

#### [CROS-004] `#112` (`new_words_vocab_112`) — `Augment`

- **Problem Description:** Headword 'Augment' appears in multiple clusters (also at #99).
- **Actual Observed Output:** `Record #112 'Augment' in Cluster 41 ('Improve: Enhance, Augment, Ameliorate')`
- **Expected Output:** `Multiple semantic cluster occurrences preserved ([99])`
- **Root Cause:** Source text intentionally reuses term under distinct semantic clusters with tailored explanations.
- **Corrective Action:** Preserve distinct addressable record with cross-cluster reference and nuanced definition.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Augment"`
- **Resolution Status:** `distinct_cluster_record_preserved`

### Category: Essential question group verification (Count: 1)

- **Affected Vocabulary Entries:** `N/A` (#0)

#### [ESSE-001] `#0` (`source_audit_new_words`) — `N/A`

- **Problem Description:** Source audit completed: 0 general questions present at end of new_words.md (159 total lexical entries).
- **Actual Observed Output:** `0 questions detected in source`
- **Expected Output:** `0 questions in new_words.md; schema prepared for Type: Essential`
- **Root Cause:** new_words.md contains 56 semantic clusters without an appended general question section.
- **Corrective Action:** Verify schema supports 'type' field and confirm 0 questions were present at end of new_words.md.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe -m parsers.new_words.parser`
- **Resolution Status:** `schema_prepared_for_type_field`

### Category: Phrasal and multiword expressions (Count: 12)

- **Affected Vocabulary Entries:** `Lead to` (#22), `Give rise to` (#23), `Be capable of` (#37), `A proportion of` (#45), `In many cases` (#48), `Myriad of` (#76), `A smaller amount of` (#78), `In no case` (#81), `Under no condition` (#82), `Contingent on` (#119), `Hinge on` (#120), `Financially secure` (#122)

#### [PHRA-001] `#22` (`new_words_vocab_022`) — `Lead to`

- **Problem Description:** Preserved multiword lexical unit 'Lead to' in RAW.
- **Actual Observed Output:** `multiword expression: 'Lead to'`
- **Expected Output:** `Complete multiword expression 'Lead to'`
- **Root Cause:** Source includes genuine multiword phrasal verbs, idioms, and prepositional phrases.
- **Corrective Action:** Preserve multiword expression as a complete lexical unit; do not fragment into single words.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Lead to"`
- **Resolution Status:** `preserved_as_cohesive_unit`

#### [PHRA-002] `#23` (`new_words_vocab_023`) — `Give rise to`

- **Problem Description:** Preserved multiword lexical unit 'Give rise to' in RAW.
- **Actual Observed Output:** `multiword expression: 'Give rise to'`
- **Expected Output:** `Complete multiword expression 'Give rise to'`
- **Root Cause:** Source includes genuine multiword phrasal verbs, idioms, and prepositional phrases.
- **Corrective Action:** Preserve multiword expression as a complete lexical unit; do not fragment into single words.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Give rise to"`
- **Resolution Status:** `preserved_as_cohesive_unit`

#### [PHRA-003] `#37` (`new_words_vocab_037`) — `Be capable of`

- **Problem Description:** Preserved multiword lexical unit 'Be capable of' in RAW.
- **Actual Observed Output:** `multiword expression: 'Be capable of'`
- **Expected Output:** `Complete multiword expression 'Be capable of'`
- **Root Cause:** Source includes genuine multiword phrasal verbs, idioms, and prepositional phrases.
- **Corrective Action:** Preserve multiword expression as a complete lexical unit; do not fragment into single words.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Be capable of"`
- **Resolution Status:** `preserved_as_cohesive_unit`

#### [PHRA-004] `#45` (`new_words_vocab_045`) — `A proportion of`

- **Problem Description:** Preserved multiword lexical unit 'A proportion of' in RAW.
- **Actual Observed Output:** `multiword expression: 'A proportion of'`
- **Expected Output:** `Complete multiword expression 'A proportion of'`
- **Root Cause:** Source includes genuine multiword phrasal verbs, idioms, and prepositional phrases.
- **Corrective Action:** Preserve multiword expression as a complete lexical unit; do not fragment into single words.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "A proportion of"`
- **Resolution Status:** `preserved_as_cohesive_unit`

#### [PHRA-005] `#48` (`new_words_vocab_048`) — `In many cases`

- **Problem Description:** Preserved multiword lexical unit 'In many cases' in RAW.
- **Actual Observed Output:** `multiword expression: 'In many cases'`
- **Expected Output:** `Complete multiword expression 'In many cases'`
- **Root Cause:** Source includes genuine multiword phrasal verbs, idioms, and prepositional phrases.
- **Corrective Action:** Preserve multiword expression as a complete lexical unit; do not fragment into single words.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "In many cases"`
- **Resolution Status:** `preserved_as_cohesive_unit`

#### [PHRA-006] `#76` (`new_words_vocab_076`) — `Myriad of`

- **Problem Description:** Preserved multiword lexical unit 'Myriad of' in RAW.
- **Actual Observed Output:** `multiword expression: 'Myriad of'`
- **Expected Output:** `Complete multiword expression 'Myriad of'`
- **Root Cause:** Source includes genuine multiword phrasal verbs, idioms, and prepositional phrases.
- **Corrective Action:** Preserve multiword expression as a complete lexical unit; do not fragment into single words.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Myriad of"`
- **Resolution Status:** `preserved_as_cohesive_unit`

#### [PHRA-007] `#78` (`new_words_vocab_078`) — `A smaller amount of`

- **Problem Description:** Preserved multiword lexical unit 'A smaller amount of' in RAW.
- **Actual Observed Output:** `multiword expression: 'A smaller amount of'`
- **Expected Output:** `Complete multiword expression 'A smaller amount of'`
- **Root Cause:** Source includes genuine multiword phrasal verbs, idioms, and prepositional phrases.
- **Corrective Action:** Preserve multiword expression as a complete lexical unit; do not fragment into single words.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "A smaller amount of"`
- **Resolution Status:** `preserved_as_cohesive_unit`

#### [PHRA-008] `#81` (`new_words_vocab_081`) — `In no case`

- **Problem Description:** Preserved multiword lexical unit 'In no case' in RAW.
- **Actual Observed Output:** `multiword expression: 'In no case'`
- **Expected Output:** `Complete multiword expression 'In no case'`
- **Root Cause:** Source includes genuine multiword phrasal verbs, idioms, and prepositional phrases.
- **Corrective Action:** Preserve multiword expression as a complete lexical unit; do not fragment into single words.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "In no case"`
- **Resolution Status:** `preserved_as_cohesive_unit`

#### [PHRA-009] `#82` (`new_words_vocab_082`) — `Under no condition`

- **Problem Description:** Preserved multiword lexical unit 'Under no condition' in RAW.
- **Actual Observed Output:** `multiword expression: 'Under no condition'`
- **Expected Output:** `Complete multiword expression 'Under no condition'`
- **Root Cause:** Source includes genuine multiword phrasal verbs, idioms, and prepositional phrases.
- **Corrective Action:** Preserve multiword expression as a complete lexical unit; do not fragment into single words.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Under no condition"`
- **Resolution Status:** `preserved_as_cohesive_unit`

#### [PHRA-010] `#119` (`new_words_vocab_119`) — `Contingent on`

- **Problem Description:** Preserved multiword lexical unit 'Contingent on' in RAW.
- **Actual Observed Output:** `multiword expression: 'Contingent on'`
- **Expected Output:** `Complete multiword expression 'Contingent on'`
- **Root Cause:** Source includes genuine multiword phrasal verbs, idioms, and prepositional phrases.
- **Corrective Action:** Preserve multiword expression as a complete lexical unit; do not fragment into single words.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Contingent on"`
- **Resolution Status:** `preserved_as_cohesive_unit`

#### [PHRA-011] `#120` (`new_words_vocab_120`) — `Hinge on`

- **Problem Description:** Preserved multiword lexical unit 'Hinge on' in RAW.
- **Actual Observed Output:** `multiword expression: 'Hinge on'`
- **Expected Output:** `Complete multiword expression 'Hinge on'`
- **Root Cause:** Source includes genuine multiword phrasal verbs, idioms, and prepositional phrases.
- **Corrective Action:** Preserve multiword expression as a complete lexical unit; do not fragment into single words.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Hinge on"`
- **Resolution Status:** `preserved_as_cohesive_unit`

#### [PHRA-012] `#122` (`new_words_vocab_122`) — `Financially secure`

- **Problem Description:** Preserved multiword lexical unit 'Financially secure' in RAW.
- **Actual Observed Output:** `multiword expression: 'Financially secure'`
- **Expected Output:** `Complete multiword expression 'Financially secure'`
- **Root Cause:** Source includes genuine multiword phrasal verbs, idioms, and prepositional phrases.
- **Corrective Action:** Preserve multiword expression as a complete lexical unit; do not fragment into single words.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Financially secure"`
- **Resolution Status:** `preserved_as_cohesive_unit`
