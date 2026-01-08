"""
Domain Models
=============

Core data models used throughout the CV optimization system.
All models use dataclasses for immutability and type safety.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Set, Optional
from enum import Enum


class SeniorityLevel(str, Enum):
    """Job seniority levels."""
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    PRINCIPAL = "principal"


class Language(str, Enum):
    """Supported languages."""
    ENGLISH = "en"
    FRENCH = "fr"


@dataclass(frozen=True)
class ExperienceItem:
    """
    Single work experience entry.
    
    Attributes:
        title: Job title
        company: Company name
        location: Work location
        dates: Employment period
        bullets: Achievement/responsibility bullets
        keywords: Extracted keywords for matching
    """
    title: str
    company: str
    location: str
    dates: str
    bullets: tuple[str, ...]  # Immutable tuple
    keywords: tuple[str, ...] = field(default_factory=tuple)
    
    def with_bullets(self, new_bullets: List[str]) -> "ExperienceItem":
        """Return new ExperienceItem with updated bullets."""
        return ExperienceItem(
            title=self.title,
            company=self.company,
            location=self.location,
            dates=self.dates,
            bullets=tuple(new_bullets),
            keywords=self.keywords
        )


@dataclass(frozen=True)
class EducationItem:
    """Single education entry."""
    degree: str
    institution: str
    location: str
    dates: str
    details: str = ""


@dataclass(frozen=True)
class ProjectItem:
    """Single project entry."""
    name: str
    description: str
    technologies: tuple[str, ...] = field(default_factory=tuple)
    url: Optional[str] = None


@dataclass
class ContactInfo:
    """Contact information."""
    email: str = ""
    phone: str = ""
    linkedin: str = ""
    github: str = ""
    location: str = ""
    portfolio: str = ""


@dataclass
class JobData:
    """
    Structured job description data.
    
    Contains all extracted information from a job posting,
    used to optimize and tailor CVs.
    """
    raw_text: str
    title: str
    company: Optional[str] = None
    seniority_level: SeniorityLevel = SeniorityLevel.MID
    required_skills: List[str] = field(default_factory=list)
    preferred_skills: List[str] = field(default_factory=list)
    responsibilities: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    language: Language = Language.ENGLISH
    
    def all_skills(self) -> Set[str]:
        """Get all skills (required + preferred)."""
        return set(self.required_skills + self.preferred_skills)
    
    def is_junior(self) -> bool:
        """Check if this is a junior position."""
        return self.seniority_level == SeniorityLevel.JUNIOR
    
    def is_senior(self) -> bool:
        """Check if this is a senior/lead position."""
        return self.seniority_level in (SeniorityLevel.SENIOR, SeniorityLevel.LEAD, SeniorityLevel.PRINCIPAL)


@dataclass
class CVData:
    """
    Structured CV data.
    
    Contains all parsed information from a LaTeX CV file.
    """
    name: str
    role: str
    contact: ContactInfo
    summary: str
    experience: List[ExperienceItem]
    education: List[EducationItem]
    skills: List[str]
    projects: List[ProjectItem] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    languages: List[str] = field(default_factory=list)
    
    def total_experience_years(self) -> int:
        """Estimate total years of experience."""
        return len(self.experience)  # Rough estimate
    
    def has_skill(self, skill: str) -> bool:
        """Check if CV has a specific skill (case-insensitive)."""
        skill_lower = skill.lower()
        return any(s.lower() == skill_lower or skill_lower in s.lower() for s in self.skills)


@dataclass
class ValidationResult:
    """Result of CV validation."""
    passed: bool
    ats_compliant: bool
    hr_tone_approved: bool
    one_page_compliant: bool
    ats_warnings: List[str] = field(default_factory=list)
    tone_warnings: List[str] = field(default_factory=list)
    factual_warnings: List[str] = field(default_factory=list)
    page_warnings: List[str] = field(default_factory=list)
    
    @property
    def all_warnings(self) -> List[str]:
        """Get all warnings combined."""
        return self.ats_warnings + self.tone_warnings + self.factual_warnings + self.page_warnings
    
    @property
    def warning_count(self) -> int:
        """Total number of warnings."""
        return len(self.all_warnings)


@dataclass
class RelevanceScore:
    """Relevance score for a CV component."""
    component_id: str
    component_type: str  # 'experience', 'project', 'skill'
    score: float  # 0.0 to 1.0
    matched_keywords: List[str] = field(default_factory=list)
    
    @property
    def is_high_relevance(self) -> bool:
        """Check if highly relevant (>0.7)."""
        return self.score >= 0.7
    
    @property
    def is_low_relevance(self) -> bool:
        """Check if low relevance (<0.3)."""
        return self.score < 0.3


@dataclass
class OptimizationConfig:
    """Configuration for CV optimization."""
    max_bullets_per_experience: int = 3
    max_experiences: int = 3
    max_projects: int = 2
    max_summary_chars: int = 340
    max_content_chars: int = 3800
    prioritize_recent_experience: bool = True
    remove_graduate_from_title: bool = True
    quantify_achievements: bool = True
