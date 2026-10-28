# Processing Rules & Invariants (`PROCESSING_RULES.md`)

## 1. Absolute Stage-Execution Rule

> [!IMPORTANT]
> **Agents must NEVER execute a processing stage without explicit user authorization.**
> 
> - A request for Stage $X$ authorizes Stage $X$ **ONLY**.
> - Do not automatically proceed to Stage $X+1$.
> - After completing the authorized stage: 1) Save outputs, 2) Validate stage results, 3) Document issues, 4) Document backtesting, 5) Update `CURRENT_WORK.md`, 6) **STOP**.

---

## 2. Common Processing Principles

All data transformations must adhere to four cardinal principles from `PARSING_KNOWLEDGE_TRANSFER.md`:

1. **Fix the Earliest Responsible Stage:** Never compensate for broken RAW segmentation in CLEAN, and never mask data defects in downstream views or previews.
2. **Readable ≠ Faithful:** Fluent or grammatically correct text can still cross entry boundaries or omit source tokens. Verify spatial ownership and adjacent records.
3. **Preserve Exact Evidence (5 Codex RAW Principles):**
   - **Exact Source Text & Spans:** Store the full unmodified source text alongside exact slice offsets (`start`, `end`) for every extracted entry, line, and component. It must be possible to reconstruct every extracted entry's raw text directly from unchanged source slices (`validate_raw` invariant).
   - **Readable Text Interpretation:** Store readable projections *alongside* exact original strings—never overwrite the original text.
   - **Semantic Component Ownership:** Explicitly record which entry and sub-component owns each text span or visual object.
   - **Focused Genuine Assets vs. Diagnostic Previews:** Separate genuine content assets (tables, illustrations) from debugging previews.
   - **Honest Extraction Issues:** Emit structured RAW findings whenever segmentation, encoding, visual ownership, or raster/OCR fidelity is uncertain. Never mask uncertainty via destructive cleanup.
4. **Token-Ledger Verification:** Normalization must never lose non-whitespace semantic tokens.

---

## 3. Permitted & Prohibited Operations by Stage

### Acquisition Stage (`acquisition/sources/<source_id>/`)
- **Permitted:** Computing SHA-256 hashes; recording file origin, line counts, format, and ingestion date; organizing sources by dedicated source directory.
- **Prohibited:** Renaming source contents, recompressing PDFs, executing automated OCR overwrites, or changing byte contents.

### RAW Extraction Stage (`data/raw/sources/<source_id>/`, `parsers/<source_id>/`)
- **Permitted:**
  - Segmenting source streams into entries based on verified layout, margin, or numbering anchors.
  - Slicing exact character/byte spans into stored page strings.
  - Applying font-map decoders **only** when supported by verified glyph evidence.
  - Cropping genuine visual or tabular assets and computing asset SHA-256 hashes.
  - Emitting structured findings for uncertain boundaries or unverified text.
- **Prohibited:**
  - Removing newlines destructively.
  - Discarding unrecognized tokens or glyphs.
  - Deduplicating cross-section homographs (e.g., `present` in verb vs. adjective sections must remain separate records).

### CLEAN / Normalization Stage (`data/clean/sources/<source_id>/`, `processors/normalization/`)
- **Permitted:**
  - Reflowing wrapped lines where typography and sentence grammar establish continuous prose.
  - Separating distinct lexical components (e.g., separating base lemma `account` from parenthetical particle `for`) into ordered block structures while keeping `word` intact.
  - Normalizing whitespace and standardizing quotes/dashes while verifying token ledgers.
  - Initializing `"difficulty": null`.
- **Prohibited:**
  - Overwriting or mutating RAW records.
  - Applying naive reflow rules.
  - Stripping parenthetical particles or hyphens from `word`.
  - Silently altering British or American spelling conventions.
  - Populating non-null `difficulty` values.

### Vocabulary Enrichment Stage (`processors/enrichment/`)
- **Permitted:**
  - Assigning accurate grammatical Part of Speech.
  - Populating Russian translation: **Maximum of TWO translation alternatives per entry**. Each alternative may consist of multiple Russian words.
  - Populating clear, non-circular English explanations (`>= 15` chars, headword lemma excluded).
  - Flagging polysemous or morphologically sensitive records as `review_pending`.
- **Prohibited:**
  - Restricting translations to an arbitrary word limit (e.g., the obsolete "two-word" cap).
  - Exceeding two translation alternatives per entry.
  - Truncating multiword translations (e.g., `в отличие от` or `снимать одежду`).
  - Using circular explanations that repeat the headword lemma.
  - Silently guessing senses on ambiguous entries.

---

## 4. Source Independence Invariants

- Shared processors (`processors/provenance.py`, `processors/stage_artifacts.py`) must remain completely source-agnostic.
- Source-specific logic (e.g., comma-delimited lists, section headers `233 verbs`) must live exclusively within that source's parser and documentation (`parsers/<source>/`, `docs/sources/<source>/`).
- A bug fix or layout adjustment for one source must never alter or regress processing for another source.
