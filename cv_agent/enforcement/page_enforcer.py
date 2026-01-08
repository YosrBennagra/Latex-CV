"""
One Page Enforcer
=================

Ensures CV fits on exactly one page by intelligent trimming.
"""

import logging
from typing import Dict, Any, List

from ..domain import OptimizationConfig

logger = logging.getLogger(__name__)


class OnePageEnforcer:
    """
    Enforces strict one-page limit on CV.
    
    Strategy:
    1. Estimate content size
    2. Remove lowest-relevance content
    3. Limit bullets per experience
    4. Trim projects
    5. Shorten summary if needed
    """
    
    # Character estimates for CV components
    ESTIMATES = {
        'header': 200,
        'summary': 340,
        'section_title': 30,
        'experience_header': 80,
        'bullet': 100,
        'skill_line': 60,
        'education': 80,
        'project_header': 50,
        'project_bullet': 80,
        'certification': 40,
    }
    
    def __init__(self, config: OptimizationConfig = None):
        """Initialize with config."""
        self.config = config or OptimizationConfig()
    
    def enforce(self, cv_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enforce one-page limit.
        
        Args:
            cv_data: Optimized CV data
            
        Returns:
            CV data trimmed to fit one page
        """
        logger.info("Enforcing one-page limit...")
        
        current_size = self.estimate_size(cv_data)
        logger.info(f"Initial size: {current_size} chars (max: {self.config.max_content_chars})")
        
        if current_size <= self.config.max_content_chars:
            logger.info("Already fits on one page ✓")
            return cv_data
        
        trimmed = self._deep_copy(cv_data)
        
        # Strategy 1: Limit bullets per experience to 3
        trimmed = self._limit_bullets(trimmed, max_bullets=3)
        current_size = self.estimate_size(trimmed)
        
        if current_size <= self.config.max_content_chars:
            logger.info("Fit achieved by limiting bullets")
            return trimmed
        
        # Strategy 2: Limit projects to 2
        if len(trimmed.get('projects', [])) > 2:
            logger.info("Trimming projects to 2")
            trimmed['projects'] = trimmed['projects'][:2]
            current_size = self.estimate_size(trimmed)
        
        if current_size <= self.config.max_content_chars:
            logger.info("Fit achieved by limiting projects")
            return trimmed
        
        # Strategy 3: Further limit bullets to 2
        trimmed = self._limit_bullets(trimmed, max_bullets=2)
        current_size = self.estimate_size(trimmed)
        
        if current_size <= self.config.max_content_chars:
            logger.info("Fit achieved by aggressive bullet trimming")
            return trimmed
        
        # Strategy 4: Remove projects entirely
        if trimmed.get('projects'):
            logger.warning("Removing projects section entirely")
            trimmed['projects'] = []
            current_size = self.estimate_size(trimmed)
        
        if current_size <= self.config.max_content_chars:
            return trimmed
        
        # Strategy 5: Shorten summary
        summary = trimmed.get('summary', '')
        if len(summary) > 200:
            logger.info("Shortening summary")
            trimmed['summary'] = summary[:200].rsplit('.', 1)[0] + '.'
        
        final_size = self.estimate_size(trimmed)
        logger.info(f"Final size: {final_size} chars")
        
        return trimmed
    
    def estimate_size(self, cv_data: Dict[str, Any]) -> int:
        """Estimate character count for CV."""
        total = self.ESTIMATES['header']
        
        # Summary
        summary = cv_data.get('summary', '')
        total += len(summary)
        
        # Skills
        skills = cv_data.get('skills', [])
        skill_lines = max(len(skills) // 4, 2)
        total += skill_lines * self.ESTIMATES['skill_line']
        
        # Experience
        total += self.ESTIMATES['section_title']
        for exp in cv_data.get('experience', []):
            total += self.ESTIMATES['experience_header']
            bullets = exp.get('bullets', [])
            total += len(bullets) * self.ESTIMATES['bullet']
        
        # Education
        total += self.ESTIMATES['section_title']
        education = cv_data.get('education', [])
        total += len(education) * self.ESTIMATES['education']
        
        # Projects
        projects = cv_data.get('projects', [])
        if projects:
            total += self.ESTIMATES['section_title']
            total += len(projects) * self.ESTIMATES['project_header']
        
        # Certifications
        certs = cv_data.get('certifications', [])
        if certs:
            total += self.ESTIMATES['section_title']
            total += len(certs) * self.ESTIMATES['certification']
        
        return total
    
    def estimate_pages(self, cv_data: Dict[str, Any]) -> float:
        """Estimate page count."""
        size = self.estimate_size(cv_data)
        return round(size / self.config.max_content_chars, 2)
    
    def _limit_bullets(self, cv_data: Dict[str, Any], max_bullets: int) -> Dict[str, Any]:
        """Limit bullets per experience."""
        for exp in cv_data.get('experience', []):
            bullets = exp.get('bullets', [])
            if len(bullets) > max_bullets:
                logger.info(f"Trimming {exp.get('company', '?')}: {len(bullets)} → {max_bullets} bullets")
                exp['bullets'] = bullets[:max_bullets]
        return cv_data
    
    def _deep_copy(self, data: Dict) -> Dict:
        """Deep copy dictionary."""
        import copy
        return copy.deepcopy(data)
