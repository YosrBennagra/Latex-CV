---
name: scaffold-project-skills
description: 'Use when bootstrapping a new project''s .github/skills/ folder structure, creating empty SKILL.md files adapted to detected technologies. Covers technology detection, domain selection, folder creation, and empty skill stubs.'
---

# Scaffold Project Skills

## Overview

Scan a project's tech stack and create a `.github/skills/` folder tree with empty `SKILL.md` stubs for every relevant domain. Skills are selected by matching detected technologies to the catalog in `references/scaffold-skill-catalog.md`.

## When to Use

- Setting up a new project's skill library from scratch
- Bootstrapping `.github/skills/` for an existing repo that has none
- When NOT to use: the project already has a populated skills folder

## Core Pattern

### 1. Detect the stack

Scan for: `package.json`, `tsconfig.json`, `Dockerfile`, `docker-compose*`, `prisma/schema.prisma`, `.github/workflows/`, `tailwind.config*`, `next.config*`, `sonar-project.properties`, `pnpm-workspace.yaml`, auth config files, and test config files (`vitest`, `jest`, `playwright`).

### 2. Map technologies to skills

Use [`references/scaffold-skill-catalog.md`](references/scaffold-skill-catalog.md) to select domains and skill names based on detected technologies. Always include Universal Skills.

### 3. Create the folder tree

For each selected skill:

```
.github/skills/{Domain Name}/{Skill Name}/SKILL.md
```

### 4. Write empty stubs

Each `SKILL.md` gets this template:

```yaml
---
name: {kebab-case-name}
description: 'Use when ... (fill in later).'
---

# {Skill Name}

<!-- TODO: Fill in skill content -->
```

### 5. Generate copilot-instructions.md index

Create `.github/copilot-instructions.md` with a keyword → skill path table matching all scaffolded skills.

## Quick Reference

| Step | Command |
|---|---|
| Detect stack | Read `package.json` deps, scan for config files |
| Map skills | Cross-reference `references/scaffold-skill-catalog.md` |
| Create folders | `mkdir -p .github/skills/{Domain}/{Skill}` |
| Write stubs | Write minimal frontmatter `SKILL.md` per skill |
| Generate index | Build keyword table in `copilot-instructions.md` |

## Common Mistakes

- **Creating skills for technologies not in the project** — only scaffold what's detected
- **Filling in skill content during scaffold** — stubs should be empty; content comes later
- **Forgetting the index** — without `copilot-instructions.md`, agents can't find the skills
- **Using spaces in `name` frontmatter** — must be kebab-case, letters/numbers/hyphens only
