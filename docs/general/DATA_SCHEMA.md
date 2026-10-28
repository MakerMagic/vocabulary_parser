# Data Schema & Contracts (`DATA_SCHEMA.md`)

## 1. Purpose & Authority

This document defines the **shared structural data contracts, identity standards, and provenance conventions** across the Vocabulary parsing pipeline, including multi-source support and the corrected Russian translation specification.

---

## 2. Source-Independent Architecture Conventions

The schema supports multiple independent Vocabulary sources (e.g. `uclouvain`, future academic word lists, and exam sets):

1. **Storage Authority:** Canonical records exist only as validated JSON files inside [`data/`](file:///c:/Users/user/Desktop/vocabulary_parser/data).
2. **Immutability:** Once written and verified, upstream records are read-only.
3. **Format Integrity:** All JSON files are serialized with deterministic sorted keys, UTF-8 encoding without BOM, and 2-space indentation via [`write_canonical_json`](file:///c:/Users/user/Desktop/vocabulary_parser/processors/provenance.py#L29-L35).
4. **Source Scoping:** Every record explicitly identifies its `source_id` / `source_family` (e.g., `"uclouvain"`), preventing collisions across heterogeneous sources.

---

## 3. Identity & Provenance Invariants

Every structured record emitted by the pipeline maintains strict identity and evidence traceability:

1. **Deterministic Record Identity (`id`):**
   - Format: `<source_id>_vocab_<ordinal>` (e.g., `justprepy_vocab_001` or `uclouvain_vocab_001`), derived deterministically from the source structure.
   - Never uses random UUIDs, timestamps, or volatile runtime iteration order.
2. **File Provenance Hash (`source_sha256`):**
   - The SHA-256 hash of the exact source file in `acquisition/sources/<source_id>/` from which the record was extracted.
3. **Upstream Evidence Pointers (`upstream_file_sha256`, `upstream_json_pointer`):**
   - Every record in `CLEAN`, `ENRICHED`, and `PRE-FINAL` points to its exact predecessor file SHA-256 and RFC 6901 JSON pointer (`/records/0`, `/records/1`, ...).
4. **Content Hash (`record_content_hash`):**
   - Deterministic SHA-256 of the record's semantic content to detect drift or verify rebindings.

---

## 4. Required, Optional, and Null Semantics

| State | JSON Representation | Meaning & Invariant |
|---|---|---|
| **Present Value** | `"field": <value>` | Field was extracted from source or deterministically enriched and verified. |
| **Unavailable / Reserved Future Stage** | `"difficulty": null`, `"parenthetical_modifier": null` | Field is legitimately absent in source (`parenthetical_modifier`) or reserved for an unimplemented future stage (`difficulty`). |
| **Validated** | `"validation_status": "validated"` | Record passed all provenance, translation alternative limit, non-circular English, and POS checks with zero ambiguity. |
| **Review Pending** | `"validation_status": "review_pending"` | Record satisfies all formal schema constraints, but carries a documented linguistic notice (e.g., parenthetical phrasal syntax, defective modal morphology, or secondary polysemous sense) for human curriculum review. |
| **Active Error** | `"validation_status": "error"` | Record failed a mandatory schema or quality check (`0` tolerated in PRE-FINAL). |

---

## 5. Russian Translation Field Contract (CORRECTED)

> [!IMPORTANT]
> The rule is **NOT** "maximum two words". An individual Russian translation may contain multiple words.
>
> **SPECIFICATION:**
> - **Field Name:** `russian_translation` (`str` or `list[str]`)
> - **Maximum TWO translation alternatives per entry.**
> - **Each alternative may consist of multiple Russian words.**
> - Examples:
>   - Single-word alternative: `"взлетать"`
>   - Multi-word alternative: `"снимать одежду"` (2 words — valid)
>   - Multi-word alternative: `"в отличие от"` (3 words — valid)
>   - Two alternatives: `"взлетать; снимать одежду"` (2 alternatives — valid)
>   - Invalid (>2 alternatives): `"взлетать; снимать одежду; отправляться"` (3 alternatives — REJECTED)
> - **Integrity Rules:**
>   - Do not truncate multiword translations to fit an arbitrary word count.
>   - Do not split one meaningful phrase into separate alternatives.
>   - Do not invent a second translation if one accurate translation suffices.
>   - Must use standard Cyrillic script (`CYRILLIC_CHAR_RE` and `CYRILLIC_PHRASE_RE`).

---

## 6. Stage Record Contracts

### 6.1 RAW Contract (`data/raw/sources/<source_id>/entries.raw.json`)
- `id`: Deterministic string (`<source>_vocab_<ordinal>`).
- `number`: Sequential ordinal (`1..N`).
- `raw_text`: Exact unmodified source string (retaining raw encoding tokens or brackets, e.g. `"account (for)"`, `"so-called"`).
- `readable_text`: Projected text alongside `raw_text`.
- `source_spans`: Exact slice coordinates (`file_char_start`, `file_char_end`, `line_number`, `line_char_start`, `line_char_end`).
- `extraction_issues`: Array of structured warnings or blockers encountered during extraction.

### 6.2 CLEAN Contract (`data/clean/sources/<source_id>/entries.clean.json`)
- `raw_record`: Embedded snapshot of the predecessor RAW record.
- `word`: Normalized surface word (100% non-whitespace token-ledger match with `raw_text`).
- `headword_lemma`: Base alphabetic lemma (`"account"` for `"account (for)"`).
- `parenthetical_modifier`: Modifier or particle (`"for"` for `"account (for)"`, `null` otherwise).
- `spelling_convention`: E.g. `"standard_shared"`, `"british_ise_or_our"`, `"american_or_oxford_ize"`.
- `normalization_audit`: `{"raw_non_whitespace_tokens", "clean_non_whitespace_tokens", "token_ledger_match", "transformations_applied"}`.
- `difficulty`: `null` (strictly enforced; reserved for future Difficulty Classification stage).

### 6.3 ENRICHED & PRE-FINAL Contract (`data/pre_final/vocabulary.json`)
Every final vocabulary record contains:
- `number` (`int`): Sequential record number.
- `word` (`str`): Original English word preserved verbatim.
- `part_of_speech` (`str`): Grammatically accurate part of speech (`verb`, `verb (phrasal)`, `verb (modal)`, `adjective`, etc.).
- `russian_translation` (`str`): Maximum of **TWO translation alternatives**, each of which may contain multiple Russian words.
- `english_explanation` (`str`): Non-circular English explanation (`>= 15` chars, excluding headword lemma).
- `difficulty`: `null` (reserved for future `Easy`/`Medium`/`Hard` stage).
- `validation_status`: `"validated"`, `"review_pending"`, or `"error"`.
- `provenance`: Complete upstream hash and pointer chain back to RAW and source file.
