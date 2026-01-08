"""
Domain Package
==============

Core data models and verified skill inventory.
"""

from .models import (
    SeniorityLevel,
    Language,
    ExperienceItem,
    EducationItem,
    ProjectItem,
    ContactInfo,
    JobData,
    CVData,
    ValidationResult,
    RelevanceScore,
    OptimizationConfig,
)

from .inventory import (
    VERIFIED_SKILLS,
    FORBIDDEN_SKILLS,
    VERIFIED_EXPERIENCES,
    VERIFIED_PROJECTS,
    SKILL_CATEGORIES,
    VerifiedExperience,
    VerifiedProject,
    is_skill_verified,
    is_skill_forbidden,
    get_experience_by_company,
    get_matching_skills,
)

__all__ = [
    # Models
    "SeniorityLevel",
    "Language",
    "ExperienceItem",
    "EducationItem",
    "ProjectItem",
    "ContactInfo",
    "JobData",
    "CVData",
    "ValidationResult",
    "RelevanceScore",
    "OptimizationConfig",
    # Inventory
    "VERIFIED_SKILLS",
    "FORBIDDEN_SKILLS",
    "VERIFIED_EXPERIENCES",
    "VERIFIED_PROJECTS",
    "SKILL_CATEGORIES",
    "VerifiedExperience",
    "VerifiedProject",
    "is_skill_verified",
    "is_skill_forbidden",
    "get_experience_by_company",
    "get_matching_skills",
]
