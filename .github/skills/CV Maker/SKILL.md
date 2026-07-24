---
name: cv-maker
description: 'Use when creating, updating, or maintaining English/French CVs in this repo.'
---

# CV Maker

## When to Use
- User asks to create, update, or edit a CV
- User provides new personal data to add
- When NOT to use: tailoring a CV for a specific job posting (use CV Tailoring skill)

## Inputs
- `data_profile.json` (canonical profile data)
- Existing `.tex` files in `applications/` or `templates/`

## Non-Negotiable Rules
1. Never fabricate data.
2. Do not overwrite user-provided values with placeholders.
3. If a value is missing, ask the user.
4. Keep English and French versions aligned.
5. Keep text ASCII unless user requests accents.
6. Never delete previously saved user data unless user explicitly asks.

## Procedure
1. Update `data_profile.json` with new user data.
2. Reflect the same updates in all relevant CV files.
3. Confirm changes and list edited files.

## Key Files
- `data_profile.json` — canonical data (update here first)
- `templates/` — 9 CV templates; pick per `templates/README.md` situation guide (default: `cv_template_professional.tex`)
- `profile/` — organized profile views (job titles, skills, technologies with evidence, ATS keywords)
- `applications/{Company}_{Position}_{Date}/cv_{company}_en.tex` + `cv_{company}_fr.tex`
- `.github/skills/skills_tracker.md` — skill inventory

## Quick Reference

| data_profile.json field | CV section |
|---|---|
| `name`, `phone`, `email`, `location` | Header |
| `skills.*` | Technical Skills |
| `projects[]` | Internships |
| `personal_projects[]` | Solo/Personal Projects |
| `current_job` | Current Position |
| `education[]` | Education |
| `certificates[]` | Certifications |
| `languages` | Languages |

## LaTeX Conventions
- Document class: `10pt, a4paper, article`
- Colors: `primary` (RGB 0,70,130), `accent` (RGB 60,60,60)
- Font: TeX Gyre Heros (sans-serif), FontAwesome5 for icons
- Margins: `0.6in` sides, `0.5in` top/bottom
- Style: English = concise action verbs, French = equivalent professional tone
- Always ASCII unless user requests accents

## Common Mistakes
- **Editing CV without updating data_profile.json** — always update JSON first, then CVs
- **EN/FR desync** — every change must go in both language files
- **Deleting user data** — never remove existing data unless explicitly asked
- **Adding fontawesome5 commands without fallback** — always use `\IfFileExists` guard

## Output
- Modified LaTeX files only. No PDF generation unless requested.
