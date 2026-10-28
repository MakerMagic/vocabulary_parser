# Vocabulary Source Profiles Registry (`SOURCE_PROFILES.md`)

> **Status:** Active — 1 source profile documented (`justprepy_vocabulary_list_v1`).
> **Rule:** Before writing or modifying any parser for a Vocabulary document family in [`acquisition/local/`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/local), complete a source profile entry below.

---

## Profile 1: `justprepy_wordlist` (`justprepy_vocabulary_list_v1`)

- **Files in `acquisition/local/`:** [`acquisition/local/justprepy_vocabulary_list.txt`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/local/justprepy_vocabulary_list.txt)
- **SHA-256:** `e1b15633f274f58f093a3e1950dd1f368aad83fd54fb67ca9f682344d5628d7e`
- **Document Role:** Sectioned English academic vocabulary word list (`233 verbs` + `180 adjectives` = `413` total entries).
- **Text & Encoding Observations:**
  - Native UTF-8 plain text (4 lines total, ASCII character set).
  - Mixed British and American/Oxford spelling conventions present in source (`analyse`, `characterise`, `favour`, `summarise`, `favourable` alongside `emphasize`). Exact supplied spellings must be preserved in `word`.
- **Layout & Entry Boundary Signals:**
  - **Section Header Pattern:** `^(\d+)\s+(verbs|adjectives)$` on odd lines (Line 1: `233 verbs`; Line 3: `180 adjectives`).
  - **Entry Delimiter:** Comma-separated tokens (`, `) on the line immediately following each section header (Line 2 and Line 4).
  - **Declared vs. Actual Counts:** `233 verbs` = `233` items; `180 adjectives` = `180` items; total = `413` items (`411` unique strings).
- **Detected Edge Cases & Control Fixtures:**
  1. **Parenthetical Phrasal Token (`#2 account (for)`):** Contains internal space and parentheses `(for)`. Parser must split only on commas `,`, never on whitespace or parentheses.
  2. **Cross-Section Homographs (`present` at `#167` & `#346`; `separate` at `#203` & `#372`):** Both words appear once under `233 verbs` and once under `180 adjectives`. Record IDs and enrichment must be scoped by section (`verb` vs. `adjective`) so neither is dropped or merged.
  3. **Modal Auxiliary Verbs (`#36 can`, `#149 may`, `#204 should`):** Included under `233 verbs`. Enrichment must note their modal status (and that `should` lacks a Russian infinitive).
  4. **Hyphenated Compound (`#380 so-called`):** Contains internal hyphen `-`; must be preserved intact.
