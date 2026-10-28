# Source Provenance, Identity & Data Contracts

This document establishes the foundational rules for source traceability, evidence versioning, and stage-to-stage contracts across the Vocabulary parsing pipeline. It does **not** prematurely lock the domain-specific Vocabulary field schema (which must follow source inspection), but defines the **structural invariants** every future schema must satisfy.

---

## 1. Identity vs. Evidence Versioning

A recurring failure in the previous project was confusing **stable item identity** with **evidence version** (Codex Lesson #9 & Section 10.9).

1. **Stable Record ID (`id`):**
   - Deterministically derived from intrinsic source attributes (e.g., `source_family`, `document_id`, `section_or_unit`, `entry_or_item_number`).
   - Must **never** depend on random UUIDs, execution timestamps, or arbitrary runtime iteration order.
2. **Evidence Locks (Hashes & Pointers):**
   - Downstream records (CLEAN, Matching, Categorization, PRE-FINAL) must bind to their upstream inputs via:
     - `source_sha256`: SHA-256 hash of the original file in `acquisition/local/`.
     - `upstream_file_sha256` and `upstream_json_pointer`: Exact pointer to the upstream JSON record.
     - `record_content_hash`: Semantic hash of the specific record's content and assets.
   - **Rule:** If an upstream RAW or CLEAN record changes, downstream artifacts referencing the old hash are **stale**. Never silently overwrite a stored hash in a downstream file; revalidate or explicitly rebind with proof that decision-relevant content is unchanged.

---

## 2. Exact Source Spans vs. Readable Projections

Readable output is not proof of faithful extraction (Codex Lessons #1, #2, Section 5.1 & 5.2).

Every RAW extraction record must keep these layers separate:

1. **Exact Source Evidence:**
   - Unmodified extracted text strings (including raw encoding tokens, ligatures, or PDF stream order artifacts).
   - Exact source coordinates: page number(s), character/byte slice offsets (`start`, `end`) into the stored page text, and bounding boxes (`bbox` with explicit coordinate frame and page dimensions).
2. **Readable Interpretation:**
   - Decoded text (e.g., resolved font encodings, normalized Unicode/IPA characters, spatially reordered tokens).
   - **Offset Invariant:** Because decoded strings often differ in character length from raw encoded strings, span exclusions and provenance slices must always index into the **original source string**, never the decoded string.
3. **Semantic Component Ownership:**
   - Explicit assignment of text and visuals to structural roles (e.g., headword, pronunciation, part of speech, definition, example sentence, question stem, option, header/footer exclusion).

---

## 3. Ordered Block Streams

Vocabulary documents frequently interleave prose definitions, numbered senses, bulleted collocations, usage notes, tables, and illustrations.

- **Do not split content into disconnected per-type arrays** that lose reading order (Codex Lesson #11 & Section 7.4).
- Represent multi-component content as a single **canonical ordered block stream** where each block carries its `type`, source order/line range, and content.
- Deduplication must distinguish **aliases of the same source block** from **legitimate repeated words/phrases at different source positions**.

---

## 4. Explicit Availability and Issue States

Never conflate missing source material, intentional policy skips, and parser failures (Codex Lessons #8, #12, #13):

- **Unavailable (`null` with explicit status):** E.g., a Vocabulary word list has no example sentence in the source, or an exercise sheet has an answer key without explanations. This is valid data when source unavailability is documented.
- **Policy Excluded (`excluded`):** Content intentionally skipped by project scope rules (e.g., cover pages, non-vocabulary reading sections).
- **Unresolved Extraction/Cleaning Issue (`issue` / `blocker`):** A parser or normalization defect (e.g., ambiguous entry boundary, unverified OCR/raster text, missing option). Records with unresolved issues **must be blocked** from PRE-FINAL admission.
- **Review Pending (`review_pending`):** Ambiguous semantic boundaries or AI-generated explanations/tags awaiting human or candidate-hash-bound semantic verification.

---

## 5. Manual Interventions & Supplied Overlays

Undocumented manual edits to generated JSON or HTML previews corrupt reproducibility (Codex Lesson #18 & Section 7.6):

1. **Never edit generated files in `data/raw/`, `data/clean/`, or `inspections/` by hand.**
2. If a source document has an unrecoverable print defect, missing answer key, or requires an approved manual override:
   - Store the override in a dedicated, version-controlled manual source file (e.g., `acquisition/manual_overrides/` or stage-specific `manual_sources/`).
   - Record explicit provenance: `target_id`, `source_reference`, `approval_scope`, `reason`, and `author/date`.
   - Retain the original unresolved RAW evidence alongside the manual override so parser quality metrics remain honest.
