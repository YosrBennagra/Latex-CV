# LaTeX CV Project - AI Agent Instructions

## 🚨 CRITICAL: MCP SERVER VERIFICATION REQUIRED

**BEFORE adapting any CV for a job:**

1. **Query the cv-data MCP server** using these tools:
   - `get_verified_skills` - See what skills are available
   - `validate_skill` - Check if each job requirement exists
   - `get_canonical_experience` - Get exact experience bullets
   - `get_projects` - Get verified project descriptions

2. **Validation Process:**
   ```
   For each skill in job description:
   → Use validate_skill(skill_name)
   → If verified: ✅ Can use in CV
   → If NOT verified: ❌ FORBIDDEN - Do not add
   → If uncertain: Ask user before proceeding
   ```

3. **Never Skip Verification:**
   - DO NOT assume skills exist
   - DO NOT add skills from forbidden_skills list
   - DO NOT fabricate experience or projects
   - ONLY use data returned by MCP server tools

## 🎯 PURPOSE

When adapting my CV to a new job position, follow these exact rules.

## 🔧 CHANGE ONLY THESE SECTIONS

### Role / Job Title
- Update it to match the new job post using `\cvrole{New Title}`
- **Do NOT use "Graduate" in the title** (e.g., use "Software Engineer" not "Graduate Software Engineer")

### Professional Summary
- Rewrite it completely to fit the new position and required skills using `\cvsummary{...}`

### Skills Section
- **Add** new skills mentioned in the job post if they are not already in the CV
- **Keep** all existing skills
- **Reorganize** the skills (group, order, or format them) to improve clarity and presentation

## 🚫 DO NOT CHANGE

- **Work experience bullet points** - NEVER modify the experience descriptions, they are locked and must remain exactly as in the General CV
- Work experience (titles, companies, dates)
- Education, certifications, or projects
- Layout, formatting, or section order
- Personal information

## 🧠 IMPROVEMENT RULE

Each time you make changes, make the CV slightly better organized, cleaner, and more professional, while keeping its original content intact.

## 🪶 SUMMARY GUIDELINES

When rewriting the summary:

- **Maximum length: 340 characters** (approximately 3-4 sentences)
- **CRITICAL: Only claim skills/experience that exist in the Experience and Projects sections** - Never fabricate or exaggerate capabilities
- **Source of truth:** Experience bullet points and Projects are locked and factual - summary must derive from these only
- Match the job title and keywords from the description
- Highlight relevant technical and soft skills that are proven in the CV
- Keep it short, confident, and natural
- Reflect growth, autonomy, and communication ability
- If the job involves new technologies (AI, LLMs, cloud, etc.), mention adaptability or curiosity
- Focus on the most relevant skills for the specific position
- **Example:** Don't say "experienced in AWS" if there's no AWS in Experience/Projects; say "eager to apply skills to AWS" instead

## 🧩 SKILLS GUIDELINES

When updating skills:

- Add only new relevant skills from the job post
- Organize logically (e.g., Frontend, Backend, AI/ML, Testing, DevOps, Databases)
- Avoid duplicates or outdated entries
- Ensure the list looks balanced and modern

## ✅ FINAL RESULT EXPECTATION

- The role/title, summary, and skills are updated to fit the new job
- The rest of the CV remains 100% unchanged
- The CV looks cleaner, sharper, and more tailored to the position each time
- **The CV compiles successfully to PDF**
- **All auxiliary files (.aux, .log, .out, etc.) are cleaned up**

---

## Project Architecture

This is a modular LaTeX CV system optimized for ATS compatibility and multi-language job applications.

### Structure
```
E:\LatexCv/
├── preamble.tex              # Shared formatting macros (used by all CVs)
├── CVs/
│   ├── English/              # English CV versions
│   │   ├── CV_Yosr_BenNagra_English.tex (job-specific)
│   │   └── CV_Yosr_BenNagra_English_General.tex
│   └── French/               # French CV versions
│       ├── CV_Yosr_BenNagra_French.tex (job-specific)
│       └── CV_Yosr_BenNagra_French_General.tex
├── CoverLetters/             # Cover letter templates
└── CV_ADAPTATION_INSTRUCTIONS.md
```

### Key Dependency
**All CV files in subfolders MUST reference preamble as:** `\input{../../preamble}`
- If you move files or create new CVs, update this path or compilation will fail

### Compilation
```powershell
cd E:\LatexCv\CVs\English  # or French
pdflatex CV_Yosr_BenNagra_English.tex
```
Second pass ensures references: `pdflatex CV_Yosr_BenNagra_English.tex`

### 🧹 Cleanup After Compilation (MANDATORY)
**ALWAYS clean up auxiliary files after compiling:**
```powershell
Remove-Item *.aux, *.log, *.out, *.fdb_latexmk, *.fls, *.synctex.gz -Force
```

**CRITICAL**: After every CV or cover letter adaptation:
1. Compile the document twice (for references)
2. Verify the PDF was generated successfully
3. Clean up auxiliary files (.aux, .log, .out, .fdb_latexmk, .fls, .synctex.gz)
4. Only keep the .tex source and .pdf output

