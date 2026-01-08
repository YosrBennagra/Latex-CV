"""
Relevance Analyzer
==================

Analyzes and ranks CV components by relevance to job requirements.
Used to prioritize content for one-page optimization.
"""

import logging
from typing import Dict, List, Tuple

from ..domain import CVData, JobData, RelevanceScore

logger = logging.getLogger(__name__)


class RelevanceAnalyzer:
    """
    Analyzes CV content relevance to job requirements.
    
    Provides:
    - Component-level relevance scores
    - Priority rankings for trimming decisions
    - Skill gap analysis
    """
    
    def analyze(self, cv_data: CVData, job_data: JobData) -> Dict[str, any]:
        """
        Comprehensive relevance analysis.
        
        Returns:
            Dictionary with analysis results
        """
        logger.info("Analyzing CV relevance to job...")
        
        skill_analysis = self._analyze_skills(cv_data, job_data)
        exp_ranking = self._rank_experiences(cv_data, job_data)
        proj_ranking = self._rank_projects(cv_data, job_data)
        gap_analysis = self._identify_skill_gaps(cv_data, job_data)
        
        overall_score = self._calculate_overall_relevance(
            skill_analysis, exp_ranking, proj_ranking
        )
        
        return {
            'overall_score': overall_score,
            'skill_analysis': skill_analysis,
            'experience_ranking': exp_ranking,
            'project_ranking': proj_ranking,
            'skill_gaps': gap_analysis,
        }
    
    def _analyze_skills(self, cv_data: CVData, job_data: JobData) -> Dict[str, any]:
        """Analyze skill match between CV and job."""
        cv_skills = set(s.lower() for s in cv_data.skills)
        required = set(s.lower() for s in job_data.required_skills)
        preferred = set(s.lower() for s in job_data.preferred_skills)
        
        matched_required = cv_skills & required
        matched_preferred = cv_skills & preferred
        
        return {
            'total_cv_skills': len(cv_data.skills),
            'required_matched': len(matched_required),
            'required_total': len(required),
            'preferred_matched': len(matched_preferred),
            'preferred_total': len(preferred),
            'coverage_percent': (len(matched_required) / max(len(required), 1)) * 100,
            'matched_skills': list(matched_required | matched_preferred),
            'unmatched_cv_skills': list(cv_skills - required - preferred),
        }
    
    def _rank_experiences(
        self, cv_data: CVData, job_data: JobData
    ) -> List[Tuple[int, float, str]]:
        """
        Rank experiences by relevance.
        
        Returns:
            List of (index, score, company) tuples, sorted by score descending
        """
        job_skills = set(s.lower() for s in job_data.all_skills())
        job_keywords = set(k.lower() for k in job_data.keywords)
        
        rankings = []
        for idx, exp in enumerate(cv_data.experience):
            score = self._calculate_experience_score(exp, job_skills, job_keywords)
            rankings.append((idx, score, exp.company))
        
        rankings.sort(key=lambda x: x[1], reverse=True)
        return rankings
    
    def _rank_projects(
        self, cv_data: CVData, job_data: JobData
    ) -> List[Tuple[int, float, str]]:
        """Rank projects by relevance."""
        job_skills = set(s.lower() for s in job_data.all_skills())
        
        rankings = []
        for idx, proj in enumerate(cv_data.projects):
            proj_tech = set(t.lower() for t in proj.technologies)
            overlap = len(proj_tech & job_skills)
            score = overlap / max(len(job_skills), 1)
            rankings.append((idx, min(score * 2, 1.0), proj.name))
        
        rankings.sort(key=lambda x: x[1], reverse=True)
        return rankings
    
    def _identify_skill_gaps(self, cv_data: CVData, job_data: JobData) -> Dict[str, List[str]]:
        """Identify skills required by job but missing from CV."""
        cv_skills = set(s.lower() for s in cv_data.skills)
        required = set(s.lower() for s in job_data.required_skills)
        preferred = set(s.lower() for s in job_data.preferred_skills)
        
        return {
            'missing_required': list(required - cv_skills),
            'missing_preferred': list(preferred - cv_skills),
            'extra_skills': list(cv_skills - required - preferred),
        }
    
    def _calculate_experience_score(self, exp, job_skills: set, job_keywords: set) -> float:
        """Calculate relevance score for an experience."""
        text = f"{exp.title} {' '.join(exp.bullets)}".lower()
        
        skill_matches = sum(1 for s in job_skills if s in text)
        keyword_matches = sum(1 for k in job_keywords if k in text)
        
        total = len(job_skills) + len(job_keywords)
        if total == 0:
            return 0.5
        
        return min((skill_matches + keyword_matches) / total * 2, 1.0)
    
    def _calculate_overall_relevance(
        self,
        skill_analysis: Dict,
        exp_ranking: List,
        proj_ranking: List
    ) -> float:
        """Calculate overall relevance score (0-100)."""
        skill_score = skill_analysis['coverage_percent']
        
        exp_score = 0
        if exp_ranking:
            top_exp_scores = [r[1] for r in exp_ranking[:3]]
            exp_score = (sum(top_exp_scores) / len(top_exp_scores)) * 100
        
        proj_score = 0
        if proj_ranking:
            top_proj_scores = [r[1] for r in proj_ranking[:2]]
            proj_score = (sum(top_proj_scores) / len(top_proj_scores)) * 100
        
        # Weighted average
        overall = skill_score * 0.4 + exp_score * 0.4 + proj_score * 0.2
        return round(overall, 1)
