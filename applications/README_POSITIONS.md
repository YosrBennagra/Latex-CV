# Applications Catalog

One folder per reusable position variant. Each folder contains `EN/` and `FR/`
versions of the CV (`.tex` + compiled `.pdf`). For a real, company-specific
application, copy the closest variant into a new folder named
`applications/{Company}_{Position}_{Date}/` and tailor it there
(cover letters are mandatory for real applications — see
`.github/skills/Cover Letter/SKILL.md`).

> All variants include the current Wico experience (ERP, Angular/Spring Boot,
> 2024 - Present). If you update `data_profile.json`, re-tailor and rebuild the
> variants you actively use.

## Variants

| Folder | Focus | Use when the posting says... |
|--------|-------|------------------------------|
| `Frontend_React` | React, TypeScript, UI | "React Developer", "Frontend Developer" |
| `React_FullStack_Generic` | React-first full stack | "Full Stack (React)" at React-heavy companies |
| `FullStack_NodeJS_React` | Node.js/Express + React | "Full Stack JavaScript", "Node.js Developer" |
| `FullStack_MERN_React` | MongoDB, Express, React, Node | "MERN Stack Developer" |
| `FullStack_MEAN` | MongoDB, Express, Angular, Node | "MEAN Stack Developer" |
| `FullStack_Java` | Spring Boot, Java, Angular | "Java Developer", "Full Stack Java/Angular" — **strongest match** (Wico stack) |
| `FullStack_General` | Broad full stack | Generic "Full Stack Developer" postings |
| `Universal_FullStack` | Everything (incl. `_ats` and `_long` variants) | Spontaneous applications, recruiters, job fairs |
| `AI_Engineer` | AI/ML, Flask, RAG, LLM | "AI Engineer", "ML Engineer (junior)" |
| `QA_Automation` | Testing, CI quality | "QA Automation", "SDET" |
| `IT_Application_Operations` | Ops, support, monitoring | "IT Operations", "Application Support" |
| `Customer_Support_Telephone_Operator` | Client contact, CRM | Support/telephone operator roles |

## Which title to put in the header

See `profile/job_titles.md` for the full tier list (EN + FR). Always mirror the
exact title from the posting.

## File naming

- Working files: `EN/cv_{variant}_en.tex` / `FR/cv_{variant}_fr.tex` (+ `.pdf`)
- Send-ready copies at the folder root (e.g. `cv_BenNagraYosr.pdf`) are
  renamed exports made when actually sending an application — regenerate them
  from the freshly built EN/FR PDF before sending (recruiters see this filename).

## Build

```bash
# Linux/macOS
./build.sh applications/FullStack_Java
# Windows
.\build.ps1 -Path applications\FullStack_Java
```
