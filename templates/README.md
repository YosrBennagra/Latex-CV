# Templates Catalog

Reusable, ATS-friendly LaTeX templates for Yosr Ben Nagra's CVs and cover letters.
Copy a template into an `applications/{Position_Name}/` folder, then replace the
placeholders (`[ROLE]`, `[COMPANY]`, ...) for the specific job.

All CV templates are designed to be **1 page** and **ATS-parseable** (real text,
selectable, no images of text). Pick based on the company and how the application is submitted.

## CV Templates

| Template | Style | Photo | Columns | Best for |
|----------|-------|:-----:|:-------:|----------|
| `cv_template_classic.tex` | Plain serif, black & white | No | Single | **Maximum ATS safety.** Large ATS (Workday, Taleo, SuccessFactors), banks, public sector, when the parser is unknown. |
| `cv_template_compact.tex` | Compact, blue accents, icons | Yes | Mixed | Dense 1-pager with lots of content. General use when a photo is fine. |
| `cv_template_minimal.tex` | Clean, thin rules, whitespace | No | Single | Modern, design-aware companies; still single-column and ATS-safe. |
| `cv_template_modern.tex` | Colored sidebar | No | Two (sidebar) | Startups / portfolios / direct-to-human applications where look matters more than strict ATS. |

> Tip: if you are not sure whether the company uses a strict ATS, use
> `cv_template_classic.tex` or `cv_template_minimal.tex` (both single-column).

## Cover Letter Types

| Template | Tone | Best for |
|----------|------|----------|
| `cover_letter_formal.tex` | Traditional, formal | Corporates, banks, public sector, recruiters expecting a standard letter. Has full recipient address block. |
| `cover_letter_universal.tex` | Casual, storytelling | Startups / product teams that appreciate personality and a non-templated voice. |
| `cover_letter_concise.tex` | Short, punchy (3 paragraphs) | Fast-moving teams, short "message to the hiring team" boxes, when you want one screen. |
| `cover_letter_technical.tex` | Achievement / metrics-driven | Engineer-led panels and detailed tech-stack postings; maps experience onto requirements with results. |

## Placeholders to replace

- `[ROLE]` — the exact job title from the posting
- `[COMPANY]` — the company name
- `[HIRING MANAGER]` — recipient name if known (formal letter), else keep "Hiring Manager"
- `[CITY]`, `[SOURCE]`, `[STACK]`, `[SPECIFIC REASON]` — only in some letters; see comments at the top of each file
- CV **Key Strengths** bullets — tailor to the job description

## Language

Each CV template defaults to English. To produce the French version, change the `babel`
option near the top of the file:

```latex
\usepackage[english]{babel}  ->  \usepackage[french]{babel}
```

and translate the body text. Keep EN and FR versions synchronized (see `CLAUDE.md`).

## Build

```powershell
cd applications/{Position_Name}
pdflatex cv_{name}_en.tex      # run twice if using references
# or
latexmk -pdf cv_{name}_en.tex
```

`cv_template_modern.tex` requires the `paracol` package (ships with TeX Live / MiKTeX).
`cv_template_compact.tex` optionally uses `fontawesome5` (it has a text fallback if absent).
