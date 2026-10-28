---
name: project-architecture-guardrails
description: Preserves the modular stage boundaries of the Vocabulary document-parsing pipeline (Acquisition, Inspection, RAW Extraction, CLEAN Normalization, Matching, Categorization, and PRE-FINAL Assembly). Use when changing folder structures, creating parser/processor modules, or checking stage ownership.
---

# Project Architecture Guardrails Skill

## Purpose

Use this skill to preserve the architecture of the **Vocabulary document-processing pipeline**.

This repository is not a single PDF scraper. It is a modular document-processing system for Vocabulary materials (word lists, glossaries, definitions, usage examples, lexical exercises, and accompanying keys/explanations).

The main architectural rules are:

1. **File acquisition, source inspection, and document parsing are separate concerns.** A parser must not depend on how the input file was obtained.
2. **One parser per source layout profile.** Do not force distinct document layouts into a single universal parser.
3. **Fix the earliest responsible stage.** Never patch RAW segmentation errors in CLEAN or hide data defects in downstream views.

## Canonical Pipeline

The intended pipeline is:

```text
acquisition/local/ (Original source files + SHA-256 provenance)
↓
inspections/SOURCE_PROFILES.md (Pre-parser layout, encoding & boundary profiling)
↓
source-profile parser (parsers/<profile>/)
↓
raw structured data (data/raw/<profile>/)
↓
normalization / cleaning (processors/normalization/ → data/clean/)
↓
matching / merging (optional: only when prompts & keys/explanations are split)
↓
categorization / lexical tagging (optional: CEFR, POS, domain)
↓
PRE-FINAL canonical dataset (data/pre_final/)
```

Each stage must remain independently replaceable and testable.

## Stage Responsibilities

- **`acquisition/` (`acquisition/local/`)**:
  Stores unmodified original Vocabulary source files and records SHA-256 provenance hashes, source family, and document role. Must not parse entries, clean text, match keys, or alter file bytes.
- **`inspections/` (`inspections/SOURCE_PROFILES.md`)**:
  Profiles layout, character encoding (IPA/phonetics, CID font maps, ligatures), reading order vs. stream order, and entry boundary anchors before parser creation; hosts targeted disposable previews. Must never serve as canonical data storage.
- **`parsers/` (created only after source inspection)**:
  Extracts raw structured records from already-available local files in `acquisition/local/`. Grouped by source layout profile (`parsers/<source_profile>/`). Must not download files or perform destructive text normalization.
- **`data/raw/`**:
  Stores immutable RAW extraction outputs: unmodified page/source text, exact character/byte slice spans (`start`, `end`), readable decoded projections (when proven), bounding boxes, extracted visual assets, and structured extraction issues.
- **Normalization / Cleaning (`processors/normalization/`, `data/clean/`)**:
  Performs context-gated line-wrap reflow, proper-noun continuation joins, punctuation cleanup with non-whitespace token-ledger verification, and semantic block separation while retaining an immutable `raw_record` snapshot/reference. Must never overwrite `data/raw/`.
- **Matching (`processors/matching/`, `data/merged/`)**:
  Associates exercises/entries with separate keys or explanations using scoped deterministic identities and content verification. Must not reparse PDFs or shift answers across ordinal gaps.
- **Categorization (`categorization/`, `data/categorized/`)**:
  Assigns lexical/pedagogical tags bound to semantic content hashes on already-structured data, abstaining when uncertain. Must not read PDFs directly.
- **`qa/`**:
  Holds `<STAGE>_BACKTESTING.md` and `<STAGE>_ISSUES.md` pairs generated deterministically from stage validation JSON (including zero-issue runs) plus `qa/ISSUE_LOG.md`.

## Strict Boundaries

Do not combine these responsibilities:
- downloading/acquiring + parsing;
- parsing + destructive cleaning;
- parsing + categorization;
- raw extraction + final dataset generation;
- matching + PDF extraction.

## Required Safeguards

When editing architecture or pipeline code, check:
1. Does this change keep `acquisition/local/` separate from parsing?
2. Has the target source family been profiled in `inspections/SOURCE_PROFILES.md` before parser coding?
3. Does RAW extraction preserve exact original source spans alongside readable projections?
4. Does cleaning happen after RAW output in a separate layer (`data/clean/`) without mutating `data/raw/`?
5. Are stage validation summaries and `<STAGE>_BACKTESTING.md` / `<STAGE>_ISSUES.md` wired to `qa/`?
6. Is the change limited to the requested stage?

## When to Read Original Docs

This skill is enough for ordinary development tasks. Read the original docs when:
- changing the architecture (`docs/general/ARCHITECTURE.md`);
- adding a new pipeline stage;
- changing folder responsibilities;
- resolving unclear or conflicting rules (`docs/general/PROJECT_CONTEXT.md`, `docs/PROVENANCE_AND_CONTRACTS.md`).
