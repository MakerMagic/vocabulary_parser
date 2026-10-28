---
name: data-schema-consistency
description: Enforces shared data contracts, deterministic identity, SHA-256 provenance locks, and explicit availability/issue state semantics across RAW, CLEAN, and downstream Vocabulary datasets. Use when designing or modifying JSON schemas, record IDs, provenance references, or dataset validators.
---

# Data Schema and Dataset Consistency Skill

## Purpose

Use this skill when working with structured JSON records and references produced by the Vocabulary document-parsing pipeline.

The goal is to keep `data/raw/`, `data/clean/`, and future downstream layers consistent, traceable, and unambiguous.

## Core Schema Invariants

1. **Identity vs. Evidence Version:**
   - **Deterministic Record ID (`id`):** Derived from intrinsic source metadata (`<source_family>_<doc_id>_<unit_or_section>_<item_or_entry_id>`). Never use random UUIDs, timestamps, or runtime iteration order.
   - **Provenance & Evidence Locks:** Every record must carry `source_sha256` (locking to `acquisition/local/`). Downstream records must also carry `upstream_file_sha256`, `upstream_json_pointer`, and `record_content_hash`.
   - Never silently overwrite a stale upstream hash in a downstream record; revalidate or rebind with proof that decision-relevant content is unchanged.

2. **Dual Text & Coordinate Layers in RAW (`data/raw/`):**
   - `raw_text`: Unmodified extracted source string.
   - `source_spans`: Exact character/byte slice coordinates (`start`, `end`, `page_number`, `bbox`) indexing into the unmodified page string.
   - `readable_text`: Decoded or spatially ordered text (populated when a verified decoder applies).
   - `raw_assets`: Extracted visual/table references with coordinate frame, bounding box, and asset SHA-256.
   - `extraction_issues`: Structured findings for any extraction uncertainty.

3. **Ordered Block Streams in CLEAN (`data/clean/`):**
   - Represent interleaved lexical components (`headword`, `pronunciation`, `pos`, `definition`, `example`, `collocation`, `note`, `visual`, `stem`, `option`) as a single canonical `ordered_blocks` stream preserving source reading order.
   - Embed or lock to the exact predecessor `raw_record`.

4. **Explicit Availability, Policy Skip, and Defect States:**
   - **Present (`"field": <value>`):** Faithfully extracted from source.
   - **Unavailable (`"field": null`):** Legitimately absent in the source document (e.g., a glossary entry with no example sentence). Valid when documented.
   - **Policy Excluded (`"status": "excluded"`):** Intentionally skipped by project scope rules.
   - **Active Defect (`"status": "issue"`):** Extraction or normalization anomaly; **must block PRE-FINAL admission**.
   - **Review Pending (`"status": "review_pending"`):** Ambiguous boundary or candidate awaiting verification; **must block PRE-FINAL admission**.

## Forbidden Patterns

Do not:
- conflate missing source fields (`null`), policy exclusions, and parser defects in schemas or summary counts;
- sum overlapping issue tags as unique rejected items (always provide `excluded_total` and a disjoint primary-reason partition);
- collapse `raw_text` and `readable_text` into a single destructive field;
- hand-edit generated JSON in `data/` (use provenance-tracked manual overlays per `docs/PROVENANCE_AND_CONTRACTS.md`).

## When to Read Original Docs

Read original docs when:
- defining or updating stage schemas (`docs/general/DATA_SCHEMA.md`);
- changing provenance, hash-locking, or manual-override rules (`docs/PROVENANCE_AND_CONTRACTS.md`).
