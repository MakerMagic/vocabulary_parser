# QA Issue & Root-Cause Log (`qa/ISSUE_LOG.md`)

> **Status:** Active (`0` open defects — pipeline extraction has not started yet).
> **Purpose:** Track non-trivial parsing, normalization, matching, and validation defects using the root-cause discipline from Section 10 of [`PARSING_KNOWLEDGE_TRANSFER.md`](file:///c:/Users/user/Desktop/vocabulary_parser/PARSING_KNOWLEDGE_TRANSFER.md).

---

## Defect Documentation Rules

1. **Fix the Earliest Responsible Stage:**
   - Entry boundary / glyph / stream-order / visual ownership defects -> **RAW (`parsers/`)**.
   - Line-wrap reflow / headword-definition-example separation / punctuation cleanup -> **CLEAN (`processors/normalization/`)**.
   - Key/explanation association & edition mismatches -> **Matching (`processors/matching/`)**.
   - Never hide an upstream extraction error inside CLEAN, PRE-FINAL, or HTML rendering.
2. **No Hardcoded Record IDs in Production Code:**
   - Specific record IDs belong in [`tests/`](file:///c:/Users/user/Desktop/vocabulary_parser/tests) regression fixtures or provenance-tracked manual overrides, never as `if record_id == ...` branches in parser/cleaner logic.
3. **Verify Neighboring Entries:**
   - Whenever a boundary or visual-ownership defect is fixed on Entry $N$, explicitly inspect and test Entry $N-1$ and Entry $N+1$ to verify content was transferred rather than silently dropped (Codex Section 10.1).

---

## Active & Resolved Defect Registry

*(Record defects below as pipeline stages are built and tested.)*

### Template: `[ISSUE-001] Short Descriptive Title`

- **Status:** `Open` | `In Progress` | `Resolved` | `Blocked (Source Limitation)`
- **Affected Source / Stage:** *(e.g., `source_profile_x` / `RAW`)*
- **Representative Record IDs:** *(e.g., `vocab_source_x_unit_1_q2` and adjacent `q3`)*
- **Symptom:** *(What looked wrong in the extracted JSON or validation output)*
- **Root Cause:** *(Underlying layout, stream-order, encoding, or state-handling mechanism)*
- **Responsible Stage:** *(Which stage owns the fix and why)*
- **Working Correction:** *(Structural rule implemented)*
- **Rejected Shortcut:** *(What brittle workaround was avoided, e.g., regex trimming or ID-branching)*
- **Regression Test Reference:** *(Path and test function in `tests/` covering positive + untouched negative controls)*
