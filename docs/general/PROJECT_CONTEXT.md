# Project Context (`PROJECT_CONTEXT.md`)

## 1. Project Definition & Purpose

The **Vocabulary Document-Parsing Project** exists to transform heterogeneous, unstructured or semi-structured Vocabulary source documents into verified, structured, and source-faithful digital datasets for downstream educational, testing, and language-learning systems.

Source documents may include:
- Word lists and bilingual/monolingual glossaries.
- Lexical exercises and multiple-choice vocabulary assessments.
- Accompanying answer keys, explanations, and usage notes.
- Lexical reference materials containing headwords, phonetic transcriptions (IPA), parts of speech, numbered sense definitions, usage collocations, and example sentences.

Historical architectural lessons, common parsing failure modes, and recovery strategies are preserved in [`PARSING_KNOWLEDGE_TRANSFER.md`](file:///c:/Users/user/Desktop/vocabulary_parser/PARSING_KNOWLEDGE_TRANSFER.md) and [`DOCUMENTATION_ARCHITECTURE_HANDOVER.md`](file:///c:/Users/user/Desktop/vocabulary_parser/DOCUMENTATION_ARCHITECTURE_HANDOVER.md).

---

## 2. Intended Capabilities & High-Level Workflow

The pipeline operates across strictly separated, reproducible stages:

```text
[Source Documents in acquisition/local/]
        │
        ▼
[Pre-Parsing Profiling in inspections/SOURCE_PROFILES.md]
        │
        ▼
[Profile-Specific RAW Extraction (parsers/) -> data/raw/]
        │
        ▼
[CLEAN Normalization & Structural Projection -> data/clean/]
        │
        ├──► (Optional) [Key / Explanation Matching -> data/merged/]
        ├──► (Optional) [Lexical Categorization & Tagging -> data/categorized/]
        │
        ▼
[PRE-FINAL Admission & Canonical Assembly -> data/pre_final/]
```

1. **Acquisition:** Ingest and register unmodified local source files with SHA-256 provenance hashes.
2. **Inspection:** Profile source typography, character encoding, reading order, and entry boundaries before writing parser code.
3. **RAW Extraction:** Extract exact text slices, bounding boxes, and image assets without destructive normalization.
4. **CLEAN Normalization:** Reflow wrapped prose, separate semantic fields, and clean punctuation using strict token-ledger controls.
5. **Matching (Conditional):** Associate prompts with independently published answer keys or explanations when sources are split.
6. **Categorization (Conditional):** Assign verified lexical domains, CEFR levels, or task types based on semantic content hashes.
7. **PRE-FINAL Assembly:** Gate canonical dataset inclusion on zero unresolved upstream defects and verified dependency hashes.

---

## 3. Important Conceptual Distinctions

To prevent repeating mistakes from prior parsing initiatives, agents must maintain these distinctions:

- **Exact Source Evidence vs. Readable Interpretation:** Unmodified source text and exact character/byte spans must be preserved in RAW alongside any decoded or normalized readable text (e.g., resolved ligatures or font encodings).
- **One Parser Per Source Profile:** Different document layouts require dedicated profile parsers emitting a compatible intermediate contract; there is no single universal parser.
- **Availability vs. Defect vs. Policy Skip:** Missing source fields (e.g., an entry without an example sentence) are valid `null` values; parser segmentation failures are active `issue` blockers; and out-of-scope sections are explicit `policy_excluded` records. Never conflate these categories in schemas or counts.
- **Canonical JSON vs. Disposable Views:** Stored JSON files in `data/` are authoritative. Generated Markdown reports in `qa/` and HTML previews in `inspections/` are disposable diagnostic projections.
- **Earliest Responsible Stage:** RAW defects must be fixed in RAW, normalization defects in CLEAN, and key-association defects in Matching. Never patch upstream data errors in downstream stages.

---

## 4. Durable Design Priorities

1. **Source Fidelity Over Surface Cleanliness:** A syntactically valid or fluent string that omits source text or absorbs adjacent content is an extraction failure.
2. **Deterministic Reproducibility:** Every pipeline stage must run deterministically, producing identical output bytes for identical inputs.
3. **Auditability & Provenance:** Any manual correction or external key must live in a dedicated, tracked overlay file—never via hand-edits to generated data.
4. **Lean Evolution:** Build only what is justified by active source documents. Do not create speculative pipeline stages or schemas ahead of source evidence.

---

## 5. Navigation & Authority Links

- **Component Boundaries & Responsibilities:** [`ARCHITECTURE.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/ARCHITECTURE.md)
- **Data Contracts & Provenance Invariants:** [`DATA_SCHEMA.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/DATA_SCHEMA.md) and [`PROVENANCE_AND_CONTRACTS.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/PROVENANCE_AND_CONTRACTS.md)
- **Allowed Data Transformations:** [`PROCESSING_RULES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/PROCESSING_RULES.md)
- **Change Management & QA Governance:** [`DEVELOPMENT_RULES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/DEVELOPMENT_RULES.md)
- **Agent Skill Discovery & Routing:** [`CODEX_SKILLS_USAGE.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/CODEX_SKILLS_USAGE.md)
- **Current Operational Handoff State:** [`CURRENT_WORK.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/CURRENT_WORK.md)
