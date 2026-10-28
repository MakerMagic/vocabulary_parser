# Development Rules & Artifact Governance (`DEVELOPMENT_RULES.md`)

## 1. Absolute Stage-Execution Rule

> [!IMPORTANT]
> **Agents must NEVER execute a processing stage without explicit user authorization.**
> 
> - A request for Stage $X$ authorizes Stage $X$ **ONLY**.
> - Do not automatically proceed to Stage $X+1$.
> - After completing the authorized stage: 1) Save outputs, 2) Validate stage results, 3) Document issues, 4) Document backtesting, 5) Update `CURRENT_WORK.md`, 6) **STOP**.

---

## 2. Documentation Governance & Prohibition on Redundant README Files

- **Do NOT create new `README.md` files.**
- **Do NOT create README files merely to explain a folder.**
- All architectural and operational instructions must be placed in purpose-specific Markdown files:
  - Global docs in [`docs/general/`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general) (`PROJECT_CONTEXT.md`, `ARCHITECTURE.md`, `DATA_SCHEMA.md`, `PROCESSING_RULES.md`, `DEVELOPMENT_RULES.md`, `CODEX_SKILLS_USAGE.md`, `CURRENT_WORK.md`).
  - Source-specific docs in [`docs/sources/<source_id>/`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/sources) (`SOURCE_INSPECTION.md`, `PROCESSING_NOTES.md`, `STAGE_ISSUES.md`).
- Never duplicate documentation across multiple locations.

---

## 3. Scope & Preservation Safeguards

1. **Fix Upstream, Never Downstream:** Fix extraction defects in `parsers/`, cleaning/reflow defects in `processors/normalization/`, and matching defects in `processors/matching/`. Never introduce compensatory patches in PRE-FINAL or HTML rendering.
2. **Preserve Historical Handover Files:** `PARSING_KNOWLEDGE_TRANSFER.md` and `DOCUMENTATION_ARCHITECTURE_HANDOVER.md` are permanent historical records. Never modify, delete, or rewrite them.
3. **No Unaudited Manual Edits:** Never edit canonical JSON files in `data/` by hand. Any manual correction must follow the manual overlay contract in [`docs/PROVENANCE_AND_CONTRACTS.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/PROVENANCE_AND_CONTRACTS.md).

---

## 4. Mandatory Test Categories (When Tests Are Written)

Every parser and normalization stage must include tests across these four dimensions:

1. **Source Preservation & Reconstruction Tests:**
   - Reconstruct every extracted entry/excerpt from its recorded `data/raw/` source string slices (`start`, `end`).
   - Verify that CLEAN retains an unchanged `raw_record` snapshot, `source_sha256`, and non-whitespace token ledger.
2. **Structural Completeness & Neighboring-Entry Ownership Tests ($N \pm 1$ Rule):**
   - Assert unique deterministic IDs, ordered sequences without shifted gaps, and complete entry text.
   - When testing a boundary repair on Entry $N$, assert the exact content of **both Entry $N$ and adjacent Entry $N-1$ / $N+1$** to prevent silent text leakage or truncation.
3. **Positive and Negative Regression Controls:**
   - Pair every structural repair with **untouched negative controls** (e.g., verifying that multiword Russian translation alternatives pass, while entries with >2 translation alternatives fail; verifying that `difficulty != null` fails).
4. **Stage Artifact & Hash-Binding Tests:**
   - Verify that stage execution deterministically produces matching validation JSON and `<STAGE>_BACKTESTING.md` / `<STAGE>_ISSUES.md` pairs in [`qa/`](file:///c:/Users/user/Desktop/vocabulary_parser/qa) (including zero-issue runs).
   - Verify that downstream consumers reject stale upstream file/content hashes unless an authorized rebinding proof passes.

---

## 5. Generated Stage Artifact Responsibilities (`qa/`)

Every executed pipeline stage must satisfy the stage-artifact contract from `PARSING_KNOWLEDGE_TRANSFER.md`:

1. **Mandatory Artifact Pair:**
   - Each executed stage must generate a `<STAGE>_BACKTESTING.md` and `<STAGE>_ISSUES.md` pair inside [`qa/`](file:///c:/Users/user/Desktop/vocabulary_parser/qa) (or `qa/sources/<source_id>/` for source-specific runs).
2. **Derived from Structured JSON:**
   - Stage reports must be deterministically generated from the stage's `validation.json` in `data/`. Never manually write or update numbers in Markdown reports.
3. **Zero-Issue Reporting:**
   - When a stage executes with zero defects, `<STAGE>_ISSUES.md` must still be emitted explicitly stating `0 active issues`. The absence of an issues file is ambiguous and prohibited.
4. **Disjoint Partitioning:**
   - Never sum overlapping issue tags as total rejected records. Always report `excluded_total` alongside a disjoint primary-reason partition.
