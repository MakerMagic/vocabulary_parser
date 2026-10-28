# ENRICHMENT Stage Issues Report (`ENRICHMENT_ISSUES.md`)

> **Source:** `new_words`  
> **Generated deterministically from:** `data/enriched/sources/new_words/validation.json`  
> **Total Issue Occurrences:** `2`  
> **Unique Affected Records:** `2`

```text
ISSUE SUMMARY — NEW_WORDS / ENRICHMENT
Lexical sense and morphology review notices: 2
TOTAL DISTINCT ISSUES: 2
UNIQUE AFFECTED RECORDS: 2
```

---

## 1. Issue Summary by Error Category

| Error Category | Issue Occurrences | Unique Records | Primary Severity |
|---|---|---|---|
| `Lexical sense and morphology review notices` | `2` | `2` | `review_pending` |
| **TOTAL DISTINCT ISSUES** | **`2`** | **`2`** | |

---

## 2. Itemized Issues Grouped by Error Category

### Category: Lexical sense and morphology review notices (Count: 2)

- **Affected Vocabulary Entries:** `Necessitates` (#27), `Opulent` (#126)

#### [LEXI-001] `#27` (`new_words_vocab_027`) — `Necessitates`

- **Problem Description:** Grammatical morphology note: Ingested as third-person singular inflected form 'necessitates'; base lemma is 'necessitate'.
- **Actual Observed Output:** `verb | делает необходимым; требует`
- **Expected Output:** `Approved curriculum representation`
- **Root Cause:** Grammatical morphology note: Ingested as third-person singular inflected form 'necessitates'; base lemma is 'necessitate'.
- **Corrective Action:** Review primary sense selection and morphological form in HTML backtesting interface; confirm whether a lemma adjustment or curriculum note is appropriate.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Necessitates"`
- **Resolution Status:** `review_pending_curriculum_decision`

#### [LEXI-002] `#126` (`new_words_vocab_126`) — `Opulent`

- **Problem Description:** Semantic contrast note: 'Opulent' (wealthy/luxurious) appears in Cluster 46 ('Unwealthy') as an antonymous/contrasting term.
- **Actual Observed Output:** `adjective | богатый; роскошный`
- **Expected Output:** `Approved curriculum representation`
- **Root Cause:** Semantic contrast note: 'Opulent' (wealthy/luxurious) appears in Cluster 46 ('Unwealthy') as an antonymous/contrasting term.
- **Corrective Action:** Review primary sense selection and morphological form in HTML backtesting interface; confirm whether a lemma adjustment or curriculum note is appropriate.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source new_words --word "Opulent"`
- **Resolution Status:** `review_pending_curriculum_decision`
