"""
CV Validator
============

Validates CV for HR tone, ATS compliance, and factual accuracy.
"""

import re
import logging
from typing import Dict, Any, List

from ..domain import ValidationResult, JobData

logger = logging.getLogger(__name__)


class CVValidator:
    """
    Validates CV for quality and compliance.
    
    Checks:
    - ATS compliance (section structure)
    - HR-approved tone (professional language)
    - Factual accuracy (no obvious hallucination)
    - One-page compliance
    """
    
    # Unprofessional phrases
    UNPROFESSIONAL = [
        'responsible for', 'duties included', 'tried to', 'helped with',
        'worked on', 'stuff', 'things', 'etc.', 'very', 'really',
        'i think', 'i believe', 'i feel', 'basically', 'actually'
    ]
    
    # Weak action verbs
    WEAK_VERBS = [
        'assisted', 'helped', 'participated', 'contributed',
        'worked', 'tried', 'attempted', 'was involved'
    ]
    
    def validate(
        self,
        cv_data: Dict[str, Any],
        job_data: JobData,
        page_estimate: float = 1.0
    ) -> ValidationResult:
        """
        Validate CV data.
        
        Args:
            cv_data: Optimized CV data
            job_data: Job description data
            page_estimate: Estimated page count
            
        Returns:
            ValidationResult with compliance status
        """
        logger.info("Validating CV...")
        
        ats_warnings = []
        tone_warnings = []
        factual_warnings = []
        page_warnings = []
        
        # Validate ATS
        ats_ok = self._validate_ats(cv_data, ats_warnings)
        
        # Validate tone
        tone_ok = self._validate_tone(cv_data, tone_warnings)
        
        # Validate factual accuracy
        factual_ok = self._validate_factual(cv_data, job_data, factual_warnings)
        
        # Validate page count
        page_ok = page_estimate <= 1.0
        if not page_ok:
            page_warnings.append(f"Estimated {page_estimate:.1f} pages (must be ≤ 1)")
        
        passed = ats_ok and tone_ok and factual_ok and page_ok
        
        result = ValidationResult(
            passed=passed,
            ats_compliant=ats_ok,
            hr_tone_approved=tone_ok,
            one_page_compliant=page_ok,
            ats_warnings=ats_warnings,
            tone_warnings=tone_warnings,
            factual_warnings=factual_warnings,
            page_warnings=page_warnings
        )
        
        if passed:
            logger.info("Validation passed ✓")
        else:
            logger.warning(f"Validation failed: {result.warning_count} issues")
        
        return result
    
    def _validate_ats(self, cv_data: Dict[str, Any], warnings: List[str]) -> bool:
        """Validate ATS compliance."""
        ok = True
        
        required = ['experience', 'skills', 'education']
        for section in required:
            if not cv_data.get(section):
                warnings.append(f"Missing required section: {section}")
                ok = False
        
        # Check summary length
        summary = cv_data.get('summary', '')
        if len(summary) > 400:
            warnings.append(f"Summary too long: {len(summary)} chars (max 400)")
            ok = False
        
        return ok
    
    def _validate_tone(self, cv_data: Dict[str, Any], warnings: List[str]) -> bool:
        """Validate HR-approved tone."""
        ok = True
        all_text = self._collect_text(cv_data).lower()
        
        # Check for unprofessional phrases
        for phrase in self.UNPROFESSIONAL:
            if phrase in all_text:
                warnings.append(f"Unprofessional phrase: '{phrase}'")
                ok = False
        
        # Check bullets for weak verbs
        for exp in cv_data.get('experience', []):
            for bullet in exp.get('bullets', []):
                first_word = bullet.split()[0].lower() if bullet.split() else ''
                if first_word in self.WEAK_VERBS:
                    warnings.append(f"Weak verb in bullet: '{first_word}'")
                    ok = False
        
        return ok
    
    def _validate_factual(
        self,
        cv_data: Dict[str, Any],
        job_data: JobData,
        warnings: List[str]
    ) -> bool:
        """Validate factual accuracy (detect potential hallucination)."""
        ok = True
        
        # Check for suspicious 100% skill match
        cv_skills = set(s.lower() for s in cv_data.get('skills', []))
        job_skills = job_data.all_skills()
        job_skills_lower = set(s.lower() for s in job_skills)
        
        if job_skills_lower and cv_skills:
            match_ratio = len(cv_skills & job_skills_lower) / len(job_skills_lower)
            if match_ratio > 0.95 and len(job_skills_lower) > 10:
                warnings.append("Suspiciously high skill match - verify authenticity")
        
        # Check for vague language
        all_text = self._collect_text(cv_data).lower()
        vague_count = sum(1 for v in ['various', 'multiple', 'several', 'numerous'] if v in all_text)
        if vague_count > 5:
            warnings.append("Excessive vague quantifiers - be more specific")
        
        return ok
    
    def _collect_text(self, cv_data: Dict[str, Any]) -> str:
        """Collect all text from CV."""
        parts = [
            cv_data.get('summary', ''),
            cv_data.get('role', '')
        ]
        parts.extend(cv_data.get('skills', []))
        
        for exp in cv_data.get('experience', []):
            parts.append(exp.get('title', ''))
            parts.extend(exp.get('bullets', []))
        
        return ' '.join(parts)
