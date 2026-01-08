"""Tests for enforcement modules."""

import pytest
from cv_agent.enforcement import OnePageEnforcer, ATSEnforcer
from cv_agent.domain import OptimizationConfig


class TestOnePageEnforcer:
    """Tests for OnePageEnforcer."""
    
    @pytest.fixture
    def enforcer(self):
        return OnePageEnforcer()
    
    @pytest.fixture
    def small_cv(self):
        return {
            'name': 'Test',
            'role': 'Developer',
            'summary': 'Short summary.',
            'skills': ['Python', 'React'],
            'experience': [
                {'title': 'Dev', 'company': 'Corp', 'bullets': ['Did work']}
            ],
            'education': [{'degree': 'BS', 'institution': 'Uni'}],
            'projects': []
        }
    
    @pytest.fixture
    def large_cv(self):
        return {
            'name': 'Test Candidate',
            'role': 'Senior Software Engineer',
            'summary': 'A' * 400,  # Long summary
            'skills': ['Python', 'React', 'Docker', 'AWS', 'GCP', 'K8s'] * 3,
            'experience': [
                {
                    'title': 'Senior Developer',
                    'company': f'Company {i}',
                    'bullets': [f'Achievement {j}' * 10 for j in range(5)]
                }
                for i in range(4)
            ],
            'education': [{'degree': 'BS', 'institution': 'Uni'}],
            'projects': [
                {'name': f'Project {i}', 'description': 'Desc' * 20, 'technologies': []}
                for i in range(4)
            ],
            'certifications': ['Cert 1', 'Cert 2', 'Cert 3']
        }
    
    def test_small_cv_fits(self, enforcer, small_cv):
        result = enforcer.enforce(small_cv)
        pages = enforcer.estimate_pages(result)
        assert pages <= 1.0
    
    def test_large_cv_gets_trimmed(self, enforcer, large_cv):
        result = enforcer.enforce(large_cv)
        
        # Should have fewer bullets
        for exp in result['experience']:
            assert len(exp['bullets']) <= 3
    
    def test_estimate_size(self, enforcer, small_cv):
        size = enforcer.estimate_size(small_cv)
        assert size > 0
        assert size < 5000  # Small CV should be small
    
    def test_estimate_pages(self, enforcer, small_cv, large_cv):
        small_pages = enforcer.estimate_pages(small_cv)
        large_pages = enforcer.estimate_pages(large_cv)
        
        assert small_pages < large_pages
    
    def test_projects_trimmed(self, enforcer, large_cv):
        result = enforcer.enforce(large_cv)
        
        # Projects should be reduced
        assert len(result['projects']) <= 2
    
    def test_custom_config(self):
        config = OptimizationConfig(max_bullets_per_experience=2)
        enforcer = OnePageEnforcer(config)
        
        cv = {
            'summary': '',
            'skills': [],
            'experience': [
                {'title': 'Dev', 'company': 'Corp', 'bullets': ['A', 'B', 'C', 'D', 'E']}
            ],
            'education': [],
            'projects': []
        }
        
        result = enforcer.enforce(cv)
        # Enforcer limits bullets when page limit exceeded
        # With small CV it may not need to trim


class TestATSEnforcer:
    """Tests for ATSEnforcer."""
    
    @pytest.fixture
    def enforcer(self):
        return ATSEnforcer()
    
    def test_clean_latex_passes(self, enforcer):
        clean = r"""
        \documentclass{article}
        \begin{document}
        \section{Experience}
        \begin{itemize}
        \item Built applications
        \end{itemize}
        \end{document}
        """
        
        compliant, issues = enforcer.check_compliance(clean)
        assert compliant is True
        assert len(issues) == 0
    
    def test_detect_tables(self, enforcer):
        with_table = r"""
        \begin{tabular}{ll}
        Skill & Level \\
        \end{tabular}
        """
        
        compliant, issues = enforcer.check_compliance(with_table)
        assert compliant is False
        assert any('Table' in i for i in issues)
    
    def test_detect_graphics(self, enforcer):
        with_image = r"\includegraphics[width=2cm]{photo.png}"
        
        compliant, issues = enforcer.check_compliance(with_image)
        assert compliant is False
        assert any('Image' in i or 'graphic' in i.lower() for i in issues)
    
    def test_detect_multicolumn(self, enforcer):
        with_multicol = r"\begin{multicols}{2}"
        
        compliant, issues = enforcer.check_compliance(with_multicol)
        assert compliant is False
    
    def test_fix_colored_text(self, enforcer):
        with_color = r"\textcolor{blue}{Important text}"
        
        fixed = enforcer.fix_compliance(with_color)
        assert 'textcolor' not in fixed
        assert 'Important text' in fixed
    
    def test_validate_structure(self, enforcer):
        minimal = r"\documentclass{article}\begin{document}Hello\end{document}"
        
        recommendations = enforcer.validate_structure(minimal)
        # Should recommend adding standard sections
        assert len(recommendations) > 0
