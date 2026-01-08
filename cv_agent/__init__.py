"""
CV Optimization Agent v2.0
==========================

An AI-powered agent that optimizes LaTeX CVs based on job descriptions.

🏗️ Architecture (Domain-Driven Design):
┌─────────────────────────────────────────────────────────────┐
│                        cv-agent/                            │
├──────────────┬──────────────┬──────────────┬───────────────┤
│   domain/    │   parsing/   │   scoring/   │ optimization/ │
│  • Models    │  • JobParser │  • ATSScorer │  • Optimizer  │
│  • Inventory │  • CVParser  │  • Relevance │  • Bullets    │
├──────────────┼──────────────┼──────────────┼───────────────┤
│ enforcement/ │ validation/  │  rendering/  │     mcp/      │
│  • OnePage   │  • Validator │  • LaTeX     │  • Server     │
│  • ATS       │  • Hallucin. │              │  • Tools      │
├──────────────┴──────────────┴──────────────┴───────────────┤
│                      core/orchestrator                      │
│                      cli/commands                           │
└─────────────────────────────────────────────────────────────┘

Usage:
    from cv_agent import CVOptimizationAgent
    
    agent = CVOptimizationAgent()
    result = agent.optimize(
        job_description="Senior React Developer needed...",
        output_path=Path("CVs/English/CV_Optimized.tex")
    )
    
    print(f"ATS Score: {result.ats_score}")
    print(f"Pages: {result.page_count}")

Zero-Hallucination Policy:
    The agent NEVER adds skills, experiences, or achievements
    not present in the verified inventory (domain/inventory.py).
"""

__version__ = "2.0.0"
__author__ = "Yosr Ben Nagra"

from .core import CVOptimizationAgent, OptimizationResult
from .domain import (
    JobData, CVData, ExperienceItem, ValidationResult,
    VERIFIED_SKILLS, is_skill_verified, is_skill_forbidden
)
from .rendering import PDFGenerator


def generate_cv(
    job_description: str,
    company: str = "Company",
    candidate_name: str = "Yosr Ben Nagra"
) -> OptimizationResult:
    """
    Generate an optimized PDF CV for a job description.
    
    This is the main entry point for quick CV generation.
    
    Args:
        job_description: The job posting text
        company: Company name for filename
        candidate_name: Your name
        
    Returns:
        OptimizationResult with pdf_path, ats_score, etc.
        
    Example:
        >>> from cv_agent import generate_cv
        >>> result = generate_cv("Senior React Developer...", company="Google")
        >>> print(f"Generated: {result.pdf_path}")
        >>> print(f"ATS Score: {result.ats_score}")
    """
    agent = CVOptimizationAgent()
    return agent.generate_pdf(
        job_description=job_description,
        company_name=company,
        candidate_name=candidate_name
    )


__all__ = [
    # Core
    "CVOptimizationAgent",
    "OptimizationResult",
    # High-level API
    "generate_cv",
    # Domain
    "JobData",
    "CVData", 
    "ExperienceItem",
    "ValidationResult",
    # Inventory
    "VERIFIED_SKILLS",
    "is_skill_verified",
    "is_skill_forbidden",
    # Rendering
    "PDFGenerator",
]
