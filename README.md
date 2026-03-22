# Latex-CV

Personal CV management system — generates ATS-friendly, 1-page LaTeX CVs tailored to job positions in English and French.

## Project Structure

```
Latex-CV/
├── data_profile.json              # Master profile data (update here first)
├── build.ps1                      # Build script (compile .tex → .pdf)
├── .latexmkrc                     # LaTeX build configuration
├── CLAUDE.md                      # Project conventions
│
├── templates/
│   ├── cv_template_compact.tex    # Base CV template
│   └── cover_letter_universal.tex # Base cover letter template
│
├── applications/                  # One folder per position type
│   ├── Frontend_React/            # EN/cv_frontend_react_en.tex + FR/cv_frontend_react_fr.tex
│   ├── FullStack_Java/            # EN/ + FR/ language split
│   ├── FullStack_MERN_React/      # EN/ + FR/ language split
│   ├── FullStack_NodeJS_React/    # EN/ + FR/ language split
│   ├── Universal_FullStack/       # EN/cv_fullstack_en(.long).tex + FR/cv_fullstack_fr(.long).tex
│   └── ...                        # More position variants
│
├── .github/
│   ├── copilot-instructions.md    # AI assistant configuration
│   ├── cv-generation-instructions.md
│   ├── job-search-strategy.md
│   └── skills/
│       ├── skills_tracker.md      # Skills inventory (✅ ❌ 🔄)
│       ├── CV Maker/SKILL.md      # Create/update CVs
│       ├── Cover Letter/SKILL.md  # Create cover letters
│       ├── CV Tailoring/SKILL.md  # Tailor CV to job posting
│       └── Skill Authoring/       # Meta-skills for managing skills
```

## Quick Start

### 1. Update your profile
Edit `data_profile.json` with your latest data (skills, experience, projects).

### 2. Create a tailored CV
Paste a job posting to Copilot — it will:
1. Extract required skills and match against your profile
2. Ask about any missing skills
3. Create a tailored CV (EN + FR) + cover letters
4. Save everything in `applications/{Company}_{Position}_{Date}/`

### 3. Build PDFs

```powershell
# Build one folder
.\build.ps1 -Path applications\Frontend_React

# Build a single file
.\build.ps1 -Path applications\Frontend_React\EN\cv_frontend_react_en.tex

# Build all applications
.\build.ps1 -All

# Clean build artifacts
.\build.ps1 -Clean
```

Or manually:
```powershell
cd applications\Frontend_React\EN
pdflatex cv_frontend_react_en.tex
```

## Available Position Variants

Existing folders in `applications/` are reusable role-based variants. For a new company-specific application, create a new folder using `applications/{Company}_{Position}_{Date}/`.

| Folder | Focus | Best For |
|---|---|---|
| `Frontend_React` | React, TypeScript, UI/UX | Frontend-only roles |
| `FullStack_Java` | Spring Boot, Java, Angular | Enterprise Java roles |
| `FullStack_MERN_React` | MongoDB, Express, React, Node | MERN stack startups |
| `FullStack_NodeJS_React` | Node.js, Express, React | Node.js full stack |
| `FullStack_MEAN` | MongoDB, Express, Angular, Node | MEAN stack roles |
| `FullStack_General` | Broad full stack | General applications |
| `Universal_FullStack` | Everything | Widest coverage |
| `AI_Engineer` | AI/ML, Flask, RAG | AI/ML positions |
| `IT_Application_Operations` | IT ops, support | IT operations roles |
| `React_FullStack_Generic` | React-first full stack | React-heavy companies |

## Requirements

- **LaTeX distribution**: MiKTeX (Windows), TeX Live (Linux), or MacTeX (Mac)
- **Required packages**: fontenc, inputenc, babel, geometry, enumitem, xcolor, hyperref, titlesec, tgheros
- **Optional**: fontawesome5 (for icons)

## Features

- **ATS-optimized**: Standard section names, keywords, clean formatting
- **1-page compact**: Everything fits on one page
- **Bilingual**: English + French versions for every CV
- **Skills tracking**: Automatic inventory of known/unknown/learning skills
- **Honest**: Only real experience — never fabricated