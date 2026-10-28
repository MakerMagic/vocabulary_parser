# Codex Skills Usage & Tooling Guide (`CODEX_SKILLS_USAGE.md`)

## 1. Purpose & Authority

Use this guide to decide which project skill and environment tool to load for a task in the **Vocabulary Document-Parsing Project**.

Do not read all skills or all project docs by default. It serves as an **index and routing guide**, not a duplicate container for skill bodies.

---

## 2. Skills Directory Location & Organization

All project-local skills are installed under the unified root recommended by [`DOCUMENTATION_ARCHITECTURE_HANDOVER.md`](file:///c:/Users/user/Desktop/vocabulary_parser/DOCUMENTATION_ARCHITECTURE_HANDOVER.md) (Section 5):

👉 **[`.agents/skills/`](file:///c:/Users/user/Desktop/vocabulary_parser/.agents/skills)**

```text
.agents/skills/
├── README.md
├── project-architecture-guardrails/
│   └── SKILL.md
├── processing-raw-preservation/
│   └── SKILL.md
├── testing-validation-expectations/
│   └── SKILL.md
├── data-schema-consistency/
│   └── SKILL.md
├── safe-development-workflow/
│   └── SKILL.md
├── token-efficient-context-routing/
│   └── SKILL.md
└── token-saver-codex/
    ├── SKILL.md
    ├── assets/
    ├── references/
    └── scripts/
```

---

## 3. Installed Project Skills & Task Routing

### Core Active Skills

| Task Type | Skill Name | Exact Location | Applicability |
|---|---|---|---|
| **Architecture, folders, stage boundaries** | `project-architecture-guardrails` | [`.agents/skills/project-architecture-guardrails/SKILL.md`](file:///c:/Users/user/Desktop/vocabulary_parser/.agents/skills/project-architecture-guardrails/SKILL.md) | **Required** when adding directories, creating parser/processor modules, or checking stage ownership. |
| **PDF parsing, RAW extraction, font/IPA decoding, CLEAN reflow** | `processing-raw-preservation` | [`.agents/skills/processing-raw-preservation/SKILL.md`](file:///c:/Users/user/Desktop/vocabulary_parser/.agents/skills/processing-raw-preservation/SKILL.md) | **Required** when extracting raw entries, preserving `source_spans`, decoding fonts, or normalizing prose. |
| **Tests, span reconstruction, $N \pm 1$ controls, `pytest` / `ruff` checks** | `testing-validation-expectations` | [`.agents/skills/testing-validation-expectations/SKILL.md`](file:///c:/Users/user/Desktop/vocabulary_parser/.agents/skills/testing-validation-expectations/SKILL.md) | **Required** when writing or updating `pytest` suites, regression fixtures, or stage QA artifacts. |

### Optional & Specialized Skills

Use these only when the task specifically involves their domain:

| Task Type | Skill Name | Exact Location | Applicability |
|---|---|---|---|
| **JSON schemas, deterministic IDs, SHA-256 locks, `null`/`issue` states** | `data-schema-consistency` | [`.agents/skills/data-schema-consistency/SKILL.md`](file:///c:/Users/user/Desktop/vocabulary_parser/.agents/skills/data-schema-consistency/SKILL.md) | **Optional:** Load when designing or validating `data/raw/`, `data/clean/`, or downstream JSON contracts. |
| **Safe editing, `.venv` dependencies, stage artifact workflow** | `safe-development-workflow` | [`.agents/skills/safe-development-workflow/SKILL.md`](file:///c:/Users/user/Desktop/vocabulary_parser/.agents/skills/safe-development-workflow/SKILL.md) | **Optional:** Load when modifying multiple files, updating `requirements.txt`, or checking change scope. |
| **Unsure which skill or doc to load** | `token-efficient-context-routing` | [`.agents/skills/token-efficient-context-routing/SKILL.md`](file:///c:/Users/user/Desktop/vocabulary_parser/.agents/skills/token-efficient-context-routing/SKILL.md) | **Optional:** Load when classifying a task to minimize context usage. |
| **Agent token/credit limits, session efficiency, config audit** | `token-saver-codex` | [`.agents/skills/token-saver-codex/SKILL.md`](file:///c:/Users/user/Desktop/vocabulary_parser/.agents/skills/token-saver-codex/SKILL.md) | **Optional:** Load when auditing token usage (`node .agents/skills/token-saver-codex/scripts/audit.mjs --agent codex`) or stretching session limits. |

---

## 4. Installed PDF-Processing Tools & Libraries

The Python virtual environment is configured at **[`.venv/`](file:///c:/Users/user/Desktop/vocabulary_parser/.venv)** (Python `3.13.16`) and pinned in **[`requirements.txt`](file:///c:/Users/user/Desktop/vocabulary_parser/requirements.txt)** (also installed in the system Python `3.13.16` site-packages).

### Installed & Verified Resources

| Exact Name | Version / Type | Location / Invocation | Intended Role in Vocabulary Workflow | Usage Limitations |
|---|---|---|---|---|
| `pdfplumber` | `0.11.10` (Python library) | `.venv\Scripts\python.exe -c "import pdfplumber"` | Primary text, line, character, and coordinate extraction for RAW parsers; geometry for column flow, headwords, and entry boundaries. | PDF stream order can differ from visual reading order; missing font maps yield `(cid:...)`; raster text is not recovered natively. |
| `pdfminer.six` | `20260107` (Python library) | `.venv\Scripts\python.exe -c "import pdfminer"` | Low-level font map, character encoding, and vector-object inspection (underlying engine of `pdfplumber`). Used to diagnose IPA/phonetic fonts and CID tokens. | CID codes and font sizes cannot be interpreted universally across unrelated PDF families. |
| `pypdfium2` | `5.14.0` (Python library) | `.venv\Scripts\python.exe -c "import pypdfium2"` | Page rendering, focused visual/table asset cropping, and independent visual verification of extracted text. | Rendering does not prove component ownership; incorrect bounding boxes still produce incorrect crops. |
| `Pillow (PIL)` | `12.3.0` (Python library) | `.venv\Scripts\python.exe -c "import PIL"` | Image crop inspection, pixel-preservation verification, and diagnostic image processing. | Rescaling or contrast changes cannot recover already-clipped glyphs. |
| `pytest` | `9.1.1` (Testing framework) | `.venv\Scripts\pytest.exe` / `python -m pytest` | Automated unit, source-span reconstruction, $N \pm 1$ adjacent-entry, and positive/negative regression checks in [`tests/`](file:///c:/Users/user/Desktop/vocabulary_parser/tests). | Real-source tests skipping when local PDFs are absent do not count as passing source-regression proof. |
| `ruff` | `0.16.10` (Linter / formatter) | `.venv\Scripts\ruff.exe` / `python -m ruff` | Fast static analysis and formatting checks on modified Python modules. | Checks Python syntax/style only; does not verify extraction fidelity. |
| `hashlib.sha256` + JSON pointers | Python standard library | `import hashlib` | Binding `acquisition/local/` files, `data/raw/` records, assets, and downstream projections to exact evidence versions. | Detects file/record drift; does not prove semantic correctness by itself. |
| `python -m http.server` | Python standard library | `.venv\Scripts\python.exe -m http.server 8765 --bind 127.0.0.1` | Loopback HTTP preview server when inspecting a selected disposable HTML preview in [`inspections/`](file:///c:/Users/user/Desktop/vocabulary_parser/inspections). | Preview delivery only; not a parser or validator. |
| `git`, `rg`, `PowerShell`, `node` | CLI utilities / shell | `git`, `rg` (ripgrep), `powershell`, `node` | Version control, fast repository pattern search (`rg`), command execution, and running `.agents/skills/token-saver-codex/scripts/audit.mjs`. | Text search (`rg`) never substitutes for checking PDF layout geometry. |

### Conditional / Deferred Resources (Not Installed Pre-emptively)

- **Local OCR packages (`tesseract.js + eng.traineddata`, `pix2text`, `cnocr`):** Intentionally kept uninstalled until initial source inspection in [`inspections/SOURCE_PROFILES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/inspections/SOURCE_PROFILES.md) determines whether any Vocabulary PDFs lack a native text layer.
- **Browser layout automation (`Playwright` + Microsoft Edge `msedge`):** Microsoft Edge (`msedge.exe`) is present at `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`; `Playwright` is deferred until the `PRE-FINAL` / rendering preview stage is implemented.
- **Repository utilities (`normalize_text`, `token_ledger`):** Domain concepts from the prior repository. Their architectural rules are codified in [`PROCESSING_RULES.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/PROCESSING_RULES.md) and `.agents/skills/processing-raw-preservation/SKILL.md`, to be implemented as clean Python modules when the `CLEAN` stage is built.

### Excluded Resources (Irrelevant to Vocabulary)

- **`parsers.mathematics.formulas` & `MathML`:** Specific to mathematical fraction/radical/system geometry and LaTeX-to-MathML rendering; not applicable to Vocabulary prose and lexical entries.
- **`view_image`:** Assistant-internal tool name from the prior environment; image inspection in this workspace uses the native `read_file` tool.

---

## 5. Selective Context Loading & Prompt Examples

For ordinary tasks, read in this order:
1. [`AGENTS.md`](file:///c:/Users/user/Desktop/vocabulary_parser/AGENTS.md)
2. [`docs/general/CURRENT_WORK.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/CURRENT_WORK.md) (if task continuation matters)
3. **One** relevant skill from `.agents/skills/<skill-name>/SKILL.md`
4. Directly relevant project files only

Read full guides in `docs/general/` only when changing architecture, schema, processing rules, development rules, adding a new source profile, or resolving ambiguity not covered by the skill.

### Good Prompt Examples

```text
Use AGENTS.md and .agents/skills/processing-raw-preservation/SKILL.md.
Inspect the new PDF in acquisition/local/ and document its profile in inspections/SOURCE_PROFILES.md.
Do not write parser code yet.

Use AGENTS.md and .agents/skills/testing-validation-expectations/SKILL.md.
Add span-reconstruction and adjacent-entry pytest checks in tests/.
Do not modify stage boundaries.
```
