# Skill: Cover Letter Creator

## When to Use
Use this skill when the user asks to create a cover letter for a job application.

## Inputs
- Job description provided by user
- Canonical data from `data_profile.json`
- User's skills, experience, and background

## Non-Negotiable Rules
1. Always use canonical data from `data_profile.json` for contact info and profile details.
2. Never fabricate experience or skills not in the user's profile.
3. Create both English and French versions unless user specifies otherwise.
4. Tailor the letter to match the specific job requirements.
5. Highlight relevant skills and experience from the user's actual background.
6. Keep format consistent with existing cover letters in applications/ folder.
7. Create a dedicated folder in applications/ with format: CompanyName_Position_YYYY-MM-DD

## Procedure
1. Read `data_profile.json` for canonical user data.
2. Analyze job description for key requirements and company info.
3. Match user's skills and experience to job requirements.
4. Create folder: applications/CompanyName_Position_YYYY-MM-DD/
5. Create cover_letter_company_en.txt and cover_letter_company_fr.txt
6. Optionally create job_description.md and notes.md for reference.

## Structure
- Header: Name, phone, location, portfolio, GitHub, LinkedIn
- Recipient: Company name and HR/department
- Subject line: Position applied for
- Opening: Express interest in the position
- Body paragraphs:
  - Educational background and experience summary
  - Technical skills alignment with job requirements
  - Relevant project experience with specific achievements
  - What motivates you about this position
  - How you can contribute to the company
- Closing: Availability and call to action
- Signature: Name

## Tone
- Professional and enthusiastic
- Specific and evidence-based (reference actual projects)
- Confident but not arrogant
- Show genuine interest in company mission and role

## Output
- cover_letter_[company]_en.txt (English version)
- cover_letter_[company]_fr.txt (French version)
- job_description.md (job posting saved for reference)
- notes.md (optional analysis notes)
