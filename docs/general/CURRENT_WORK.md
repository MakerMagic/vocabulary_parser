# Current Operational State (`CURRENT_WORK.md`)

> **Last Updated:** 2026-10-28  
> **Status:** Initial Architecture & Documentation Framework Completed

---

## Current milestone

Establish the initial repository foundation, architectural contracts, documentation system (`docs/general/`), and skills structure (`.agents/skills/`) for the Vocabulary Document-Parsing Pipeline, fully incorporating lessons from [`PARSING_KNOWLEDGE_TRANSFER.md`](file:///c:/Users/user/Desktop/vocabulary_parser/PARSING_KNOWLEDGE_TRANSFER.md) and [`DOCUMENTATION_ARCHITECTURE_HANDOVER.md`](file:///c:/Users/user/Desktop/vocabulary_parser/DOCUMENTATION_ARCHITECTURE_HANDOVER.md).

---

## Already completed

1. **Codex Handover Preservation:** Preserved [`PARSING_KNOWLEDGE_TRANSFER.md`](file:///c:/Users/user/Desktop/vocabulary_parser/PARSING_KNOWLEDGE_TRANSFER.md) and [`DOCUMENTATION_ARCHITECTURE_HANDOVER.md`](file:///c:/Users/user/Desktop/vocabulary_parser/DOCUMENTATION_ARCHITECTURE_HANDOVER.md) as immutable historical reference material.
2. **Repository Foundation:**
   - Initialized drop zone for source documents in [`acquisition/local/`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/local).
   - Established pre-parsing profiling registry in [`inspections/SOURCE_PROFILES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/inspections/SOURCE_PROFILES.md).
   - Created immutable extraction storage directory [`data/raw/`](file:///c:/Users/user/Desktop/vocabulary_parser/data/raw) with strict data contracts.
   - Initialized QA defect ledger [`qa/ISSUE_LOG.md`](file:///c:/Users/user/Desktop/vocabulary_parser/qa/ISSUE_LOG.md) and stage reporting rules.
   - Defined automated testing standards in [`tests/README.md`](file:///c:/Users/user/Desktop/vocabulary_parser/tests/README.md).
   - Created root [`.gitignore`](file:///c:/Users/user/Desktop/vocabulary_parser/.gitignore).
3. **Documentation Architecture (`docs/general/`):**
   - [`PROJECT_CONTEXT.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/PROJECT_CONTEXT.md): Project definition, workflow, and durable priorities.
   - [`ARCHITECTURE.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/ARCHITECTURE.md): Component ownership matrix, data flow, and allowed/forbidden interactions.
   - [`DATA_SCHEMA.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/DATA_SCHEMA.md): Shared contracts, identity rules, and required/optional/null semantics.
   - [`PROCESSING_RULES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/PROCESSING_RULES.md): Permitted stage transformations, token ledgers, and prohibited shortcuts.
   - [`DEVELOPMENT_RULES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/DEVELOPMENT_RULES.md): Safe change workflow, canonical JSON inspection, and artifact governance.
   - [`CODEX_SKILLS_USAGE.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/CODEX_SKILLS_USAGE.md): Task-to-skill routing and selective loading rules.
   - [`CURRENT_WORK.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/CURRENT_WORK.md): This operational handoff state.
4. **Skills Root:** Initialized dedicated project skill directory at [`.agents/skills/`](file:///c:/Users/user/Desktop/vocabulary_parser/.agents/skills) with structural conventions.
5. **Instruction Router:** Updated [`AGENTS.md`](file:///c:/Users/user/Desktop/vocabulary_parser/AGENTS.md) to route agents directly into the new architecture.

---

## In progress

- Awaiting intake of first Vocabulary source documents into `acquisition/local/`.

---

## Next task

1. Ingest initial Vocabulary source document(s) (PDF, DOCX, HTML, TXT, etc.) into [`acquisition/local/`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/local).
2. Generate SHA-256 manifest and document role metadata in `acquisition/`.
3. Perform source layout, font/IPA encoding, and boundary inspection, recording findings in [`inspections/SOURCE_PROFILES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/inspections/SOURCE_PROFILES.md).

---

## Do not work on yet

- **Do NOT write parsers or extraction code** before source documents are ingested and profiled.
- **Do NOT create downstream directories** (`data/clean/`, `data/pre_final/`, `processors/`) prematurely.
- **Do NOT install or invent custom skills** without real operational tasks requiring them.
- **Do NOT hand-edit generated JSON or stage reports.**
