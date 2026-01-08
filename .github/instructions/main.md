# CV Optimization Agent - Main Instructions

## 🎯 Core Mission

Generate a PDF CV optimized for a specific job description.

## Workflow

When user pastes a job description:

1. **Parse Job** - Extract title, skills, seniority, requirements
2. **Verify Skills** - Check against `instructions/skills-inventory.md`
3. **Generate CV** - Create optimized CV matching job
4. **Export PDF** - Compile and output final PDF

## Quick Command

```bash
# User pastes job description, Copilot runs:
python -m cv_agent.cli.main generate --job "PASTE_JOB_HERE" --output CV_CompanyName.pdf
```

## 🚨 Critical Rules

### Zero-Hallucination Policy
- **NEVER** add skills not in verified inventory
- **NEVER** modify experience bullets
- **NEVER** fabricate achievements or metrics
- See `instructions/zero-hallucination.md`

### ATS Compliance
- Single-column layout only
- No tables, images, multi-column
- Target score: ≥ 80/100
- See `instructions/ats-rules.md`

### One-Page Limit
- Maximum 3800 characters
- Maximum 9 bullets total
- See `instructions/ats-rules.md`

## What Changes Per Job

### ✅ CHANGE
- **Role/Title**: Match job title exactly
- **Summary**: Rewrite for job requirements
- **Skills Order**: Prioritize job-required skills first

### ❌ DO NOT CHANGE
- Experience bullet points (LOCKED)
- Work history dates/companies
- Education details
- Contact information

## Reference Files

| File | Purpose |
|------|---------|
| `instructions/ats-rules.md` | Formatting & scoring |
| `instructions/bullet-engineering.md` | Action verbs & structure |
| `instructions/zero-hallucination.md` | Verification policy |
| `instructions/skills-inventory.md` | Verified skills list |
| `instructions/summary-writing.md` | Summary guidelines |

## Python Agent Usage

```python
from cv_agent import CVOptimizationAgent

agent = CVOptimizationAgent()
result = agent.generate_pdf(
    job_description="...",
    output_path="CV_CompanyName.pdf",
    company_name="CompanyName"
)

print(f"PDF generated: {result.pdf_path}")
print(f"ATS Score: {result.ats_score}/100")
```

## Output Location

Generated CVs go to: `output/CV_Yosr_BenNagra_{CompanyName}.pdf`
