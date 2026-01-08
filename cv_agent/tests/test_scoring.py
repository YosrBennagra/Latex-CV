"""Tests for scoring modules."""

import pytest
from cv_agent.scoring import ATSScorer, RelevanceAnalyzer
from cv_agent.domain import (
    JobData, CVData, ExperienceItem, ContactInfo, SeniorityLevel
)


class TestATSScorer:
    """Tests for ATSScorer."""
    
    @pytest.fixture
    def scorer(self):
        return ATSScorer()
    
    @pytest.fixture
    def sample_cv(self):
        return CVData(
            name="Test Candidate",
            role="Software Engineer",
            contact=ContactInfo(email="test@example.com"),
            summary="Experienced developer with Python and React skills.",
            experience=[
                ExperienceItem(
                    title="Developer",
                    company="TechCorp",
                    location="NYC",
                    dates="2023-2024",
                    bullets=(
                        "Developed React applications",
                        "Built Python APIs",
                    )
                )
            ],
            education=[],
            skills=["Python", "React", "Docker", "PostgreSQL"]
        )
    
    @pytest.fixture
    def sample_job(self):
        return JobData(
            raw_text="Test job",
            title="Full Stack Developer",
            seniority_level=SeniorityLevel.MID,
            required_skills=["Python", "React"],
            preferred_skills=["Docker"],
            keywords=["python", "react", "docker", "api"]
        )
    
    def test_calculate_score_returns_number(self, scorer, sample_cv, sample_job):
        score = scorer.calculate_score(sample_cv, sample_job)
        assert isinstance(score, float)
        assert 0 <= score <= 100
    
    def test_high_score_for_matching_skills(self, scorer, sample_cv, sample_job):
        # CV has all required skills
        score = scorer.calculate_score(sample_cv, sample_job)
        assert score >= 50  # Should be reasonably high
    
    def test_score_relevance(self, scorer, sample_cv, sample_job):
        relevance = scorer.score_relevance(sample_cv, sample_job)
        
        assert 'experience' in relevance
        assert 'projects' in relevance
        assert 'skills' in relevance
    
    def test_skill_relevance_scoring(self, scorer, sample_cv, sample_job):
        relevance = scorer.score_relevance(sample_cv, sample_job)
        
        # Python is a required skill, should have high score
        python_scores = [s for s in relevance['skills'] if s.component_id == 'Python']
        assert len(python_scores) > 0
        assert python_scores[0].score >= 0.5
    
    def test_check_latex_compliance(self, scorer):
        good_latex = r"""
        \documentclass{article}
        \begin{document}
        \section{Experience}
        \begin{itemize}
        \item Developed applications
        \end{itemize}
        \end{document}
        """
        
        warnings = scorer.check_latex_compliance(good_latex)
        assert len(warnings) == 0
    
    def test_detect_latex_issues(self, scorer):
        bad_latex = r"""
        \documentclass{article}
        \begin{document}
        \begin{tabular}{ll}
        Name & Value
        \end{tabular}
        \includegraphics{photo.png}
        \end{document}
        """
        
        warnings = scorer.check_latex_compliance(bad_latex)
        assert len(warnings) >= 2  # Tables and graphics


class TestRelevanceAnalyzer:
    """Tests for RelevanceAnalyzer."""
    
    @pytest.fixture
    def analyzer(self):
        return RelevanceAnalyzer()
    
    @pytest.fixture
    def sample_cv(self):
        return CVData(
            name="Test",
            role="Developer",
            contact=ContactInfo(),
            summary="Developer",
            experience=[
                ExperienceItem(
                    title="Python Developer",
                    company="PyCorp",
                    location="Remote",
                    dates="2024",
                    bullets=("Built Python APIs", "Deployed to AWS")
                )
            ],
            education=[],
            skills=["Python", "AWS", "Docker"]
        )
    
    @pytest.fixture
    def sample_job(self):
        return JobData(
            raw_text="",
            title="Python Developer",
            required_skills=["Python", "AWS"],
            keywords=["python", "aws", "api"]
        )
    
    def test_analyze_returns_structure(self, analyzer, sample_cv, sample_job):
        result = analyzer.analyze(sample_cv, sample_job)
        
        assert 'overall_score' in result
        assert 'skill_analysis' in result
        assert 'experience_ranking' in result
        assert 'skill_gaps' in result
    
    def test_skill_analysis(self, analyzer, sample_cv, sample_job):
        result = analyzer.analyze(sample_cv, sample_job)
        skill_analysis = result['skill_analysis']
        
        assert skill_analysis['total_cv_skills'] == 3
        assert skill_analysis['required_matched'] == 2  # Python and AWS
    
    def test_skill_gaps(self, analyzer, sample_cv, sample_job):
        # Add a missing skill to job
        sample_job.required_skills.append("Kubernetes")
        
        result = analyzer.analyze(sample_cv, sample_job)
        gaps = result['skill_gaps']
        
        assert 'kubernetes' in [g.lower() for g in gaps['missing_required']]
