# Data Schema & Contracts (`DATA_SCHEMA.md`)

## 1. Purpose & Authority

This document defines the **shared structural data contracts, identity standards, and provenance conventions** across the Vocabulary parsing pipeline.

Detailed domain-level schemas for specific Vocabulary document profiles will be defined in dedicated guides once incoming source documents are inspected. This shared guide defines the **invariants that all stage schemas must satisfy**.

---

## 2. Canonical Source Convention

1. **Storage Authority:** Canonical records exist only as validated JSON files inside [`data/`](file:///c:/Users/user/Desktop/vocabulary_parser/data).
2. **Immutability:** Once written and verified, upstream records are read-only.
3. **Format Integrity:** All JSON files must be serialized with deterministic key order, UTF-8 encoding without BOM, and standard 2-space indentation.

---

## 3. Identity & Provenance Invariants

Every structured record emitted by the pipeline must maintain strict identity and evidence traceability as specified in [`docs/PROVENANCE_AND_CONTRACTS.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/PROVENANCE_AND_CONTRACTS.md):

1. **Deterministic Record Identity (`id`):**
   - Must be derived from intrinsic, human-readable source components (e.g., `<source_family>_<doc_id>_<unit_or_section>_<item_or_entry_id>`).
   - Must **never** use random UUIDs, wall-clock timestamps, or runtime loop counters.
2. **File Provenance Hash (`source_sha256`):**
   - The SHA-256 hash of the exact source document in `acquisition/local/` from which the record was extracted.
3. **Upstream Evidence Pointers (`upstream_file_sha256`, `upstream_json_pointer`):**
   - In downstream stages (`CLEAN`, `PRE-FINAL`), every record must point to its exact predecessor file hash and JSON pointer (RFC 6901).
4. **Content Hash (`record_content_hash`):**
   - A deterministic hash of the record's semantic content and associated assets to detect silent drift or verify safe rebindings.

---

## 4. Required, Optional, and Null Semantics

A major lesson from [`PARSING_KNOWLEDGE_TRANSFER.md`](file:///c:/Users/user/Desktop/vocabulary_parser/PARSING_KNOWLEDGE_TRANSFER.md) is never to conflate missing source data, extraction failures, and policy decisions:

| State | JSON Representation | Meaning & Invariant |
|---|---|---|
| **Present Value** | `"field": <value>` | The field was present in the source and faithfully extracted. |
| **Unavailable** | `"field": null` | The field is legitimately absent in the source document (e.g., a word list entry that contains no example sentence). Explicitly permitted by schema. |
| **Policy Excluded** | `"status": "excluded"` | The source unit/section is intentionally skipped by project scope rules. Kept out of the canonical dataset. |
| **Active Defect** | `"status": "issue"` | Extraction or normalization encountered an anomaly or uncertainty. **Must block record admission to PRE-FINAL.** |
| **Review Pending** | `"status": "review_pending"` | Ambiguous boundary or candidate classification awaiting verified human or hash-bound audit. Blocked from PRE-FINAL. |

---

## 5. Structural Layers in RAW and CLEAN Records

### RAW Contract (`data/raw/`)
Every RAW record must keep these evidence layers distinct:
- `raw_text`: Exact, unmodified source string (retaining raw encoding tokens or ligatures).
- `source_spans`: Exact slice coordinates (`start`, `end`, `page_number`, `bbox`) referencing the stored raw page text.
- `readable_text`: Decoded or spatially normalized projection (only populated when a verified font/layout decoder exists).
- `raw_assets`: Referenced table or image crops with bounding box, coordinate frame, and asset SHA-256.
- `extraction_issues`: Array of structured warnings or blockers encountered during extraction.

### CLEAN Contract (`data/clean/`)
Every CLEAN record preserves:
- `raw_record`: An embedded snapshot or verified reference to the predecessor RAW record.
- `ordered_blocks`: The canonical reading sequence of lexical components (`headword`, `pronunciation`, `pos`, `definition`, `example`, `collocation`, `note`, `visual`).
- `clean_assets`: Derived assets where option labels or decorative artifacts have been cleanly removed without pixel loss to genuine content.
- `normalization_audit`: Audit metadata detailing reflowed line joins and verified token counts.

---

## 6. Future Vocabulary Domain Schemas

*(To be created once documents arrive in `acquisition/local/` and are profiled in `inspections/SOURCE_PROFILES.md`.)*

Anticipated profile schemas (pending source evidence):
- **Lexical Entry Schema:** Headwords, IPA transcriptions, parts of speech, numbered senses, examples, collocations, etymology.
- **Vocabulary Exercise Schema:** Stems/contexts, multiple-choice options, target lexical targets, associated answer keys, and explanations.
