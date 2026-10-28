# Vocabulary Source Profiles Registry (`SOURCE_PROFILES.md`)

> **Status:** No Vocabulary source documents have been ingested or profiled yet.
> **Rule:** Before writing or modifying any parser for a new Vocabulary document family in [`acquisition/local/`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/local), complete a source profile entry below. Do not assume a single universal parser can handle distinct document layouts (Codex Lesson #3).

---

## Pre-Parsing Inspection Checklist

When examining a new Vocabulary source family, verify and record the following:

1. **Identity & Provenance:**
   - Source family name, file format(s) (PDF, DOCX, HTML, TXT, CSV), file count, and SHA-256 hashes in `acquisition/local/`.
   - Document role: Is it a self-contained glossary/word list, a reading passage with target vocabulary, a lexical exercise paper, a standalone answer key, or an explanation document?
2. **Text Layer & Encoding Health:**
   - Does the document contain a valid native text layer, or is it raster/scanned (requiring OCR gating per Codex Section 9.5)?
   - Are there missing font maps, `(cid:...)` tokens, broken ligatures, or custom fonts for **IPA/phonetic transcriptions**, diacritics, or part-of-speech markers?
3. **Stream Order vs. Visual Geometry:**
   - Does PDF/document stream order match visual reading order? (Watch for displaced margin numbers, multi-column dictionary layouts, sidebars, or floating callouts—Codex Lesson #1 & Section 10.1).
4. **Entry / Item Boundary Signals:**
   - What structurally defines the start and end of a vocabulary entry or question? (e.g., bold headword at left margin, numbered item + punctuation, tabular row, indentation change).
   - Where could a regex-only boundary detector fail? (e.g., numbered definition senses `1. ... 2. ...` inside a single headword vs. item numbers `1. ... 2. ...`; capitalized proper nouns wrapping across lines—Codex Lessons #5 & #6).
5. **Internal Component Structure:**
   - Which components appear within an entry (headword, pronunciation/IPA, part of speech, multiple definitions, example sentences, synonyms/antonyms, question stem, options A–D/E, visuals/tables)?
   - How are they ordered, and which fields are legitimately optional (`null` when absent in source)?
6. **Non-Content Exclusions:**
   - Running headers, footers, page numbers, watermarks, cover pages, or non-vocabulary sections that must be excluded without clipping entry content.

---

## Recorded Source Profiles

*(Add one section per distinct source profile below as documents arrive in `acquisition/local/`.)*

### Template: `[Source Profile Name / ID]`

- **Files in `acquisition/local/`:** *(None yet)*
- **Document Role:** *(e.g., Glossary / Exercise Paper / Key)*
- **Text & Encoding Observations:** *(Native text vs. raster, IPA/font encoding status)*
- **Layout & Geometry Signals:** *(Single/multi-column, stream-order quirks, header/footer bounds)*
- **Entry Boundary Rules:** *(Structural anchors separating entries)*
- **Component Inventory:** *(Headword, POS, definitions, examples, options, visuals)*
- **Known Edge Cases / Positive & Negative Control Candidates:** *(Specific pages/entries to use as test fixtures)*
