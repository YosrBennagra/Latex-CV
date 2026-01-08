# CV Agent 2.0 - Architecture Documentation

## 🎯 Complete Reorganization Summary

**Previous Structure (Monolithic):**
```
cv-agent/
  agent/           # All modules mixed together
    orchestrator.py
    job_parser.py
    cv_parser.py
    optimizer.py
    ats_scorer.py
    one_page_enforcer.py
    validator.py
  latex/           # Single renderer
  mcp/             # MCP server
  tests/           # Few tests
  data/            # Mixed data
```

**New Structure (Domain-Driven Design):**
```
cv_agent/
  domain/          # Core models & verified inventory
  parsing/         # Job & CV parsing
  scoring/         # ATS & relevance scoring
  optimization/    # Content optimization
  enforcement/     # Rules enforcement
  validation/      # Quality validation
  rendering/       # LaTeX generation
  mcp/             # MCP server integration
  cli/             # Command-line interface
  core/            # Main orchestrator
  tests/           # Comprehensive test suite
```

---

## 📦 Package Structure (10 Modules)

### 1. **domain/** - Core Models & Verified Inventory
**Purpose:** Define data structures and canonical truth

**Files:**
- `models.py` - Data classes (JobData, CVData, ExperienceItem, ValidationResult, etc.)
- `inventory.py` - VERIFIED_SKILLS, VERIFIED_EXPERIENCES, FORBIDDEN_SKILLS

**Key Classes:**
- `JobData` - Parsed job requirements
- `CVData` - Structured CV content
- `ExperienceItem` - Work experience entry
- `ValidationResult` - Validation outcome
- `VerifiedExperience` - Canonical experience bullets
- `VerifiedProject` - Canonical project descriptions

**Zero-Hallucination Guarantee:**
```python
VERIFIED_SKILLS = {
    "Python", "Java", "JavaScript", "TypeScript", "React",
    "Node.js", "Docker", "Kubernetes", "AWS", ...  # 61 total
}

FORBIDDEN_SKILLS = {
    "Rust", "Go", "C++", "Blockchain", ...
}
```

---

### 2. **parsing/** - Input Parsing
**Purpose:** Extract structured data from job descriptions and LaTeX CVs

**Files:**
- `job_parser.py` - JobParser class
- `cv_parser.py` - CVParser class

**Key Methods:**
```python
class JobParser:
    def parse(text: str) -> JobData:
        # Extracts: title, seniority, skills, responsibilities
        # Detects: language (EN/FR), required vs preferred skills
        
class CVParser:
    def parse(path: Path) -> CVData:
        # Extracts: experiences, skills, education, projects
        # Handles: LaTeX macros (\cvrole, \cvsummary, \item)
```

---

### 3. **scoring/** - Analysis & Scoring
**Purpose:** Calculate ATS compatibility and job relevance

**Files:**
- `ats_scorer.py` - ATSScorer class (0-100 score)
- `relevance.py` - RelevanceAnalyzer class

**Key Metrics:**
```python
class ATSScorer:
    def calculate_score(cv: CVData, job: JobData) -> int:
        # Keyword match: 40%
        # Formatting: 30%
        # Experience relevance: 20%
        # Skills match: 10%
        
class RelevanceAnalyzer:
    def analyze(cv: CVData, job: JobData) -> RelevanceScore:
        # Ranks experiences, projects by job fit
        # Identifies skill gaps
```

---

### 4. **optimization/** - Content Optimization
**Purpose:** Rewrite CV content for job relevance while preserving truth

**Files:**
- `optimizer.py` - ContentOptimizer class
- `bullets.py` - BulletEngineer class (action verbs)

**Canonical Experience Enforcement:**
```python
class ContentOptimizer:
    def _get_canonical_experience(company: str) -> VerifiedExperience:
        # Returns LOCKED bullet points from inventory
        # NEVER modifies experience bullets
        # Only reorders/prioritizes by relevance
        
class BulletEngineer:
    POWER_VERBS = {"Architected", "Engineered", "Optimized"}
    WEAK_VERBS = {"helped", "tried", "worked on"}
```

---

### 5. **enforcement/** - Rules Enforcement
**Purpose:** Ensure one-page limit and ATS compliance

**Files:**
- `page_enforcer.py` - OnePageEnforcer class
- `ats_enforcer.py` - ATSEnforcer class

