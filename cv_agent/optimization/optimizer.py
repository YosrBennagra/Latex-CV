"""
Content Optimizer
=================

Optimizes CV content based on job requirements.
Rewrites summary, reorders skills, improves bullets.
"""

import re
import logging
from typing import Dict, List, Set, Any

from ..domain import (
    CVData, JobData, OptimizationConfig,
    is_skill_verified, is_skill_forbidden,
    VERIFIED_EXPERIENCES, get_experience_by_company
)

logger = logging.getLogger(__name__)


class ContentOptimizer:
    """
    Optimizes CV content for maximum job relevance.
    
    Operations:
    - Customize role/title to match job
    - Rewrite professional summary
    - Reorder skills by relevance
    - Ensure experience bullets are canonical (no modification)
    - Filter low-relevance content
    
    CRITICAL: Never adds fabricated content.
    """
    
    # Strong action verbs for bullet validation
    STRONG_VERBS = {
        'developed', 'designed', 'implemented', 'built', 'created',
        'architected', 'optimized', 'improved', 'enhanced', 'streamlined',
        'automated', 'integrated', 'deployed', 'managed', 'led',
        'coordinated', 'delivered', 'achieved', 'established', 'configured'
    }
    
    WEAK_VERBS = {'helped', 'tried', 'worked on', 'assisted', 'participated'}
    
    def __init__(self, config: OptimizationConfig = None):
        """Initialize with optional config."""
        self.config = config or OptimizationConfig()
    
    def optimize(
        self,
        cv_data: CVData,
        job_data: JobData,
        relevance_scores: Dict[str, Any],
        company_name: str = None
    ) -> Dict[str, Any]:
        """
        Optimize CV for the job.
        
        Args:
            cv_data: Parsed CV data
            job_data: Parsed job description
            relevance_scores: From RelevanceAnalyzer
            company_name: Target company name
            
        Returns:
            Optimized CV as dictionary
        """
        logger.info("Optimizing CV content...")
        
        warnings = []
        
        # Optimize role/title
        optimized_role = self._optimize_role(cv_data.role, job_data)
        
        # Optimize summary
        optimized_summary = self._optimize_summary(cv_data, job_data, company_name)
        
        # Optimize skills (reorder, no fabrication)
        optimized_skills, skill_warnings = self._optimize_skills(cv_data.skills, job_data)
        warnings.extend(skill_warnings)
        
        # Experience: use canonical bullets only
        optimized_exp = self._get_canonical_experience(cv_data)
        
        # Projects: prioritize by relevance
        optimized_projects = self._prioritize_projects(
            cv_data.projects,
            relevance_scores.get('project_ranking', [])
        )
        
        return {
            'name': cv_data.name,
            'role': optimized_role,
            'contact': cv_data.contact,
            'summary': optimized_summary,
            'skills': optimized_skills,
            'experience': optimized_exp,
            'education': cv_data.education,
            'projects': optimized_projects,
            'certifications': cv_data.certifications,
            'languages': cv_data.languages,
            'warnings': warnings,
        }
    
    def _optimize_role(self, current_role: str, job_data: JobData) -> str:
        """
        Optimize role/title to match job.
        
        Rules:
        - Match job title closely
        - Remove 'Graduate' prefix
        - Keep professional and accurate
        """
        job_title = job_data.title
        
        # Remove 'Graduate' prefix
        if self.config.remove_graduate_from_title:
            job_title = re.sub(r'\bGraduate\s+', '', job_title, flags=re.IGNORECASE)
        
        # Clean up
        job_title = re.sub(r'\s+', ' ', job_title).strip()
        
        # Truncate if too long
        if len(job_title) > 60:
            job_title = re.sub(r'\s*\(.*?\)', '', job_title)
            job_title = job_title[:60].rsplit(' ', 1)[0]
        
        logger.info(f"Role: {current_role} → {job_title}")
        return job_title
    
    def _optimize_summary(
        self,
        cv_data: CVData,
        job_data: JobData,
        company_name: str = None
    ) -> str:
        """
        Generate optimized professional summary.
        
        CRITICAL: Only claims skills/experience from CV.
        Max 340 characters.
        """
        years_exp = len(cv_data.experience)
        top_skills = self._get_matching_skills(cv_data.skills, job_data, limit=5)
        
        # Build summary
        role = job_data.title.split(',')[0]  # First part of title
        intro = f"{role} with {years_exp}+ years of experience"
        
        # Specialization based on skills
        if any(s in top_skills for s in ['React', 'Angular', 'Vue.js']):
            specialization = "in full-stack web development"
        elif any(s in top_skills for s in ['Python', 'Java', 'Spring Boot']):
            specialization = "in backend systems and APIs"
        elif any(s in top_skills for s in ['LLM', 'RAG', 'LangChain', 'AI']):
            specialization = "in AI-powered applications"
        else:
            specialization = "building scalable applications"
        
        # Skills mention
        if top_skills:
            skills_text = ", ".join(top_skills[:4])
            skills_part = f"Proficient in {skills_text}"
        else:
            skills_part = "Strong technical foundation"
        
        # Value proposition
        value = "Eager to deliver impactful solutions"
        
        summary = f"{intro} {specialization}. {skills_part}. {value}."
        
        # Enforce character limit
        if len(summary) > self.config.max_summary_chars:
            summary = f"{intro} {specialization}. {skills_part}."
        
        if len(summary) > self.config.max_summary_chars:
            summary = f"{intro} {specialization}."
        
        logger.info(f"Summary: {len(summary)} chars")
        return summary
    
    def _optimize_skills(
        self,
        current_skills: List[str],
        job_data: JobData
    ) -> tuple[List[str], List[str]]:
        """
        Optimize skills section.
        
        Rules:
        - Reorder to put job-required skills first
        - Never add skills not in verified inventory
        - Warn about fabrication attempts
        
        Returns:
            (optimized_skills, warnings)
        """
        warnings = []
        job_skills = job_data.all_skills()
        
        # Partition skills
        matching = []
        other = []
        
        for skill in current_skills:
            if any(skill.lower() == js.lower() for js in job_skills):
                matching.append(skill)
            else:
                other.append(skill)
        
        # Check for any requested skills we don't have
        cv_skills_lower = set(s.lower() for s in current_skills)
        for req_skill in job_data.required_skills:
            if req_skill.lower() not in cv_skills_lower:
                if is_skill_verified(req_skill):
                    # Could add, but not in CV currently
                    pass  # Don't add - it's not in current skills
                elif is_skill_forbidden(req_skill):
                    warnings.append(f"Cannot add forbidden skill: {req_skill}")
        
        # Combine: matching first, then others
        optimized = matching + other
        
        logger.info(f"Skills: {len(matching)} matching, {len(other)} other")
        return optimized, warnings
    
    def _get_canonical_experience(self, cv_data: CVData) -> List[Dict]:
        """
        Get canonical experience bullets.
        
        CRITICAL: Experience bullets are LOCKED and never modified.
        Uses verified inventory when available.
        """
        experiences = []
        
        for exp in cv_data.experience:
            # Try to get verified version
            verified = get_experience_by_company(exp.company)
            
            if verified:
                # Use canonical bullets from inventory
                experiences.append({
                    'title': exp.title,
                    'company': exp.company,
                    'location': exp.location,
                    'dates': exp.dates,
                    'bullets': list(verified.bullets),
                })
            else:
                # Use original bullets (unchanged)
                experiences.append({
                    'title': exp.title,
                    'company': exp.company,
                    'location': exp.location,
                    'dates': exp.dates,
                    'bullets': list(exp.bullets),
                })
        
        return experiences
    
    def _prioritize_projects(
        self,
        projects,
        ranking: List
    ) -> List[Dict]:
        """Prioritize projects by relevance ranking."""
        if not ranking:
            # No ranking, return first N projects
            return [
                {
                    'name': p.name,
                    'description': p.description,
                    'technologies': list(p.technologies),
                }
                for p in projects[:self.config.max_projects]
            ]
        
        # Sort by ranking
        sorted_projects = []
        idx_to_rank = {r[0]: r[1] for r in ranking}
        
        for idx, proj in enumerate(projects):
            sorted_projects.append((idx_to_rank.get(idx, 0), proj))
        
        sorted_projects.sort(key=lambda x: x[0], reverse=True)
        
        return [
            {
                'name': p.name,
                'description': p.description,
                'technologies': list(p.technologies),
            }
            for _, p in sorted_projects[:self.config.max_projects]
        ]
    
    def _get_matching_skills(
        self,
        skills: List[str],
        job_data: JobData,
        limit: int = 5
    ) -> List[str]:
        """Get skills that match job requirements."""
        job_skills = set(s.lower() for s in job_data.all_skills())
        matching = [s for s in skills if s.lower() in job_skills]
        return matching[:limit]
