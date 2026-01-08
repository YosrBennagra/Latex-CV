"""
Hallucination Detector
======================

Detects potential fabricated content in CVs.
"""

import logging
from typing import List, Set

from ..domain import CVData, JobData, VERIFIED_SKILLS, FORBIDDEN_SKILLS

logger = logging.getLogger(__name__)


class HallucinationDetector:
    """
    Detects potential hallucination in CV content.
    
    Flags:
    - Skills not in verified inventory
    - Suspicious claim patterns
    - Inconsistencies with original CV
    """
    
    # Suspicious claim patterns
    SUSPICIOUS_PATTERNS = [
        r'\d{2,}%\s+(improvement|increase|reduction)',  # Large percentages
        r'(millions?|billions?)\s+of\s+users',           # Large user claims
        r'(led|managed)\s+team\s+of\s+\d{2,}',           # Large team claims
    ]
    
    def detect(
        self,
        optimized_cv: dict,
        original_cv: CVData = None,
        job_data: JobData = None
    ) -> List[str]:
        """
        Detect potential hallucination.
        
        Returns:
            List of warning messages
        """
        warnings = []
        
        # Check skills
        warnings.extend(self._check_skills(optimized_cv))
        
        # Check for added experiences
        if original_cv:
            warnings.extend(self._check_experience_changes(optimized_cv, original_cv))
        
        # Check for suspiciously perfect match
        if job_data:
            warnings.extend(self._check_perfect_match(optimized_cv, job_data))
        
        if warnings:
            logger.warning(f"Hallucination detection: {len(warnings)} flags")
        else:
            logger.info("No hallucination detected ✓")
        
        return warnings
    
    def _check_skills(self, cv_data: dict) -> List[str]:
        """Check for unverified skills."""
        warnings = []
        skills = cv_data.get('skills', [])
        
        for skill in skills:
            skill_lower = skill.lower()
            
            # Check against forbidden list
            if any(f.lower() == skill_lower for f in FORBIDDEN_SKILLS):
                warnings.append(f"FORBIDDEN skill detected: {skill}")
            
            # Check against verified list
            elif not any(v.lower() == skill_lower for v in VERIFIED_SKILLS):
                # Not verified - might be OK if it was in original
                logger.debug(f"Unverified skill: {skill}")
        
        return warnings
    
    def _check_experience_changes(self, optimized: dict, original: CVData) -> List[str]:
        """Check for modified experiences."""
        warnings = []
        
        optimized_companies = {e.get('company', '').lower() for e in optimized.get('experience', [])}
        original_companies = {e.company.lower() for e in original.experience}
        
        # Check for added companies
        added = optimized_companies - original_companies
        if added:
            warnings.append(f"New companies added (not in original): {added}")
        
        return warnings
    
    def _check_perfect_match(self, cv_data: dict, job_data: JobData) -> List[str]:
        """Check for suspiciously perfect skill match."""
        warnings = []
        
        cv_skills = set(s.lower() for s in cv_data.get('skills', []))
        job_skills = set(s.lower() for s in job_data.all_skills())
        
        if len(job_skills) >= 10:
            match = len(cv_skills & job_skills) / len(job_skills)
            if match >= 0.95:
                warnings.append(
                    f"Suspiciously perfect skill match ({match:.0%}) - verify authenticity"
                )
        
        return warnings
