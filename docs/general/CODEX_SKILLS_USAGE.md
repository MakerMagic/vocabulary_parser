# Codex Skills Usage & Routing (`CODEX_SKILLS_USAGE.md`)

## 1. Purpose & Authority

This guide connects specific development tasks in the **Vocabulary Document-Parsing Project** to relevant AI agent skills while preventing unnecessary context loading.

It serves as an **index and routing router**, not a duplicate container for skill bodies or policies.

---

## 2. Skills Directory Location & Organization

As recommended in [`DOCUMENTATION_ARCHITECTURE_HANDOVER.md`](file:///c:/Users/user/Desktop/vocabulary_parser/DOCUMENTATION_ARCHITECTURE_HANDOVER.md) (Section 5), custom project-local skills reside under:

👉 **[`.agents/skills/`](file:///c:/Users/user/Desktop/vocabulary_parser/.agents/skills)**

Each project skill added in the future should follow this structure:

```text
.agents/skills/
└── <skill-name>/
    ├── SKILL.md             # Primary instructions, trigger conditions, and workflow
    ├── references/          # Optional: in-depth references read only when needed
    ├── scripts/             # Optional: executable helper utilities
    └── assets/              # Optional: templates and static resources
```

---

## 3. Task-to-Skill Routing Table

> **Current Status:** The `.agents/skills/` directory is initialized and ready to receive skills. No custom project skills have been installed or created yet.
> Built-in Antigravity/Codex platform skills available in the environment are listed below alongside placeholders for planned domain skills.

| Task Category | Applicable Skill | Skill Location | Applicability |
|---|---|---|---|
| **Scheduled Pipeline Automations** | `automation` | Built-in environment | Optional: use when recurring background parsing or validation is needed. |
| **Interactive Visualizations / Rich Previews** | `generative_ui` | Built-in environment | Optional: use for diagnostic visual rendering beyond plain markdown. |
| **Custom Agent Extensions / Plugins** | `plugin` / `agy-customizations` | Built-in environment | Optional: use when packaging new multi-skill agent workflows. |
| **Source Document Profiling** *(Planned)* | *TBD (source-profiler)* | `.agents/skills/source-profiler` | Required once added: guides document layout, font-map, and boundary discovery. |
| **RAW Parser Development** *(Planned)* | *TBD (raw-parser-builder)* | `.agents/skills/raw-parser-builder` | Required once added: enforces exact span retention and `validate_raw` tests. |
| **CLEAN Normalization & Reflow** *(Planned)* | *TBD (clean-normalizer)* | `.agents/skills/clean-normalizer` | Required once added: enforces token ledgers, proper-noun wrap rules, and field splitting. |

---

## 4. Selective Context Loading Guidelines

Agents must obey the following reading discipline to conserve context:

1. **Do Not Preload All Skills:** Read `CODEX_SKILLS_USAGE.md` first to determine if a skill exists for the active task.
2. **Read Entry `SKILL.md` First:** When a skill is selected, read only its top-level `SKILL.md`.
3. **Defer References:** Do not read files in `references/`, `scripts/`, or `assets/` unless the primary `SKILL.md` explicitly directs you to do so for the specific problem at hand.
4. **Physical Presence vs. Runtime Availability:** Verify that a referenced skill physically exists in `.agents/skills/<skill-name>/SKILL.md` or the active agent catalog before attempting to execute its workflow.

---

## 5. Maintenance Rules

- When a new skill is added to `.agents/skills/`:
  1. Add an entry to the Task-to-Skill Routing Table above with its exact path and trigger condition.
  2. Verify that its `SKILL.md` contains valid metadata and instructions.
- Never paste the full text of a skill or prompt template into this routing document.
