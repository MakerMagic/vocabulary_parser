# UCLouvain Stage Issues & Backtesting Registry (`STAGE_ISSUES.md`)

> **Source Identifier:** `uclouvain`  
> **Source Document:** [`acquisition/sources/uclouvain/uclouvain_vocabulary_list.txt`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/sources/uclouvain/uclouvain_vocabulary_list.txt)  
> **Authority:** Tracks source-specific issues across `uclouvain` pipeline stages.

---

## 1. Stage Findings Summary for `uclouvain`

| Stage | Input Records | Validated | Review Pending | Blocking Errors | Core Findings |
|---|---|---|---|---|---|
| **Acquisition** | `1` file | `1` | `0` | `0` | SHA-256 locked (`e1b15633...`); UTF-8 verified. |
| **Inspection** | `413` | `413` | `5` notices | `0` | 2 sections (233+180=413); 1 parenthetical (`account (for)`), 2 homograph pairs (`present`, `separate`), 3 modals (`can`, `may`, `should`), 1 hyphenated (`so-called`). |
| **RAW Extraction** | `413` | `413` | `5` notices | `0` | 100% exact character/line span reconstruction; $N \pm 1$ neighbor boundaries verified. |
| **Cleaning** | `413` | `413` | `1` notice | `0` | 100% token-ledger match; `#2 account (for)` lemma/modifier separated; 6 UK/US spellings preserved; `"difficulty": null` set. |
| **Enrichment** | `413` | `408` | `5` | `0` | 408 unambiguous records; 5 records flagged `review_pending`. *Note: Previously generated under the old <=2-word constraint; pending update to the maximum-two-alternatives rule upon authorization.* |
| **Validation / PRE-FINAL** | `413` | `408` | `5` | `0` | Provenance verified; 0 blocking errors. |

---

## 2. Active Review Pending Items (`uclouvain`)

### [UCLOUVAIN-001] Record `#2` (`justprepy_vocab_002`) — `account (for)`
- **Stage:** CLEAN / ENRICHMENT
- **Observation:** Parenthetical phrasal verb. Has two common academic senses: *"explain"* (`объяснять`) and *"constitute a proportion"* (`составлять`).
- **Handling:** Retain verbatim `account (for)`; primary translation `объяснять` assigned; flagged `review_pending` for curriculum sense sign-off.

### [UCLOUVAIN-002] Record `#204` (`justprepy_vocab_204`) — `should`
- **Stage:** ENRICHMENT / VALIDATION
- **Observation:** Defective modal auxiliary verb under `233 verbs`. Lacks a Russian infinitive.
- **Handling:** Translated via modal predicative `следует` (alternative: `должен`); tagged `verb (modal)`. Flagged `review_pending`.

### [UCLOUVAIN-003] Record `#252` (`justprepy_vocab_252`) — `certain`
- **Stage:** ENRICHMENT / VALIDATION
- **Observation:** Academic polysemy: attributive *"particular/specific"* (`определённый`) vs. predicative *"sure/confident"* (`уверенный`).
- **Handling:** Assigned primary sense `определённый`; flagged `review_pending`.

### [UCLOUVAIN-004] Record `#346` (`justprepy_vocab_346`) — `present`
- **Stage:** ENRICHMENT / VALIDATION
- **Observation:** Cross-section homograph (`#167` verb vs. `#346` adjective). As adjective, has senses *"current"* (`настоящий`) and *"in attendance"* (`присутствующий`).
- **Handling:** Assigned `настоящий`; flagged `review_pending`.

### [UCLOUVAIN-005] Record `#402` (`justprepy_vocab_402`) — `unlike`
- **Stage:** ENRICHMENT / VALIDATION
- **Observation:** Adjective sense *"different from"* (`непохожий`). Prepositional usage translates as multi-word phrase `в отличие от`. Under the corrected translation rule, multi-word alternatives like `в отличие от` are fully valid.
- **Handling:** Assigned `непохожий`; flagged `review_pending` to add `в отличие от` as second translation alternative when Enrichment is re-authorized.
