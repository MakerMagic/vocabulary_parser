# Inspections (`inspections/`)

## 1. Intended Responsibility

The `inspections/` directory is dedicated to **examining and documenting source document characteristics** before parser development, and hosting **targeted, disposable diagnostic previews** during development.

As established in [`PARSING_KNOWLEDGE_TRANSFER.md`](file:///c:/Users/user/Desktop/vocabulary_parser/PARSING_KNOWLEDGE_TRANSFER.md) (Lessons #3, #15, Section 13.2):
- Different document layouts require distinct source profiles rather than a single universal parser.
- Canonical JSON in `data/` is the inspection authority; generated HTML/image previews are disposable views over canonical data.

---

## 2. What Belongs Here

- **[`SOURCE_PROFILES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/inspections/SOURCE_PROFILES.md):** Structured pre-parsing documentation of each Vocabulary source family's layout, typography, encoding, entry boundaries, and anomalies.
- **Targeted diagnostic exports (when needed later):** Selected single-record or small-sample HTML/image inspection outputs generated on demand to diagnose a specific layout or crop question.

---

## 3. What Must NOT Be Stored Here

- **No canonical dataset files:** Never treat files in `inspections/` as pipeline inputs or authoritative outputs. Canonical data lives exclusively in `data/`.
- **No mass static catalogs:** Do not generate hundreds of per-entry HTML files or static full-bank reports (Codex Section 14, #12). Keep inspection outputs targeted and disposable.
- **No manual data repairs:** Editing an HTML preview or inspection snippet does not fix the dataset (Codex Section 13.2). Fix the responsible upstream stage (`parsers/` or `processors/`) and regenerate.
- **No stage issue registries:** Formal stage defect tracking and `<STAGE>_BACKTESTING.md` / `<STAGE>_ISSUES.md` pairs belong in [`qa/`](file:///c:/Users/user/Desktop/vocabulary_parser/qa).

---

## 4. Relationship to Other Parts of the Project

1. **Consumes [`acquisition/local/`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/local):** Source files placed in `acquisition/local/` are inspected first to populate [`SOURCE_PROFILES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/inspections/SOURCE_PROFILES.md).
2. **Guides Future `parsers/`:** A parser module may only be designed after its source profile (entry anchors, stream order vs. geometry, encoding health, visual ownership) is recorded here.
3. **Complements [`qa/`](file:///c:/Users/user/Desktop/vocabulary_parser/qa):** When [`qa/`](file:///c:/Users/user/Desktop/vocabulary_parser/qa) identifies a recurring defect in `data/raw/` or downstream stages, targeted inspection views can be rendered here to verify the root cause against the source document.
