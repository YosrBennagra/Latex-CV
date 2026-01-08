# CV Optimization Agent

AI-powered CV generator that creates tailored PDF CVs for job applications.

## 🚀 Quick Start

```python
from cv_agent import generate_cv

# Paste job description, get optimized PDF
result = generate_cv(
    job_description="Senior React Developer needed...",
    company="Google"
)

print(f"PDF: {result.pdf_path}")
print(f"ATS Score: {result.ats_score}/100")
```

## 📁 Project Structure

```
LatexCv/
├── .github/
│   ├── copilot-instructions.md    # Main Copilot context
│   └── instructions/              # Detailed instruction files
│       ├── main.md                # Core workflow
│       ├── ats-rules.md           # ATS optimization
│       ├── bullet-engineering.md  # Action verbs
│       ├── zero-hallucination.md  # Verification policy
│       ├── skills-inventory.md    # Verified skills list
│       └── summary-writing.md     # Summary guidelines
├── cv_agent/                      # Python package
│   ├── domain/                    # Data models & inventory
│   ├── parsing/                   # Job & CV parsing
│   ├── scoring/                   # ATS scoring
│   ├── optimization/              # Content optimization
│   ├── enforcement/               # Page & ATS rules
│   ├── validation/                # Hallucination detection
│   ├── rendering/                 # LaTeX & PDF generation
│   ├── mcp/                       # MCP server
│   ├── cli/                       # Command-line interface
│   └── core/                      # Main orchestrator
├── templates/                     # Base CV templates
│   ├── CV_Base_English.tex
│   ├── CV_Base_French.tex
│   └── preamble.tex
├── output/                        # Generated PDFs go here
└── archive/                       # Old CVs (reference)
```

## 🔧 Installation

```bash
cd cv_agent
pip install -e .
```

## 💻 Usage

### With Copilot Chat

Just paste a job description and say:
> "Generate a CV for this job"

### CLI

```bash
# Generate PDF for a job
python -m cv_agent.cli.main generate --job "job_description.txt" --company Google

# List verified skills
python -m cv_agent.cli.main skills --list

# Score existing CV
python -m cv_agent.cli.main score --cv templates/CV_Base_English.tex --job "..."
```

### Python API

```python
from cv_agent import generate_cv, CVOptimizationAgent

# Quick generation
result = generate_cv("Full Stack Developer...", company="Startup")

# Or with more control
agent = CVOptimizationAgent()
result = agent.generate_pdf(
    job_description="...",
    company_name="CompanyName"
)
```

## 🛡️ Zero-Hallucination Policy

The agent **NEVER** fabricates content:
- Only uses skills from verified inventory (61 skills)
- Never modifies experience bullets
- Never adds fake achievements

See [.github/instructions/zero-hallucination.md](.github/instructions/zero-hallucination.md)

## 📊 What Gets Optimized

| Section | Customized? | Notes |
|---------|-------------|-------|
| Role/Title | ✅ Yes | Matches job title |
| Summary | ✅ Yes | Rewritten for job |
| Skills Order | ✅ Yes | Job-relevant first |
| Experience Bullets | ❌ No | LOCKED |
| Education | ❌ No | Static |

## ⚙️ Requirements

- Python 3.10+
- pdflatex (TeX Live or MiKTeX) for PDF generation
- pydantic

## 📄 Output

Generated CVs saved to: `output/CV_Yosr_BenNagra_{Company}.pdf`

## Author

**Yosr Ben Nagra**
- Email: yosrbennagra@gmail.com
- LinkedIn: [linkedin.com/in/yosr-ben-nagra](https://linkedin.com/in/yosr-ben-nagra)
