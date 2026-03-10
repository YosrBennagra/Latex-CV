---
name: skill-agent-governance
description: >-
  Use when adding, removing, or updating skills or agents; when the skill index
  in copilot-instructions drifts from the actual files; when a new technology is
  added to the project; or when an agent's responsibilities expand.
---

# Skill & Agent Governance

Keep the skill library, agent roster, and routing index consistent as the project evolves.

---

## Follow This Workflow

### Adding a Skill

1. Create `.github/skills/<Domain>/<Skill Name>/SKILL.md` following the Skill Authoring Guide.
2. Add a keyword → path entry to `.github/copilot-instructions.md`.
3. Verify the skill has proper YAML frontmatter (`name`, `description` starting with "Use when...").

### Adding or Modifying an Agent

1. Create/edit `<name>.agent.md` in `.github/agents/`.
2. If the agent's description changes, update `copilot-instructions.md` and `CLAUDE.md` if referenced.

### Auditing After Skill Changes

Run this checklist after any batch of skill/agent changes:

| Check | What to verify |
|---|---|
| **Files match index** | Every `SKILL.md` under `.github/skills/` has a keyword entry in `.github/copilot-instructions.md` |
| **No orphans** | No keyword entries pointing to nonexistent skill files |
| **Agent roster** | Agent files in `.github/agents/` match any agent references in copilot-instructions |
| **Frontmatter** | Every SKILL.md has `name` (kebab-case) and `description` (starts with "Use when...") |

---

## Decision Rules

| Situation | Action |
|---|---|
| New skill created | Add keyword entry to `.github/copilot-instructions.md` |
| Skill renamed or moved | Update keyword path in copilot-instructions |
| Skill deleted | Remove keyword entry from copilot-instructions |
| New agent added | Create `.agent.md` in `.github/agents/` |
| Agent responsibilities changed | Review if copilot-instructions keywords need updating |

---

## Quality Bar

- Zero orphaned skills (files without index entries)
- Zero stale entries (index entries pointing to nonexistent files)
- Copilot instructions reference only files that actually exist
- Skill rules match the real `.github/` folder structure in this repo

---

## Avoid These Failure Modes

- **Index drift** — adding skills but forgetting to update `.github/copilot-instructions.md`
- **Orphaned entries** — copilot-instructions referencing deleted or moved skills
- **Missing frontmatter** — SKILL.md files without proper `name`/`description` YAML