**Page Limit Strategy:**
```python
class OnePageEnforcer:
    MAX_CONTENT_CHARS = 3800  # Empirical limit for 1 page
    
    def enforce(cv: CVData) -> CVData:
        # 1. Estimate page count
        # 2. Trim low-relevance bullets
        # 3. Limit to 3 bullets per experience
        # 4. Remove oldest experiences if needed
```

**ATS Red Flags:**
```python
class ATSEnforcer:
    FORBIDDEN_PATTERNS = [
        r"\\begin{tabular}",     # Tables
        r"\\includegraphics",    # Images
        r"\\begin{multicol}",    # Multi-column
    ]
```

---

### 6. **validation/** - Quality Checks
**Purpose:** Validate tone, ATS compliance, and detect hallucination

**Files:**
- `validator.py` - CVValidator class
- `hallucination.py` - HallucinationDetector class

**Hallucination Detection:**
```python
class HallucinationDetector:
    def detect(original: CVData, optimized: CVData) -> List[str]:
        # Check: Skills not in VERIFIED_SKILLS
        # Check: Modified experience bullets
        # Check: Fabricated projects
        # Check: Perfect skill match (suspiciously aligned)
```

---

### 7. **rendering/** - LaTeX Generation
**Purpose:** Generate clean, ATS-friendly LaTeX output

**Files:**
- `renderer.py` - LaTeXRenderer class

**Output Structure:**
```latex
\input{../../preamble}
\cvrole{Software Engineer}
\cvname{Yosr Ben Nagra}
\cvsummary{280-340 character summary}
\begin{cvskills}
  \item Python, JavaScript, TypeScript, React, Node.js
\end{cvskills}
\begin{cvexperience}
  \cventry{IT Serv}{Full-Stack Developer Intern}{Feb 2025 - Aug 2025}{Tunis}
  \begin{itemize}
    \item Designed full-stack web platform integrating AI, DevOps, and RAG
    \item Implemented AI-powered symptom checker, doctor blog, patient forum
    \item Fine-tuned AI model and set up CI/CD, containerization, monitoring
  \end{itemize}
\end{cvexperience}
```

---

### 8. **mcp/** - MCP Server Integration
**Purpose:** Expose CV optimization tools via Model Context Protocol

**Files:**
- `server.py` - MCPServer class

**Available Tools:**
```python
class MCPServer:
    def handle_request(tool_name: str, params: dict):
        # get_verified_skills - List all verified skills
        # validate_skill - Check if skill exists
        # get_canonical_experience - Get locked bullets
        # get_projects - Get verified projects
        # score_cv - Calculate ATS score
        # optimize_cv - Full optimization pipeline
```

---

### 9. **cli/** - Command-Line Interface
**Purpose:** User-friendly terminal commands

**Files:**
- `main.py` - CLI entry point

**Commands:**
```bash
# Optimize CV for job
python -m cv_agent.cli.main optimize --job "job.txt" --output cv_optimized.tex

# Score ATS compatibility
python -m cv_agent.cli.main score --cv cv.tex --job "job.txt"

# Validate CV
python -m cv_agent.cli.main validate --cv cv.tex

# List verified skills
python -m cv_agent.cli.main skills --list
```

---

### 10. **core/** - Main Orchestrator
**Purpose:** Coordinate all modules in 10-step optimization pipeline

**Files:**
- `orchestrator.py` - CVOptimizationAgent class

**Optimization Pipeline:**
```python
class CVOptimizationAgent:
    def optimize(job_description, cv_path, output_path, company):
        # Step 1: Parse job description
        # Step 2: Parse existing CV
        # Step 3: Calculate ATS score
        # Step 4: Analyze relevance
        # Step 5: Optimize content (role, summary, skills)
        # Step 6: Enforce one page
        # Step 7: Validate ATS compliance
        # Step 8: Detect hallucination
        # Step 9: Render LaTeX
        # Step 10: Return result with metrics
```

---

## 🧪 Test Suite

**Structure:**
```
tests/
  test_domain.py       # Data models & inventory (17 tests)
  test_parsing.py      # Job & CV parsing (8 tests)
  test_scoring.py      # ATS & relevance scoring (6 tests)
  test_enforcement.py  # Page & ATS enforcement (8 tests)
  test_validation.py   # Validation & hallucination (10 tests)
```

**Run Tests:**
```bash
cd E:\LatexCv\cv_agent
pytest tests/ -v
pytest tests/test_domain.py -v
pytest tests/ --cov=cv_agent --cov-report=html
```

