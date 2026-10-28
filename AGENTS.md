# AGENTS.md — Vocabulary Parsing Pipeline Router

## 1. Project Purpose

This repository houses the **Vocabulary Document-Parsing Pipeline**. Its goal is to ingest heterogeneous Vocabulary source documents (word lists, definitions, usage examples, lexical exercises, and accompanying keys/explanations), extract source-faithful RAW records, normalize and validate structured lexical data, and assemble verified datasets for downstream applications.

Historical architectural lessons from the prior TSA/BMAT and Mathematics parsing project are preserved in [`PARSING_KNOWLEDGE_TRANSFER.md`](file:///c:/Users/user/Desktop/vocabulary_parser/PARSING_KNOWLEDGE_TRANSFER.md) and [`DOCUMENTATION_ARCHITECTURE_HANDOVER.md`](file:///c:/Users/user/Desktop/vocabulary_parser/DOCUMENTATION_ARCHITECTURE_HANDOVER.md). Both are immutable historical reference materials; do not rewrite or delete them.

---

## 2. Current Implementation Status

> **IMPORTANT:** This repository is currently at the **Initial Architecture & Foundation** stage. **No extraction, parsing, cleaning, matching, categorization, or rendering code has been implemented yet.** Do not claim a pipeline stage is operational simply because its foundational directory exists.

| Stage / Area | Status | Location | Notes |
|---|---|---|---|
| **Documentation Architecture** | **Initialized** | [`docs/general/`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general) | 7 core docs: Context, Architecture, Schema, Processing, Development, Skills, Current Work. |
| **Agent Skills Root** | **Structure Ready** | [`.agents/skills/`](file:///c:/Users/user/Desktop/vocabulary_parser/.agents/skills) | Dedicated skill root ready to receive individual skills (`<skill-name>/SKILL.md`). |
| **Acquisition (Source Intake)** | **Structure Ready** | [`acquisition/`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition) | Ready to receive source files in `acquisition/local/` and log provenance. No documents ingested yet. |
| **Source Inspection** | **Structure Ready** | [`inspections/`](file:///c:/Users/user/Desktop/vocabulary_parser/inspections) | Ready for pre-parser document profiling (`SOURCE_PROFILES.md`). |
| **RAW Extraction Storage** | **Placeholder Only** | [`data/raw/`](file:///c:/Users/user/Desktop/vocabulary_parser/data/raw) | Directory established with data contract rules; **no RAW parser exists yet**. |
| **QA & Issue Tracking** | **Structure Ready** | [`qa/`](file:///c:/Users/user/Desktop/vocabulary_parser/qa) | Ready for stage `<STAGE>_BACKTESTING.md` / `<STAGE>_ISSUES.md` pairs and defect tracking. |
| **Verification Suite** | **Placeholder Only** | [`tests/`](file:///c:/Users/user/Desktop/vocabulary_parser/tests) | Testing standards defined; **no executable tests exist yet**. |
| **Source-Profile Parsers** | **Not Implemented** | *(Deferred: `parsers/`)* | Create per-profile parser modules only after source inspection is documented. |
| **Cleaning & Normalization** | **Not Implemented** | *(Deferred: `processors/normalization/`, `data/clean/`)* | Wait until RAW extraction and schema are verified. |
| **Matching / Key Association** | **Not Implemented** | *(Deferred: `processors/matching/`, `data/merged/`)* | Only needed if Vocabulary sources separate prompts/entries from keys/explanations. |
| **Categorization / Lexical Tagging** | **Not Implemented** | *(Deferred: `categorization/`, `data/categorized/`)* | Wait until Vocabulary taxonomy requirements are defined. |
| **PRE-FINAL & Rendering** | **Not Implemented** | *(Deferred: `processors/pre_final/`, `data/pre_final/`)* | Wait until upstream contracts are stable. |

---

## 3. Documentation System (`docs/general/`)

The documentation architecture follows [`DOCUMENTATION_ARCHITECTURE_HANDOVER.md`](file:///c:/Users/user/Desktop/vocabulary_parser/DOCUMENTATION_ARCHITECTURE_HANDOVER.md):

| Document | Purpose | Authority Link |
|---|---|---|
| **PROJECT_CONTEXT.md** | Why the project exists, scope, terminology, and durable priorities. | [`docs/general/PROJECT_CONTEXT.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/PROJECT_CONTEXT.md) |
| **ARCHITECTURE.md** | Component responsibilities, stage boundaries, and data flow. | [`docs/general/ARCHITECTURE.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/ARCHITECTURE.md) |
| **DATA_SCHEMA.md** | Shared contracts, identity rules, and null/issue semantics. | [`docs/general/DATA_SCHEMA.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/DATA_SCHEMA.md) |
| **PROCESSING_RULES.md** | Permitted transformations, preservation rules, and prohibited shortcuts. | [`docs/general/PROCESSING_RULES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/PROCESSING_RULES.md) |
| **DEVELOPMENT_RULES.md** | Rules for code modifications, validation, and stage artifact generation. | [`docs/general/DEVELOPMENT_RULES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/DEVELOPMENT_RULES.md) |
| **CODEX_SKILLS_USAGE.md** | Task-to-skill routing, discovery, and context-loading discipline. | [`docs/general/CODEX_SKILLS_USAGE.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/CODEX_SKILLS_USAGE.md) |
| **CURRENT_WORK.md** | Operational handoff state (milestone, completed, in progress, next task). | [`docs/general/CURRENT_WORK.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/CURRENT_WORK.md) |

---

## 4. Operational Routing for Future Agents

1. **Before Starting Any Task:**
   - Check [`docs/general/CURRENT_WORK.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/CURRENT_WORK.md) for the active continuation state and next task.
   - Consult [`docs/general/CODEX_SKILLS_USAGE.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/CODEX_SKILLS_USAGE.md) to see if a dedicated skill covers your task.
2. **Where to place incoming source documents:**
   Place unmodified original files inside [`acquisition/local/`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/local) and record SHA-256 hashes following [`acquisition/README.md`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/README.md).
3. **Before writing any parser:**
   Inspect actual source files and document their layout, typography, encoding, and entry boundaries in [`inspections/SOURCE_PROFILES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/inspections/SOURCE_PROFILES.md).
4. **How to preserve source provenance:**
   Follow [`docs/general/DATA_SCHEMA.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/DATA_SCHEMA.md) and [`docs/PROVENANCE_AND_CONTRACTS.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/PROVENANCE_AND_CONTRACTS.md). Every extracted record must retain source file SHA-256, page/line/byte coordinates, and exact original source spans.
5. **Where to document findings and issues:**
   - Pre-extraction source characteristics go in [`inspections/SOURCE_PROFILES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/inspections/SOURCE_PROFILES.md).
   - Stage validation summaries and defects go in [`qa/`](file:///c:/Users/user/Desktop/vocabulary_parser/qa) (`<STAGE>_BACKTESTING.md`, `<STAGE>_ISSUES.md`, and [`qa/ISSUE_LOG.md`](file:///c:/Users/user/Desktop/vocabulary_parser/qa/ISSUE_LOG.md)).
6. **Core Invariants:**
   - **Fix the earliest responsible stage:** Never patch RAW segmentation errors in CLEAN or hide data defects in downstream views.
   - **One parser per source profile:** Write separate profile parsers emitting a compatible intermediate RAW contract.
   - **Readable ≠ Faithful:** Verify ownership and adjacent entries.
   - **Explicit state separation:** Keep policy exclusions, unavailable fields, parser errors, and pending reviews distinct.
   - **Auditable manual overrides:** Manual corrections live in dedicated provenance-tracked overlay files.
   - **Canonical JSON is authoritative:** Stored JSON in `data/` is the single source of truth.
