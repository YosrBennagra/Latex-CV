# Latex-CV

## Overview
Personal CV management system for **Yosr Ben Nagra**. Generates ATS-friendly, 1-page LaTeX CVs tailored to specific job positions, in both English and French.

## Stack
- **LaTeX** (pdflatex) — document typesetting
- **JSON** (`data_profile.json`) — canonical profile data
- **Git** — version control (PDFs tracked intentionally)

## Critical Rules
1. `data_profile.json` is the **single source of truth** for all personal data
2. **Never fabricate** experience, skills, companies, or dates
3. Both EN and FR versions must stay **synchronized**
4. Cover letters are **mandatory** for every job application
5. Use ASCII text by default — no accents unless user requests
6. Never delete user data without explicit permission

## Architecture
```
data_profile.json          ← Master profile (update here first)
profile/                   ← Organized views of the profile data
  job_titles.md            ← Job titles qualified for (by fit tier)
  skills.md                ← Skills inventory by category
  technologies.md          ← Technology list with usage evidence
  experience.md            ← Experience/internships (EN + FR)
  projects.md              ← Personal projects catalog + selection guide
  education_certifications.md
  languages_soft_skills.md
  ats_keywords.md          ← ATS keyword bank per target role
templates/                 ← Reusable LaTeX templates (9 CV + 4 letters)
  cv_template_compact.tex  ← Base 1-page CV template
  cv_template_*.tex        ← Variants: classic, minimal, modern,
                             professional, elegant, tech, graduate, executive
  cover_letter_universal.tex ← Base cover letter template
applications/              ← Position-specific tailored CVs
  {Position_Name}/
    cv_{name}_en.tex       ← English CV
    cv_{name}_fr.tex       ← French CV
    cover_letter_*.tex     ← Cover letters (EN + FR)
.github/skills/            ← AI agent skills
  skills_tracker.md        ← Skills inventory with status
```

## Commands

### Build a single CV
```powershell
cd applications/{Position_Name}
pdflatex cv_{name}_en.tex
```

### Build with latexmk (auto-runs twice for references)
```powershell
latexmk -pdf cv_{name}_en.tex
```

### Build all CVs in an application folder
```powershell
.\build.ps1 -Path applications/{Position_Name}
```

### Build everything
```powershell
.\build.ps1 -All
```

### Clean build artifacts
```powershell
.\build.ps1 -Clean
```

## Git & Workflow
- **PDFs are tracked** — commit compiled CVs for easy sharing
- **Build artifacts** (.aux, .log, .fls, .fdb_latexmk, .out, .synctex.gz) — gitignored
- **Workflow**: Update `data_profile.json` → sync affected `profile/*.md` views → generate/update LaTeX files → compile → commit

## Profile Data Fields
Key fields in `data_profile.json`:
- `name`, `phone`, `email`, `location`, `gender`, `focus`
- `github`, `linkedin`, `website`
- `skills.*` (frontend, backend, database, devops, etc.)
- `projects[]` (internships with dates, tech, descriptions)
- `personal_projects[]` (Veinpal, Overlayos, etc.)
- `certificates[]`, `education[]`, `languages`
- `current_job` (Concentrix)
