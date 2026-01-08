"""
LaTeX Renderer
==============

Generates ATS-compliant LaTeX CV output.
"""

import re
import logging
from typing import Dict, Any, List
from pathlib import Path

logger = logging.getLogger(__name__)


class LaTeXRenderer:
    """
    Renders CV data to LaTeX format.
    
    Features:
    - ATS-compliant output
    - Clean single-column layout
    - Proper character escaping
    - Template-based rendering
    """
    
    # LaTeX special characters that need escaping
    SPECIAL_CHARS = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        '—': '-',  # Em dash causes encoding issues
        '–': '-',  # En dash
        '"': "''",
        '"': "''",
        ''': "'",
        ''': "'",
    }
    
    def __init__(self, template_path: Path = None):
        """Initialize with optional template."""
        self.template_path = template_path
    
    def render(self, cv_data: Dict[str, Any], candidate_name: str = None) -> str:
        """
        Render CV data to LaTeX.
        
        Args:
            cv_data: Optimized CV data
            candidate_name: Candidate name (defaults to cv_data['name'])
            
        Returns:
            LaTeX document string
        """
        logger.info("Rendering LaTeX output...")
        
        name = candidate_name or cv_data.get('name', 'Candidate')
        
        parts = [
            self._render_preamble(),
            self._render_header(cv_data, name),
            self._render_summary(cv_data),
            self._render_skills(cv_data),
            self._render_experience(cv_data),
            self._render_education(cv_data),
            self._render_projects(cv_data),
            self._render_footer(),
        ]
        
        latex = '\n\n'.join(parts)
        logger.info(f"Generated {len(latex)} characters of LaTeX")
        
        return latex
    
    def _render_preamble(self) -> str:
        """Render document preamble."""
        return r"""\documentclass[11pt,a4paper]{article}
\input{../../preamble}
\begin{document}"""
    
    def _render_header(self, cv_data: Dict[str, Any], name: str) -> str:
        """Render header with name and contact."""
        contact = cv_data.get('contact', {})
        role = cv_data.get('role', 'Software Engineer')
        
        lines = [
            f"\\cvname{{{self._escape(name)}}}",
            f"\\cvrole{{{self._escape(role)}}}",
        ]
        
        if hasattr(contact, 'email') and contact.email:
            lines.append(f"\\cvmail{{{contact.email}}}")
        elif isinstance(contact, dict) and contact.get('email'):
            lines.append(f"\\cvmail{{{contact.get('email')}}}")
        
        if hasattr(contact, 'phone') and contact.phone:
            lines.append(f"\\cvphone{{{contact.phone}}}")
        elif isinstance(contact, dict) and contact.get('phone'):
            lines.append(f"\\cvphone{{{contact.get('phone')}}}")
        
        if hasattr(contact, 'linkedin') and contact.linkedin:
            lines.append(f"\\cvlinkedin{{{contact.linkedin}}}")
        elif isinstance(contact, dict) and contact.get('linkedin'):
            lines.append(f"\\cvlinkedin{{{contact.get('linkedin')}}}")
        
        if hasattr(contact, 'github') and contact.github:
            lines.append(f"\\cvgithub{{{contact.github}}}")
        elif isinstance(contact, dict) and contact.get('github'):
            lines.append(f"\\cvgithub{{{contact.get('github')}}}")
        
        if hasattr(contact, 'location') and contact.location:
            lines.append(f"\\cvlocation{{{self._escape(contact.location)}}}")
        elif isinstance(contact, dict) and contact.get('location'):
            lines.append(f"\\cvlocation{{{self._escape(contact.get('location'))}}}")
        
        lines.append("\\makeheader")
        
        return '\n'.join(lines)
    
    def _render_summary(self, cv_data: Dict[str, Any]) -> str:
        """Render professional summary."""
        summary = cv_data.get('summary', '')
        if not summary:
            return ''
        
        return f"\\cvsummary{{{self._escape(summary)}}}"
    
    def _render_skills(self, cv_data: Dict[str, Any]) -> str:
        """Render skills section."""
        skills = cv_data.get('skills', [])
        if not skills:
            return ''
        
        # Group skills by category
        grouped = self._group_skills(skills)
        
        lines = ["\\section{Skills}"]
        
        for category, category_skills in grouped.items():
            skills_text = " | ".join(self._escape(s) for s in category_skills)
            lines.append(f"\\textbf{{{category}:}} {skills_text}")
        
        return '\n'.join(lines)
    
    def _render_experience(self, cv_data: Dict[str, Any]) -> str:
        """Render work experience section."""
        experience = cv_data.get('experience', [])
        if not experience:
            return ''
        
        lines = ["\\section{Work Experience}"]
        
        for exp in experience:
            title = exp.get('title', '')
            company = exp.get('company', '')
            location = exp.get('location', '')
            dates = exp.get('dates', '')
            bullets = exp.get('bullets', [])
            
            lines.append(
                f"\\begin{{internship}}{{{self._escape(title)}}}"
                f"{{{self._escape(company)}}}{{{self._escape(location)}}}"
                f"{{{self._escape(dates)}}}{{}}"
            )
            lines.append("\\begin{itemize}")
            
            for bullet in bullets:
                lines.append(f"  \\item {self._escape(bullet)}")
            
            lines.append("\\end{itemize}")
            lines.append("\\end{internship}")
        
        return '\n'.join(lines)
    
    def _render_education(self, cv_data: Dict[str, Any]) -> str:
        """Render education section."""
        education = cv_data.get('education', [])
        if not education:
            return ''
        
        lines = ["\\section{Education}"]
        
        for edu in education:
            if hasattr(edu, 'degree'):
                degree = edu.degree
                institution = edu.institution
                location = edu.location
                dates = edu.dates
            else:
                degree = edu.get('degree', '')
                institution = edu.get('institution', '')
                location = edu.get('location', '')
                dates = edu.get('dates', '')
            
            lines.append(
                f"\\begin{{education}}{{{self._escape(degree)}}}"
                f"{{{self._escape(institution)}}}{{{self._escape(location)}}}"
                f"{{{self._escape(dates)}}}"
            )
            lines.append("\\end{education}")
        
        return '\n'.join(lines)
    
    def _render_projects(self, cv_data: Dict[str, Any]) -> str:
        """Render projects section."""
        projects = cv_data.get('projects', [])
        if not projects:
            return ''
        
        lines = ["\\section{Projects}"]
        
        for proj in projects:
            name = proj.get('name', '')
            tech = proj.get('technologies', [])
            desc = proj.get('description', '')
            
            tech_str = ', '.join(tech) if tech else ''
            
            lines.append(
                f"\\begin{{project}}{{{self._escape(name)}}}"
                f"{{{self._escape(tech_str)}}}"
            )
            lines.append(self._escape(desc))
            lines.append("\\end{project}")
        
        return '\n'.join(lines)
    
    def _render_footer(self) -> str:
        """Render document footer."""
        return "\\end{document}"
    
    def _escape(self, text: str) -> str:
        """Escape LaTeX special characters."""
        if not text:
            return ''
        
        result = str(text)
        for char, replacement in self.SPECIAL_CHARS.items():
            result = result.replace(char, replacement)
        
        return result
    
    def _group_skills(self, skills: List[str]) -> Dict[str, List[str]]:
        """Group skills by category."""
        categories = {
            'Languages': ['Python', 'Java', 'JavaScript', 'TypeScript', 'SQL'],
            'Frontend': ['React', 'Angular', 'Vue.js', 'Next.js', 'HTML5', 'CSS3', 'Tailwind'],
            'Backend': ['Node.js', 'NestJS', 'Express.js', 'Spring Boot', 'Django', 'Flask'],
            'Databases': ['PostgreSQL', 'MySQL', 'MongoDB', 'Redis'],
            'DevOps': ['Docker', 'Kubernetes', 'AWS', 'CI/CD', 'GitHub Actions'],
            'AI/ML': ['LLM', 'RAG', 'LangChain', 'Machine Learning', 'NLP'],
        }
        
        grouped = {}
        assigned = set()
        
        for cat, cat_skills in categories.items():
            matching = [s for s in skills if s in cat_skills]
            if matching:
                grouped[cat] = matching
                assigned.update(matching)
        
        # Remaining skills
        other = [s for s in skills if s not in assigned]
        if other:
            grouped['Other'] = other
        
        return grouped
