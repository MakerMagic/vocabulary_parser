# Quality Assurance & Issue Tracking (`qa/`)

## 1. Intended Responsibility

The `qa/` directory owns **stage readiness reporting, structured defect tracking, and verification audits** across the Vocabulary parsing pipeline.

It directly enforces Lessons #12, #13, #16, and Section 10.12 / 13.3 of [`PARSING_KNOWLEDGE_TRANSFER.md`](file:///c:/Users/user/Desktop/vocabulary_parser/PARSING_KNOWLEDGE_TRANSFER.md):
- **"No detected issue" in one stage is not a global fidelity certificate** for later stages.
- **Stage-specific `<STAGE>_BACKTESTING.md` and `<STAGE>_ISSUES.md` pairs** must be generated from authoritative validation JSON for every executed stage, even when the issue count is zero.
- **Exclusion policy is not parser quality:** Intentional skips, unavailable source material, unresolved parser defects, and pending semantic reviews must be partitioned cleanly.

---

## 2. What Belongs Here

1. **[`ISSUE_LOG.md`](file:///c:/Users/user/Desktop/vocabulary_parser/qa/ISSUE_LOG.md):** Central engineering ledger for investigating recurring parsing/normalization defects, recording their root cause, owning pipeline stage, rejected shortcuts, and regression test references.
2. **Generated Stage Artifact Pairs (once pipeline stages execute):**
   - `<STAGE>_BACKTESTING.md` (e.g., `RAW_BACKTESTING.md`, `CLEAN_BACKTESTING.md`) — Population counts, eligibility rules, primary-reason exclusion partitions, and verification summary derived directly from canonical JSON.
   - `<STAGE>_ISSUES.md` (e.g., `RAW_ISSUES.md`, `CLEAN_ISSUES.md`) — Itemized active findings with `source`, `record_id`, `field`, `issue_code`, and `state`. Must still be emitted explicitly stating zero active issues when a stage has `0` findings.
3. **Refresh & Semantic Review Audits (when applicable later):** Documented audits for hash rebindings or semantic reviews of classifications/explanations.

---

## 3. Reporting Invariants (From Codex Section 3 & 10.12)

Whenever stage reports are generated in `qa/`, they must obey these rules:

- **Never sum overlapping issue tags as unique rejected items:** Report `excluded_total` and a disjoint **primary-reason partition** alongside `reason_counts_overlapping`.
- **Name the exact population and readiness predicate:** State clearly whether a count refers to RAW extracted items, CLEAN admitted items, or PRE-FINAL eligible items.
- **Derive Markdown reports from canonical JSON:** Never hand-edit stage counts in `<STAGE>_BACKTESTING.md` or `<STAGE>_ISSUES.md` to make progress look better.

---

## 4. What Must NOT Be Stored Here

- **No canonical dataset JSON or extracted assets:** Those belong in [`data/`](file:///c:/Users/user/Desktop/vocabulary_parser/data).
- **No pre-parsing document layout profiles:** Initial source family discovery notes belong in [`inspections/SOURCE_PROFILES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/inspections/SOURCE_PROFILES.md).
- **No disposable HTML previews:** Selected visual/HTML previews belong in [`inspections/`](file:///c:/Users/user/Desktop/vocabulary_parser/inspections).
- **No executable test scripts:** Automated pytest suites belong in [`tests/`](file:///c:/Users/user/Desktop/vocabulary_parser/tests).

---

## 5. Relationship to Other Parts of the Project

1. **Summarizes [`data/`](file:///c:/Users/user/Desktop/vocabulary_parser/data) Validation State:** Every `<STAGE>_BACKTESTING.md` and `<STAGE>_ISSUES.md` pair in `qa/` is a deterministic projection of the stage's structured validation JSON in `data/`.
2. **Drives Regression Coverage in [`tests/`](file:///c:/Users/user/Desktop/vocabulary_parser/tests):** Every defect logged and resolved in [`qa/ISSUE_LOG.md`](file:///c:/Users/user/Desktop/vocabulary_parser/qa/ISSUE_LOG.md) must graduate to a positive and negative regression test in [`tests/`](file:///c:/Users/user/Desktop/vocabulary_parser/tests).
3. **Prevents Premature Stage Promotion:** Records flagged with active issues in `qa/<STAGE>_ISSUES.md` are blocked from downstream admission until fixed in their **earliest responsible stage** (Codex Lesson #10).
