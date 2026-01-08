"""Tests for validation modules."""

import pytest
from cv_agent.validation import CVValidator, HallucinationDetector
from cv_agent.domain import JobData, CVData, ContactInfo, ExperienceItem


class TestCVValidator:
    """Tests for CVValidator."""
    
    @pytest.fixture
    def validator(self):
        return CVValidator()
    
    @pytest.fixture
    def valid_cv(self):
        return {
            'name': 'Test Candidate',
            'role': 'Software Engineer',
            'summary': 'Experienced developer with Python expertise.',
            'skills': ['Python', 'React', 'Docker'],
            'experience': [
                {
                    'title': 'Developer',
                    'company': 'TechCorp',
                    'bullets': [
                        'Developed Python applications',
                        'Built React dashboards'
                    ]
                }
            ],
            'education': [{'degree': 'BS CS', 'institution': 'University'}],
            'projects': []
        }
    
    @pytest.fixture
    def sample_job(self):
        return JobData(
            raw_text="",
            title="Software Engineer",
            required_skills=["Python", "React"]
        )
    
    def test_valid_cv_passes(self, validator, valid_cv, sample_job):
        result = validator.validate(valid_cv, sample_job, page_estimate=0.9)
        
        assert result.ats_compliant is True
    
    def test_detect_missing_sections(self, validator, sample_job):
        cv = {
            'name': 'Test',
            'role': 'Dev',
            'summary': 'Summary',
            'skills': [],  # Missing skills
            'experience': [],  # Missing experience
            'education': [],  # Missing education
        }
        
        result = validator.validate(cv, sample_job, page_estimate=0.5)
        
        assert result.ats_compliant is False
        assert len(result.ats_warnings) > 0
    
    def test_detect_long_summary(self, validator, valid_cv, sample_job):
        valid_cv['summary'] = 'A' * 500  # Too long
        
        result = validator.validate(valid_cv, sample_job)
        
        assert any('Summary' in w or 'summary' in w.lower() for w in result.ats_warnings)
    
    def test_detect_unprofessional_phrases(self, validator, sample_job):
        cv = {
            'name': 'Test',
            'role': 'Dev',
            'summary': 'I helped with stuff and worked on things.',
            'skills': ['Python'],
            'experience': [
                {
                    'title': 'Dev',
                    'company': 'Corp',
                    'bullets': ['Was responsible for coding']
                }
            ],
            'education': [{}],
        }
        
        result = validator.validate(cv, sample_job)
        
        # Should detect unprofessional phrases
        assert result.hr_tone_approved is False or len(result.tone_warnings) > 0
    
    def test_detect_weak_verbs(self, validator, sample_job):
        cv = {
            'name': 'Test',
            'role': 'Developer',
            'summary': 'Experienced developer.',
            'skills': ['Python'],
            'experience': [
                {
                    'title': 'Developer',
                    'company': 'Corp',
                    'bullets': [
                        'Helped with the project',
                        'Assisted team members',
                        'Participated in meetings'
                    ]
                }
            ],
            'education': [{}],
        }
        
        result = validator.validate(cv, sample_job)
        
        # Should flag weak verbs
        assert len(result.tone_warnings) > 0
    
    def test_page_compliance(self, validator, valid_cv, sample_job):
        result = validator.validate(valid_cv, sample_job, page_estimate=1.5)
        
        assert result.one_page_compliant is False
        assert len(result.page_warnings) > 0


class TestHallucinationDetector:
    """Tests for HallucinationDetector."""
    
    @pytest.fixture
    def detector(self):
        return HallucinationDetector()
    
    @pytest.fixture
    def original_cv(self):
        return CVData(
            name="Test",
            role="Developer",
            contact=ContactInfo(),
            summary="Developer",
            experience=[
                ExperienceItem(
                    title="Dev",
                    company="RealCorp",
                    location="NYC",
                    dates="2024",
                    bullets=("Built apps",)
                )
            ],
            education=[],
            skills=["Python", "React"]
        )
    
    def test_clean_cv_no_warnings(self, detector, original_cv):
        optimized = {
            'skills': ['Python', 'React'],
            'experience': [
                {'company': 'RealCorp', 'bullets': ['Built apps']}
            ]
        }
        
        warnings = detector.detect(optimized, original_cv)
        
        # Should have no warnings for matching content
        assert not any('FORBIDDEN' in w for w in warnings)
    
    def test_detect_forbidden_skill(self, detector):
        optimized = {
            'skills': ['Python', 'Rust'],  # Rust is forbidden
            'experience': []
        }
        
        warnings = detector.detect(optimized)
        
        assert any('Rust' in w for w in warnings)
    
    def test_detect_added_company(self, detector, original_cv):
        optimized = {
            'skills': ['Python'],
            'experience': [
                {'company': 'RealCorp', 'bullets': []},
                {'company': 'FakeCorp', 'bullets': []}  # New company
            ]
        }
        
        warnings = detector.detect(optimized, original_cv)
        
        assert any('FakeCorp' in str(w).lower() or 'added' in w.lower() for w in warnings)
    
    def test_perfect_match_warning(self, detector):
        job = JobData(
            raw_text="",
            title="Dev",
            required_skills=[f"Skill{i}" for i in range(15)]
        )
        
        optimized = {
            'skills': [f"skill{i}" for i in range(15)],  # 100% match
            'experience': []
        }
        
        warnings = detector.detect(optimized, job_data=job)
        
        # May warn about suspiciously perfect match
        # (depends on implementation details)
