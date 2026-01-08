"""
CV Parser
=========

Extracts structured information from LaTeX CV files.
Parses custom CV macros and environments.
"""

import re
import logging
from pathlib import Path
from typing import List, Dict

from ..domain import CVData, ExperienceItem, EducationItem, ProjectItem, ContactInfo

logger = logging.getLogger(__name__)


class CVParser:
    """
    Parses LaTeX CV files into structured data.
    
    Extracts:
    - Personal information
    - Professional summary
    - Work experience with bullets
    - Skills
    - Education
    - Projects
    """
    
    def parse(self, cv_path: Path) -> CVData:
        """
        Parse a LaTeX CV file.
        
        Args:
            cv_path: Path to LaTeX CV file
            
        Returns:
            CVData object with structured information
        """
        logger.info(f"Parsing CV from {cv_path}")
        
        if not cv_path.exists():
            raise FileNotFoundError(f"CV file not found: {cv_path}")
        
        content = cv_path.read_text(encoding='utf-8')
        
        name = self._extract_name(content)
        role = self._extract_role(content)
        contact = self._extract_contact(content)
        summary = self._extract_summary(content)
        experience = self._extract_experience(content)
        education = self._extract_education(content)
        skills = self._extract_skills(content)
        projects = self._extract_projects(content)
        certifications = self._extract_certifications(content)
        languages = self._extract_languages(content)
        
        cv_data = CVData(
            name=name,
            role=role,
            contact=contact,
            summary=summary,
            experience=experience,
            education=education,
            skills=skills,
            projects=projects,
            certifications=certifications,
            languages=languages
        )
        
        logger.info(f"Parsed CV: {name}, {len(experience)} experiences, {len(skills)} skills")
        return cv_data
    
    def _extract_name(self, content: str) -> str:
        """Extract candidate name."""
        match = re.search(r'\\cvname\{([^}]+)\}', content)
        return match.group(1).strip() if match else "Unknown"
    
    def _extract_role(self, content: str) -> str:
        """Extract current role/title."""
        match = re.search(r'\\cvrole\{([^}]+)\}', content)
        return match.group(1).strip() if match else "Software Engineer"
    
    def _extract_contact(self, content: str) -> ContactInfo:
        """Extract contact information."""
        contact = ContactInfo()
        
        patterns = {
            'email': r'\\cvmail\{([^}]+)\}',
            'phone': r'\\cvphone\{([^}]+)\}',
            'linkedin': r'\\cvlinkedin\{([^}]+)\}',
            'github': r'\\cvgithub\{([^}]+)\}',
            'location': r'\\cvlocation\{([^}]+)\}',
            'portfolio': r'\\cvportfolio\{([^}]+)\}',
        }
        
        for field, pattern in patterns.items():
            match = re.search(pattern, content)
            if match:
                setattr(contact, field, match.group(1).strip())
        
        return contact
    
    def _extract_summary(self, content: str) -> str:
        """Extract professional summary."""
        match = re.search(r'\\cvsummary\{([^}]+)\}', content)
        if match:
            summary = match.group(1).strip()
            summary = self._clean_latex(summary)
            return summary
        return ""
    
    def _extract_experience(self, content: str) -> List[ExperienceItem]:
        """Extract work experience entries."""
        experiences = []
        
        # Pattern for internship environment
        pattern = r'\\begin\{internship\}\{([^}]+)\}\{([^}]+)\}\{([^}]+)\}\{([^}]+)\}\{[^}]*\}(.*?)\\end\{internship\}'
        
        for match in re.finditer(pattern, content, re.DOTALL):
            title = match.group(1).strip()
            company = match.group(2).strip()
            location = match.group(3).strip()
            dates = match.group(4).strip()
            body = match.group(5).strip()
            
            # Extract bullets
            bullet_matches = re.findall(r'\\item\s+([^\n]+)', body)
            bullets = tuple(self._clean_latex(b.strip()) for b in bullet_matches if b.strip())
            
            # Extract keywords from bullets
            keywords = self._extract_keywords_from_bullets(bullets)
            
            experiences.append(ExperienceItem(
                title=title,
                company=company,
                location=location,
                dates=dates,
                bullets=bullets,
                keywords=tuple(keywords)
            ))
        
        return experiences
    
    def _extract_education(self, content: str) -> List[EducationItem]:
        """Extract education entries."""
        education = []
        
        # Pattern for education environment
        pattern = r'\\begin\{education\}\{([^}]+)\}\{([^}]+)\}\{([^}]+)\}\{([^}]+)\}(.*?)\\end\{education\}'
        
        for match in re.finditer(pattern, content, re.DOTALL):
            degree = match.group(1).strip()
            institution = match.group(2).strip()
            location = match.group(3).strip()
            dates = match.group(4).strip()
            body = match.group(5).strip()
            
            details = self._clean_latex(body)
            
            education.append(EducationItem(
                degree=degree,
                institution=institution,
                location=location,
                dates=dates,
                details=details
            ))
        
        return education
    
    def _extract_skills(self, content: str) -> List[str]:
        """Extract skills list."""
        skills = []
        
        # Look for cvskills macro
        match = re.search(r'\\cvskills\{([^}]+)\}', content)
        if match:
            skills_text = match.group(1)
            # Split by common delimiters
            raw_skills = re.split(r'[,\|•·]', skills_text)
            skills = [s.strip() for s in raw_skills if s.strip()]
        
        # Also look for skills in skillsbox
        box_pattern = r'\\begin\{skillsbox\}(.*?)\\end\{skillsbox\}'
        box_match = re.search(box_pattern, content, re.DOTALL)
        if box_match:
            skills_text = box_match.group(1)
            # Extract individual skill entries
            skill_matches = re.findall(r'\\skill\{([^}]+)\}', skills_text)
            skills.extend(skill_matches)
        
        # Deduplicate while preserving order
        seen = set()
        unique_skills = []
        for skill in skills:
            skill_clean = self._clean_latex(skill)
            if skill_clean.lower() not in seen:
                seen.add(skill_clean.lower())
                unique_skills.append(skill_clean)
        
        return unique_skills
    
    def _extract_projects(self, content: str) -> List[ProjectItem]:
        """Extract project entries."""
        projects = []
        
        # Pattern for project environment
        pattern = r'\\begin\{project\}\{([^}]+)\}\{([^}]+)\}(.*?)\\end\{project\}'
        
        for match in re.finditer(pattern, content, re.DOTALL):
            name = match.group(1).strip()
            tech = match.group(2).strip()
            body = match.group(3).strip()
            
            description = self._clean_latex(body)
            technologies = tuple(t.strip() for t in tech.split(',') if t.strip())
            
            projects.append(ProjectItem(
                name=name,
                description=description,
                technologies=technologies
            ))
        
        return projects
    
    def _extract_certifications(self, content: str) -> List[str]:
        """Extract certifications."""
        certs = []
        
        # Look for certification entries
        pattern = r'\\certification\{([^}]+)\}'
        matches = re.findall(pattern, content)
        certs = [self._clean_latex(c) for c in matches]
        
        return certs
    
    def _extract_languages(self, content: str) -> List[str]:
        """Extract spoken languages."""
        langs = []
        
        # Look for language entries
        pattern = r'\\language\{([^}]+)\}\{([^}]+)\}'
        matches = re.findall(pattern, content)
        langs = [f"{lang} ({level})" for lang, level in matches]
        
        if not langs:
            # Try simple format
            pattern = r'\\cvlanguages\{([^}]+)\}'
            match = re.search(pattern, content)
            if match:
                langs_text = match.group(1)
                langs = [l.strip() for l in langs_text.split(',')]
        
        return langs
    
    def _clean_latex(self, text: str) -> str:
        """Clean LaTeX commands from text."""
        # Remove common LaTeX formatting
        text = re.sub(r'\\textbf\{([^}]+)\}', r'\1', text)
        text = re.sub(r'\\emph\{([^}]+)\}', r'\1', text)
        text = re.sub(r'\\textit\{([^}]+)\}', r'\1', text)
        text = re.sub(r'\\underline\{([^}]+)\}', r'\1', text)
        text = re.sub(r'\\href\{[^}]+\}\{([^}]+)\}', r'\1', text)
        text = re.sub(r'\\[a-zA-Z]+\s*', '', text)  # Remove other commands
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        return text.strip()
    
    def _extract_keywords_from_bullets(self, bullets: tuple) -> List[str]:
        """Extract technology keywords from bullet points."""
        keywords = []
        tech_pattern = r'\b(React|Angular|Vue|Node\.js|Python|Java|Spring|Docker|AWS|PostgreSQL|MongoDB|CI/CD|LangChain|RAG)\b'
        
        for bullet in bullets:
            matches = re.findall(tech_pattern, bullet, re.IGNORECASE)
            keywords.extend(matches)
        
        return list(set(keywords))
