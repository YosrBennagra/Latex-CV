"""Tests for domain models and inventory."""

import pytest
from cv_agent.domain import (
    JobData, CVData, ExperienceItem, ValidationResult,
    SeniorityLevel, Language, ContactInfo,
    VERIFIED_SKILLS, FORBIDDEN_SKILLS,
    is_skill_verified, is_skill_forbidden, get_matching_skills
)


class TestJobData:
    """Tests for JobData model."""
    
    def test_create_job_data(self):
        job = JobData(
            raw_text="Test job",
            title="Software Engineer",
            required_skills=["Python", "React"],
            preferred_skills=["Docker"]
        )
        assert job.title == "Software Engineer"
        assert len(job.required_skills) == 2
        assert len(job.preferred_skills) == 1
    
    def test_all_skills(self):
        job = JobData(
            raw_text="Test",
            title="Developer",
            required_skills=["Python"],
            preferred_skills=["Docker"]
        )
        all_skills = job.all_skills()
        assert "Python" in all_skills
        assert "Docker" in all_skills
    
    def test_is_senior(self):
        job = JobData(raw_text="", title="Senior Engineer", seniority_level=SeniorityLevel.SENIOR)
        assert job.is_senior() is True
        
        junior_job = JobData(raw_text="", title="Junior Developer", seniority_level=SeniorityLevel.JUNIOR)
        assert junior_job.is_senior() is False


class TestExperienceItem:
    """Tests for ExperienceItem model."""
    
    def test_create_experience(self):
        exp = ExperienceItem(
            title="Developer",
            company="TechCorp",
            location="Paris",
            dates="2024",
            bullets=("Built systems", "Deployed apps")
        )
        assert exp.company == "TechCorp"
        assert len(exp.bullets) == 2
    
    def test_immutable_bullets(self):
        exp = ExperienceItem(
            title="Dev", company="Corp", location="NYC", dates="2024",
            bullets=("One", "Two")
        )
        # Tuples are immutable
        with pytest.raises(TypeError):
            exp.bullets[0] = "Modified"
    
    def test_with_bullets(self):
        exp = ExperienceItem(
            title="Dev", company="Corp", location="NYC", dates="2024",
            bullets=("One", "Two")
        )
        new_exp = exp.with_bullets(["New One", "New Two", "New Three"])
        assert len(new_exp.bullets) == 3
        assert exp.bullets == ("One", "Two")  # Original unchanged


class TestValidationResult:
    """Tests for ValidationResult model."""
    
    def test_all_warnings(self):
        result = ValidationResult(
            passed=False,
            ats_compliant=True,
            hr_tone_approved=False,
            one_page_compliant=True,
            ats_warnings=["ATS issue"],
            tone_warnings=["Tone issue", "Another tone"],
            factual_warnings=[],
            page_warnings=[]
        )
        assert result.warning_count == 3
        assert "ATS issue" in result.all_warnings
        assert "Tone issue" in result.all_warnings


class TestInventory:
    """Tests for verified skills inventory."""
    
    def test_verified_skills_not_empty(self):
        assert len(VERIFIED_SKILLS) > 0
    
    def test_forbidden_skills_not_empty(self):
        assert len(FORBIDDEN_SKILLS) > 0
    
    def test_is_skill_verified(self):
        assert is_skill_verified("Python") is True
        assert is_skill_verified("React") is True
        assert is_skill_verified("NotARealSkill") is False
    
    def test_is_skill_verified_case_insensitive(self):
        assert is_skill_verified("python") is True
        assert is_skill_verified("PYTHON") is True
    
    def test_is_skill_forbidden(self):
        assert is_skill_forbidden("Rust") is True
        assert is_skill_forbidden("Go") is True
        assert is_skill_forbidden("Python") is False
    
    def test_get_matching_skills(self):
        job_skills = {"Python", "React", "Rust", "UnknownTech"}
        matching = get_matching_skills(job_skills)
        
        assert "Python" in matching
        assert "React" in matching
        assert "Rust" not in matching  # Forbidden
        assert "UnknownTech" not in matching  # Not verified
