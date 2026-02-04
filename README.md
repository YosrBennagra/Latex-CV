# Latex-CV Project

A comprehensive CV management system for job applications with ATS-friendly templates.

## 📁 Project Structure

```
Latex-CV/
├── data_profile.json           # Your master profile (skills, experience, education)
├── cv_en.tex                   # Generic English CV
├── cv_fr.tex                   # Generic French CV
├── templates/
│   └── cv_template_compact.tex # 1-page compact template (copy for new applications)
├── applications/
│   └── [Company]_[Position]_[Date]/
│       ├── job_description.md   # Saved job posting
│       ├── cv_[company]_en.tex  # Tailored English CV
│       ├── cv_[company]_fr.tex  # Tailored French CV
│       ├── cover_letter_[company]_en.txt
│       ├── cover_letter_[company]_fr.txt
│       └── notes.md             # Analysis and interview prep
├── .github/
│   ├── copilot-instructions.md  # Copilot rules
│   ├── cv-generation-instructions.md  # CV generation workflow
│   └── skills/
│       └── skills_tracker.md    # Skills database with status
└── README.md                    # This file
```

## 🚀 Quick Start

### 1. Update Your Profile
Edit `data_profile.json` with your latest information:
- Personal info (name, phone, location)
- Skills (frontend, backend, devops, etc.)
- Projects and experience
- Education and certifications

### 2. Apply for a Job
Just paste the job description to Copilot and it will:
1. ✅ Extract required skills
2. ✅ Ask you about missing skills
3. ✅ Update your skills tracker
4. ✅ Create tailored CV (EN + FR)
5. ✅ Create cover letters (EN + FR)
6. ✅ Save everything organized

### 3. Compile to PDF
```bash
cd applications/[Company]_[Position]_[Date]/
pdflatex cv_[company]_fr.tex
pdflatex cv_[company]_en.tex
```

## 📋 Features

### ATS-Friendly Format
- Standard section names (Experience, Education, Skills)
- No tables, images, or complex formatting
- Keywords from job description included
- Clean structure parseable by ATS systems

### 1-Page Compact Template
- Fits everything on one page
- Professional blue color scheme
- Two-column layout for efficiency
- FontAwesome icons (with fallback)

### Skills Tracking
- All skills logged in `.github/skills/skills_tracker.md`
- Status: ✅ Known, ❌ Unknown, 🔄 Learning
- Updated for each job application

### Honest Approach
- Only real experience
- No fabricated years or companies
- Highlights transferable skills
- Clear about actual expertise level

## 🛠 Requirements

### LaTeX Distribution
- **Windows**: MiKTeX or TeX Live
- **Mac**: MacTeX
- **Linux**: TeX Live

### Required Packages
```
fontenc, inputenc, babel, geometry, enumitem, 
xcolor, hyperref, titlesec, multicol, tgheros
```

### Optional (recommended)
```
fontawesome5  # For icons in header
```

## 📝 Customization

### Colors
In the template, modify:
```latex
\\definecolor{primary}{RGB}{0,70,130}  % Blue
\\definecolor{darkgray}{RGB}{50,50,50}  % Text
```

### Margins
```latex
\\usepackage[a4paper,margin=0.5in,top=0.4in,bottom=0.4in]{geometry}
```

### Font Size
```latex
\\documentclass[10pt,a4paper]{article}  % 10pt for compact, 11pt for more space
```

## 📊 Your Profile Summary

**Name:** Yosr Ben Nagra  
**Role:** Full Stack Developer (React focus)  
**Location:** Tunis, Tunisia

**Core Skills:**
- Frontend: React, TypeScript, JavaScript, Angular
- Backend: Java, Spring Boot, NestJS, Flask
- DevOps: Jenkins, Docker, SonarQube, CI/CD
- Database: PostgreSQL, MongoDB, SQL

**Languages:** English (Fluent), French (Professional), Arabic (Native)

**Domain Knowledge:** Banking/Finance

---

*Last updated: 2026-02-03*