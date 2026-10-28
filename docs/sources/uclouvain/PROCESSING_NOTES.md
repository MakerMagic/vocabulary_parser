# UCLouvain Processing Notes & Stage Decisions (`PROCESSING_NOTES.md`)

> **Source Identifier:** `uclouvain`  
> **Source Document:** [`acquisition/sources/uclouvain/uclouvain_vocabulary_list.txt`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/sources/uclouvain/uclouvain_vocabulary_list.txt)  
> **Status:** Active Reference for `uclouvain` Stage Implementation

---

## 1. Stage-Specific Processing Rules for `uclouvain`

### Acquisition
- Maintain the raw source file in [`acquisition/sources/uclouvain/uclouvain_vocabulary_list.txt`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/sources/uclouvain/uclouvain_vocabulary_list.txt).
- Lock SHA-256 (`e1b15633f274f58f093a3e1950dd1f368aad83fd54fb67ca9f682344d5628d7e`).

### RAW Extraction
- Read strictly from `acquisition/sources/uclouvain/`.
- Segment by section headers (`233 verbs`, `180 adjectives`) and split entries strictly on `, ` (comma + space).
- Record exact character offsets: `file_char_start`, `file_char_end`, `line_number`, `line_char_start`, `line_char_end`.
- Reconstruct 100% of tokens byte-for-byte from raw source slices.
- Do not strip parentheses from `account (for)` or hyphens from `so-called`.

### Cleaning & Normalization
- Normalize whitespace without mutating non-whitespace tokens (100% token-ledger conservation).
- Non-destructively separate `account (for)` into `headword_lemma="account"` and `parenthetical_modifier="for"`, keeping `word="account (for)"`.
- Keep British and American spellings verbatim in `word`, annotating `spelling_convention` in metadata.
- Reserve `"difficulty": null` across all records.

### Vocabulary Enrichment (When Authorized)
- **Part of Speech:** Assign `verb`, `verb (phrasal)`, `verb (modal)`, or `adjective` based on section and lexical analysis.
- **Russian Translation Rule (CORRECTED):**
  - **Maximum TWO Russian translation alternatives per entry.**
  - **Each translation alternative may consist of multiple Russian words.**
  - Examples:
    - `take off` -> `1. взлетать`, `2. снимать одежду` (valid: 2 alternatives; alternative 2 has 2 words).
    - `unlike` -> `непохожий; в отличие от` (valid: 2 alternatives; alternative 2 has 3 words).
  - Do NOT truncate multiword phrases.
  - Do NOT invent a second translation if one accurate translation suffices.
- **English Explanation:**
  - Clear, non-circular explanation (`>= 15` characters, headword lemma excluded).

---

## 2. Distinction from Shared Architecture

- Shared pipeline processors (`processors/provenance.py`, `processors/stage_artifacts.py`) provide generic hashing, deterministic JSON serialization, and QA report generation.
- All rules above (comma splitting, 2 sections, 233+180 counts, `account (for)` parsing) are **source-specific to `uclouvain`** and must not be imposed on future sources with different layouts or structures.
