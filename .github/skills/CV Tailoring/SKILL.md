---
name: cv-tailoring
description: 'Use when creating a position-specific CV from data_profile.json, adapting skills/experience emphasis for a job posting.'
---

# CV Tailoring

## Overview
Generate position-targeted CVs by reordering and emphasizing skills/experience from `data_profile.json` to match a job posting — without fabricating anything.

## When to Use
- User provides a job posting and wants a tailored CV
- Creating a new application variant (e.g. Frontend React, FullStack Java)
- When NOT to use: updating personal data (use CV Maker skill instead)

## Procedure

1. **Parse job requirements** — extract required skills, tools, frameworks, seniority
2. **Match against `data_profile.json`** — identify which user skills/projects align
3. **Check `skills_tracker.md`** — flag any required skills not yet tracked; ask user
4. **Create folder** — `applications/{Company}_{Position}_{Date}/`
5. **Generate EN + FR CVs** from templates, applying these tailoring rules:
   - **Title**: Match the job title (e.g. "Full Stack Java Developer")
   - **Summary**: 2-3 sentences highlighting matching stack
   - **Skills order**: Job-required skills first in each category
   - **Experience titles**: Adjust role titles to emphasize relevant aspect (e.g. "Frontend Developer" vs "Full Stack Developer" for the same internship)
   - **Bullet points**: Lead with achievements using job-relevant technologies
   - **Keywords**: Include job posting terms naturally for ATS
6. **Create cover letters** (EN + FR) — MANDATORY for every application

## Tailoring Rules

| Aspect | How to Adapt |
|---|---|
| Professional title | Match the job posting's role name |
| Summary | Highlight the stack the employer wants |
| Skills section | Reorder categories: job-critical first |
| Experience bullets | Lead with relevant tech, quantify results |
| Projects | Promote projects using target stack |
| Keywords | Mirror exact terms from job posting |

## Honesty Policy
- NEVER fabricate experience, skills, or companies
- Reorder and emphasize — never invent
- If a required skill is missing, highlight transferable skills instead
- Mark uncertain skills as learning in skills_tracker.md

## Key Files
- `data_profile.json` — source of all profile data
- `templates/` — 9 CV templates; pick per `templates/README.md` situation guide (default: `cv_template_professional.tex`)
- `profile/ats_keywords.md` — ATS keyword bank per role
- `profile/job_titles.md` — header titles by fit tier
- `templates/cover_letter_universal.tex` — base cover letter template
- `.github/skills/skills_tracker.md` — check/update skill statuses
- `applications/` — one subfolder per position variant

## Quick Reference — Existing Variants

| Folder | Stack Focus |
|---|---|
| `Frontend_React` | React, TypeScript, UI/UX |
| `FullStack_Java` | Spring Boot, Java, Angular |
| `FullStack_MERN_React` | MongoDB, Express, React, Node |
| `FullStack_NodeJS_React` | Node.js, Express, React |
| `FullStack_MEAN` | MongoDB, Express, Angular, Node |
| `FullStack_General` | Broad full stack |
| `Universal_FullStack` | Everything |
| `AI_Engineer` | AI/ML, Flask, RAG |
| `IT_Application_Operations` | IT ops, support |
| `React_FullStack_Generic` | React-first full stack |

## Common Mistakes
- **Fabricating skills not in data_profile.json** — reorder and emphasize only
- **Forgetting cover letters** — MANDATORY for every application
- **Ignoring skills_tracker.md** — always check for gaps and update statuses
- **Not adjusting experience titles** — same internship can be "Frontend Developer" or "Full Stack Developer" depending on target role
- **Copy-pasting without adapting** — each variant needs a unique summary and skill ordering

## Output
- `cv_{position}_en.tex` + `cv_{position}_fr.tex`
- `cover_letter_{company}_en.tex` + `cover_letter_{company}_fr.tex`
- Updated `skills_tracker.md` if new skills discovered
