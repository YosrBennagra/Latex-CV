#!/usr/bin/env bash
# scaffold-skill.sh — Create a new skill directory with boilerplate.
#
# Usage:
#   bash scaffold-skill.sh <skill-name> [--task|--reference]
#
# Examples:
#   bash scaffold-skill.sh api-conventions --reference
#   bash scaffold-skill.sh deploy --task

set -euo pipefail

SKILL_NAME="\${1:?Usage: scaffold-skill.sh <skill-name> [--task|--reference]}"
KIND="\${2:---reference}"

# Determine base directory
if [ -d ".claude/skills" ]; then
  BASE=".claude/skills"
elif [ -d ".github/skills" ]; then
  BASE=".github/skills"
else
  BASE=".claude/skills"
fi

DIR="\$BASE/\$SKILL_NAME"

if [ -d "\$DIR" ]; then
  echo "Error: \$DIR already exists."
  exit 1
fi

mkdir -p "\$DIR/references" "\$DIR/scripts" "\$DIR/examples"

# ─── Generate SKILL.md ──────────────────────────────────

if [ "\$KIND" = "--task" ]; then
  cat > "\$DIR/SKILL.md" << 'SKILL_EOF'
---
name: SKILL_NAME_PLACEHOLDER
description: Describe what this skill does and when to use it
disable-model-invocation: true
---

# SKILL_NAME_PLACEHOLDER

## Steps

1. First step
2. Second step
3. Third step

## Additional resources

- See [references/details.md](references/details.md) for more info
SKILL_EOF
else
  cat > "\$DIR/SKILL.md" << 'SKILL_EOF'
---
name: SKILL_NAME_PLACEHOLDER
description: Describe what this skill does and when to use it
---

# SKILL_NAME_PLACEHOLDER

## Conventions

- Convention one
- Convention two
- Convention three

## Examples

### Good example

\`\`\`
// example code
\`\`\`

## Additional resources

- See [references/details.md](references/details.md) for more info
SKILL_EOF
fi

# Replace placeholder with actual name
sed -i "s/SKILL_NAME_PLACEHOLDER/\$SKILL_NAME/g" "\$DIR/SKILL.md"

# ─── Generate reference stub ────────────────────────────

cat > "\$DIR/references/details.md" << 'REF_EOF'
# Detailed Reference

Add detailed documentation, API specs, or conventions here.
This file is loaded on demand when referenced from SKILL.md.
REF_EOF

echo "✓ Created skill at \$DIR"
echo "  Edit \$DIR/SKILL.md to customize."
