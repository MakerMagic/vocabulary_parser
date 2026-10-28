---
name: safe-development-workflow
description: Guides safe, stage-scoped edits, dependency discipline, and QA artifact maintenance in the Vocabulary parsing repository. Use when starting a coding task, modifying multiple files, adding dependencies, or updating pipeline artifacts.
---

# Safe Development Workflow Skill

## Purpose

Use this skill to keep edits in the Vocabulary parsing repository focused, reproducible, and architecture-compliant without broad refactors or undocumented side effects.

## Default Workflow

For each task:
1. Identify the single pipeline stage involved (`acquisition`, `inspections`, `RAW`, `CLEAN`, `matching`, `categorization`, `PRE-FINAL`, or `qa`/`tests`).
2. Load only the relevant skill and directly affected files.
3. Inspect canonical JSON in `data/` first when diagnosing data issues (HTML previews in `inspections/` are disposable views).
4. Make the smallest safe change in the **earliest responsible stage**.
5. Run focused `pytest` and `ruff` checks via `.venv\Scripts\python.exe`.
6. Regenerate `<STAGE>_BACKTESTING.md` and `<STAGE>_ISSUES.md` in `qa/` if a pipeline stage was executed or modified.
7. Update `docs/general/CURRENT_WORK.md` concisely if milestone progress changed.

## Dependency & Environment Discipline

- The project environment uses `.venv` (`c:\Users\user\Desktop\vocabulary_parser\.venv`) with pinned core dependencies in `requirements.txt` (`pdfplumber`, `pdfminer.six`, `pypdfium2`, `pillow`, `pytest`, `ruff`).
- Do not add new packages to `requirements.txt` unless the standard library and installed packages are genuinely insufficient and the task requires them.
- Keep heavy or conditional OCR packages uninstalled unless source inspection in `inspections/SOURCE_PROFILES.md` proves raster PDFs exist.

## File & Artifact Safeguards

Do not:
- modify `PARSING_KNOWLEDGE_TRANSFER.md` or `DOCUMENTATION_ARCHITECTURE_HANDOVER.md` (both are immutable historical handovers);
- manually edit generated JSON datasets in `data/` or manually alter counts in `qa/<STAGE>_BACKTESTING.md` / `qa/<STAGE>_ISSUES.md`;
- modify multiple pipeline stages in one task unless explicitly requested;
- create speculative directories or stages ahead of source inspection.

## When to Read Original Docs

Read original docs when:
- changing development policy or stage-artifact rules (`docs/general/DEVELOPMENT_RULES.md`);
- changing architecture boundaries (`docs/general/ARCHITECTURE.md`);
- checking or updating active handoff state (`docs/general/CURRENT_WORK.md`).
