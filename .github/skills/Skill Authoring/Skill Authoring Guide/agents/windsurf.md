# Windsurf — Skill Setup

Windsurf (by Codeium) uses a `.windsurfrules` file or workspace rules.

## Root rules file

Create `.windsurfrules` in the project root:

```markdown
# Project Conventions

When writing API endpoints:
- Use RESTful naming conventions
- Return consistent error formats
- Include request validation with Zod schemas

When writing tests:
- Use Vitest for unit tests
- Use Playwright for E2E tests
- Aim for 80% coverage on business logic
```

## Workspace rules

In Windsurf settings, you can define workspace-level rules that apply to all
conversations within that workspace.

## Mapping skill concepts to Windsurf

| Skill concept | Windsurf equivalent |
|---------------|---------------------|
| `SKILL.md` | `.windsurfrules` or workspace rules |
| `description` frontmatter | Not directly supported — rules always apply |
| Supporting files | Reference with relative paths |
| Multiple skills | Sections within the rules file |

## Tips

- Keep `.windsurfrules` organized with clear section headers.
- Use markdown formatting for readability.
- Reference other project files so the agent can load them on demand.