**Complete workflow for cover letters:**
```powershell
cd E:\LatexCv\CoverLetters
Remove-Item *.aux, *.log, *.out, *.fdb_latexmk, *.fls, *.synctex.gz -Force
pdflatex CoverLetter_Yosr_BenNagra_{Company}.tex
pdflatex CoverLetter_Yosr_BenNagra_{Company}.tex
Remove-Item *.aux, *.log, *.out, *.fdb_latexmk, *.fls, *.synctex.gz -Force
```

### Error Checking
After edits, use VS Code's LaTeX diagnostics or compile to verify no errors

## Project-Specific Patterns

### Custom Macros (in preamble.tex)
```latex
\cvname{Name}           # Uppercase name in header
\cvrole{Title}          # Job title (appears with name)
\cvsummary{Text}        # Professional summary
\cvsection{Title}       # Section headers
\begin{internship}{Title}{Company}{Location}{Dates}{}
  \item Bullet point
\end{internship}
```

### Two-Column Skills Layout
```latex
\begin{minipage}[t]{0.48\textwidth}
  \textbf{Category:} Skill1, Skill2\\[1.5pt]
\end{minipage}
\hfill
\begin{minipage}[t]{0.48\textwidth}
  \textbf{Category:} Skill3, Skill4\\[1.5pt]
\end{minipage}
```

### Space Optimization
- Preamble uses tight spacing: `\parskip{0.5pt}`, `itemsep=1pt`
- Internship environment has `-7pt` spacing between dates and bullets
- All CVs target single-page fit

## File Organization Conventions

### Naming Pattern
- `CV_Yosr_BenNagra_{Language}_{Company}.tex` for job-specific versions (e.g., CV_Yosr_BenNagra_English_Signaturit.tex)
- `CV_Yosr_BenNagra_{Language}_ATS.tex` for general ATS versions
- Cover letters: `CoverLetter_Yosr_BenNagra_{Company}.tex`

**IMPORTANT**: When adapting CV for a specific company:
1. Copy the appropriate ATS CV (English or French)
2. Rename to include company name: `CV_Yosr_BenNagra_{Language}_{Company}.tex`
3. Make adaptations for that specific job
4. Keep the ATS version as a general baseline

### Auxiliary File Cleanup (MANDATORY)
**ALWAYS clean up after compilation:**
```powershell
Remove-Item *.aux, *.log, *.fdb_latexmk, *.fls, *.out, *.synctex.gz -Force
```

**Files to NEVER commit:**
- `.aux` - Auxiliary compilation data
- `.log` - LaTeX compilation logs
- `.fdb_latexmk` - Latexmk database
- `.fls` - File list
- `.out` - Hyperref output
- `.synctex.gz` - SyncTeX data

**Only commit:**
- `.tex` source files
- `.pdf` compiled output (optional)

## Common Adaptation Patterns

### ⚠️ CRITICAL: Experience Bullet Points
**NEVER modify the experience bullet points.** They are locked and must remain exactly as written in `CV_Yosr_BenNagra_English_General.tex`:

**IT Serv (Feb 2025 - Aug 2025):**
- Designed full-stack web platform integrating AI, DevOps, and RAG
- Implemented AI-powered symptom checker, doctor blog, patient forum, admin dashboard
- Fine-tuned AI model and set up CI/CD, containerization, and monitoring

**IronByte (Jun 2024 - Aug 2024):**
- Developed educational web application with assignment submission and lesson sharing
- Added timetable creation tool improving scheduling efficiency

**Ooredoo Tunisie (Jul 2023 - Sep 2023):**
- Built internal communication app with real-time chat, filtering, and search
- Delivered UX/UI design and unit/integration tests

**Only change:** The Keywords line at the end (can remain the same or be updated if needed)

### Backend/Full-Stack Role
```latex
\cvrole{Full Stack Developer}
Skills: Frontend (React, TypeScript) + Backend (Java/Spring Boot, Node.js/NestJS)
```

### AI/ML Focus
```latex
Add skills: \textbf{AI/ML:} LLMs Integration, Hugging Face, RAG
Mention in summary: "integrating Large Language Models"
```

### Frontend Specialization
```latex
\cvrole{Frontend Developer}
Emphasize: React.js, TypeScript, component-based architecture
```

## Language-Specific Notes

## What NOT to Do

❌ Don't change experience bullet points (titles, companies, dates, achievements)
❌ Don't add technologies to experience that weren't actually used
❌ Don't remove existing skills when adapting
❌ Don't change layout or formatting in preamble.tex without testing
❌ Don't use absolute paths in `\input{}` statements
❌ Don't skip compilation after making changes
❌ Don't leave auxiliary files (.aux, .log, .out, etc.) uncommitted
❌ Don't forget to clean cover letter auxiliary files in CoverLetters/ folder
## What NOT to Do

❌ Don't change experience bullet points (titles, companies, dates, achievements)
❌ Don't add technologies to experience that weren't actually used
❌ Don't remove existing skills when adapting
❌ Don't change layout or formatting in preamble.tex without testing
❌ Don't use absolute paths in `\input{}` statements
❌ Don't skip compilation after making changes
❌ Don't leave auxiliary files (.aux, .log, .out, etc.) uncommitted
