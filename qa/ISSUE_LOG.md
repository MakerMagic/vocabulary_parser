# QA Issue & Root-Cause Log (`qa/ISSUE_LOG.md`)

> **Status:** Active — `0` blocking errors (`error`), `5` records flagged for linguistic review (`review_pending`), `379` records fully validated (`validated`), `29` records excluded (`elementary_a1_a2`) out of `413` input items.
> **Authority:** Synchronized with `data/pre_final/validation.json` and stage `<STAGE>_ISSUES.md` reports.

---

## 1. Stage-by-Stage Defect & Finding Summary

| Stage | Entered | Succeeded / Validated | Review Pending | Excluded (A1/A2) | Blocking Errors | Primary Findings | Report Pair |
|---|---|---|---|---|---|---|---|
| **ACQUISITION** | `1` file | `1` | `0` | `0` | `0` | 0 issues; SHA-256 lock established | [`ACQUISITION_BACKTESTING.md`](file:///c:/Users/user/Desktop/vocabulary_parser/qa/ACQUISITION_BACKTESTING.md) / [`ACQUISITION_ISSUES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/qa/ACQUISITION_ISSUES.md) |
| **INSPECTION** | `413` | `413` | `5` notices | `0` | `0` | 1 parenthetical token (`account (for)`), 2 cross-section homograph pairs (`present`, `separate`), 3 modals (`can`, `may`, `should`), 1 hyphenated (`so-called`) | [`INSPECTION_BACKTESTING.md`](file:///c:/Users/user/Desktop/vocabulary_parser/qa/INSPECTION_BACKTESTING.md) / [`INSPECTION_ISSUES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/qa/INSPECTION_ISSUES.md) |
| **RAW** | `413` | `413` | `5` notices | `0` | `0` | Exact character/line spans verified for all 413 entries; 1 parenthetical & 4 homograph records tagged | [`RAW_BACKTESTING.md`](file:///c:/Users/user/Desktop/vocabulary_parser/qa/RAW_BACKTESTING.md) / [`RAW_ISSUES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/qa/RAW_ISSUES.md) |
| **CLEAN** | `413` | `384` | `1` notice | `29` | `0` | 100% token-ledger match; `#2 account (for)` separated into lemma + particle; 29 elementary A1/A2 items excluded from curriculum; slash-separation architecture supported | [`CLEAN_BACKTESTING.md`](file:///c:/Users/user/Desktop/vocabulary_parser/qa/CLEAN_BACKTESTING.md) / [`CLEAN_ISSUES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/qa/CLEAN_ISSUES.md) |
| **ENRICHMENT** | `413` | `379` | `5` | `29` | `0` | All records enriched with POS, <=2 translation alternatives (multiword allowed), contextual explanation; 5 flagged `review_pending`; 29 tracked as excluded | [`ENRICHMENT_BACKTESTING.md`](file:///c:/Users/user/Desktop/vocabulary_parser/qa/ENRICHMENT_BACKTESTING.md) / [`ENRICHMENT_ISSUES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/qa/ENRICHMENT_ISSUES.md) |
| **VALIDATION / PRE-FINAL** | `413` | `379` | `5` | `29` | `0` | End-to-end provenance, <=2 translation alternatives, non-circular explanation, and unset `difficulty: null` verified | [`VALIDATION_BACKTESTING.md`](file:///c:/Users/user/Desktop/vocabulary_parser/qa/VALIDATION_BACKTESTING.md) / [`VALIDATION_ISSUES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/qa/VALIDATION_ISSUES.md) |

---

## 2. Itemized Active Review Entries (`review_pending`)

### [ISSUE-001] Record `#2` (`uclouvain_vocab_002`) — `account (for)`

- **Status:** `review_pending`
- **Affected Stage:** `ENRICHMENT / VALIDATION`
- **Symptom / Observation:** Dual primary academic senses: causal/explanatory ('объяснять; являться причиной') and proportional ('составлять часть'); requires parenthetical preposition '(for)'.
- **Root Cause:** Dual primary academic senses: causal/explanatory ('объяснять; являться причиной') and proportional ('составлять часть'); requires parenthetical preposition '(for)'.
- **Working Handling:** Preserved exact word `account (for)`, populated primary Russian translation (<=2 alternatives) and contextual English explanation, and flagged as `review_pending` for human curriculum review rather than silently guessing or truncating.
- **Reproduction Command:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "account (for)"`
- **Regression Test Reference:** `tests/test_vocabulary_pipeline.py`

### [ISSUE-002] Record `#206` (`uclouvain_vocab_206`) — `should`

- **Status:** `review_pending`
- **Affected Stage:** `ENRICHMENT / VALIDATION`
- **Symptom / Observation:** Defective English modal auxiliary verb; lacks a grammatical infinitive in Russian and is rendered via the modal predicative 'следует' (or 'должен').
- **Root Cause:** Defective English modal auxiliary verb; lacks a grammatical infinitive in Russian and is rendered via the modal predicative 'следует' (or 'должен').
- **Working Handling:** Preserved exact word `should`, populated primary Russian translation (<=2 alternatives) and contextual English explanation, and flagged as `review_pending` for human curriculum review rather than silently guessing or truncating.
- **Reproduction Command:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "should"`
- **Regression Test Reference:** `tests/test_vocabulary_pipeline.py`

### [ISSUE-003] Record `#252` (`uclouvain_vocab_252`) — `certain`

- **Status:** `review_pending`
- **Affected Stage:** `ENRICHMENT / VALIDATION`
- **Symptom / Observation:** Dual core adjectival senses with distinct Russian translations: (1) attributive 'определённый' (specific/particular) and (2) predicative 'уверенный' (confident/sure).
- **Root Cause:** Dual core adjectival senses with distinct Russian translations: (1) attributive 'определённый' (specific/particular) and (2) predicative 'уверенный' (confident/sure).
- **Working Handling:** Preserved exact word `certain`, populated primary Russian translation (<=2 alternatives) and contextual English explanation, and flagged as `review_pending` for human curriculum review rather than silently guessing or truncating.
- **Reproduction Command:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "certain"`
- **Regression Test Reference:** `tests/test_vocabulary_pipeline.py`

### [ISSUE-004] Record `#347` (`uclouvain_vocab_347`) — `present`

- **Status:** `review_pending`
- **Affected Stage:** `ENRICHMENT / VALIDATION`
- **Symptom / Observation:** Cross-section homograph (also #167 verb); dual adjectival senses: temporal ('настоящий') and locational ('присутствующий').
- **Root Cause:** Cross-section homograph (also #167 verb); dual adjectival senses: temporal ('настоящий') and locational ('присутствующий').
- **Working Handling:** Preserved exact word `present`, populated primary Russian translation (<=2 alternatives) and contextual English explanation, and flagged as `review_pending` for human curriculum review rather than silently guessing or truncating.
- **Reproduction Command:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "present"`
- **Regression Test Reference:** `tests/test_vocabulary_pipeline.py`

### [ISSUE-005] Record `#402` (`uclouvain_vocab_402`) — `unlike`

- **Status:** `review_pending`
- **Affected Stage:** `ENRICHMENT / VALIDATION`
- **Symptom / Observation:** Scoped as predicative adjective ('непохожий') per '180 adjectives' header; distinct from the prepositional role ('в отличие от').
- **Root Cause:** Scoped as predicative adjective ('непохожий') per '180 adjectives' header; distinct from the prepositional role ('в отличие от').
- **Working Handling:** Preserved exact word `unlike`, populated primary Russian translation (<=2 alternatives) and contextual English explanation, and flagged as `review_pending` for human curriculum review rather than silently guessing or truncating.
- **Reproduction Command:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "unlike"`
- **Regression Test Reference:** `tests/test_vocabulary_pipeline.py`
