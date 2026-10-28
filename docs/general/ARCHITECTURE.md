# Vocabulary Pipeline Architecture & Boundaries (`ARCHITECTURE.md`)

## 1. System Purpose & Core Architectural Principles

This document defines the structural components, data flow, ownership boundaries, and dependency directions of the **Vocabulary Document-Parsing Pipeline**.

### Three Architectural Pillars

1. **Shared Processing Architecture:**
   Generic, source-independent utilities applicable across all sources: cryptographic provenance hashing, deterministic canonical JSON serialization (`processors/provenance.py`), standardized QA stage artifact pair generation (`processors/stage_artifacts.py`), universal schema contracts, and common testing framework.
2. **Source-Specific Organization:**
   Dedicated, isolated directories holding raw documents, profiles, parsers, stage artifacts, and issue reports for each source independently (e.g. `uclouvain`).
3. **Strict Separation Between Shared & Source-Specific Behavior:**
   A source-specific problem or format change must not require rewriting the shared pipeline. Likewise, adding a new source must never require duplicating or restructuring the shared engine.

---

## 2. Pipeline Flow Diagram & Execution Sequence

Data flows strictly in a forward direction through isolated stages. Downstream stages consume upstream artifacts as read-only inputs and write to their own isolated directories.

```text
[1. Acquisition]       ──► acquisition/sources/<source_id>/ + manifest.json + data/acquisition/validation.json
       │                   (Unmodified source files + SHA-256 provenance manifest)
       ▼
[2. Inspection]        ──► inspections/sources/<source_id>/profile.json + docs/sources/<source_id>/SOURCE_INSPECTION.md
       │                   (Pre-parser layout, section counts, homographs & anomaly profiling)
       ▼
[3. RAW Parsers]       ──► data/raw/sources/<source_id>/entries.raw.json
       │                   (Exact character/line spans, raw tokens & extraction notices)
       ▼
[4. CLEAN / Norm]      ──► data/clean/sources/<source_id>/entries.clean.json
       │                   (Normalized headwords, parenthetical modifiers, token-ledger audits, difficulty=null)
       ▼
[5. Enrichment]        ──► data/enriched/<source_id>/entries.enriched.json
       │                   (Part of speech, <=2 Russian translation alternatives, non-circular English explanation)
       │
       ├───► [Future: Difficulty Stage] ──► data/difficulty/<source_id>/ (ARCHITECTURALLY PREPARED ONLY — NOT IMPLEMENTED)
       │                                    (Reserved for Easy / Medium / Hard classification; currently difficulty=null)
       ▼
[6. Validation / QA]   ──► data/pre_final/vocabulary.json + data/pre_final/validation.json + qa/<STAGE>_*.md
       │                   (End-to-end provenance & quality gates: <=2 Russian alternatives, non-circular English, difficulty=null)
       ▼
[7. HTML Review UI]    ──► inspections/review/vocabulary_review.html
                           (Self-contained local browser backtesting & QA inspection interface)
```

---

## 3. Current Source: `uclouvain` Isolation

The source currently in the workspace is **`uclouvain`** (`413` words: `233 verbs` and `180 adjectives`). Its materials are strictly isolated in dedicated directories:

