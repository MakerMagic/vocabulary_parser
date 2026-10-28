# AGENTS.md — Vocabulary Parsing Pipeline Router & Behavioral Guardrails

## 1. ABSOLUTE RULE — EXECUTE ONLY THE EXPLICITLY REQUESTED STAGES

> [!IMPORTANT]
> **THIS IS THE SUPREME, HIGHEST-PRIORITY RULE FOR ALL WORK IN THIS REPOSITORY.**
> 
> You must **NEVER** execute a pipeline stage unless the user **EXPLICITLY AUTHORIZES THAT SPECIFIC STAGE**.
> 
> - If the user requests **Acquisition**, execute Acquisition **ONLY**.
> - If the user requests **Inspection**, execute Inspection **ONLY**.
> - If the user requests **RAW Extraction**, execute RAW Extraction **ONLY**.
> - If the user requests **RAW + Cleaning**, execute **ONLY** RAW and Cleaning.
> - If the user requests **Validation**, execute Validation **ONLY**.
> 
> **DO NOT automatically proceed to the next stage after completing the requested one.**
> Even if the next stage appears obvious, necessary, easy, or already planned, **YOU ARE FORBIDDEN FROM EXECUTING IT WITHOUT USER AUTHORIZATION**.
> 
> This prohibition strictly includes:
> - Vocabulary enrichment.
> - Russian translation generation.
> - English explanation generation.
> - Difficulty classification.
> - Final dataset generation.
> - Downstream artifact regeneration.
> - Any other processing stage not explicitly authorized.
> 
> **Stage completion behavior:**
> After completing the authorized stage:
> 1. Save its actual outputs.
> 2. Validate that stage's results.
> 3. Document stage-specific issues.
> 4. Document how to backtest the stage.
> 5. Update the current-work documentation ([`docs/general/CURRENT_WORK.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/CURRENT_WORK.md)).
> 6. **STOP.**
> 
> **ONE REQUESTED STAGE MEANS ONE STAGE. NO EXCEPTIONS UNLESS THE USER EXPLICITLY SPECIFIES OTHERWISE.**

---

## 2. Project Purpose & Multi-Source Architecture

This repository houses the **Vocabulary Document-Parsing Pipeline** (`justprepy`). Its goal is to ingest heterogeneous Vocabulary source documents from **multiple independent sources** (e.g., `uclouvain`, future exams, academic word lists, and reference vocabularies), extract source-faithful RAW records, normalize and enrich structured lexical data, and assemble verified datasets and local HTML backtesting views for downstream educational applications.

Historical architectural lessons from the prior TSA/BMAT and Mathematics parsing project are preserved in `PARSING_KNOWLEDGE_TRANSFER.md` and `DOCUMENTATION_ARCHITECTURE_HANDOVER.md`. Both are immutable historical reference materials; do not rewrite or delete them.

### Source Independence Principles

The entire project must **NEVER** be hardcoded around one particular PDF layout, website, filename convention, or vocabulary organization:

1. **A. Shared Processing Architecture (`processors/`, `docs/general/`):**
   Reusable, source-independent logic: deterministic JSON serialization, cryptographic hashing (`processors/provenance.py`), standardized stage artifact generation (`processors/stage_artifacts.py`), generic schema contracts, and common testing infrastructure.
2. **B. Source-Specific Organization:**
   Dedicated source directories holding materials, inspection findings, parsers, artifacts, and issues for each source independently:
   - Documentation: `docs/sources/<source_id>/`
   - Acquisition: `acquisition/sources/<source_id>/`
   - Inspection: `inspections/sources/<source_id>/`
   - RAW Artifacts: `data/raw/sources/<source_id>/`
   - Cleaning Artifacts: `data/clean/sources/<source_id>/`
   - Stage QA Reports: `qa/sources/<source_id>/`
3. **C. Adding Future Sources Without Restructuring:**
   A new source (e.g. `oxford_3000`) is introduced simply by creating its source directory hierarchy (`acquisition/sources/<source>/`, `inspections/sources/<source>/`, `parsers/<source>/`, `docs/sources/<source>/`), without modifying shared processors or contaminating existing sources like `uclouvain`.

---

## 3. Current Source — `uclouvain`

The source currently in the workspace is **`uclouvain`** (academic selection of `413` vocabulary words: `233 verbs` and `180 adjectives` from Université catholique de Louvain).

- **Documentation:** [`docs/sources/uclouvain/SOURCE_INSPECTION.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/sources/uclouvain/SOURCE_INSPECTION.md), [`docs/sources/uclouvain/PROCESSING_NOTES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/sources/uclouvain/PROCESSING_NOTES.md), [`docs/sources/uclouvain/STAGE_ISSUES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/sources/uclouvain/STAGE_ISSUES.md)
- **Acquisition Source File:** [`acquisition/sources/uclouvain/uclouvain_vocabulary_list.txt`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/sources/uclouvain/uclouvain_vocabulary_list.txt) (SHA-256: `e1b15633f274f58f093a3e1950dd1f368aad83fd54fb67ca9f682344d5628d7e`) and [`acquisition/sources/uclouvain/manifest.json`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/sources/uclouvain/manifest.json)
- **Inspection Findings:** [`inspections/sources/uclouvain/profile.json`](file:///c:/Users/user/Desktop/vocabulary_parser/inspections/sources/uclouvain/profile.json)
- **RAW Artifacts:** [`data/raw/sources/uclouvain/`](file:///c:/Users/user/Desktop/vocabulary_parser/data/raw/sources/uclouvain)
- **Cleaning Artifacts:** [`data/clean/sources/uclouvain/`](file:///c:/Users/user/Desktop/vocabulary_parser/data/clean/sources/uclouvain)
- **Stage QA Reports:** [`qa/sources/uclouvain/STAGE_ISSUES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/qa/sources/uclouvain/STAGE_ISSUES.md)

---

## 4. Current Stage Status (Audit Findings)

Agents must clearly distinguish between four different operational states:
1. **Architecture Prepared:** Structural contract, interfaces, and guards exist; stage is NOT executed.
2. **Stage Implemented:** Production parser/processor code written.
3. **Stage Executed:** Stage module run on actual source inputs, emitting outputs.
4. **Output Validated:** Output verified against invariant checks, schema, and negative controls.

| Stage | Operational State | Location / Artifacts | Notes |
|---|---|---|---|
| **1. Acquisition (`uclouvain`)** | **Executed & Validated** | [`acquisition/sources/uclouvain/`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/sources/uclouvain), [`data/acquisition/validation.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/acquisition/validation.json) | Source SHA-256 locked (`e1b15633...`). |
| **2. Inspection (`uclouvain`)** | **Executed & Validated** | [`inspections/sources/uclouvain/profile.json`](file:///c:/Users/user/Desktop/vocabulary_parser/inspections/sources/uclouvain/profile.json), [`docs/sources/uclouvain/SOURCE_INSPECTION.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/sources/uclouvain/SOURCE_INSPECTION.md) | Profiled 233 verbs + 180 adjectives = 413 items; edge cases documented. |
| **3. RAW Extraction (`uclouvain`)** | **Executed & Validated** | [`data/raw/sources/uclouvain/`](file:///c:/Users/user/Desktop/vocabulary_parser/data/raw/sources/uclouvain), [`data/raw/justprepy_wordlist/`](file:///c:/Users/user/Desktop/vocabulary_parser/data/raw/justprepy_wordlist) | 413 records with exact character and line slice spans. |
| **4. Cleaning (`uclouvain`)** | **Executed & Validated** | [`data/clean/sources/uclouvain/`](file:///c:/Users/user/Desktop/vocabulary_parser/data/clean/sources/uclouvain), [`data/clean/justprepy_wordlist/`](file:///c:/Users/user/Desktop/vocabulary_parser/data/clean/justprepy_wordlist) | 100% token-ledger match, `#2 account (for)` separated, `"difficulty": null` set. |
| **5. Vocabulary Enrichment** | **Previously Executed (Flagged for Re-Enrichment upon authorization)** | [`data/enriched/justprepy_wordlist/entries.enriched.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/enriched/justprepy_wordlist/entries.enriched.json) | Generated in a prior session under the former 2-word constraint. Needs re-enrichment under the corrected rule (maximum 2 translation alternatives) when authorized. |
| **Future: Difficulty Stage** | **Architecture Prepared Only (NOT IMPLEMENTED)** | [`processors/difficulty/contract.py`](file:///c:/Users/user/Desktop/vocabulary_parser/processors/difficulty/contract.py) | Contract prepared for `Easy`/`Medium`/`Hard`; `"difficulty": null` enforced across all records. |
| **6. Validation & PRE-FINAL** | **Previously Executed** | [`data/pre_final/vocabulary.json`](file:///c:/Users/user/Desktop/vocabulary_parser/data/pre_final/vocabulary.json) | 408 validated, 5 review_pending, 0 errors under existing checks. |
| **7. Local HTML Review UI** | **Implemented & Verified** | [`inspections/review/vocabulary_review.html`](file:///c:/Users/user/Desktop/vocabulary_parser/inspections/review/vocabulary_review.html) | Local table with stage switcher and filters. |
| **Test Suite** | **Implemented & Passing** | [`tests/test_vocabulary_pipeline.py`](file:///c:/Users/user/Desktop/vocabulary_parser/tests/test_vocabulary_pipeline.py) | 9 tests covering positive invariants and negative controls. |

---

## 5. Correct Russian Translation Rule

> [!CAUTION]
> The rule is **NOT** "Russian translation must contain no more than two words." That former constraint was incorrect and has been repealed.
>
> **CORRECT RULE:**
> - **Each English vocabulary entry may contain a maximum of TWO Russian translation alternatives.**
> - **An individual translation alternative may consist of multiple Russian words.**
> - Example: English word **Take off** -> Valid Russian translations:
>   1. **взлетать**
>   2. **снимать одежду**
>   *(The second alternative contains two Russian words, and that is completely acceptable.)*
> - Multiword phrases (e.g. `в отличие от` for `unlike`) are completely valid translation alternatives.
> - Maximum 2 translation alternatives per entry (1 is fine, 2 is maximum, >2 is invalid).
> - Do not truncate multiword translations; do not split one meaningful translation phrase into separate alternatives; do not invent a second translation merely to fill a slot.

---

## 6. Documentation System & Ban on Redundant README Files

- **Do NOT create new `README.md` files.**
- **Do NOT create README files merely to explain a folder.**
- **Use purpose-specific Markdown files:**
  - Global docs: [`docs/general/PROJECT_CONTEXT.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/PROJECT_CONTEXT.md), [`docs/general/ARCHITECTURE.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/ARCHITECTURE.md), [`docs/general/DATA_SCHEMA.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/DATA_SCHEMA.md), [`docs/general/PROCESSING_RULES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/PROCESSING_RULES.md), [`docs/general/DEVELOPMENT_RULES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/DEVELOPMENT_RULES.md), [`docs/general/CODEX_SKILLS_USAGE.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/CODEX_SKILLS_USAGE.md), [`docs/general/CURRENT_WORK.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/CURRENT_WORK.md).
  - Source docs: [`docs/sources/<source_id>/`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/sources) (`SOURCE_INSPECTION.md`, `PROCESSING_NOTES.md`, `STAGE_ISSUES.md`).

---

## 7. Operational Routing for Future Agents

1. **Before Starting Any Task:**
   - Read [`docs/general/CURRENT_WORK.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/CURRENT_WORK.md) for the active milestone and exact authorization boundaries.
   - Load only the **single** matching skill from [`.agents/skills/`](file:///c:/Users/user/Desktop/vocabulary_parser/.agents/skills) following [`docs/general/CODEX_SKILLS_USAGE.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/CODEX_SKILLS_USAGE.md).
2. **Execute ONLY the Explicitly Authorized Stage:**
   - Run the authorized stage, validate results, write stage issues and backtesting instructions, update `CURRENT_WORK.md`, and **STOP**.
3. **Core Invariants:**
   - **Fix the earliest responsible stage:** Never patch RAW segmentation errors in CLEAN or hide data defects in downstream views.
   - **One parser per source profile:** Write separate profile parsers emitting a compatible intermediate RAW contract.
   - **Canonical JSON is authoritative:** Stored JSON in `data/` is the single source of truth.
