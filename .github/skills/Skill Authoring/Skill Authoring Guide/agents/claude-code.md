# Claude Code — Skill Setup

Claude Code natively supports the Agent Skills standard via the
`.claude/skills/` directory.

## Directory structure

```
.claude/skills/
└── my-skill/
    ├── SKILL.md          # Required entry point
    ├── references/       # Optional reference docs
    ├── scripts/          # Optional executable scripts
    └── examples/         # Optional example outputs
```

## Scope

| Scope        | Path                                   |
|------------- |----------------------------------------|
| Personal     | `~/.claude/skills/<name>/SKILL.md`     |
| Project      | `.claude/skills/<name>/SKILL.md`       |
| Enterprise   | Managed settings (admin-controlled)    |

## SKILL.md format

```yaml
---
name: my-skill
description: What this skill does and when to use it
allowed-tools: Read, Grep
---

Instructions the agent follows…
```

## Discovery

- Claude Code **automatically** discovers skills from `.claude/skills/` in the
  project root and in nested directories (monorepo support).
- Skill descriptions are loaded into context so Claude knows what is available.
- Full skill content loads only when invoked.

## Invocation

- **Auto**: Claude invokes when the conversation matches the description.
- **Manual**: User types `/skill-name` in the chat.

## Advanced: Sub-agents

```yaml
---
name: research
description: Deep codebase research
context: fork
agent: Explore
---
```

Sets `context: fork` to run in an isolated sub-agent with its own context
window. The `agent` field picks a built-in agent type (`Explore`, `Plan`,
`general-purpose`) or a custom agent from `.claude/agents/`.

## Tips

- Keep SKILL.md under 500 lines.
- Use `disable-model-invocation: true` for destructive workflows.
- Use `!\`command\`` syntax to inject dynamic shell output.
