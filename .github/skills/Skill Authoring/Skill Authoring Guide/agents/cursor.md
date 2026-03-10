# Cursor — Skill Setup

Cursor uses **rule files** in `.cursor/rules/` or a root `.cursorrules` file.

## Rule directory (recommended)

```
.cursor/rules/
├── api-conventions.mdc
├── testing-patterns.mdc
└── deploy-workflow.mdc
```

Each `.mdc` file has YAML-style frontmatter:

```yaml
---
description: API design patterns for this codebase
globs: ["src/app/api/**/*.ts"]
alwaysApply: false
---

When writing API endpoints:
- Use RESTful naming conventions
- Return consistent error formats
- Include request validation with Zod schemas
```

## Frontmatter fields

| Field | Purpose |
|-------|---------|
| `description` | When to apply this rule (auto-matched by Cursor) |
| `globs` | File patterns that trigger the rule automatically |
| `alwaysApply` | `true` → always loaded; `false` → only when relevant |

## Root .cursorrules file

A single `.cursorrules` file in the project root applies to all conversations:

```markdown
# Project Rules

- Use TypeScript strict mode
- Prefer Server Components by default
- No `any` types — use `unknown` with type guards
```

## Mapping skill concepts to Cursor

| Skill concept | Cursor equivalent |
|---------------|-------------------|
| `SKILL.md` | `.mdc` file in `.cursor/rules/` |
| `description` frontmatter | `description` frontmatter |
| `disable-model-invocation: true` | Not directly supported — use Notepads for manual-only |
| `allowed-tools` | Not directly supported |
| Supporting files | Reference with relative paths in the rule body |

## Tips

- Use `globs` to scope rules to relevant file types.
- Split rules by domain: one `.mdc` per concern.
- Use `@file` mentions in chat to give Cursor extra context.