---

## 📊 Key Improvements

### Before → After

| Aspect | Before (Monolithic) | After (Domain-Driven) |
|--------|---------------------|----------------------|
| **Structure** | 1 package, 8 files mixed | 10 packages, clear separation |
| **Testability** | Few tests, hard to mock | 5 test modules, fixtures |
| **Modularity** | Tight coupling | Loose coupling, single responsibility |
| **Maintainability** | Hard to find code | Clear domain boundaries |
| **Extensibility** | Risky to modify | Easy to add features |
| **Hallucination Prevention** | Scattered logic | Centralized inventory + detector |

---

## 🚀 Usage Examples

### 1. Basic CV Optimization
```python
from cv_agent import CVOptimizationAgent
from pathlib import Path

agent = CVOptimizationAgent()
result = agent.optimize(
    job_description="Full-Stack Developer, React, Node.js, AWS...",
    cv_path=Path("CVs/English/CV_Yosr_BenNagra_English_ATS.tex"),
    output_path=Path("CVs/English/CV_Yosr_BenNagra_English_CompanyX.tex"),
    company_name="CompanyX"
)

print(f"ATS Score: {result.ats_score}/100")
print(f"Relevance: {result.relevance_score}")
print(f"Page Count: {result.estimated_pages}")
print(f"Warnings: {result.warnings}")
```

### 2. Skill Verification
```python
from cv_agent.domain import is_skill_verified, is_skill_forbidden

# Verify skills before adding
is_skill_verified("React")        # True
is_skill_verified("Blockchain")   # False
is_skill_forbidden("Rust")        # True
```

### 3. Custom Parsing
```python
from cv_agent.parsing import JobParser, CVParser
from pathlib import Path

# Parse job description
job_parser = JobParser()
job_data = job_parser.parse("Senior React Developer, 5+ years...")

print(f"Title: {job_data.title}")
print(f"Seniority: {job_data.seniority}")
print(f"Required Skills: {job_data.required_skills}")

# Parse CV
cv_parser = CVParser()
cv_data = cv_parser.parse(Path("CVs/English/CV_Yosr_BenNagra_English_ATS.tex"))

print(f"Role: {cv_data.role}")
print(f"Skills: {cv_data.skills}")
print(f"Experiences: {len(cv_data.experiences)}")
```

### 4. ATS Scoring
```python
from cv_agent.scoring import ATSScorer, RelevanceAnalyzer

scorer = ATSScorer()
score = scorer.calculate_score(cv_data, job_data)
print(f"ATS Score: {score}/100")

analyzer = RelevanceAnalyzer()
relevance = analyzer.analyze(cv_data, job_data)
print(f"Skill Gaps: {relevance.skill_gaps}")
```

### 5. CLI Usage
```bash
# List all verified skills
python -m cv_agent.cli.main skills --list

# Check specific skill
python -m cv_agent.cli.main skills --check "React"

# Optimize CV
python -m cv_agent.cli.main optimize \
  --job job_description.txt \
  --cv CVs/English/CV_Yosr_BenNagra_English_ATS.tex \
  --output CVs/English/CV_Yosr_BenNagra_English_NewCompany.tex \
  --company "NewCompany"

# Score CV
python -m cv_agent.cli.main score \
  --cv CVs/English/CV_Yosr_BenNagra_English_ATS.tex \
  --job job_description.txt

# Validate CV
python -m cv_agent.cli.main validate \
  --cv CVs/English/CV_Yosr_BenNagra_English_ATS.tex
```

---

## 🛡️ Zero-Hallucination Policy

**How It Works:**

1. **Verified Inventory** (`domain/inventory.py`)
   - `VERIFIED_SKILLS` - 61 skills that can be claimed
   - `VERIFIED_EXPERIENCES` - 3 companies with locked bullets
   - `VERIFIED_PROJECTS` - 2 projects with frozen descriptions
   - `FORBIDDEN_SKILLS` - Skills that should never be added

2. **Optimization Constraints** (`optimization/optimizer.py`)
   - Can only reorder/prioritize existing content
   - Cannot modify experience bullet points
   - Cannot add skills not in VERIFIED_SKILLS
   - Cannot fabricate metrics or achievements

3. **Hallucination Detection** (`validation/hallucination.py`)
   - Compares original vs optimized CV
   - Flags new skills not in inventory
   - Detects modified experience bullets
   - Warns about perfect skill matches (suspicious alignment)

