# Verification & Regression Suite (`tests/`)

> **Status:** Initialized foundation only. **No executable tests exist yet** because no parser or normalization modules have been implemented.

## 1. Intended Responsibility

The `tests/` directory houses the **automated verification and regression suite** (`pytest`) for the Vocabulary parsing pipeline.

As established in [`PARSING_KNOWLEDGE_TRANSFER.md`](file:///c:/Users/user/Desktop/vocabulary_parser/PARSING_KNOWLEDGE_TRANSFER.md) (Section 11 & Section 14, #1 & #5):
- Entry count and schema validity are never sufficient proof of correct extraction.
- Source-preservation and ownership assertions must be introduced **before** scaling the first parser.

---

## 2. Mandatory Test Categories (When Code Is Implemented)

Every parser and normalization stage must include tests across these four dimensions:

1. **Source Preservation & Reconstruction Tests:**
   - Reconstruct every extracted entry/excerpt from its recorded `data/raw/` page-string slices (`start`, `end`).
   - Verify that original source span offsets remain intact even when a decoded readable projection has a different character length.
   - Verify that CLEAN retains an unchanged `raw_record` snapshot, `source_sha256`, and non-whitespace token ledger.
2. **Structural Completeness & Neighboring-Entry Ownership Tests:**
   - Assert unique deterministic IDs, ordered entry/option sequences without shifted gaps, and complete final-entry/final-option text.
   - When testing a boundary repair on Entry $N$, assert the exact content of **both Entry $N$ and adjacent Entry $N-1$ / $N+1$** to prevent silent text leakage or truncation.
3. **Positive and Negative Regression Controls:**
   - Pair every structural repair (e.g., joining a wrapped proper noun across lines, splitting a definition from an example sentence, grouping a visual) with **untouched negative controls** (e.g., a real paragraph break, a list item, an unaligned cross-page continuation, or an already-correct asset hash that must not change).
4. **Stage Artifact & Hash-Binding Tests:**
   - Verify that stage execution deterministically produces matching validation JSON and `<STAGE>_BACKTESTING.md` / `<STAGE>_ISSUES.md` pairs in [`qa/`](file:///c:/Users/user/Desktop/vocabulary_parser/qa) (including zero-issue runs).
   - Verify that downstream consumers reject stale upstream file/content hashes unless an authorized rebinding proof passes.

---

## 3. What Belongs Here

- `test_<stage_or_profile>_*.py` modules executable via `python -m pytest`.
- Small, self-contained synthetic fixtures isolating tricky layout/boundary edge cases alongside real-source regression assertions.

---

## 4. What Must NOT Be Stored Here

- **No production parser or pipeline logic:** Reusable validation helpers that run during pipeline execution belong in `parsers/` or `processors/`, not only in `tests/`.
- **No canonical pipeline outputs:** `tests/` must write temporary outputs to pytest `tmp_path` fixtures, never overwriting [`data/`](file:///c:/Users/user/Desktop/vocabulary_parser/data) or [`qa/`](file:///c:/Users/user/Desktop/vocabulary_parser/qa).
- **No original primary document dumps:** Real-source tests should read from [`acquisition/local/`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/local) (read-only) and skip cleanly with an explicit reason if local files are not yet present.

---

## 5. Relationship to Other Parts of the Project

1. **Guards [`data/raw/`](file:///c:/Users/user/Desktop/vocabulary_parser/data/raw) and Downstream Stages:** Blocks regressions in segmentation, text reflow, asset cropping, and hash integrity.
2. **Linked from [`qa/ISSUE_LOG.md`](file:///c:/Users/user/Desktop/vocabulary_parser/qa/ISSUE_LOG.md):** Every resolved issue in `qa/ISSUE_LOG.md` cites its corresponding test module in `tests/`.
