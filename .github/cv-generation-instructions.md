# CV Generation Instructions

## Purpose
This file provides step-by-step instructions for generating tailored CVs for job applications.

## Workflow

### 1. When User Provides a Job Posting

#### Step 1: Extract Required Skills
- Parse the job description
- List all technical skills, tools, frameworks, and methodologies
- Categorize them: Frontend, Backend, Database, DevOps, Methodologies, etc.

#### Step 2: Check Against Skills Tracker
- Open `.github/skills/skills_tracker.md`
- Compare required skills against known skills
- Identify missing skills

#### Step 3: Ask User About Missing Skills
For each unknown skill, ask:
```
Do you have experience with [SKILL]?
- If yes: How much? (years/projects)
- If no: Mark as unknown
```

#### Step 4: Update Skills Tracker
- Add new skills to `skills_tracker.md`
- Update `data_profile.json` with confirmed skills

#### Step 5: Create Application Folder
- Create folder: `applications/[Company]_[Position]_[Date]/`
- Store job description, notes, and CV files

#### Step 6: Generate Tailored CV
- Use data from `data_profile.json`
- Highlight relevant experience matching job requirements
- Emphasize matching skills
- Reorder sections for maximum relevance
- Keep it honest - never fabricate experience

#### Step 7: Create Both Versions
- Generate English CV: `cv_[company]_en.tex`
- Generate French CV: `cv_[company]_fr.tex`
- Store in application folder

#### Step 8: Create Cover Letters (MANDATORY)
- Generate French cover letter: `cover_letter_[company]_fr.tex`
- Generate English cover letter: `cover_letter_[company]_en.tex`
- Tailor each letter to the specific job posting
- Address key requirements and company context
- Store in application folder

**IMPORTANT**: Always create cover letters when generating CVs for job applications. This is a mandatory step.

### 2. CV Structure for ATS & HR Approval

#### Must-Have Sections (in order):
1. **Header**: Name, contact, links
2. **Professional Summary**: 2-3 sentences tailored to position
3. **Key Skills**: Bullet points matching job requirements
4. **Experience**: Real projects/internships (most recent first)
5. **Education**: Degrees and institutions
6. **Certifications**: If relevant to position
7. **Languages**: Language proficiency

#### ATS Optimization:
- Use standard section names (Experience, Education, Skills)
- Include keywords from job description naturally
- No tables, images, or complex formatting
- Use standard fonts (Arial, Helvetica, Times)
- Save as .pdf with proper encoding
- Use full skill names (not abbreviations)

#### HR Approval Tips:
- Quantify achievements (percentages, metrics)
- Action verbs (Built, Implemented, Designed)
- Keep to 1-2 pages maximum
- Consistent date formats
- No typos or grammar errors
- Professional language

### 3. Honesty Policy

**NEVER**:
- Fabricate work experience
- Invent years of experience
- Claim skills you don't have
- Add fake companies or projects

**ALWAYS**:
- Use real internships and projects
- Accurately represent skill levels
- Be truthful about dates
- If experience is insufficient, highlight transferable skills

### 4. File Organization

```
Latex-CV/
├── data_profile.json           # Master profile data
├── build.ps1                   # Build helper for PDFs and cleanup
├── templates/
│   ├── cv_template_compact.tex
│   └── cover_letter_universal.tex
├── .github/
│   ├── copilot-instructions.md # Main instructions
│   ├── cv-generation-instructions.md # This file
│   └── skills/
│       ├── skills_tracker.md   # Skills tracking
│       ├── CV Maker/
│       ├── Cover Letter/
│       └── CV Tailoring/
├── applications/
│   ├── Cognizant_FullStack_2026-02-03/
│   │   ├── job_description.md
│   │   ├── cv_cognizant_en.tex
│   │   ├── cv_cognizant_fr.tex
│   │   ├── cover_letter_cognizant_en.tex
│   │   ├── cover_letter_cognizant_fr.tex
│   │   └── notes.md
│   └── [Company]_[Position]_[Date]/
└── README.md
```

### 5. Skills Update Process

When a job requires new skills:
1. Add to `skills_tracker.md` with status (Known/Unknown/Learning)
2. If Known: Add to `data_profile.json` in appropriate category
3. Document which projects/experience demonstrates this skill
4. Update notes in application folder

### 6. Template Variables

Each CV should use these variables from `data_profile.json`:
- `name`, `phone`, `email`, `location`
- `github`, `linkedin`, `website`
- `role` (can be customized per application)
- `skills.[category][]`
- `projects[]`
- `education[]`
- `certificates[]`

---

*Last updated: 2026-02-03*
