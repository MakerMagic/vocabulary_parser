# Project Agent Skills (`.agents/skills/`)

## 1. Intended Purpose

This directory is the **dedicated root for project-local AI agent skills**, following the architectural convention in [`DOCUMENTATION_ARCHITECTURE_HANDOVER.md`](file:///c:/Users/user/Desktop/vocabulary_parser/DOCUMENTATION_ARCHITECTURE_HANDOVER.md) (Section 5).

Skills placed here encapsulate repeatable, stage-safe agent workflows for the Vocabulary parsing pipeline.

---

## 2. Installed Project Skills

| Skill Name | Path | Purpose |
|---|---|---|
| `project-architecture-guardrails` | [`.agents/skills/project-architecture-guardrails/SKILL.md`](file:///c:/Users/user/Desktop/vocabulary_parser/.agents/skills/project-architecture-guardrails/SKILL.md) | Preserves modular stage separation (`acquisition`, `inspections`, `RAW`, `CLEAN`, `matching`, `categorization`, `PRE-FINAL`). |
| `processing-raw-preservation` | [`.agents/skills/processing-raw-preservation/SKILL.md`](file:///c:/Users/user/Desktop/vocabulary_parser/.agents/skills/processing-raw-preservation/SKILL.md) | Enforces exact RAW span retention, dual `raw_text`/`readable_text` layers, and token-ledger-verified CLEAN reflow. |
| `testing-validation-expectations` | [`.agents/skills/testing-validation-expectations/SKILL.md`](file:///c:/Users/user/Desktop/vocabulary_parser/.agents/skills/testing-validation-expectations/SKILL.md) | Enforces source-slice reconstruction tests, $N \pm 1$ adjacent-entry controls, positive/negative regression guards, and QA stage pairs. |
| `data-schema-consistency` | [`.agents/skills/data-schema-consistency/SKILL.md`](file:///c:/Users/user/Desktop/vocabulary_parser/.agents/skills/data-schema-consistency/SKILL.md) | Protects deterministic record IDs, SHA-256 provenance locks, ordered block streams, and `null`/`excluded`/`issue`/`review_pending` separation. |
| `safe-development-workflow` | [`.agents/skills/safe-development-workflow/SKILL.md`](file:///c:/Users/user/Desktop/vocabulary_parser/.agents/skills/safe-development-workflow/SKILL.md) | Guides stage-scoped edits, `.venv` dependency discipline, and canonical JSON inspection rules. |
| `token-efficient-context-routing` | [`.agents/skills/token-efficient-context-routing/SKILL.md`](file:///c:/Users/user/Desktop/vocabulary_parser/.agents/skills/token-efficient-context-routing/SKILL.md) | Routes tasks to the minimal necessary skill and documentation files to conserve context. |
| `token-saver-codex` | [`.agents/skills/token-saver-codex/SKILL.md`](file:///c:/Users/user/Desktop/vocabulary_parser/.agents/skills/token-saver-codex/SKILL.md) | Lean-execution rules and audit scripts (`scripts/audit.mjs`) for stretching agent usage limits. |

---

## 3. Directory Conventions for Skills

Each skill resides in its own subdirectory:

```text
.agents/skills/
└── <skill-name>/
    ├── SKILL.md             # Required: YAML frontmatter (name, description) + workflow instructions
    ├── references/          # Optional: In-depth documentation read only when needed
    ├── scripts/             # Optional: Deterministic helper scripts
    └── assets/              # Optional: Templates or static resources
```

Whenever a skill is added or updated here, keep [`docs/general/CODEX_SKILLS_USAGE.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/CODEX_SKILLS_USAGE.md) synchronized.
