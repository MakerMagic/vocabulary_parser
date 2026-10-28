---
name: token-efficient-context-routing
description: Routes tasks to the minimal necessary skill and documentation files in the Vocabulary parsing repository to avoid unnecessary context loading. Use when classifying a task or deciding which skill and project files to read.
---

# Token-Efficient Context Routing Skill

## Purpose

Use this skill to avoid loading every `.md` file and every skill on routine tasks in the Vocabulary parsing repository.

## Task-to-Skill Routing Map

Classify the task first and load only the matching skill under `.agents/skills/`:

```text
Architecture, folders, stage boundaries
→ .agents/skills/project-architecture-guardrails/SKILL.md

PDF extraction, RAW parsing, font/IPA decoding, CLEAN reflow
→ .agents/skills/processing-raw-preservation/SKILL.md

Tests, span reconstruction, N±1 controls, pytest / ruff checks
→ .agents/skills/testing-validation-expectations/SKILL.md

JSON schemas, record IDs, SHA-256 locks, null/issue state semantics
→ .agents/skills/data-schema-consistency/SKILL.md

Safe editing, dependency discipline, stage artifact workflow
→ .agents/skills/safe-development-workflow/SKILL.md

Codex usage limits, config tuning, lean session habits
→ .agents/skills/token-saver-codex/SKILL.md
```

## Default Context Strategy

For ordinary tasks:
1. Read `AGENTS.md` (short router).
2. Read `docs/general/CURRENT_WORK.md` only if task continuation or milestone state matters.
3. Read **one** relevant skill's `SKILL.md` from `.agents/skills/`.
4. Inspect only the directly affected project files and tests.
5. Read full guides in `docs/general/` only when the skill summary is insufficient or when changing architecture, schema, or governance rules.

## What to Avoid

- Do not read all 7 files in `docs/general/` or both historical handover documents for a narrow single-stage task.
- Do not load all skills in `.agents/skills/` at once.
- Do not read entire generated JSON datasets when a targeted lookup or test check is sufficient.
