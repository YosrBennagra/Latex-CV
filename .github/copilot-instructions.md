# Copilot Instructions - Latex-CV Project

## Project
Personal CV management system for **Yosr Ben Nagra**. Generates ATS-friendly LaTeX CVs tailored to job positions, in English and French. See [CLAUDE.md](../CLAUDE.md) for full conventions.

## Source of Truth
- **`data_profile.json`** — canonical profile data. Update here first, then reflect in CVs.
- User-provided data is law. Never invent, guess, or replace it.

### Canonical Data
- Name: Yosr Ben Nagra
- Phone: +216 53916040
- Gender: male (only include if user explicitly wants it in the CV)
- Focus: React (primary area of expertise)

## Rules
1. Never falsify or fabricate user data.
2. If any field is missing, ask the user before adding or changing it.
3. Keep EN and FR versions consistent (same facts, localized language).
4. Default to ASCII text unless user explicitly asks for accents.
5. Only update CV files and `data_profile.json` when user provides new data.
6. Never delete or blank-out previously saved user data unless user explicitly asks.
7. If user asks to add content not provided, request clarification.
8. Cover letters are **mandatory** for every job application.

## Update Workflow
1. Update `data_profile.json` with new user data.
2. Apply the same changes to relevant CV files.
3. Confirm what was changed and where.

## Skills

| Match these keywords | Skill path |
|---|---|
| create CV, update CV, edit CV, add experience, add skill | `.github/skills/CV Maker/SKILL.md` |
| cover letter, application letter, motivation letter | `.github/skills/Cover Letter/SKILL.md` |
| tailor CV, job posting, position-specific, adapt CV, new application | `.github/skills/CV Tailoring/SKILL.md` |
| CV generation workflow, step-by-step CV creation | `.github/cv-generation-instructions.md` |
| scaffold skills, bootstrap, init skills | `.github/skills/Skill Authoring/Scaffold Project Skills/SKILL.md` |
| update agent, add skill, skill index drift | `.github/skills/Skill Authoring/Skill & Agent Governance/SKILL.md` |
| skill, SKILL.md, create skill, build skill | `.github/skills/Skill Authoring/Skill Authoring Guide/SKILL.md` |

## Key Files
- `data_profile.json` — master profile data
- `.github/skills/skills_tracker.md` — skills inventory with status
- `templates/cv_template_compact.tex` — base CV template
- `templates/cover_letter_universal.tex` — base cover letter template
- `applications/` — position-specific CVs (one folder per position type)
- `build.ps1` — build script (run `.\build.ps1` for usage)

## Output
- LaTeX files only; PDFs generated via `pdflatex` or `.\build.ps1`.
