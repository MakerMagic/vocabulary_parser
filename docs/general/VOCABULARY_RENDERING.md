# Vocabulary Rendering Stage Documentation (`VOCABULARY_RENDERING.md`)

> **Stage Name:** Vocabulary Rendering  
> **Status:** Implemented & Verified  
> **Package:** [`processors/rendering/`](file:///c:/Users/user/Desktop/vocabulary_parser/processors/rendering)  
> **Module Interfaces:** [`contract.py`](file:///c:/Users/user/Desktop/vocabulary_parser/processors/rendering/contract.py), [`renderer.py`](file:///c:/Users/user/Desktop/vocabulary_parser/processors/rendering/renderer.py), [`template.py`](file:///c:/Users/user/Desktop/vocabulary_parser/processors/rendering/template.py)

---

## 1. Stage Purpose & Scope

The **Vocabulary Rendering Stage** prepares validated vocabulary records for future website display and implements an accurate, source-independent HTML preview system.

### Scope Boundaries
- **Parser-Side Stage:** Implemented entirely within the vocabulary parsing repository.
- **No Direct Website Integration:** Creates preview models and backtesting views without modifying external website production code.
- **Strict Read-Only Discipline:** Evaluates existing vocabulary records without re-running earlier stages (Acquisition, RAW, Cleaning, Enrichment, Difficulty, Validation) or silently altering source records.

---

## 2. Zero Unresolved Issues Admission Criteria

To guarantee that defective or unapproved vocabulary items never enter user-facing interfaces, the Rendering Stage enforces a strict admission gate:

```text
Admission Criteria:
  1. Record validation status MUST be "validated"
  2. Record "final_output_eligible" flag MUST be true
  3. Validation error count MUST be zero (no active errors)
  4. Linguistic / curriculum review notes MUST be null (no "review_pending")
  5. Mandatory fields present and non-empty:
     - English headword (string)
     - Part of speech (string)
     - Russian translation and alternatives (1 to 2 alternatives)
     - English explanation (>= 15 characters, non-circular)
     - Preset classification (e.g. "Basics", "nature")
     - Difficulty classification ("Easy", "Medium", "Hard")
```

Any record failing any of these conditions is **BLOCKED** from rendering as an active website flashcard.

---

## 3. Reusable Visual Layout Architecture

Rendering produces a single unified review document structured into two distinct vertical areas:

### Area A: Website Display Preview (Top)
- **Eligible Records:**
  - Faithfully reproduces the production website card design:
  - Rounded card container (`border-radius: 24px`, white background, subtle border, max-width `640px`, padding `36px 40px`).
  - Top header: English headword in bold black (`20px`, font-weight `800`) followed by part of speech in italics (`15.5px`, color `#64748b`), with a bookmark outline SVG icon aligned right.
  - Vertical spacing: `76px` between header and main text.
  - Russian translation: Large bold Cyrillic headline (`42px`, font-weight `800`, color `#0f172a`), comma-separated if multiple alternatives (e.g. `пышный, буйный`).
  - English explanation: Positioned directly beneath translation (`16.5px`, color `#64748b`, line-height `1.48`).
- **Blocked / Ineligible Records:**
  - Displays a coral/red diagnostic notification banner (`.ineligible-card`).
  - Clearly flags `NOT ELIGIBLE FOR WEBSITE DISPLAY`, identifies upstream status (`EXCLUDED` or `REVIEW_PENDING`), and provides the exact admission exclusion reason.

### Area B: Technical Quality Assurance & Upstream Audit (Bottom)
- Positioned below Area A, separated by a distinct section divider.
- Top metadata row: Record number, headword, record ID, Preset badge, Difficulty tier badge, Type badge, Final Output eligibility badge, and Validation Status badge.
- Four comprehensive stage audit panes:
  1. **Acquisition & RAW Extraction:** Source file path, SHA-256 hash, raw headword, exact source character/line spans, extraction verification status.
  2. **Cleaning & Normalization:** Headword lemma, token-ledger match status, curriculum status, exclusion reason, spelling convention.
  3. **Vocabulary Enrichment:** Part of speech, numbered Russian alternatives list (enforcing <=2 alternatives), contextual English explanation.
  4. **Difficulty & Final Eligibility:** CEFR level, Difficulty tier (`Easy`/`Medium`/`Hard`), Preset, Rendering admission verdict (`ADMITTED` / `BLOCKED`), stage QA issues.

---

## 4. Single Reusable Template Architecture

In accordance with project architectural guardrails, individual static HTML files are **not** pre-generated for every individual word in the repository.

Instead, the system utilizes **ONE reusable template** (`processors/rendering/template.py`) dynamically invoked by:
1. **The Rendering Engine API:** `processors.rendering.renderer.render_record(record)`.
2. **The Batch Audit Engine:** `processors.rendering.renderer.audit_and_render_all()`.
3. **The PowerShell Backtesting CLI:** `python tools/vocabulary_review.py --source <source> --word <query>`.

---

## 5. Read-Only Systematic Repository Audit Results

A complete read-only audit across all **1,015 records** in the repository yielded the following verified distribution:

| Dataset / Source | Total Records | Admitted (Eligible) | Blocked (Ineligible) | Blocked: Policy Exclusions | Blocked: Review Pending | Active Errors |
|---|---|---|---|---|---|---|
| **`uclouvain`** | 413 | 379 | 34 | 29 (A1/A2) | 5 | 0 |
| **`new_words`** | 159 | 154 | 5 | 3 (A1/A2) | 2 | 0 |
| **`nature`** | 169 | 142 | 27 | 27 (A1/A2) | 0 | 0 |
| **`math_basics`** | 274 | 183 | 91 | 91 (Duplicate term) | 0 | 0 |
| **Total Repository** | **1,015** | **858** | **157** | **150** | **7** | **0** |

### Blocked Records Breakdown
- **Policy-Excluded Elementary A1/A2 Words (59 records):**
  - `uclouvain` (29 words): systematically excluded elementary A1/A2 words (e.g. `sure`).
  - `new_words` (3 words): `Repair`, `Several`, `Nearly`.
  - `nature` (27 words): elementary terms (e.g. `Food`, `Sun`, `Earth`, `Natural`). Note: 12 explicitly approved A2 nature terms (`Whales`, `Wind`, `Oil`, etc.) remain admitted and eligible.
- **Policy-Excluded Duplicate Terms (91 records):**
  - `math_basics` (91 duplicate occurrences): duplicate study section terms preserved for provenance but excluded from user-facing flashcard presentation in favor of the canonical master record.
- **Pending Review (7 records):**
  - `uclouvain` (5 words): `#2 account (for)`, `#206 should`, `#252 certain`, `#347 present`, `#402 unlike`.
  - `new_words` (2 words): `#27 Necessitates` (inflected form), `#126 Opulent` (semantic contrast note).
- **Validation Errors (0 records):**
  - Zero active errors across all datasets.

---

## 6. PowerShell Backtesting Verification

The CLI tool [`tools/vocabulary_review.py`](file:///c:/Users/user/Desktop/vocabulary_parser/tools/vocabulary_review.py) seamlessly integrates the Vocabulary Rendering Stage:

```powershell
# 1. Backtest eligible word (renders website card + metadata)
.\.venv\Scripts\python.exe tools/vocabulary_review.py --source nature --word "Whales"

# 2. Backtest policy-excluded word (renders diagnostic blocked card + metadata)
.\.venv\Scripts\python.exe tools/vocabulary_review.py --source nature --word "Food"

# 3. Backtest review-pending word (renders diagnostic blocked card + metadata)
.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "account for"

# 4. Backtest mathematical vocabulary word (renders website card + metadata)
.\.venv\Scripts\python.exe tools/vocabulary_review.py --source math_basics --word "altitude"

# 5. Backtest duplicate mathematical word (shows master admitted card + duplicate blocked cards)
.\.venv\Scripts\python.exe tools/vocabulary_review.py --source math_basics --word "decimal"
```
