"""
Core Orchestrator
=================

Main CV optimization agent that coordinates all components.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass

from ..domain import CVData, JobData, ValidationResult, OptimizationConfig
from ..parsing import JobParser, CVParser
from ..scoring import ATSScorer, RelevanceAnalyzer
from ..optimization import ContentOptimizer
from ..enforcement import OnePageEnforcer, ATSEnforcer
from ..validation import CVValidator, HallucinationDetector
from ..rendering import LaTeXRenderer, PDFGenerator

logger = logging.getLogger(__name__)


@dataclass
class OptimizationResult:
    """Result of CV optimization."""
    optimized_cv: str
    output_path: Optional[Path]
    ats_score: float
    relevance_score: float
    page_count: float
    validation_passed: bool
    warnings: List[str]
    pdf_path: Optional[Path] = None


class CVOptimizationAgent:
    """
    Main orchestrator for CV optimization.
    
    Workflow:
    1. Parse job description
    2. Parse existing CV
    3. Analyze relevance
    4. Optimize content
    5. Enforce one-page limit
    6. Validate output
    7. Render LaTeX
    
    Zero-Hallucination: Never adds fabricated content.
    """
    
    # Default base CV path (templates folder)
    DEFAULT_CV = Path(__file__).parent.parent.parent / "templates" / "CV_Base_English.tex"
    
    def __init__(self, config: OptimizationConfig = None):
        """Initialize the agent with all components."""
        self.config = config or OptimizationConfig()
        
        # Initialize components
        self.job_parser = JobParser()
        self.cv_parser = CVParser()
        self.ats_scorer = ATSScorer()
        self.relevance_analyzer = RelevanceAnalyzer()
        self.optimizer = ContentOptimizer(self.config)
        self.page_enforcer = OnePageEnforcer(self.config)
        self.ats_enforcer = ATSEnforcer()
        self.validator = CVValidator()
        self.hallucination_detector = HallucinationDetector()
        self.renderer = LaTeXRenderer()
        self.pdf_generator = PDFGenerator()
        
        # Preamble path for PDF generation (templates folder)
        self.preamble_path = Path(__file__).parent.parent.parent / "templates" / "preamble.tex"
        
        logger.info("CV Optimization Agent initialized")
    
    def optimize(
        self,
        job_description: str,
        cv_path: Path = None,
        output_path: Path = None,
        company_name: str = None,
        candidate_name: str = "Yosr Ben Nagra"
    ) -> OptimizationResult:
        """
        Optimize a CV for a job description.
        
        Args:
            job_description: Raw job posting text
            cv_path: Path to existing CV (defaults to base CV)
            output_path: Where to save output
            company_name: Company name for customization
            candidate_name: Candidate name
            
        Returns:
            OptimizationResult with metrics and output
        """
        logger.info(f"Starting optimization for {company_name or 'job'}")
        warnings = []
        
        # Step 1: Parse job description
        logger.info("Step 1: Parsing job description...")
        job_data = self.job_parser.parse(job_description)
        logger.info(f"  Found {len(job_data.required_skills)} required skills")
        
        # Step 2: Parse existing CV
        cv_path = cv_path or self.DEFAULT_CV
        logger.info(f"Step 2: Parsing CV from {cv_path.name}...")
        cv_data = self.cv_parser.parse(cv_path)
        logger.info(f"  Found {len(cv_data.experience)} experiences, {len(cv_data.skills)} skills")
        
        # Step 3: Analyze relevance
        logger.info("Step 3: Analyzing relevance...")
        relevance = self.relevance_analyzer.analyze(cv_data, job_data)
        logger.info(f"  Overall relevance: {relevance['overall_score']:.0f}%")
        
        # Step 4: Optimize content
        logger.info("Step 4: Optimizing content...")
        optimized = self.optimizer.optimize(cv_data, job_data, relevance, company_name)
        if optimized.get('warnings'):
            warnings.extend(optimized['warnings'])
        
        # Step 5: Detect hallucination
        logger.info("Step 5: Checking for hallucination...")
        hall_warnings = self.hallucination_detector.detect(optimized, cv_data, job_data)
        warnings.extend(hall_warnings)
        
        # Step 6: Enforce one-page
        logger.info("Step 6: Enforcing one-page limit...")
        enforced = self.page_enforcer.enforce(optimized)
        page_count = self.page_enforcer.estimate_pages(enforced)
        logger.info(f"  Estimated pages: {page_count}")
        
        # Step 7: Validate
        logger.info("Step 7: Validating output...")
        validation = self.validator.validate(enforced, job_data, page_count)
        warnings.extend(validation.all_warnings)
        
        # Step 8: Calculate ATS score
        ats_score = self.ats_scorer.calculate_score(cv_data, job_data)
        
        # Step 9: Render LaTeX
        logger.info("Step 8: Rendering LaTeX...")
        latex_output = self.renderer.render(enforced, candidate_name)
        
        # Step 10: Check LaTeX compliance
        compliant, latex_issues = self.ats_enforcer.check_compliance(latex_output)
        if not compliant:
            warnings.extend(latex_issues)
        
        # Step 11: Save output
        if output_path:
            logger.info(f"Saving to {output_path}...")
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(latex_output, encoding='utf-8')
        
        logger.info("Optimization complete!")
        
        return OptimizationResult(
            optimized_cv=latex_output,
            output_path=output_path,
            ats_score=ats_score,
            relevance_score=relevance['overall_score'],
            page_count=page_count,
            validation_passed=validation.passed,
            warnings=warnings,
            pdf_path=None
        )

    def generate_pdf(
        self,
        job_description: str,
        company_name: str = "Company",
        candidate_name: str = "Yosr Ben Nagra",
        cv_path: Path = None,
    ) -> OptimizationResult:
        """
        Generate an optimized PDF CV for a job.
        
        This is the main entry point for CV generation.
        
        Args:
            job_description: Raw job posting text
            company_name: Company name for output filename
            candidate_name: Candidate name
            cv_path: Path to base CV (optional)
            
        Returns:
            OptimizationResult with pdf_path set
        """
        logger.info(f"Generating PDF CV for {company_name}")
        
        # Sanitize company name for filename
        safe_company = "".join(c for c in company_name if c.isalnum() or c in " _-").strip()
        safe_company = safe_company.replace(" ", "_")
        
        # Generate output name
        output_name = f"CV_Yosr_BenNagra_{safe_company}"
        
        # Create temp .tex output path
        tex_output = self.pdf_generator.output_dir / f"{output_name}.tex"
        
        # Run optimization
        result = self.optimize(
            job_description=job_description,
            cv_path=cv_path,
            output_path=tex_output,
            company_name=company_name,
            candidate_name=candidate_name
        )
        
        # Generate PDF
        if self.pdf_generator.is_available():
            try:
                pdf_path = self.pdf_generator.generate(
                    latex_content=result.optimized_cv,
                    output_name=output_name,
                    preamble_path=self.preamble_path
                )
                result.pdf_path = pdf_path
                logger.info(f"PDF generated: {pdf_path}")
            except RuntimeError as e:
                result.warnings.append(f"PDF generation failed: {e}")
                logger.error(f"PDF generation failed: {e}")
        else:
            result.warnings.append("pdflatex not available - only .tex file generated")
            logger.warning("pdflatex not available")
        
        return result
