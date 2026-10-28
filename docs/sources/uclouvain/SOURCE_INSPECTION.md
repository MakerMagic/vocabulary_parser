# UCLouvain Vocabulary Source Inspection (`SOURCE_INSPECTION.md`)

> **Source Identifier:** `uclouvain`  
> **Source Document:** [`acquisition/sources/uclouvain/uclouvain_vocabulary_list.txt`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/sources/uclouvain/uclouvain_vocabulary_list.txt)  
> **SHA-256 Digest:** `e1b15633f274f58f093a3e1950dd1f368aad83fd54fb67ca9f682344d5628d7e`  
> **Origin:** Université catholique de Louvain (CECL / Louvain EAP academic vocabulary selection)  
> **Scope:** Two sectioned lists containing `233 verbs` and `180 adjectives` = `413` total items (`411` unique strings).

---

## 1. Document Structure & Boundary Signals

- **Format:** Native UTF-8 plain text with CRLF/LF line endings.
- **Section Headers:**
  - Line 1: `233 verbs` (Section 1)
  - Line 3: `180 adjectives` (Section 2)
  - Header Regex: `^(\d+)\s+(verbs|adjectives)$`
- **Entry Delimiters:** Comma-separated tokens (`, `) on the line immediately following each header (Line 2 and Line 4).
- **Count Invariants:**
  - Section 1 (`verbs`): Header declares `233`; exactly `233` items extracted.
  - Section 2 (`adjectives`): Header declares `180`; exactly `180` items extracted.
  - Section Duplicates: `0` duplicate words within Section 1; `0` duplicate words within Section 2.

---

## 2. Observed Lexical Characteristics & Edge Cases

### A. Parenthetical Phrasal Token (`#2 account (for)`)
- **Raw token:** `account (for)` at Section 1 index 2.
- **Characteristics:** Contains an internal space and a parenthetical preposition `(for)`.
- **Parsing Invariant:** Parsers must split on commas only, never on whitespace or parentheses. Base headword is `account`; particle is `for`.

### B. Cross-Section Homographs (`present` and `separate`)
- `present`: Appears at record `#167` (`233 verbs`) and record `#346` (`180 adjectives`).
- `separate`: Appears at record `#203` (`233 verbs`) and record `#372` (`180 adjectives`).
- **Parsing Invariant:** Record identity must be scoped by source section (`verb` vs. `adjective`). Neither instance may be collapsed or deduplicated.

### C. Modal Auxiliary Verbs in Verbs Section (`#36 can`, `#149 may`, `#204 should`)
- Listed under `233 verbs`.
- `should` is morphologically defective and lacks a direct Russian infinitive (translated predicatively as `следует` / `должен`).

### D. Hyphenated Compound Token (`#380 so-called`)
- Listed under `180 adjectives`. Contains an internal hyphen `-`. Must be preserved intact.

### E. Mixed British / American Orthography
- British spellings in source: `#16 analyse`, `#38 characterise`, `#113 favour`, `#213 summarise`, `#282 favourable`.
- American `-ize` spelling in source: `#90 emphasize`.
- **Preservation Invariant:** Exact source spelling must be preserved verbatim in `word`.
