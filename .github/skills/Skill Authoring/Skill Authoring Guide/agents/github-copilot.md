# GitHub Copilot — Skill Setup

GitHub Copilot uses **instruction files** and **workspace settings** instead of
a `.claude/skills/` directory, but the content you write is identical.

## Instruction file

Create `.github/copilot-instructions.md` in the repo root:

```markdown
# Project Conventions

When writing API endpoints:
- Use RESTful naming conventions
- Return consistent error formats
- Include request validation with Zod schemas
```

Copilot loads this file automatically in VS Code and GitHub.com.

## VS Code workspace instructions

In `.vscode/settings.json`:

```json
{
  "github.copilot.chat.codeGeneration.instructions": [
    { "file": ".github/skills/api-conventions.md" },
    { "file": ".github/skills/testing-patterns.md" }
  ]
}
```

This lets you split instructions into multiple files — one per skill — and
Copilot loads them all into the chat context.

## Instruction format

Copilot does **not** use YAML frontmatter. Write plain markdown:

```markdown
# API Conventions

When writing API endpoints:
1. Use RESTful naming
2. Validate with Zod
3. Return Problem Details on error
```

## Prompt files (experimental)

Copilot supports `.github/prompts/*.prompt.md` files that act like reusable
slash commands:

```markdown
---
mode: agent
description: "Create a new React component"
tools: ["file_search", "read_file", "create_file"]
---

Create a new React component called $ARGUMENTS[0]:
1. Create the component file
2. Create a test file
3. Export from the barrel index
```

Invoke with `/prompt-name` in the chat panel.

## Tips

- Keep each instruction file focused on one topic.
- Reference other files with relative paths so Copilot can read them.
- Use `@workspace` in chat to give Copilot broader codebase context.