4. **MCP Integration** (`mcp/server.py`)
   - AI assistants query verified inventory before adding content
   - `validate_skill(skill)` → Returns true/false
   - `get_canonical_experience(company)` → Returns locked bullets

**Example:**
```python
from cv_agent.validation import HallucinationDetector

detector = HallucinationDetector()
warnings = detector.detect(original_cv, optimized_cv)

# Sample warnings:
# - "Skill 'Blockchain' not in verified inventory"
# - "Experience bullet modified for IT Serv"
# - "Perfect skill match (100%) - suspiciously aligned"
```

---

## 📈 Metrics & Validation

### ATS Score Breakdown (0-100)
- **40%** Keyword match (required skills present)
- **30%** Formatting compliance (no tables, images, multi-column)
- **20%** Experience relevance (seniority, responsibilities match)
- **10%** Skills match (quantity and quality)

### Page Count Estimation
```python
class OnePageEnforcer:
    def estimate_size(cv: CVData) -> int:
        # Count all content characters
        # Summary: 280-340 chars
        # Skills: ~200 chars
        # Experience: 3 bullets × 100 chars × N experiences
        # Education: ~150 chars
        # Target: ≤ 3800 chars
```

### Validation Checks
- ✅ ATS compliance (no red flags)
- ✅ Professional tone (no weak verbs)
- ✅ Factual accuracy (no hallucination)
- ✅ One-page limit (≤ 3800 chars)
- ✅ Strong action verbs (power verbs used)
- ✅ Quantified achievements (where available)

---

## 🔧 Configuration

**pyproject.toml:**
```toml
[project]
name = "cv-agent"
version = "2.0.0"
requires-python = ">=3.10"
dependencies = ["pydantic>=2.0.0"]

[project.scripts]
cv-agent = "cv_agent.cli.main:main"

[project.optional-dependencies]
dev = ["pytest>=7.0.0", "black>=23.0.0", "ruff>=0.1.0", "mypy>=1.0.0"]
```

**Install:**
```bash
cd E:\LatexCv\cv_agent
pip install -e .               # Install in editable mode
pip install -e ".[dev]"        # Install with dev dependencies
```

---

## 📚 Dependencies

- **pydantic** - Data validation and modeling
- **pytest** - Testing framework
- **black** - Code formatting
- **ruff** - Linting
- **mypy** - Type checking

---

## 🎓 Design Principles

1. **Single Responsibility Principle**
   - Each package has one clear purpose
   - No mixed concerns

2. **Domain-Driven Design**
   - Core domain (models, inventory) at center
   - Application services (parsing, scoring, optimization) around it
   - Infrastructure (rendering, MCP, CLI) at edges

3. **Immutability**
   - Data classes frozen where appropriate
   - Experience bullets stored as tuples
   - Prevents accidental modification

4. **Dependency Inversion**
   - Core depends on domain, not infrastructure
   - Easy to swap LaTeX renderer for JSON/PDF

5. **Open/Closed Principle**
   - Easy to add new scorers, validators, enforcers
   - No need to modify existing code

---

## 🚦 Next Steps

### Potential Enhancements
1. **Add More Verified Experiences**
   - Expand `VERIFIED_EXPERIENCES` with more internships
   - Add canonical bullets for freelance work

2. **Integration Tests**
   - End-to-end optimization workflow
   - Real job descriptions → optimized CVs

3. **Performance Optimization**
   - Cache parsed CVs
   - Parallel processing for multiple jobs

4. **Additional Renderers**
   - JSON output for web applications
   - PDF generation via LaTeX compilation
   - Markdown format for GitHub profiles

5. **Enhanced MCP Tools**
   - `suggest_skills` - Recommend missing skills
   - `rank_jobs` - Score multiple jobs by CV fit
   - `generate_summary` - AI-powered summary writing

6. **CI/CD Pipeline**
   - GitHub Actions for tests
   - Automatic PyPI publishing
   - Pre-commit hooks for formatting

---

## 📝 License

MIT License - See LICENSE file for details

---

## 👤 Author

**Yosr Ben Nagra**
- Email: yosrbennagra@gmail.com
- LinkedIn: [linkedin.com/in/yosr-ben-nagra](https://linkedin.com/in/yosr-ben-nagra)
- GitHub: [github.com/yosrbennagra](https://github.com/yosrbennagra)

---

**Last Updated:** January 2025
**Version:** 2.0.0
**Status:** Production Ready ✅
