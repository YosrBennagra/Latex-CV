"""
ATS Scorer
==========

Scores CV content for ATS (Applicant Tracking System) compatibility
and relevance to job requirements.
"""

import re
import logging
from typing import Dict, List

from ..domain import JobData, CVData, RelevanceScore

logger = logging.getLogger(__name__)


class ATSScorer:
    """
    Scores CV for ATS compatibility and job relevance.
    
    Scoring criteria:
    - Keyword match percentage (40%)
    - Required skills coverage (30%)
    - Formatting compliance (20%)
    - Section structure (10%)
    """
    
    # ATS-unfriendly patterns to detect in LaTeX
    ATS_RED_FLAGS = [
        (r'\\includegraphics', 'Images/graphics detected'),
        (r'\\begin\{tabular\}', 'Tables detected'),
        (r'\\begin\{multicol\}', 'Multi-column layout detected'),
        (r'\\fancyhdr', 'Complex headers/footers detected'),
        (r'\\textcolor', 'Colored text detected'),
        (r'\\colorbox', 'Color boxes detected'),
    ]
    
    def calculate_score(self, cv_data: CVData, job_data: JobData) -> float:
        """
        Calculate overall ATS compatibility score (0-100).
        
        Args:
            cv_data: Parsed CV data
            job_data: Parsed job description
            
        Returns:
            Score from 0 to 100
        """
        scores = []
        
        # Keyword match (40%)
        keyword_score = self._score_keywords(cv_data, job_data)
        scores.append(keyword_score * 0.4)
        
        # Skills coverage (30%)
        skills_score = self._score_skills_coverage(cv_data, job_data)
        scores.append(skills_score * 0.3)
        
        # Format compliance (20%)
        format_score = 100.0  # Assume good for parsed data
        scores.append(format_score * 0.2)
        
        # Structure completeness (10%)
        structure_score = self._score_structure(cv_data)
        scores.append(structure_score * 0.1)
        
        total = sum(scores)
        
        logger.info(f"ATS Score: keywords={keyword_score:.0f}, skills={skills_score:.0f}, "
                   f"format={format_score:.0f}, structure={structure_score:.0f}, total={total:.0f}")
        
        return round(total, 1)
    
    def score_relevance(self, cv_data: CVData, job_data: JobData) -> Dict[str, List[RelevanceScore]]:
        """
        Score relevance of each CV component to the job.
        
        Returns:
            Dictionary with relevance scores for experiences, projects, skills
        """
        relevance = {
            'experience': [],
            'projects': [],
            'skills': []
        }
        
        job_skills = set(s.lower() for s in job_data.all_skills())
        job_keywords = set(k.lower() for k in job_data.keywords)
        
        # Score experiences
        for idx, exp in enumerate(cv_data.experience):
            score = self._score_experience(exp, job_skills, job_keywords)
            relevance['experience'].append(RelevanceScore(
                component_id=f"exp_{idx}",
                component_type="experience",
                score=score,
                matched_keywords=self._get_matched_keywords(exp.bullets, job_keywords)
            ))
        
        # Score projects
        for idx, proj in enumerate(cv_data.projects):
            tech_lower = set(t.lower() for t in proj.technologies)
            score = len(tech_lower & job_skills) / max(len(job_skills), 1)
            relevance['projects'].append(RelevanceScore(
                component_id=f"proj_{idx}",
                component_type="project",
                score=min(score * 1.5, 1.0),
                matched_keywords=list(tech_lower & job_skills)
            ))
        
        # Score skills
        for skill in cv_data.skills:
            in_required = skill.lower() in job_skills
            relevance['skills'].append(RelevanceScore(
                component_id=skill,
                component_type="skill",
                score=1.0 if in_required else 0.3,
                matched_keywords=[skill] if in_required else []
            ))
        
        return relevance
    
    def check_latex_compliance(self, latex_content: str) -> List[str]:
        """
        Check LaTeX content for ATS compliance issues.
        
        Returns:
            List of warning messages
        """
        warnings = []
        
        for pattern, message in self.ATS_RED_FLAGS:
            if re.search(pattern, latex_content):
                warnings.append(message)
        
        return warnings
    
    def _score_keywords(self, cv_data: CVData, job_data: JobData) -> float:
        """Score keyword matching (0-100)."""
        cv_text = self._collect_cv_text(cv_data).lower()
        job_keywords = set(k.lower() for k in job_data.keywords)
        
        if not job_keywords:
            return 100.0
        
        matched = sum(1 for kw in job_keywords if kw in cv_text)
        return (matched / len(job_keywords)) * 100
    
    def _score_skills_coverage(self, cv_data: CVData, job_data: JobData) -> float:
        """Score required skills coverage (0-100)."""
        required = set(s.lower() for s in job_data.required_skills)
        cv_skills = set(s.lower() for s in cv_data.skills)
        
        if not required:
            return 100.0
        
        matched = len(required & cv_skills)
        base_score = (matched / len(required)) * 100
        
        # Bonus for preferred skills
        preferred = set(s.lower() for s in job_data.preferred_skills)
        if preferred:
            pref_matched = len(preferred & cv_skills)
            bonus = (pref_matched / len(preferred)) * 10
            base_score = min(base_score + bonus, 100.0)
        
        return base_score
    
    def _score_structure(self, cv_data: CVData) -> float:
        """Score CV structure completeness (0-100)."""
        score = 0.0
        
        if cv_data.summary:
            score += 20
        if cv_data.experience:
            score += 40
        if cv_data.skills:
            score += 20
        if cv_data.education:
            score += 10
        if cv_data.contact.email:
            score += 10
        
        return min(score, 100.0)
    
    def _score_experience(self, exp, job_skills: set, job_keywords: set) -> float:
        """Score a single experience entry."""
        # Check technology overlap
        exp_text = ' '.join(exp.bullets).lower()
        keyword_matches = sum(1 for kw in job_keywords if kw in exp_text)
        skill_matches = sum(1 for s in job_skills if s in exp_text)
        
        total_possible = len(job_keywords) + len(job_skills)
        if total_possible == 0:
            return 0.5
        
        score = (keyword_matches + skill_matches) / total_possible
        return min(score * 2, 1.0)  # Scale up but cap at 1.0
    
    def _get_matched_keywords(self, bullets: tuple, job_keywords: set) -> List[str]:
        """Get keywords that appear in bullets."""
        text = ' '.join(bullets).lower()
        return [kw for kw in job_keywords if kw in text]
    
    def _collect_cv_text(self, cv_data: CVData) -> str:
        """Collect all text content from CV."""
        parts = [cv_data.summary, cv_data.role]
        parts.extend(cv_data.skills)
        
        for exp in cv_data.experience:
            parts.append(exp.title)
            parts.extend(exp.bullets)
        
        for proj in cv_data.projects:
            parts.append(proj.name)
            parts.append(proj.description)
        
        return ' '.join(parts)
