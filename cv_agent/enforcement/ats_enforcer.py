"""
ATS Compliance Enforcer
=======================

Ensures CV LaTeX output is ATS-compliant.
"""

import re
import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)


class ATSEnforcer:
    """
    Enforces ATS compliance in LaTeX output.
    
    Rules:
    - No tables
    - No images/graphics
    - No multi-column layouts
    - No complex headers/footers
    - No colored text boxes
    - Single-column, clean structure
    """
    
    # Forbidden LaTeX patterns
    FORBIDDEN_PATTERNS: List[Tuple[str, str, str]] = [
        (r'\\includegraphics', 'Image/graphic', 'Remove all images'),
        (r'\\begin\{tabular\}', 'Table', 'Use itemize/description instead'),
        (r'\\begin\{multicol', 'Multi-column', 'Use single-column layout'),
        (r'\\fancyhdr', 'Complex header', 'Use simple header'),
        (r'\\textcolor\{', 'Colored text', 'Use black text only'),
        (r'\\colorbox', 'Color box', 'Remove colored boxes'),
        (r'\\pagecolor', 'Page color', 'Use white background'),
        (r'\\begin\{minipage\}', 'Minipage', 'Avoid side-by-side layouts'),
        (r'\\begin\{wrapfigure\}', 'Wrapped figure', 'Remove wrapped figures'),
    ]
    
    # Allowed patterns (for validation)
    ALLOWED_ENVIRONMENTS = {
        'itemize', 'enumerate', 'description',
        'document', 'section', 'internship', 'education', 'project'
    }
    
    def check_compliance(self, latex_content: str) -> Tuple[bool, List[str]]:
        """
        Check LaTeX content for ATS compliance.
        
        Returns:
            (is_compliant, list of issues)
        """
        issues = []
        
        for pattern, name, fix in self.FORBIDDEN_PATTERNS:
            if re.search(pattern, latex_content, re.IGNORECASE):
                issues.append(f"{name} detected: {fix}")
        
        is_compliant = len(issues) == 0
        
        if is_compliant:
            logger.info("LaTeX is ATS-compliant ✓")
        else:
            logger.warning(f"ATS compliance issues: {len(issues)}")
        
        return is_compliant, issues
    
    def fix_compliance(self, latex_content: str) -> str:
        """
        Attempt to fix ATS compliance issues.
        
        Returns:
            Fixed LaTeX content
        """
        fixed = latex_content
        
        # Remove color commands
        fixed = re.sub(r'\\textcolor\{[^}]+\}\{([^}]+)\}', r'\1', fixed)
        fixed = re.sub(r'\\colorbox\{[^}]+\}\{([^}]+)\}', r'\1', fixed)
        
        # Remove graphics
        fixed = re.sub(r'\\includegraphics\[[^\]]*\]\{[^}]+\}', '', fixed)
        fixed = re.sub(r'\\includegraphics\{[^}]+\}', '', fixed)
        
        # Log changes
        if fixed != latex_content:
            logger.info("Applied ATS compliance fixes")
        
        return fixed
    
    def validate_structure(self, latex_content: str) -> List[str]:
        """
        Validate CV structure for ATS parsing.
        
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Check for standard sections
        if not re.search(r'\\section\{.*[Ee]xperience', latex_content):
            recommendations.append("Add Experience section with clear heading")
        
        if not re.search(r'\\section\{.*[Ss]kills', latex_content):
            recommendations.append("Add Skills section with clear heading")
        
        if not re.search(r'\\section\{.*[Ee]ducation', latex_content):
            recommendations.append("Add Education section with clear heading")
        
        # Check for contact info
        if not re.search(r'\\cv(mail|email)', latex_content, re.IGNORECASE):
            recommendations.append("Include email contact")
        
        return recommendations
