# Copilot Instructions - CV Project

## Purpose
Create and maintain two LaTeX CV files:
- `cv_en.tex` (English)
- `cv_fr.tex` (French)

## Skills Policy
- Always check `.github/skills` for relevant skills and follow them.
- If a skill is missing or outdated for the request, update it.
- Keep skills aligned with the current workflow and project structure.

## Source of Truth
User-provided data must be treated as canonical. Do not invent, guess, or replace it.
Store and update the canonical data in `data_profile.json`.

### Current Canonical Data (from user)
- Name: Yosr Ben Nagra
- Phone: +216 53916040
- Gender: male (only include if user explicitly wants it in the CV)
- Focus: React (primary area of expertise)

## Rules
1. Never falsify or fabricate user data.
2. If any field is missing, ask the user before adding or changing it.
3. Keep both CVs consistent (same facts, localized language).
4. Default to ASCII text unless the user explicitly asks for accents.
5. Only update the CV files and `data_profile.json` when the user provides new data.
6. Never delete or blank-out previously saved user data unless the user explicitly asks to remove it.
7. If the user asks to add content not provided, request clarification.

## Update Workflow
1. Update `data_profile.json` with new user data.
2. Apply the same changes to `cv_en.tex` and `cv_fr.tex`.
3. Confirm what was changed and where.

## Output
- LaTeX files only; PDFs generated on demand by user.
