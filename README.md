# ATS + HR Friendly LaTeX CV Template

This template is designed for maximum Applicant Tracking System (ATS) compatibility and HR readability while remaining clean, dense, and professional.

## Features
- Plain, linear structure (no multi-column layout, text boxes, or graphics)
- Standard fonts (Latin Modern by default; optional sans-serif toggle)
- Semantic macros: `\cvsection`, `\cventry`, `\daterange` for consistent styling
- Optional keyword reinforcement block (`keywords.tex`)
- Minimal packages: `geometry`, `enumitem`, `hyperref`, `xcolor`, `lmodern`
- Highly scannable bullet formatting

## File Overview
- `main.tex` – Your CV content (edit this)
- `preamble.tex` – Formatting + macro definitions (adjust cautiously)
- `keywords.tex` – Optional ATS keyword block (enable/disable)
- `README.md` – Documentation & usage guidance

## Quick Start (Windows PowerShell)
1. Install a LaTeX distribution if not already (MiKTeX or TeX Live).
2. In PowerShell, navigate to the folder:
   ```powershell
   cd E:\LatexCv
   ```
3. Compile:
   ```powershell
   pdflatex main.tex
   pdflatex main.tex  # (Second pass ensures references if any)
   ```
4. Open `main.pdf`.

If `pdflatex` is not found, add your TeX distribution's `bin` directory to PATH or use its package manager UI.

## Editing Instructions
- Replace identity details near the top of `main.tex` (search for `Jane Q. Professional`).
- Keep the `\cventry` structure: arguments are `{Title}{Company}{Location}{Date Range}{Bullet Block}`.
- Write bullets in past tense (except current role where appropriate) and start with a strong verb.
- Use numbers: revenue %, hours saved, latency reduced, cost avoided, adoption increased.
- Keep bullet density at 3–5 per role (4 ideal). Remove weaker bullets first if space is tight.

## Adding / Removing Sections
- Duplicate a block like:
  ```latex
  \cvsection{Projects}
  ... content ...
  ```
- To disable the keyword block: comment out the line in `main.tex`:
  ```latex
  % \showkeywordstrue
  ```
  Or comment out `\input{keywords}` within the conditional.

## Keyword Optimization Tips
- Mirror phrasing from the target job description (e.g., "data pipeline orchestration" vs. just "ETL").
- Use both abbreviations and full forms if space allows (e.g., "KPIs (Key Performance Indicators)").
- Avoid stuffing irrelevant tools; misalignment can hurt credibility in recruiter review.

## ATS Compatibility Practices Used
| Practice | Rationale |
|----------|-----------|
| Single column | Prevents column-order parsing errors |
| Plain text bullets | Ensures extraction fidelity |
| Standard fonts | Avoids invisible glyph issues |
| Minimal packages | Reduces risk of structural PDF oddities |
| No tables for layout | Prevents merged text cells |
| Explicit section headers | Improves semantic parsing |
| Keyword block optional | Allows tailoring per application |

## Switching to Sans-Serif
Uncomment in `preamble.tex`:
```latex
%\renewcommand{\familydefault}{\sfdefault}
```

## Making It Fit One Page
- Remove lesser-impact bullets/projects.
- Slightly tighten spacing (uncomment the suggestions near end of `preamble.tex`).
- Combine similar bullets; prefer impact over method descriptions.

## Multi-Page Guidance
If truly necessary (e.g., >10 years experience):
- Let it expand naturally; page numbers already show via `plain` style.
- Do NOT add decorative headers/footers.

## Common Bullet Patterns
- Reduced X by Y% by doing Z.
- Increased A leading to B outcome within C timeframe.
- Automated X saving N hours/week across Y teams.
- Designed & deployed X resulting in Y (metric) change.

## Recommended Verbs
Led, Built, Automated, Optimized, Architected, Consolidated, Reduced, Increased, Standardized, Designed, Implemented, Developed, Delivered, Streamlined, Improved

## Custom Macros (Advanced)
You may add role-specific convenience macros (e.g., `\newcommand{\tool}[1]{\texttt{#1}}`) but keep usage sparse—ATS parsers should still output plain text logically.

## Export / Submission
Always submit as a PDF generated from LaTeX (never a scanned image). Optionally verify extraction by copying all PDF text into a plain `.txt` file—ensure ordering is logical.

## Troubleshooting
| Issue | Fix |
|-------|-----|
| Words run together after extraction | Ensure `\frenchspacing` is acceptable; if not, remove it. |
| Overfull lines warnings | Shorten or rephrase long bullets. |
| Missing package | Install via MiKTeX package prompt or TeX Live Manager. |
| PDF shows strange characters | Confirm UTF-8 encoding and keep `inputenc` + `fontenc`.

## Next Steps / Optional Enhancements
- Add `\newcommand{\metric}[1]{\textbf{#1}}` to bold key numbers.
- Add a `Publications` section if academically oriented.
- Add version control (git) to track modifications per role.

---
Tailor each submission: adjust Summary + first 2 bullets of the most recent role to align with the posting.

Good luck!
