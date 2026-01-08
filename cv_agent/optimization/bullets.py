"""
Bullet Engineering
==================

Tools for analyzing and validating CV bullet points.
Ensures action verbs, quantification, and professional tone.
"""

import re
import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)


class BulletEngineer:
    """
    Analyzes and scores CV bullet points.
    
    Evaluates:
    - Action verb strength
    - Quantification (metrics, numbers)
    - Impact clarity
    - Length appropriateness
    """
    
    # Tier 1: Strongest action verbs
    POWER_VERBS = {
        'architected', 'spearheaded', 'pioneered', 'transformed', 'revolutionized',
        'orchestrated', 'championed', 'accelerated', 'maximized', 'eliminated'
    }
    
    # Tier 2: Strong action verbs
    STRONG_VERBS = {
        'developed', 'designed', 'implemented', 'built', 'created', 'deployed',
        'optimized', 'improved', 'enhanced', 'streamlined', 'automated',
        'integrated', 'established', 'delivered', 'achieved', 'managed', 'led'
    }
    
    # Tier 3: Acceptable action verbs
    ACCEPTABLE_VERBS = {
        'configured', 'maintained', 'supported', 'utilized', 'executed',
        'analyzed', 'researched', 'documented', 'tested', 'reviewed'
    }
    
    # Weak verbs to avoid
    WEAK_VERBS = {
        'helped', 'tried', 'worked on', 'assisted', 'participated',
        'was responsible for', 'handled', 'dealt with'
    }
    
    # Patterns for quantification
    QUANTIFICATION_PATTERNS = [
        r'\d+%',           # Percentages
        r'\d+x',           # Multipliers
        r'\d+\+',          # N+ format
        r'\$\d+',          # Dollar amounts
        r'\d+\s*(users?|customers?|clients?)',  # User counts
        r'reduced|increased|improved\s+by',      # Relative changes
    ]
    
    def analyze_bullet(self, bullet: str) -> dict:
        """
        Analyze a single bullet point.
        
        Returns:
            Analysis dict with scores and suggestions
        """
        analysis = {
            'original': bullet,
            'verb_tier': self._get_verb_tier(bullet),
            'has_quantification': self._has_quantification(bullet),
            'length_ok': self._check_length(bullet),
            'score': 0,
            'suggestions': []
        }
        
        # Calculate score
        verb_scores = {'power': 30, 'strong': 25, 'acceptable': 15, 'weak': 0, 'none': 0}
        analysis['score'] = verb_scores.get(analysis['verb_tier'], 0)
        
        if analysis['has_quantification']:
            analysis['score'] += 40
        
        if analysis['length_ok']:
            analysis['score'] += 30
        
        # Suggestions
        if analysis['verb_tier'] in ('weak', 'none'):
            analysis['suggestions'].append("Start with a strong action verb")
        
        if not analysis['has_quantification']:
            analysis['suggestions'].append("Add metrics or quantified impact")
        
        if not analysis['length_ok']:
            analysis['suggestions'].append("Adjust length (aim for 80-150 characters)")
        
        return analysis
    
    def analyze_all(self, bullets: List[str]) -> dict:
        """
        Analyze all bullets and provide summary.
        
        Returns:
            Summary with individual analyses and overall score
        """
        analyses = [self.analyze_bullet(b) for b in bullets]
        
        total_score = sum(a['score'] for a in analyses)
        avg_score = total_score / len(analyses) if analyses else 0
        
        return {
            'bullets': analyses,
            'total_count': len(bullets),
            'average_score': round(avg_score, 1),
            'power_verb_count': sum(1 for a in analyses if a['verb_tier'] == 'power'),
            'quantified_count': sum(1 for a in analyses if a['has_quantification']),
            'overall_grade': self._score_to_grade(avg_score)
        }
    
    def _get_verb_tier(self, bullet: str) -> str:
        """Determine the tier of the opening action verb."""
        first_word = bullet.split()[0].lower().rstrip('ed').rstrip('ing') if bullet.split() else ''
        
        # Check if starts with verb
        bullet_lower = bullet.lower()
        
        for verb in self.POWER_VERBS:
            if bullet_lower.startswith(verb):
                return 'power'
        
        for verb in self.STRONG_VERBS:
            if bullet_lower.startswith(verb):
                return 'strong'
        
        for verb in self.ACCEPTABLE_VERBS:
            if bullet_lower.startswith(verb):
                return 'acceptable'
        
        for verb in self.WEAK_VERBS:
            if bullet_lower.startswith(verb):
                return 'weak'
        
        return 'none'
    
    def _has_quantification(self, bullet: str) -> bool:
        """Check if bullet contains quantification."""
        for pattern in self.QUANTIFICATION_PATTERNS:
            if re.search(pattern, bullet, re.IGNORECASE):
                return True
        return False
    
    def _check_length(self, bullet: str) -> bool:
        """Check if bullet length is appropriate (80-150 chars)."""
        length = len(bullet)
        return 60 <= length <= 180
    
    def _score_to_grade(self, score: float) -> str:
        """Convert score to letter grade."""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'
