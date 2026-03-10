# Building Skills for AI Agents

A comprehensive, agent-agnostic guide for creating **skills** — reusable instruction
sets that extend what an AI coding agent can do. Whether you use Claude Code,
GitHub Copilot, Cursor, Windsurf, or any other agent, the core principles are
identical: give the agent a clear scope, a well-crafted description, and
supporting files it can reference on demand.

---

## What Is a Skill?

A skill is a self-contained unit of reusable knowledge or a step-by-step
workflow that an agent can invoke. It teaches the agent *when* to activate,
*what* to do, and *how* to do it.

**Skills are:** reusable techniques, patterns, tools, reference guides.
**Skills are NOT:** narratives about how you solved a problem once, project-specific
configuration (put that in the agent's root config file instead).

---

## Skill Types

| Type | Description | Examples |
|------|-------------|---------|
| **Technique** | Concrete method with steps to follow | `condition-based-waiting`, `tdd-workflow` |
| **Pattern** | A way of thinking about problems | `reduce-complexity`, `flatten-with-flags` |
| **Reference** | API docs, syntax guides, tool documentation | `api-conventions`, `pptx-spec` |
| **Discipline** | Rules that must be followed under pressure | `verify-before-completing`, `design-before-coding` |

Discipline skills need extra work to resist rationalization — see *Bulletproofing* below.

---

## Anatomy of a Skill

Every skill lives in its own directory with a required entry-point file:

```
my-skill/
├── SKILL.md            # Entry point (required)
├── references/
│   └── api-spec.md     # Heavy reference loaded on demand
└── scripts/
    └── validate.sh     # Reusable executable helper
```

### SKILL.md Structure

```yaml
---
name: my-skill
description: Use when [specific triggering conditions and symptoms].
---

# My Skill

## Overview
Core principle in 1–2 sentences.

## When to Use
- Symptom or situation that signals this skill applies
- When NOT to use

## Core Pattern
Before/after comparison or key steps.

## Quick Reference
Table or bullets for scanning common operations.

## Common Mistakes
What goes wrong + fixes.
```

---

## Frontmatter Reference

The two universally supported fields across all agents are `name` and `description`.
Additional fields are Claude Code–specific.

| Field | Scope | Purpose |
|-------|-------|---------|
| `name` | Universal | Slash-command name. Letters, numbers, hyphens only — **no parentheses or special chars**. Max 64 chars. |
| `description` | Universal | Triggering conditions. Max ~1024 chars. Start with "Use when…". **Never summarize workflow.** |
| `argument-hint` | Claude Code | Autocomplete hint. Example: `[issue-number]` |
| `disable-model-invocation` | Claude Code | `true` → user-only invocation. Use for destructive actions. |
| `user-invocable` | Claude Code | `false` → agent-only, hidden from slash menu. |
| `allowed-tools` | Claude Code | Tools the agent may use without extra permission. |
| `context` | Claude Code | `fork` runs the skill in an isolated sub-agent context. |
| `agent` | Claude Code | Sub-agent type when `context: fork`. |

---

## Writing the Description — The CSO Trap

The description is how the agent decides whether to load a skill. It must
describe **triggering conditions only** — never summarize the workflow.

**Why it matters:** Testing shows that when a description summarizes the
workflow, the agent follows the description *instead of reading the full skill*.
A description saying "code review between tasks" caused an agent to do ONE
review, even when the skill's flowchart clearly showed TWO. When the description
was changed to just the triggering condition, the agent correctly read the
flowchart and followed both stages.

```yaml
# ❌ BAD — summarizes workflow; agent follows description, skips skill body
description: Execute plans by dispatching a subagent per task with code review between tasks

# ❌ BAD — too abstract, agent can't match
description: Helps with development tasks

# ✅ GOOD — triggering condition only, no workflow summary
description: Use when executing implementation plans with independent tasks

# ✅ GOOD — specific symptoms and context
description: Use when tests have race conditions, timing dependencies, or pass/fail inconsistently
```

**Rules for descriptions:**
- Start with "Use when…"
- Include specific symptoms, situations, error messages
- Write in third person (injected into system prompt)
- Keep under 500 characters when possible
- **NEVER summarize the skill's process or workflow**

---

## Skill Naming

Use active voice and verb-first naming. Gerunds (-ing) work well for processes.

| ✅ Good | ❌ Bad |
|--------|--------|
| `creating-skills` | `skill-creation` |
| `condition-based-waiting` | `async-test-helpers` |
| `finishing-a-branch` | `branch-finish-workflow` |

Use letters, numbers, and hyphens only — **no parentheses, dots, underscores, or
special characters** (some agents reject them).

---

## Token Efficiency

Skills that load frequently burn context. Target word counts:

| Skill category | Target |
|----------------|--------|
| Getting-started / always-on | < 150 words |
| Frequently-loaded skills | < 200 words total |
| Other skills | < 500 words |

Techniques to stay small:
- **Cross-reference other skills** instead of repeating instructions:
  `**REQUIRED BACKGROUND:** You MUST understand `other-skill-name` before using this.`
- **Move heavy reference** (100+ lines) to a supporting file; link to it.
- **One excellent example** instead of multiple mediocre ones.
- **No `@` force-loading** — `@` syntax loads files immediately and burns context
  tokens before the agent even needs them. Use plain skill names instead.

---

## Two Kinds of Skill Content

### Reference Skills — "Know This"

Conventions, patterns, or domain knowledge the agent applies silently.

```yaml
---
name: api-conventions
description: Use when writing or reviewing API endpoints in this codebase
---

When writing API endpoints:
- Use RESTful naming conventions
- Return errors using Problem Details (RFC 9457)
- Validate request bodies with Zod schemas
```

### Task Skills — "Do This"

Step-by-step instructions for a concrete action. Invoke manually via `/skill-name`.

```yaml
---
name: deploy
description: Use when deploying the application to production
disable-model-invocation: true
---

1. Run the full test suite
2. Build the production bundle
3. Push to the deployment target
4. Verify the health-check endpoint
```

---

## Supporting Files

Keep `SKILL.md` focused. Move heavy content to separate files within the skill
directory. Reference them from `SKILL.md`:

```markdown
## Additional resources
- Full API reference: [references/api-spec.md](references/api-spec.md)
- Usage examples: [examples/sample.md](examples/sample.md)
```

The agent loads these files on demand — they don't consume context until needed.

**Separate files for:**
1. Heavy reference material (100+ lines) — API docs, comprehensive syntax
2. Reusable tools — scripts, validators, templates

**Keep inline:**
- Principles and concepts
- Code patterns under 50 lines
- Everything else

---

## Where Skills Live

| Scope | Path | Available to |
|-------|------|-------------|
| Personal | `~/.claude/skills/<name>/SKILL.md` | All your projects |
| Project | `.claude/skills/<name>/SKILL.md` | This project only |
| Organization | Managed settings / shared repo | All team members |

> **Copilot / Cursor note:** These agents use `.github/copilot-instructions.md`,
> `.cursorrules`, or similar files instead of a `skills/` directory.
> The *content structure* translates directly — only the delivery wrapper differs.
> See the agent-specific configs in the `agents/` folder of this skill.

---

## TDD for Skills

The most reliable way to write a skill is to treat it like test-driven
development. This applies to **new skills and edits to existing skills**.

```
RED   → Run a pressure scenario WITHOUT the skill. Document exact failures.
GREEN → Write the minimal skill that addresses those specific failures.
REFACTOR → Find new rationalizations. Add explicit counters. Re-test.
```

**The Iron Law: No skill without a failing test first.**

| TDD concept | Skill equivalent |
|-------------|-----------------|
| Test case | Pressure scenario with a sub-agent |
| RED (fail) | Agent violates rule without skill |
| GREEN (pass) | Agent complies with skill present |
| Refactor | Close loopholes while maintaining compliance |

---

## Testing Your Skill

Different skill types need different test approaches:

| Skill type | Test approach | Success criteria |
|------------|--------------|-----------------|
| **Discipline** (rules/requirements) | Pressure scenarios: time pressure, sunk cost, authority | Agent follows rule under maximum pressure |
| **Technique** (how-to guides) | Application + variation scenarios | Agent applies technique to new scenario |
| **Pattern** (mental models) | Recognition + counter-examples | Agent identifies when/how to apply pattern |
| **Reference** (docs/APIs) | Retrieval + gap testing | Agent finds and correctly applies info |

---

## Bulletproofing Discipline Skills

Discipline skills (TDD, verify-before-completing, design-before-coding) must
resist rationalization. Agents will find loopholes under pressure.

**Build a rationalization table** from what your baseline test reveals:

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "This is different because…" | It isn't. Follow the rule. |

**Create a Red Flags list** so the agent can self-check:

```markdown
## Red Flags — STOP and Start Over
- Starting implementation before completing design
- "I already know what to do"
- "This case is simple enough to skip the process"
- "I'm following the spirit of the rule"

All of these mean: stop, go back to step one.
```

**State "spirit vs letter" explicitly:**
```markdown
Violating the letter of the rules IS violating the spirit of the rules.
```

---

## Arguments & Substitutions (Claude Code)

| Placeholder | Resolves to |
|-------------|-------------|
| `$ARGUMENTS` | All arguments as one string |
| `$ARGUMENTS[N]` / `$N` | Nth argument (0-based) |

```yaml
---
name: fix-issue
description: Use when fixing a specific GitHub issue by number
disable-model-invocation: true
---

Fix GitHub issue $ARGUMENTS following our coding standards.
1. Read the issue. 2. Implement. 3. Write tests. 4. Commit.
```

---

## Sub-agent Execution (Claude Code)

Add `context: fork` to run a skill in an isolated agent — the skill content
becomes the sub-agent's full prompt:

```yaml
---
name: deep-research
description: Use when thorough codebase research is needed before implementing
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:
1. Find relevant files with Glob and Grep
2. Read and analyze the code
3. Return findings with specific file references
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Skill doesn't trigger automatically | Add more symptom keywords to the description |
| Agent follows description, ignores skill body | Remove workflow summary from description — only triggering conditions |
| Skill triggers too often | Narrow the description; add `disable-model-invocation: true` |
| Agent ignores supporting files | Reference them explicitly with relative links in SKILL.md |
| Context budget exceeded | Move heavy reference to separate files |

---

## Cross-Agent Portability

The same content structure works across tools. See the agent-specific files in
this skill's `agents/` folder for exact file locations and discovery mechanisms for:

- **Claude Code** — `.claude/skills/`
- **GitHub Copilot** — `.github/copilot-instructions.md` or workspace instructions
- **Cursor** — `.cursor/rules/` or `.cursorrules`
- **Windsurf** — `.windsurfrules` or workspace rules

The instructions you write are the same; only the delivery wrapper changes.
