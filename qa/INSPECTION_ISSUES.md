# INSPECTION Stage Issues Report (`INSPECTION_ISSUES.md`)

> **Generated deterministically from:** `data/inspection/validation.json`

## 1. Overview & Counts

- **Stage:** `INSPECTION`
- **Records Entered:** `413`
- **Successfully Processed:** `413`
- **Records with Review Notices (`review_pending`):** `5`
- **Records with Blocking Errors (`error`):** `0`
- **Total Findings:** `9` across `9` unique record(s)

## 2. Findings by Issue Code

| Issue Code | Severity | Occurrences |
|---|---|---|
| `parenthetical_phrasal_token` | `review_notice` | `1` |
| `cross_section_homograph` | `review_notice` | `4` |
| `modal_auxiliary_in_verbs` | `info_notice` | `3` |
| `hyphenated_compound_token` | `info_notice` | `1` |

## 3. Itemized Findings & Reproduction

### [INSPECTION-001] Record `#2` (`justprepy_vocab_002`) — `account (for)`

- **Issue Code:** `parenthetical_phrasal_token`
- **Severity / State:** `review_notice`
- **Responsible Stage:** `RAW / CLEAN / ENRICHMENT`
- **Affected Field:** `word`
- **Description:** Token 'account (for)' contains parenthetical preposition '(for)', unlike single-word lemmas.
- **Probable / Verified Root Cause:** Source list includes required preposition in parentheses to specify the phrasal verb sense.
- **Corrective Action Required:** Preserve exact string 'account (for)' in RAW and CLEAN 'word' field; record base headword 'account' and particle '(for)' in normalization metadata; enrich as phrasal/prepositional verb.
- **How to Reproduce & Verify:** `.\.venv\Scripts\python.exe -m processors.inspection`

### [INSPECTION-002] Record `#167` (`justprepy_vocab_167`) — `present`

- **Issue Code:** `cross_section_homograph`
- **Severity / State:** `review_notice`
- **Responsible Stage:** `RAW / ENRICHMENT`
- **Affected Field:** `word`
- **Description:** Word 'present' appears in multiple sections: #167 (verb) and #347 (adjective).
- **Probable / Verified Root Cause:** English homograph 'present' is a core academic verb as well as another part of speech.
- **Corrective Action Required:** Scope record identity and enrichment strictly by section header (verb); do not collapse with record #347.
- **How to Reproduce & Verify:** `.\.venv\Scripts\python.exe -m processors.inspection`

### [INSPECTION-003] Record `#347` (`justprepy_vocab_347`) — `present`

- **Issue Code:** `cross_section_homograph`
- **Severity / State:** `review_notice`
- **Responsible Stage:** `RAW / ENRICHMENT`
- **Affected Field:** `word`
- **Description:** Word 'present' appears in multiple sections: #167 (verb) and #347 (adjective).
- **Probable / Verified Root Cause:** English homograph 'present' is a core academic adjective as well as another part of speech.
- **Corrective Action Required:** Scope record identity and enrichment strictly by section header (adjective); do not collapse with record #167.
- **How to Reproduce & Verify:** `.\.venv\Scripts\python.exe -m processors.inspection`

### [INSPECTION-004] Record `#205` (`justprepy_vocab_205`) — `separate`

- **Issue Code:** `cross_section_homograph`
- **Severity / State:** `review_notice`
- **Responsible Stage:** `RAW / ENRICHMENT`
- **Affected Field:** `word`
- **Description:** Word 'separate' appears in multiple sections: #205 (verb) and #373 (adjective).
- **Probable / Verified Root Cause:** English homograph 'separate' is a core academic verb as well as another part of speech.
- **Corrective Action Required:** Scope record identity and enrichment strictly by section header (verb); do not collapse with record #373.
- **How to Reproduce & Verify:** `.\.venv\Scripts\python.exe -m processors.inspection`

### [INSPECTION-005] Record `#373` (`justprepy_vocab_373`) — `separate`

- **Issue Code:** `cross_section_homograph`
- **Severity / State:** `review_notice`
- **Responsible Stage:** `RAW / ENRICHMENT`
- **Affected Field:** `word`
- **Description:** Word 'separate' appears in multiple sections: #205 (verb) and #373 (adjective).
- **Probable / Verified Root Cause:** English homograph 'separate' is a core academic adjective as well as another part of speech.
- **Corrective Action Required:** Scope record identity and enrichment strictly by section header (adjective); do not collapse with record #205.
- **How to Reproduce & Verify:** `.\.venv\Scripts\python.exe -m processors.inspection`

### [INSPECTION-006] Record `#36` (`justprepy_vocab_036`) — `can`

- **Issue Code:** `modal_auxiliary_in_verbs`
- **Severity / State:** `info_notice`
- **Responsible Stage:** `ENRICHMENT`
- **Affected Field:** `part_of_speech`
- **Description:** Token 'can' is a modal auxiliary verb included in the '233 verbs' section.
- **Probable / Verified Root Cause:** Source groups modal auxiliaries together with lexical verbs under '233 verbs'.
- **Corrective Action Required:** Preserve under 'verb' section scope; record grammatical subcategory 'verb (modal)' and note defective morphology (especially 'should', which has no Russian infinitive).
- **How to Reproduce & Verify:** `.\.venv\Scripts\python.exe -m processors.inspection`

### [INSPECTION-007] Record `#150` (`justprepy_vocab_150`) — `may`

- **Issue Code:** `modal_auxiliary_in_verbs`
- **Severity / State:** `info_notice`
- **Responsible Stage:** `ENRICHMENT`
- **Affected Field:** `part_of_speech`
- **Description:** Token 'may' is a modal auxiliary verb included in the '233 verbs' section.
- **Probable / Verified Root Cause:** Source groups modal auxiliaries together with lexical verbs under '233 verbs'.
- **Corrective Action Required:** Preserve under 'verb' section scope; record grammatical subcategory 'verb (modal)' and note defective morphology (especially 'should', which has no Russian infinitive).
- **How to Reproduce & Verify:** `.\.venv\Scripts\python.exe -m processors.inspection`

### [INSPECTION-008] Record `#206` (`justprepy_vocab_206`) — `should`

- **Issue Code:** `modal_auxiliary_in_verbs`
- **Severity / State:** `info_notice`
- **Responsible Stage:** `ENRICHMENT`
- **Affected Field:** `part_of_speech`
- **Description:** Token 'should' is a modal auxiliary verb included in the '233 verbs' section.
- **Probable / Verified Root Cause:** Source groups modal auxiliaries together with lexical verbs under '233 verbs'.
- **Corrective Action Required:** Preserve under 'verb' section scope; record grammatical subcategory 'verb (modal)' and note defective morphology (especially 'should', which has no Russian infinitive).
- **How to Reproduce & Verify:** `.\.venv\Scripts\python.exe -m processors.inspection`

### [INSPECTION-009] Record `#380` (`justprepy_vocab_380`) — `so-called`

- **Issue Code:** `hyphenated_compound_token`
- **Severity / State:** `info_notice`
- **Responsible Stage:** `RAW / CLEAN`
- **Affected Field:** `word`
- **Description:** Token 'so-called' is a hyphenated compound adjective.
- **Probable / Verified Root Cause:** Compound adjective 'so-called' requires a hyphen in standard English orthography.
- **Corrective Action Required:** Preserve internal hyphen in RAW and CLEAN; do not split on hyphen.
- **How to Reproduce & Verify:** `.\.venv\Scripts\python.exe -m processors.inspection`
