# Processing Rules & Invariants (`PROCESSING_RULES.md`)

## 1. Common Processing Principles

This document defines the rules for interpreting, extracting, and normalizing Vocabulary data while preserving source fidelity.

All data transformations must adhere to four cardinal principles from [`PARSING_KNOWLEDGE_TRANSFER.md`](file:///c:/Users/user/Desktop/vocabulary_parser/PARSING_KNOWLEDGE_TRANSFER.md):
1. **Fix the Earliest Responsible Stage:** Never compensate for broken RAW segmentation in CLEAN, and never mask data defects in downstream views or previews.
2. **Readable ≠ Faithful:** Fluent or grammatically correct text can still cross entry boundaries or omit source tokens. Verify spatial ownership and adjacent records.
3. **Preserve Exact Evidence:** Always retain raw text slices and original coordinate frames before deriving normalized projections.
4. **Token-Ledger Verification:** Normalization must never lose non-whitespace semantic tokens.

---

## 2. Permitted Operations by Stage

### Acquisition Stage (`acquisition/`)
- **Permitted:** Computing SHA-256 hashes; recording file origin and ingestion date; organizing unmodified sources by source family folder.
- **Prohibited:** Renaming source contents, recompressing PDFs, executing automated OCR overwrites, or changing byte contents.

### RAW Extraction Stage (`data/raw/`, `parsers/`)
- **Permitted:**
  - Segmenting source streams into entries based on verified layout, margin, or numbering anchors.
  - Slicing exact character/byte spans into stored page strings.
  - Applying font-map decoders **only** when supported by verified glyph evidence.
  - Cropping genuine visual or tabular assets and computing asset SHA-256 hashes.
  - Emitting structured findings for uncertain boundaries or unverified text.
- **Prohibited:**
  - Removing newlines destructively.
  - Discarding unrecognized tokens or glyphs.
  - Joining fragmented assets using generic proximity radii without structural ownership proof.

### CLEAN / Normalization Stage (`data/clean/`, `processors/normalization/`)
- **Permitted:**
  - Reflowing wrapped lines where typography and sentence grammar establish continuous prose.
  - Joining capitalized line continuations **only** when verified layout geometry, line pitch, and lack of list markers confirm a wrapped proper noun or title.
  - Separating distinct lexical components (e.g., separating a headword from an IPA transcription or definition) into ordered block structures.
  - Normalizing whitespace and standardizing quotes/dashes while verifying token ledgers.
- **Prohibited:**
  - Overwriting or mutating `data/raw/` records.
  - Applying naive reflow rules (e.g., `if next starts lowercase: join; if uppercase: paragraph`).
  - Stripping legitimate multi-sense numbering (`1.`, `2.`, `a.`, `b.`) from definitions.
  - Inventing missing definitions, parts of speech, or example sentences.

---

## 3. Preservation Requirements & Neighboring Controls

1. **Non-Whitespace Token Ledger:**
   - Any cleaning pass that normalizes whitespace or reflows lines must verify that the ordered sequence of non-whitespace tokens matches the RAW source tokens (with approved single-character punctuation/casing exceptions tracked in a validation audit).
2. **Adjacent Entry Verification ($N \pm 1$ Rule):**
   - Whenever an entry boundary repair is made to Entry $N$, the transformation must verify that content was not stolen from Entry $N-1$ or leaked into Entry $N+1$ (Codex Section 10.1).
3. **Asset Pixel Integrity:**
   - When deriving clean crops (e.g., removing an option label or border), only the proven label rectangle may be modified. All surrounding genuine content pixels must remain identical to the RAW asset (Codex Section 10.4).

---

## 4. Uncertainty Handling & Review States

- **Ambiguous Boundaries:** If a headword, definition sense, or exercise stem cannot be definitively segmented using layout anchors, the parser must emit a structured issue (e.g., `ambiguous_entry_boundary`) and flag the record as `review_pending`.
- **Raster / Unverified OCR:** If a document lacks native text, extracted text from raster OCR must not be accepted as authoritative without verified source fidelity checks. Unverified raster records must be tagged `raster_unverified` and blocked from downstream promotion.
- **Strict Abstention:** When an automated categorizer or classifier lacks sufficient evidence, it must abstain rather than guessing.

---

## 5. Prohibited Shortcuts (Lessons from Previous Failures)

- ❌ **Do not** hardcode record IDs in production parser or cleaner logic (e.g., `if entry_id == 'vocab_42': ...`). Hardcoded IDs belong exclusively in regression test fixtures or auditable manual overrides.
- ❌ **Do not** use global string replacements across files.
- ❌ **Do not** assume standard English regexes work across phonetic (IPA) or non-Latin script characters.
- ❌ **Do not** treat fluent generated text or LLM summaries as extracted source data.
