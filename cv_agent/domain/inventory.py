"""
Verified Skills Inventory
=========================

Contains the canonical list of skills, experiences, and projects
that can be claimed in CVs. Used by the MCP server and optimization
agent to prevent hallucination.

CRITICAL: Only skills listed here may appear in optimized CVs.
"""

from typing import Set, Dict, List
from dataclasses import dataclass


@dataclass
class VerifiedExperience:
    """Verified experience that can be claimed."""
    company: str
    title: str
    dates: str
    location: str
    bullets: tuple[str, ...]
    technologies: tuple[str, ...]


@dataclass
class VerifiedProject:
    """Verified project that can be claimed."""
    name: str
    description: str
    technologies: tuple[str, ...]
    achievements: tuple[str, ...]


# =============================================================================
# VERIFIED SKILLS - Only these may appear in CVs
# =============================================================================

VERIFIED_SKILLS: Set[str] = {
    # Programming Languages
    "Python", "Java", "JavaScript", "TypeScript", "SQL",
    
    # Frontend Frameworks
    "React", "Angular", "Vue.js", "Next.js", "HTML5", "CSS3",
    "Tailwind CSS", "Bootstrap", "Redux", "Material UI",
    
    # Backend Frameworks
    "Node.js", "NestJS", "Express.js", "Spring Boot", "Django", "Flask",
    
    # Databases
    "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
    
    # DevOps & Cloud
    "Docker", "Kubernetes", "AWS", "Azure", "GCP",
    "CI/CD", "Jenkins", "GitHub Actions", "Terraform",
    "Prometheus", "Grafana",
    
    # AI/ML
    "Machine Learning", "Deep Learning", "NLP", "LLM",
    "RAG", "LangChain", "Hugging Face", "OpenAI API",
    "PyTorch", "TensorFlow", "Scikit-learn",
    
    # Tools
    "Git", "Jira", "Figma", "Postman", "VS Code",
    
    # Concepts
    "REST API", "GraphQL", "Microservices", "Agile", "Scrum",
    "Unit Testing", "Integration Testing", "TDD",
}

# Skills that should NEVER be added (not verified)
FORBIDDEN_SKILLS: Set[str] = {
    "Rust", "Go", "Scala", "Haskell", "Erlang",
    "Ruby on Rails", "C++", "C#", ".NET",
    "iOS", "Swift", "Kotlin", "Android Studio",
    "Hadoop", "Spark", "Kafka",
    "Blockchain", "Web3", "Solidity",
}

# =============================================================================
# VERIFIED EXPERIENCES - Canonical bullet points (LOCKED)
# =============================================================================

VERIFIED_EXPERIENCES: List[VerifiedExperience] = [
    VerifiedExperience(
        company="IT Serv",
        title="Full-Stack Developer Intern",
        dates="Feb 2025 - Aug 2025",
        location="Tunis, Tunisia",
        bullets=(
            "Designed full-stack web platform integrating AI, DevOps, and RAG for healthcare automation",
            "Implemented AI-powered symptom checker, doctor blog, patient forum, and admin dashboard",
            "Fine-tuned AI model and set up CI/CD, containerization, and monitoring with Prometheus/Grafana",
        ),
        technologies=("React", "Node.js", "NestJS", "PostgreSQL", "Docker", "LangChain", "RAG", "CI/CD")
    ),
    VerifiedExperience(
        company="IronByte",
        title="Software Developer Intern",
        dates="Jun 2024 - Aug 2024",
        location="Tunis, Tunisia",
        bullets=(
            "Developed educational web application with assignment submission and lesson sharing features",
            "Added timetable creation tool improving scheduling efficiency for educators and students",
        ),
        technologies=("React", "Node.js", "MongoDB", "Express.js")
    ),
    VerifiedExperience(
        company="Ooredoo Tunisie",
        title="Software Developer Intern",
        dates="Jul 2023 - Sep 2023",
        location="Tunis, Tunisia",
        bullets=(
            "Built internal communication app with real-time chat, filtering, and search functionality",
            "Delivered UX/UI design and unit/integration tests achieving high code coverage",
        ),
        technologies=("Angular", "Java", "Spring Boot", "MySQL")
    ),
]

# =============================================================================
# VERIFIED PROJECTS
# =============================================================================

VERIFIED_PROJECTS: List[VerifiedProject] = [
    VerifiedProject(
        name="MediAssist AI Platform",
        description="Healthcare automation platform with AI-powered symptom checker and doctor assistance",
        technologies=("React", "NestJS", "PostgreSQL", "LangChain", "Docker"),
        achievements=(
            "Integrated RAG pipeline for medical knowledge retrieval",
            "Deployed with CI/CD and monitoring",
        )
    ),
    VerifiedProject(
        name="EduConnect",
        description="Educational platform for lesson sharing and assignment management",
        technologies=("React", "Node.js", "MongoDB"),
        achievements=(
            "Improved scheduling efficiency with timetable tool",
            "Enabled real-time collaboration between educators and students",
        )
    ),
]


# =============================================================================
# SKILL CATEGORIES - For organizing skills section
# =============================================================================

SKILL_CATEGORIES: Dict[str, List[str]] = {
    "Languages": ["Python", "Java", "JavaScript", "TypeScript", "SQL"],
    "Frontend": ["React", "Angular", "Vue.js", "Next.js", "HTML5", "CSS3", "Tailwind CSS"],
    "Backend": ["Node.js", "NestJS", "Express.js", "Spring Boot", "Django", "Flask"],
    "Databases": ["PostgreSQL", "MySQL", "MongoDB", "Redis"],
    "DevOps": ["Docker", "Kubernetes", "AWS", "CI/CD", "GitHub Actions"],
    "AI/ML": ["LLM", "RAG", "LangChain", "Machine Learning", "NLP"],
    "Tools": ["Git", "Jira", "Figma", "Postman"],
}


def is_skill_verified(skill: str) -> bool:
    """Check if a skill is in the verified inventory."""
    skill_lower = skill.lower()
    return any(vs.lower() == skill_lower for vs in VERIFIED_SKILLS)


def is_skill_forbidden(skill: str) -> bool:
    """Check if a skill is explicitly forbidden."""
    skill_lower = skill.lower()
    return any(fs.lower() == skill_lower for fs in FORBIDDEN_SKILLS)


def get_experience_by_company(company: str) -> VerifiedExperience | None:
    """Get verified experience by company name."""
    company_lower = company.lower()
    for exp in VERIFIED_EXPERIENCES:
        if company_lower in exp.company.lower():
            return exp
    return None


def get_matching_skills(job_skills: Set[str]) -> Set[str]:
    """Get skills that are both required by job AND verified."""
    return {skill for skill in job_skills if is_skill_verified(skill)}
