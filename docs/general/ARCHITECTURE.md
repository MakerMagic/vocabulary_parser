# Vocabulary Pipeline Architecture & Boundaries (`ARCHITECTURE.md`)

## 1. System Purpose

This document defines the structural components, data flow, ownership boundaries, and dependency directions of the **Vocabulary Document-Parsing Pipeline**.

It operationalizes the architectural principles from [`PARSING_KNOWLEDGE_TRANSFER.md`](file:///c:/Users/user/Desktop/vocabulary_parser/PARSING_KNOWLEDGE_TRANSFER.md) for Vocabulary processing while strictly guarding against boundary violations and premature stage coupling.

---

## 2. Pipeline Flow Diagram & Execution Sequence

Data flows strictly in a forward direction through isolated stages. Downstream stages consume upstream artifacts as read-only inputs and write to their own isolated directories.

```text
[Acquisition] ──► acquisition/local/
       │           (Source files + SHA-256 provenance manifest)
       ▼
[Inspection]  ──► inspections/SOURCE_PROFILES.md
       │           (Pre-parser layout, typography, encoding & boundary analysis)
       ▼
[RAW Parsers] ──► data/raw/<source_profile>/
       │           (Exact source spans, readable projections, raw assets & findings)
       ▼
[CLEAN / Norm]──► data/clean/<source_profile>/
       │           (Reflowed prose, semantic field separation, token-ledger audits)
       │
       ├───► [Matching (Optional)]       ──► data/merged/ (Associated keys & explanations)
       │
       └───► [Categorization (Optional)] ──► data/categorized/ (CEFR / lexical tagging)
       │
       ▼
[PRE-FINAL]   ──► data/pre_final/
                   (Admission gate: 0 unresolved issues, verified upstream hash locks)
```

---

## 3. Component Responsibilities & Ownership Matrix

| Component | Status | Owns | Must NOT Silently Do |
|---|---|---|---|
| **Acquisition** (`acquisition/`) | **Ready** | Ingestion of unmodified source documents into `acquisition/local/`, SHA-256 hashing, origin tracking, source-family identification. | Parse entries, alter source content/files, or infer identity from directory order alone. |
| **Inspection** (`inspections/`) | **Ready** | Pre-parsing analysis of document structure, fonts, phonetic symbols (IPA), multi-column flow, and entry boundary markers in `SOURCE_PROFILES.md`; targeted diagnostic previews. | Store canonical pipeline data, act as manual override files, or maintain static mass preview catalogs. |
| **RAW Parsers & Storage** (`data/raw/`, future `parsers/`) | **Directory Ready (Code Deferred)** | Extraction of raw text with exact page/line/byte span coordinates, readable projections (when verified), raw visual/table crops, and structured extraction issues. | Perform destructive normalization, discard raw spans, merge lines across uncertain boundaries, or hide OCR/raster uncertainty. |
| **CLEAN / Normalization** (future `processors/normalization/`, `data/clean/`) | **Deferred** | Controlled line-wrap reflow, semantic field separation (headword, POS, definition, example), punctuation normalization with token-ledger verification, preserving a snapshot of RAW. | Overwrite `data/raw/`, invent missing fields/definitions, or strip legitimate multi-sense numbering or list formatting. |
| **Matching** (future `processors/matching/`, `data/merged/`) | **Deferred** | Deterministic association of prompts/entries with independently published keys or explanations using scoped composite keys. | Shift answers across ordinal gaps, reparse documents, or invent answers to fill gaps. |
| **Categorization** (future `categorization/`, `data/categorized/`) | **Deferred** | Assignment of lexical categories, CEFR levels, or task tags bound to semantic content hashes, with strict abstention when ambiguous. | Use keyword guessing on unverified text, or retain stale tags after content changes. |
| **PRE-FINAL Assembly** (future `processors/pre_final/`, `data/pre_final/`) | **Deferred** | Admission filtering (rejecting any record with active upstream issues or broken hash bindings) to produce the canonical consumer dataset. | Repair upstream text, bypass hash validation, or conflate policy skips with parser failures. |

---

## 4. Repository Directory Layout

```text
vocabulary_parser/
├── AGENTS.md                                # Instruction router and active stage navigator
├── PARSING_KNOWLEDGE_TRANSFER.md          # Immutable handover from TSA/BMAT/Math project
├── DOCUMENTATION_ARCHITECTURE_HANDOVER.md # Immutable handover for Markdown documentation system
├── .gitignore                             # Ignores venvs, caches, and disposable artifacts
├── .agents/
│   └── skills/                            # Dedicated project-local AI agent skills root
├── acquisition/                           # Unmodified source documents and provenance manifest
│   ├── README.md
│   └── local/                             # Drop zone for original source files
├── inspections/                           # Pre-parsing profiles and targeted diagnostic views
│   ├── README.md
│   └── SOURCE_PROFILES.md                 # Layout, typography, and boundary profiling registry
├── data/                                  # Canonical pipeline outputs strictly segregated by stage
│   ├── README.md
│   └── raw/                               # Immutable RAW extraction artifacts
│       └── README.md
├── qa/                                    # Stage backtesting, issue tracking, and defect logs
│   ├── README.md
│   └── ISSUE_LOG.md                       # Structured root-cause defect ledger
├── docs/                                  # Pipeline specifications and guidelines
│   ├── PROVENANCE_AND_CONTRACTS.md        # Hash locking, span preservation, and manual overrides
│   └── general/                           # The seven core documentation files
│       ├── PROJECT_CONTEXT.md             # Project definition, scope, and durable priorities
│       ├── ARCHITECTURE.md                # System components, boundaries, and data flow (this file)
│       ├── DATA_SCHEMA.md                 # Shared contracts and representation rules
│       ├── PROCESSING_RULES.md            # Permitted transformations and stage invariants
│       ├── DEVELOPMENT_RULES.md           # Engineering rules for validation and artifact governance
│       ├── CODEX_SKILLS_USAGE.md          # Task-to-skill routing and discovery
│       └── CURRENT_WORK.md                # Operational handoff state
└── tests/                                 # Automated regression and source-fidelity test suite
    └── README.md
```

---

## 5. Allowed & Forbidden Interactions

### Allowed Interactions
- `parsers/` reads strictly from `acquisition/local/` (read-only) and writes to `data/raw/`.
- `processors/normalization/` reads strictly from `data/raw/` (read-only) and writes to `data/clean/`.
- `tests/` reads canonical data from `data/` or sources from `acquisition/local/` and asserts invariants without mutating pipeline data.
- `qa/` generators read stage validation summaries from `data/` and write `<STAGE>_BACKTESTING.md` / `<STAGE>_ISSUES.md` pairs to `qa/`.

### Forbidden Interactions
- **Downstream Overwriting Upstream:** A processor in `CLEAN` or `PRE-FINAL` must never modify or overwrite files in `data/raw/` or `acquisition/local/`.
- **Downstream Defect Patching:** Never compensate for broken RAW segmentation or dropped characters inside CLEAN, Matching, or downstream views. Fix the earliest responsible stage.
- **Manual Edits to Canonical JSON:** Never manually edit generated JSON in `data/`. All manual interventions must follow [`docs/PROVENANCE_AND_CONTRACTS.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/PROVENANCE_AND_CONTRACTS.md).

---

## 6. Extension Safeguards & Trade-offs

1. **One Parser Per Source Profile vs. Universal Parser:**
   - *Trade-off:* Increases the number of parser modules.
   - *Benefit:* Localizes layout quirks (e.g., multi-column dictionaries vs. single-column exercise sheets), preventing a fix for one document from regressing another.
2. **Dual Preservation (Raw Spans + Readable Projections) vs. Compact Storage:**
   - *Trade-off:* Increases raw JSON file size and memory footprint.
   - *Benefit:* Allows auditable verification of boundary coordinates, font decoding, and downstream text integrity.
3. **Strict Abstention vs. Apparent Coverage:**
   - *Trade-off:* Lowers immediate automated coverage numbers.
   - *Benefit:* Eliminates silently corrupted, truncated, or hallucinated lexical records in canonical outputs.
