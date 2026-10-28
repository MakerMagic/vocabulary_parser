---
name: processing-raw-preservation
description: Protects RAW extraction quality and prevents destructive early cleaning in the Vocabulary parsing pipeline. Use when working on PDF extraction, raw vocabulary entry/exercise parsing, font/IPA decoding, visual/table cropping, line-wrap reflow, or CLEAN normalization logic.
---

# Processing Rules and Raw Data Preservation Skill

## Purpose

Use this skill when extracting, cleaning, or transforming Vocabulary document content.

The goal is to preserve exact RAW extracted information before any normalization, cleaning, matching, or categorization happens, and to ensure transformations in CLEAN obey strict token-ledger and geometry rules.

## Main Rule

1. **RAW extraction must preserve exact source information** (`raw_text`, exact `source_spans` slice offsets, page/bbox coordinates, and raw assets).
2. **Readable ≠ Faithful:** Fluent text can still cross entry boundaries or drop phonetic/lexical markers. Always verify spatial ownership and adjacent entries ($N \pm 1$).
3. **Cleaning and normalization must happen later** and write to a separate layer (`data/clean/`).

## RAW Extraction Responsibilities (`parsers/` → `data/raw/`)

A source-profile parser must extract and preserve:
- full unmodified page/source text and exact character/byte slice spans (`start`, `end`) for every entry and component;
- readable text projection (`readable_text`) **alongside** `raw_text` when a verified font/IPA/CID mapping or spatial reading-order repair applies (never overwrite `raw_text` or index spans using decoded string lengths);
- entry/item identifier and structural components (e.g., headword, pronunciation/IPA, part of speech, numbered sense definitions, usage examples, collocations, exercise stems, options);
- image/table asset references with bounding boxes, coordinate frames, and SHA-256 hashes (distinguishing focused genuine assets from diagnostic previews);
- source file reference (`source_sha256`) and page coordinates;
- structured extraction warnings/issues (`extraction_issues`) whenever boundaries, encodings, or raster text are uncertain.

## Lexical Entry & Exercise Blocks

- Detect complete entry/item blocks using verified layout, margin, typography, and structural anchors documented in `inspections/SOURCE_PROFILES.md`.
- Distinguish top-level entry numbers from internal numbered definition senses (`1. ... 2. ...`) or list items.
- Represent multi-component entries as an **ordered block stream** so interleaved definitions, examples, notes, and tables keep their exact reading order.

## Cleaning & Normalization Rules (`processors/normalization/` → `data/clean/`)

Cleaning operates strictly on structured `data/raw/` records (never re-parsing PDFs) and writes to `data/clean/`:
- **Prose Reflow:** Join wrapped lines only when continuous layout geometry, line pitch, and grammar support continuation. Never use naive `if lowercase: join; if uppercase: paragraph` rules (which break wrapped proper nouns or merge list items).
- **Non-Whitespace Token Ledger:** Verify that reflow and whitespace normalization preserve the exact sequence of non-whitespace tokens from RAW (with approved single-character punctuation/casing rules explicitly audited).
- **Derived Asset Crops:** When removing an option marker or border from an image asset, modify only the proven marker rectangle and preserve all other pixels unmodified while keeping the RAW asset intact.
- **What Cleaning Must Never Do:** Never paraphrase definitions/examples, invent missing lexical fields, delete uncertain content, or overwrite `data/raw/`.

## Forbidden Patterns

Do not:
- hardcode record IDs in production parser or cleaner logic (`if id == ...`);
- apply universal CID offset decoders without verified font-map evidence for that specific source profile;
- join visual elements using a generic proximity radius without structural ownership proof;
- silently skip problematic entries or treat unverified raster OCR as authoritative text.

## When to Read Original Docs

Read original docs when:
- adding or updating processing rules (`docs/general/PROCESSING_RULES.md`);
- changing RAW or CLEAN data contracts (`docs/general/DATA_SCHEMA.md`, `docs/PROVENANCE_AND_CONTRACTS.md`);
- profiling a new source family (`inspections/SOURCE_PROFILES.md`).
