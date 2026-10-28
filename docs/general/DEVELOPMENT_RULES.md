# Development Rules & Artifact Governance (`DEVELOPMENT_RULES.md`)

## 1. Scope & Preservation Safeguards

This document establishes the engineering rules for modifying code, performing inspections, validating pipeline stages, and maintaining generated artifacts.

1. **Fix Upstream, Never Downstream:** Fix extraction defects in `parsers/`, cleaning/reflow defects in `processors/normalization/`, and matching defects in `processors/matching/`. Never introduce compensatory patches in PRE-FINAL or HTML rendering.
2. **Preserve Historical Handover Files:** [`PARSING_KNOWLEDGE_TRANSFER.md`](file:///c:/Users/user/Desktop/vocabulary_parser/PARSING_KNOWLEDGE_TRANSFER.md) and [`DOCUMENTATION_ARCHITECTURE_HANDOVER.md`](file:///c:/Users/user/Desktop/vocabulary_parser/DOCUMENTATION_ARCHITECTURE_HANDOVER.md) are permanent historical records. Never modify, delete, or rewrite them.
3. **No Unaudited Manual Edits:** Never edit canonical JSON files in `data/` by hand. Any manual correction must follow the manual overlay contract in [`docs/PROVENANCE_AND_CONTRACTS.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/PROVENANCE_AND_CONTRACTS.md).

---

## 2. Canonical-Input Inspection Rules

1. **Inspect Canonical JSON First:** Stored JSON records in `data/` are the authoritative ground truth (Codex Section 13.2). Inspect JSON fields and referenced assets before generating or evaluating HTML views.
2. **Previews Are Disposable Views:** Diagnostic HTML or Markdown previews in `inspections/` are transient rendering views over stored records. Fixing a preview's CSS or template does not fix the stored dataset, and old HTML files embed old styles.
3. **Targeted Inspection Only:** Generate previews only for targeted single records or small diagnostic samples (`sample <= 5`). Do not generate mass static catalogs of the entire dataset.

---

## 3. Required Validation & Testing Discipline

Before any code modification is merged or declared complete:

1. **Source Preservation & Reconstruction Tests:**
   - Verify that every extracted entry can be reconstructed byte-for-byte from recorded source string slices in `data/raw/`.
2. **Positive & Negative Regression Controls:**
   - Every bug fix must include a test asserting the repair on the affected record **and** negative controls proving that valid sibling structures (e.g., proper noun wraps, list markers, multi-sense numbering, already-correct asset hashes) were not broken.
3. **Neighboring-Entry Controls ($N \pm 1$):**
   - Boundary repairs must explicitly assert that adjacent entries remain complete and untruncated.
4. **No Hardcoded Record IDs in Production Logic:**
   - Production parser/cleaner rules must describe observable structural patterns (margins, typography, punctuation, geometry), never `if id == ...`.

---

## 4. Generated Stage Artifact Responsibilities

Every executable pipeline stage must satisfy the stage-artifact contract from [`PARSING_KNOWLEDGE_TRANSFER.md`](file:///c:/Users/user/Desktop/vocabulary_parser/PARSING_KNOWLEDGE_TRANSFER.md) (Section 13.3):

1. **Mandatory Artifact Pair:**
   - Each executed stage must generate a `<STAGE>_BACKTESTING.md` and `<STAGE>_ISSUES.md` pair inside [`qa/`](file:///c:/Users/user/Desktop/vocabulary_parser/qa).
2. **Derived from Structured JSON:**
   - Stage reports must be deterministically generated from the stage's `validation.json` in `data/`. Never manually write or update numbers in Markdown reports.
3. **Zero-Issue Reporting:**
   - When a stage executes with zero defects, `<STAGE>_ISSUES.md` must still be emitted explicitly stating `0 active issues`. The absence of an issues file is ambiguous and prohibited.
4. **Disjoint Partitioning:**
   - Never sum overlapping issue tags as total rejected records. Always report `excluded_total` alongside a disjoint primary-reason partition.

---

## 5. Safe Change Workflow

When implementing or modifying a pipeline capability:

1. **Inspect:** Profile the incoming source layout in [`inspections/SOURCE_PROFILES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/inspections/SOURCE_PROFILES.md).
2. **Write Focused Tests:** Add failing unit/regression tests in `tests/` covering positive examples, adjacent entries, and negative controls.
3. **Implement in Responsible Stage:** Implement the fix in the earliest responsible stage module.
4. **Execute & Validate:** Run the stage processor; verify deterministic JSON outputs in `data/`.
5. **Generate QA Artifacts:** Regenerate the stage's `<STAGE>_BACKTESTING.md` and `<STAGE>_ISSUES.md` in `qa/`.
6. **Log Defects / Resolutions:** If resolving a recurring defect, document root cause and test links in [`qa/ISSUE_LOG.md`](file:///c:/Users/user/Desktop/vocabulary_parser/qa/ISSUE_LOG.md).
7. **Update Operational State:** Record completion in [`docs/general/CURRENT_WORK.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/CURRENT_WORK.md).
