# Project Agent Skills (`.agents/skills/`)

## 1. Intended Purpose

This directory is the **dedicated root for project-local AI agent skills**, following the architectural convention recommended in [`DOCUMENTATION_ARCHITECTURE_HANDOVER.md`](file:///c:/Users/user/Desktop/vocabulary_parser/DOCUMENTATION_ARCHITECTURE_HANDOVER.md) (Section 5).

Skills placed here encapsulate repeatable, multi-step agent workflows for the Vocabulary parsing pipeline (e.g., source profiling, profile parser creation, normalization audits, regression backtesting).

---

## 2. Directory Conventions for Adding Skills

When adding an individual skill, create a dedicated folder under this directory matching the skill name:

```text
.agents/skills/
└── <skill-name>/
    ├── SKILL.md             # Required: Entry instructions, trigger conditions, and step-by-step workflow
    ├── references/          # Optional: In-depth documentation or domain rules read only when needed
    ├── scripts/             # Optional: Deterministic Python/PowerShell helper scripts
    └── assets/              # Optional: Output templates, JSON schemas, or static resources
```

### Guidelines for Authoring Skills:
1. **`SKILL.md` is Primary:** Every skill must have a root `SKILL.md` with a clear description of when and how the skill should be invoked.
2. **Selective Reading:** Keep `SKILL.md` concise so agents do not consume excessive context. Put extensive background or domain tables into `references/` and instruct the agent to read them only when relevant.
3. **Register in Index:** Whenever a new skill is added here, register it in the Task-to-Skill Routing Table in [`docs/general/CODEX_SKILLS_USAGE.md`](file:///c:/Users/user/Desktop/vocabulary_parser/docs/general/CODEX_SKILLS_USAGE.md).
4. **No Speculative Skills:** Do not create dummy or placeholder skill folders until actual operational tasks justify them.
