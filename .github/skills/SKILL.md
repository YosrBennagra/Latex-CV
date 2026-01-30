# Skill: CV Maker

## When to Use
Use this skill when the user asks to create, update, or maintain the English/French CVs in this repo.

## Inputs
- User-provided data (treated as canonical)
- Existing LaTeX files: `cv_en.tex`, `cv_fr.tex`
- Canonical data file: `data_profile.json`

## Non-Negotiable Rules
1. Never fabricate data.
2. Do not overwrite user-provided values with placeholders.
3. If a value is missing, ask the user.
4. Keep English and French versions aligned.
5. Keep text ASCII unless user requests accents.
6. Never delete or blank-out previously saved user data unless the user explicitly asks.

## Procedure
1. Update `data_profile.json` with new user data.
2. Reflect the same updates in both CV files.
3. Confirm changes and list edited files.

## Style
- English: concise, professional
- French: direct translation and equivalent tone

## Output
- Modified LaTeX files only.
- No PDF generation unless requested.
