# ENRICHMENT Stage Issues Report (`ENRICHMENT_ISSUES.md`)

> **Source:** `uclouvain`  
> **Generated deterministically from:** `data/enriched/sources/uclouvain/validation.json`  
> **Total Issue Occurrences:** `5`  
> **Unique Affected Records:** `5`

```text
ISSUE SUMMARY — UCLOUVAIN / ENRICHMENT
Lexical sense and morphology review notices: 5
TOTAL DISTINCT ISSUES: 5
UNIQUE AFFECTED RECORDS: 5
```

---

## 1. Issue Summary by Error Category

| Error Category | Issue Occurrences | Unique Records | Primary Severity |
|---|---|---|---|
| `Lexical sense and morphology review notices` | `5` | `5` | `review_pending` |
| **TOTAL DISTINCT ISSUES** | **`5`** | **`5`** | |

---

## 2. Itemized Issues Grouped by Error Category

### Category: Lexical sense and morphology review notices (Count: 5)

- **Affected Vocabulary Entries:** `account (for)` (#2), `should` (#206), `certain` (#252), `present` (#347), `unlike` (#402)

#### [LEXI-001] `#2` (`uclouvain_vocab_002`) — `account (for)`

- **Problem Description:** Dual primary academic senses: causal/explanatory ('объяснять; являться причиной') and proportional ('составлять часть'); requires parenthetical preposition '(for)'.
- **Actual Observed Output:** `verb (phrasal) | объяснять; являться причиной`
- **Expected Output:** `Confirmed primary curriculum sense selection`
- **Root Cause:** Dual primary academic senses: causal/explanatory ('объяснять; являться причиной') and proportional ('составлять часть'); requires parenthetical preposition '(for)'.
- **Corrective Action:** Review primary sense selection in HTML backtesting interface; confirm whether secondary sense or grammatical note requires a separate curriculum entry.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "account (for)"`
- **Resolution Status:** `review_pending_curriculum_decision`

#### [LEXI-002] `#206` (`uclouvain_vocab_206`) — `should`

- **Problem Description:** Defective English modal auxiliary verb; lacks a grammatical infinitive in Russian and is rendered via the modal predicative 'следует' (or 'должен').
- **Actual Observed Output:** `verb (modal) | следует`
- **Expected Output:** `Confirmed primary curriculum sense selection`
- **Root Cause:** Defective English modal auxiliary verb; lacks a grammatical infinitive in Russian and is rendered via the modal predicative 'следует' (or 'должен').
- **Corrective Action:** Review primary sense selection in HTML backtesting interface; confirm whether secondary sense or grammatical note requires a separate curriculum entry.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "should"`
- **Resolution Status:** `review_pending_curriculum_decision`

#### [LEXI-003] `#252` (`uclouvain_vocab_252`) — `certain`

- **Problem Description:** Dual core adjectival senses with distinct Russian translations: (1) attributive 'определённый' (specific/particular) and (2) predicative 'уверенный' (confident/sure).
- **Actual Observed Output:** `adjective | определённый; уверенный`
- **Expected Output:** `Confirmed primary curriculum sense selection`
- **Root Cause:** Dual core adjectival senses with distinct Russian translations: (1) attributive 'определённый' (specific/particular) and (2) predicative 'уверенный' (confident/sure).
- **Corrective Action:** Review primary sense selection in HTML backtesting interface; confirm whether secondary sense or grammatical note requires a separate curriculum entry.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "certain"`
- **Resolution Status:** `review_pending_curriculum_decision`

#### [LEXI-004] `#347` (`uclouvain_vocab_347`) — `present`

- **Problem Description:** Cross-section homograph (also #167 verb); dual adjectival senses: temporal ('настоящий') and locational ('присутствующий').
- **Actual Observed Output:** `adjective | настоящий; присутствующий`
- **Expected Output:** `Confirmed primary curriculum sense selection`
- **Root Cause:** Cross-section homograph (also #167 verb); dual adjectival senses: temporal ('настоящий') and locational ('присутствующий').
- **Corrective Action:** Review primary sense selection in HTML backtesting interface; confirm whether secondary sense or grammatical note requires a separate curriculum entry.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "present"`
- **Resolution Status:** `review_pending_curriculum_decision`

#### [LEXI-005] `#402` (`uclouvain_vocab_402`) — `unlike`

- **Problem Description:** Scoped as predicative adjective ('непохожий') per '180 adjectives' header; distinct from the prepositional role ('в отличие от').
- **Actual Observed Output:** `adjective | непохожий`
- **Expected Output:** `Confirmed primary curriculum sense selection`
- **Root Cause:** Scoped as predicative adjective ('непохожий') per '180 adjectives' header; distinct from the prepositional role ('в отличие от').
- **Corrective Action:** Review primary sense selection in HTML backtesting interface; confirm whether secondary sense or grammatical note requires a separate curriculum entry.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "unlike"`
- **Resolution Status:** `review_pending_curriculum_decision`
