# CV Optimization Agent - Copilot Instructions

## 🎯 What This Does

When you paste a job description, I generate a tailored PDF CV optimized for that job.

## Usage

Just paste a job description and say "generate CV" or "optimize for this job".

**Example:**
```
Generate a CV for:

Software Engineer - Google
Requirements: Python, React, Kubernetes, 3+ years experience...
```

## How It Works

1. **Parse** your job description
2. **Verify** all skills against inventory
3. **Optimize** CV content for the job
4. **Generate** PDF output

## 🚨 Critical Policies

### Zero-Hallucination
- I will NEVER add skills you don't have
- I will NEVER fabricate achievements
- I will NEVER modify your verified experience bullets
- See [zero-hallucination.md](instructions/zero-hallucination.md)

### ATS Compliance
- Single-column format only
- No tables, images, or fancy formatting
- Target ATS score: 80+/100
- See [ats-rules.md](instructions/ats-rules.md)

### One-Page Rule
- Maximum 3800 characters
- Maximum 9 bullet points
- Always exactly 1 page

## What Gets Customized

| Section | Customized? | Notes |
|---------|------------|-------|
| Role/Title | ✅ Yes | Matches job title |
| Summary | ✅ Yes | Rewritten for job |
| Skills Order | ✅ Yes | Job-relevant first |
| Experience Bullets | ❌ No | LOCKED - never changed |
| Education | ❌ No | Static |
| Contact | ❌ No | Static |

## Reference Documentation

- [Main Instructions](instructions/main.md)
- [ATS Rules](instructions/ats-rules.md)
- [Bullet Engineering](instructions/bullet-engineering.md)
- [Zero-Hallucination Policy](instructions/zero-hallucination.md)
- [Skills Inventory](instructions/skills-inventory.md)
- [Summary Writing](instructions/summary-writing.md)

## Quick Commands

```bash
# Generate PDF for job
python -m cv_agent generate "job description here"

# Check ATS score
python -m cv_agent score --job "job description"

# List verified skills
python -m cv_agent skills --list
```

## Python API

```python
from cv_agent import generate_cv

# Generate optimized PDF
result = generate_cv(
    job_description="Your job description here...",
    company="Google"
)

print(f"Generated: {result.pdf_path}")
print(f"ATS Score: {result.ats_score}")
```

## Output

Generated CVs are saved to: `output/CV_Yosr_BenNagra_{Company}.pdf`
