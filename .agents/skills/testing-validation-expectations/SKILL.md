---
name: testing-validation-expectations
description: Defines minimum testing, source-preservation, and stage-artifact validation expectations for the Vocabulary parsing pipeline. Use when adding or modifying pytest suites, parser/cleaner validators, regression controls, or QA stage artifacts.
---

# Testing and Validation Expectations Skill

## Purpose

Use this skill when creating or modifying tests, validators, and QA stage checks in the Vocabulary parsing project.

The goal is to prevent silent extraction or normalization defects and keep every pipeline stage independently verifiable.

## Main Principles

1. **Entry count and schema validity are never sufficient proof of correct extraction.**
2. **Every stage must be testable independently** without mutating canonical data in `data/` or `qa/` (use `tmp_path` in tests).
3. **Every bug fix requires positive and negative regression controls** plus adjacent-entry ($N \pm 1$) verification.

## Mandatory Test Priorities (`tests/`)

When parser or normalization behavior is created or changed, `pytest` suites must verify:

1. **Source Preservation & Span Reconstruction:**
   - Reconstruct every extracted entry/excerpt byte-for-byte from its recorded `data/raw/` page-string slices (`start`, `end`).
   - Verify that original span offsets remain valid even when `readable_text` differs in length from `raw_text` (e.g., after font/IPA decoding).
   - Verify that CLEAN preserves an unchanged `raw_record` snapshot, `source_sha256`, and non-whitespace token ledger.
2. **Neighboring-Entry Ownership ($N \pm 1$ Rule):**
   - When repairing a boundary or visual ownership defect on Entry $N$, assert the exact content of **both Entry $N$ and adjacent Entry $N-1$ / $N+1$** so text or visuals are transferred accurately rather than dropped or duplicated.
3. **Positive and Untouched Negative Controls:**
   - Pair every structural repair (e.g., joining a wrapped proper noun, separating a headword from a definition, cropping an image asset) with negative controls (e.g., genuine paragraph breaks, numbered definition senses, unaligned cross-page text, and already-correct asset SHA-256 hashes that must remain unchanged).
4. **Stage Artifact & Hash-Binding Validation:**
   - Verify that stage runs deterministically generate matching validation JSON and `<STAGE>_BACKTESTING.md` / `<STAGE>_ISSUES.md` pairs in `qa/` (including zero-issue stages).
   - Verify that downstream stages reject stale upstream file/content hashes unless an explicit rebinding proof passes.

## Quality Tools

Use the installed environment tools:
- `pytest` (`.venv\Scripts\python.exe -m pytest`) for unit, source-preservation, and regression tests.
- `ruff` (`.venv\Scripts\python.exe -m ruff check`) for linting and static verification of changed Python modules.

## Forbidden Patterns

Do not:
- treat skipped real-source tests (when a local PDF is absent) as passing source-regression proof;
- validate only final or cleaned output while ignoring `data/raw/` span reconstruction;
- overwrite canonical `data/` or `qa/` files during test execution;
- hardcode production branches by record ID (`if record_id == ...`) instead of placing IDs in test fixtures.

## When to Read Original Docs

Read original docs when:
- changing development or QA artifact governance (`docs/general/DEVELOPMENT_RULES.md`, `qa/README.md`);
- changing required schema invariants (`docs/general/DATA_SCHEMA.md`, `docs/PROVENANCE_AND_CONTRACTS.md`);
- reviewing the testing overview (`tests/README.md`).