| Component | `uclouvain` Location | Responsibility |
|---|---|---|
| **Source Acquisition** | [`acquisition/sources/uclouvain/`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/sources/uclouvain) | Holds `uclouvain_vocabulary_list.txt` (SHA-256: `e1b15633...`) and `manifest.json`. |
| **Source Inspection** | [`inspections/sources/uclouvain/`](file:///c:/Users/user/Desktop/vocabulary_parser/inspections/sources/uclouvain) | Holds `profile.json` (section counts, homographs, modals, parenthetical entry). |
| **Source Documentation** | [`docs/sources/uclouvain/`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/sources/uclouvain) | Holds `SOURCE_INSPECTION.md`, `PROCESSING_NOTES.md`, and `STAGE_ISSUES.md`. |
| **RAW Artifacts** | [`data/raw/sources/uclouvain/`](file:///c:/Users/user/Desktop/vocabulary_parser/data/raw/sources/uclouvain) | Holds `entries.raw.json` and `validation.json` (exact character spans). |
| **Cleaning Artifacts** | [`data/clean/sources/uclouvain/`](file:///c:/Users/user/Desktop/vocabulary_parser/data/clean/sources/uclouvain) | Holds `entries.clean.json` and `validation.json` (token ledgers, `difficulty: null`). |
| **Stage QA Reports** | [`qa/sources/uclouvain/`](file:///c:/Users/user/Desktop/vocabulary_parser/qa/sources/uclouvain) | Holds source-specific stage issue tracking (`STAGE_ISSUES.md`). |

---

## 4. How Additional Sources Are Introduced

To add a new independent source (e.g. `oxford_3000` or `cambridge_pet`):

1. Create `acquisition/sources/<new_source>/` and store the untouched source document + `manifest.json`.
2. Inspect the source document and document its characteristics in `docs/sources/<new_source>/SOURCE_INSPECTION.md` and `inspections/sources/<new_source>/profile.json`.
3. Implement a dedicated parser in `parsers/<new_source>/parser.py` conforming to the shared RAW data contract.
4. Output RAW artifacts to `data/raw/sources/<new_source>/` and cleaning artifacts to `data/clean/sources/<new_source>/`.
5. Document source-specific issues in `docs/sources/<new_source>/STAGE_ISSUES.md` and `qa/sources/<new_source>/`.

**No changes to shared processor logic or to existing sources like `uclouvain` are required.**

---

## 5. Component Responsibilities & Operational Status Matrix

Agents must clearly distinguish between four different operational states:
1. **Architecture Prepared:** Structural contract, interfaces, and guards exist; stage is NOT executed.
2. **Stage Implemented:** Production parser/processor code written.
3. **Stage Executed:** Stage module run on actual source inputs, emitting outputs.
4. **Output Validated:** Output verified against invariant checks, schema, and negative controls.

| Component | Operational State | Owns | Must NOT Silently Do |
|---|---|---|---|
| **1. Acquisition** | **Executed & Validated** | Ingestion of unmodified source files in `acquisition/sources/<source_id>/`, SHA-256 hashing. | Parse entries, alter source files, or infer identity from directory order alone. |
| **2. Inspection** | **Executed & Validated** | Structural analysis of section counts, cross-section homographs, parenthetical tokens in `inspections/sources/<source_id>/` and `docs/sources/<source_id>/`. | Store canonical records or mutate source files. |
| **3. RAW Extraction** | **Executed & Validated** | Extraction of raw text with exact file/line character slice coordinates (`source_spans`) and structured extraction notices. | Perform destructive normalization, strip parentheses/hyphens, or deduplicate cross-section homographs. |
| **4. CLEAN / Normalization** | **Executed & Validated** | Whitespace normalization, non-destructive separation of `headword_lemma` and `parenthetical_modifier`, non-whitespace token-ledger verification, and embedding `raw_record`. | Overwrite RAW records, alter supplied British/American spellings in `word`, or populate `difficulty`. |
| **5. Vocabulary Enrichment** | **Previously Executed (Flagged for Re-Enrichment upon authorization)** | Deterministic enrichment of `part_of_speech`, `russian_translation` (**maximum 2 translation alternatives**; multiword supported), and non-circular `english_explanation`. | Exceed 2 translation alternatives, use circular definitions, or truncate multiword translations. |
| **Future: Difficulty Stage** | **Architecture Prepared Only (NOT IMPLEMENTED)** | Architectural slot and schema contract (`"difficulty": null` reserved for `"Easy" \| "Medium" \| "Hard"`). | Classify words, invent heuristics, or populate non-null `difficulty` values until explicitly authorized. |
| **6. Validation & PRE-FINAL** | **Previously Executed** | End-to-end provenance verification, quality enforcement (max 2 translation alternatives, non-circular explanations, `difficulty is None`), and stage report generation. | Repair upstream text, bypass hash checks, or hide `review_pending` / `error` states. |
| **7. Local HTML Review UI** | **Implemented & Verified** | Self-contained local HTML table (`inspections/review/vocabulary_review.html`) displaying `# \| Word \| Part of Speech \| Russian Translation \| English Explanation` with stage/status filters. | Act as a canonical data store or diverge from canonical JSON. |

---

## 6. Directory Structure

```text
vocabulary_parser/
├── AGENTS.md                                # Supreme router & behavioral guardrails
├── pyproject.toml                         # Pytest and Ruff configuration
├── requirements.txt                       # Pinned PDF extraction & QA dependencies
├── skills-lock.json                       # Lockfile for external agent skills
├── .venv/                                 # Configured Python 3.13 virtual environment
├── .agents/skills/                        # 7 installed project-local AI agent skills
├── acquisition/
│   ├── manifest.json                      # Global provenance manifest
│   ├── local/                             # Historical local drop zone
│   └── sources/
│       └── uclouvain/                     # Source-isolated acquisition for uclouvain
├── inspections/
│   ├── SOURCE_PROFILES.md                 # Profile registry
│   ├── review/vocabulary_review.html      # Local HTML backtesting interface
│   └── sources/
│       └── uclouvain/                     # Source-isolated inspection profile for uclouvain
├── parsers/
│   └── justprepy_wordlist/parser.py       # RAW parser for uclouvain wordlist profile
├── processors/
│   ├── provenance.py                      # Shared deterministic hashing & JSON pointers
│   ├── stage_artifacts.py                 # Shared <STAGE>_BACKTESTING / <STAGE>_ISSUES generator
│   ├── acquisition.py                     # Acquisition runner
│   ├── inspection.py                      # Inspection runner
│   ├── normalization/cleaner.py           # Normalization runner
│   ├── enrichment/                        # Lexicon data & enrichment runner
│   ├── difficulty/contract.py             # Architecturally prepared contract (unimplemented)
│   ├── validation/validator.py            # Quality validator & PRE-FINAL assembler
│   ├── review_ui/html_generator.py        # Local HTML review generator
│   └── pipeline.py                        # Full pipeline runner (used only when authorized)
├── data/                                  # Canonical JSON outputs strictly segregated
│   ├── acquisition/validation.json
│   ├── inspection/profile.json & validation.json
│   ├── raw/
│   │   ├── justprepy_wordlist/            # Historical raw artifacts
│   │   └── sources/uclouvain/             # Source-isolated raw artifacts for uclouvain
│   ├── clean/
│   │   ├── justprepy_wordlist/            # Historical clean artifacts
│   │   └── sources/uclouvain/             # Source-isolated clean artifacts for uclouvain
│   ├── enriched/justprepy_wordlist/
│   └── pre_final/vocabulary.json & validation.json
├── qa/
│   ├── ISSUE_LOG.md                       # Consolidated defect ledger
│   ├── <STAGE>_BACKTESTING.md / <STAGE>_ISSUES.md (for executed stages)
│   └── sources/
│       └── uclouvain/                     # Source-isolated QA reports for uclouvain
├── docs/
│   ├── PROVENANCE_AND_CONTRACTS.md        # Hash locking, span preservation, overlays
│   ├── general/                           # The 7 core global documentation files
│   │   ├── PROJECT_CONTEXT.md
│   │   ├── ARCHITECTURE.md                # This file
│   │   ├── DATA_SCHEMA.md
│   │   ├── PROCESSING_RULES.md
│   │   ├── DEVELOPMENT_RULES.md
│   │   ├── CODEX_SKILLS_USAGE.md
│   │   └── CURRENT_WORK.md
│   └── sources/
│       └── uclouvain/                     # Source-specific documentation
│           ├── SOURCE_INSPECTION.md
│           ├── PROCESSING_NOTES.md
│           └── STAGE_ISSUES.md
└── tests/
    └── test_vocabulary_pipeline.py        # Verification suite with negative controls
```
