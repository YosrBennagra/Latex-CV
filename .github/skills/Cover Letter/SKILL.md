---
name: cover-letter
description: 'Use when creating cover letters for job applications. Always creates EN + FR versions.'
---

# Cover Letter Creator

## When to Use
- User asks to create a cover letter for a job application
- A new CV is being tailored — cover letters are MANDATORY
- When NOT to use: updating existing CVs without a new application

## Non-Negotiable Rules
1. Always use canonical data from `data_profile.json`
2. Never fabricate experience or skills
3. Create both English and French versions
4. Tailor to the specific job requirements
5. Create a dedicated folder in `applications/{Company}_{Position}_{Date}/` if one doesn't exist

## Procedure
1. Read `data_profile.json` for contact info and profile
2. Analyze job description for key requirements
3. Match user's skills and experience to job needs
4. Generate cover letter in `applications/{Company}_{Position}_{Date}/`
5. Create both `cover_letter_{company}_en.tex` and `cover_letter_{company}_fr.tex`

## Structure
1. **Header**: Name, contact, date
2. **Recipient**: Company name, HR department
3. **Subject**: Position applied for
4. **Opening**: Express genuine interest
5. **Body** (3 paragraphs):
   - Education background + experience overview
   - Technical skills aligned with job requirements
   - Project highlights with specific achievements
6. **Closing**: Availability, call to action
7. **Signature**: Name

## Tone
- Professional, enthusiastic, specific
- Reference actual projects and achievements
- Confident but authentic
- Show genuine interest in the role

## Key Files
- `templates/cover_letter_universal.tex` — base template (letter class, lmodern font)
- `data_profile.json` — canonical contact info and profile
- `applications/{Company}_{Position}_{Date}/cover_letter_{company}_en.tex` + `_fr.tex`

## LaTeX Template Notes
- Document class: `letter` (10pt, a4paper)
- Uses `lmodern` font, `hyperref` with blue URLs
- Margins: 0.6in top/bottom, 0.75in sides
- `\signature{Yosr Ben Nagra}` and `\address{}` pre-filled from profile
- Content inside `\begin{letter}{}...\end{letter}` environment

## Common Mistakes
- **Forgetting to create both EN + FR** — always generate both versions
- **Generic opening** — avoid "I am writing to express interest"; use authentic, specific tone
- **Fabricating achievements** — only reference real projects from data_profile.json
- **Missing cover letter entirely** — cover letters are MANDATORY for every application
