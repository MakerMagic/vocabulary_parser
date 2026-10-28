# UCLouvain Stage Issues & Backtesting Registry (`STAGE_ISSUES.md`)

> **Source Identifier:** `uclouvain`  
> **Source Document:** [`acquisition/sources/uclouvain/uclouvain_vocabulary_list.txt`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/sources/uclouvain/uclouvain_vocabulary_list.txt)  
> **Authority:** Tracks source-specific issues across `uclouvain` pipeline stages.

---

## 1. Stage Findings Summary for `uclouvain`

| Stage | Input Records | Validated | Review Pending | Excluded (A1/A2) | Blocking Errors | Core Findings |
|---|---|---|---|---|---|---|
| **Acquisition** | `1` file | `1` | `0` | `0` | `0` | SHA-256 locked (`e1b15633...`); UTF-8 verified. |
| **Inspection** | `413` | `413` | `5` notices | `0` | `0` | 2 sections (233+180=413); 1 parenthetical (`account (for)`), 2 homograph pairs (`present`, `separate`), 3 modals (`can`, `may`, `should`), 1 hyphenated (`so-called`). |
| **RAW Extraction** | `413` | `413` | `5` notices | `0` | `0` | 100% exact character/line span reconstruction; $N \pm 1$ neighbor boundaries verified; categorized issues emitted. |
| **Cleaning** | `413` | `384` | `1` notice | `29` | `0` | 100% token-ledger match; `#2 account (for)` separated; 29 elementary A1/A2 items systematically excluded with CEFR evidence; `"difficulty": null` set. |
| **Enrichment** | `413` | `379` | `5` | `29` | `0` | Enriched under maximum-two-alternatives rule with multiword support; 379 clean, 5 `review_pending`, 29 tracked as excluded. |
| **Validation / PRE-FINAL** | `413` | `379` | `5` | `29` | `0` | Full provenance verified; <=2 translation alternatives verified; 0 blocking errors. |

---

## 2. Active Review Pending Items (`uclouvain`)

### [UCLOUVAIN-001] Record `#2` (`uclouvain_vocab_002`) — `account (for)`
- **Stage:** ENRICHMENT / VALIDATION
- **Observation:** Academic polysemy: causal/explanatory sense (*"explain / be the cause of"*) vs. proportional sense (*"constitute a proportion"*). Requires parenthetical preposition `(for)`.
- **Handling:** Assigned 2 multiword translation alternatives: `объяснять; являться причиной`. Contextual explanation provided. Flagged as `review_pending` for curriculum decision.
- **Verification Command:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "account for"`

### [UCLOUVAIN-002] Record `#206` (`uclouvain_vocab_206`) — `should`
- **Stage:** ENRICHMENT / VALIDATION
- **Observation:** Defective modal auxiliary verb under `233 verbs`. Lacks a Russian infinitive.
- **Handling:** Translated via modal predicatives `следует` (or `должен`); tagged `verb (modal)`. Flagged `review_pending`.
- **Verification Command:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "should"`

### [UCLOUVAIN-003] Record `#252` (`uclouvain_vocab_252`) — `certain`
- **Stage:** ENRICHMENT / VALIDATION
- **Observation:** Academic polysemy: attributive *"particular/specific"* (`определённый`) vs. predicative *"sure/confident"* (`уверенный`).
- **Handling:** Assigned both valid alternatives: `определённый; уверенный`. Flagged `review_pending`.
- **Verification Command:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "certain"`

### [UCLOUVAIN-004] Record `#347` (`uclouvain_vocab_347`) — `present`
- **Stage:** ENRICHMENT / VALIDATION
- **Observation:** Cross-section homograph (`#167` verb vs. `#347` adjective). As adjective, has senses *"current"* (`настоящий`) and *"in attendance"* (`присутствующий`).
- **Handling:** Assigned both valid alternatives: `настоящий; присутствующий`. Flagged `review_pending`.
- **Verification Command:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "present"`

### [UCLOUVAIN-005] Record `#402` (`uclouvain_vocab_402`) — `unlike`
- **Stage:** ENRICHMENT / VALIDATION
- **Observation:** Predicative adjective sense *"different from"* (`непохожий`). Prepositional usage translates as multi-word phrase `в отличие от`.
- **Handling:** Assigned `непохожий` with note regarding prepositional distinction. Flagged `review_pending`.
- **Verification Command:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "unlike"`
