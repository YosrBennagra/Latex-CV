"""
Job Description Parser
======================

Extracts structured information from raw job posting text.
Uses pattern matching and heuristics to identify skills,
requirements, and job characteristics.
"""

import re
import logging
from typing import List, Set, Tuple

from ..domain import JobData, SeniorityLevel, Language

logger = logging.getLogger(__name__)


class JobParser:
    """
    Parses job descriptions to extract key information.
    
    Identifies:
    - Job title and seniority
    - Required vs preferred skills
    - Responsibilities
    - Keywords for ATS optimization
    """
    
    # Common technical skills to detect
    TECH_SKILLS = {
        # Languages
        'python', 'java', 'javascript', 'typescript', 'sql', 'go', 'rust', 'c++',
        # Frontend
        'react', 'angular', 'vue', 'vue.js', 'next.js', 'nextjs', 'svelte',
        'html', 'css', 'sass', 'tailwind', 'bootstrap', 'redux',
        # Backend
        'node.js', 'nodejs', 'nestjs', 'express', 'express.js', 'spring boot',
        'django', 'flask', 'fastapi', 'rails',
        # Databases
        'sql', 'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch',
        # DevOps
        'docker', 'kubernetes', 'k8s', 'aws', 'azure', 'gcp', 'git',
        'ci/cd', 'jenkins', 'terraform', 'ansible',
        # AI/ML
        'machine learning', 'ml', 'ai', 'llm', 'deep learning', 'nlp',
        'pytorch', 'tensorflow', 'langchain', 'rag', 'hugging face',
        # Concepts
        'rest api', 'graphql', 'microservices', 'agile', 'scrum', 'tdd',
    }
    
    SENIORITY_PATTERNS = {
        SeniorityLevel.JUNIOR: [
            r'\bjunior\b', r'\bentry.?level\b', r'\bgraduate\b',
            r'\bearly.?career\b', r'\b0-2\s*years?\b', r'\bintern\b'
        ],
        SeniorityLevel.MID: [
            r'\bmid.?level\b', r'\bintermediate\b',
            r'\b2-5\s*years?\b', r'\b3-5\s*years?\b', r'\b3\+\s*years?\b'
        ],
        SeniorityLevel.SENIOR: [
            r'\bsenior\b', r'\bsr\.\b', r'\bexperienced\b',
            r'\b5\+\s*years?\b', r'\b5-10\s*years?\b', r'\bexpert\b'
        ],
        SeniorityLevel.LEAD: [
            r'\blead\b', r'\bprincipal\b', r'\bstaff\b',
            r'\barchitect\b', r'\bhead\s+of\b', r'\bmanager\b'
        ],
    }
    
    def __init__(self):
        """Initialize the parser."""
        self._skill_patterns = self._compile_skill_patterns()
    
    def _compile_skill_patterns(self) -> List[Tuple[str, re.Pattern]]:
        """Compile regex patterns for skill detection."""
        patterns = []
        for skill in self.TECH_SKILLS:
            pattern = re.compile(r'\b' + re.escape(skill) + r'\b', re.IGNORECASE)
            patterns.append((skill, pattern))
        return patterns
    
    def parse(self, job_description: str) -> JobData:
        """
        Parse a job description into structured data.
        
        Args:
            job_description: Raw job posting text
            
        Returns:
            JobData object with extracted information
        """
        logger.info("Parsing job description...")
        
        language = self._detect_language(job_description)
        title = self._extract_title(job_description)
        company = self._extract_company(job_description)
        seniority = self._detect_seniority(job_description)
        required_skills, preferred_skills = self._extract_skills(job_description)
        responsibilities = self._extract_responsibilities(job_description)
        keywords = self._generate_keywords(job_description, required_skills, preferred_skills)
        
        job_data = JobData(
            raw_text=job_description,
            title=title,
            company=company,
            seniority_level=seniority,
            required_skills=required_skills,
            preferred_skills=preferred_skills,
            responsibilities=responsibilities,
            keywords=keywords,
            language=language
        )
        
        logger.info(f"Parsed job: {title} ({seniority.value} level, "
                   f"{len(required_skills)} required skills)")
        return job_data
    
    def _detect_language(self, text: str) -> Language:
        """Detect if job description is in English or French."""
        french_words = ['vous', 'nous', 'entreprise', 'poste', 'profil', 'compétences', 'expérience']
        english_words = ['you', 'we', 'company', 'position', 'profile', 'skills', 'experience']
        
        text_lower = text.lower()
        french_count = sum(1 for w in french_words if w in text_lower)
        english_count = sum(1 for w in english_words if w in text_lower)
        
        return Language.FRENCH if french_count > english_count else Language.ENGLISH
    
    def _extract_title(self, text: str) -> str:
        """Extract job title from description."""
        patterns = [
            r'(?:position|role|job\s+title|title)[\s:]+([^\n]+)',
            r'(?:hiring|looking\s+for|seeking)\s+(?:a\s+)?([^\n,]+?)(?:\s+to|\s+for|\s+with)',
            r'^([A-Z][^\n]+?(?:Engineer|Developer|Architect|Manager|Lead|Specialist|Designer))',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                title = match.group(1).strip()
                title = re.sub(r'\s+', ' ', title)
                if len(title) < 80:
                    return title
        
        return "Software Engineer"
    
    def _extract_company(self, text: str) -> str | None:
        """Extract company name."""
        patterns = [
            r'(?:company|at|join)\s*[:\-]?\s*([A-Z][A-Za-z0-9\s&]+?)(?:\s+is|\s+are|\.|,)',
            r'(?:about\s+)([A-Z][A-Za-z0-9\s&]+?)(?:\s*\n|\s+is)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                company = match.group(1).strip()
                if len(company) < 50:
                    return company
        return None
    
    def _detect_seniority(self, text: str) -> SeniorityLevel:
        """Detect job seniority level."""
        text_lower = text.lower()
        
        # Check patterns in order of specificity
        for level in [SeniorityLevel.LEAD, SeniorityLevel.SENIOR, 
                      SeniorityLevel.JUNIOR, SeniorityLevel.MID]:
            for pattern in self.SENIORITY_PATTERNS[level]:
                if re.search(pattern, text_lower):
                    return level
        
        return SeniorityLevel.MID  # Default
    
    def _extract_skills(self, text: str) -> Tuple[List[str], List[str]]:
        """Extract required and preferred skills."""
        required: Set[str] = set()
        preferred: Set[str] = set()
        
        # Find all skills mentioned
        all_skills = set()
        for skill, pattern in self._skill_patterns:
            if pattern.search(text):
                all_skills.add(skill)
        
        # Classify as required vs preferred
        text_lower = text.lower()
        
        # Find "required" section
        required_section = re.search(
            r'(?:required|must.?have|essential|qualifications)[:\s]+(.*?)(?:preferred|nice.?to.?have|bonus|$)',
            text_lower, re.DOTALL
        )
        
        # Find "preferred" section
        preferred_section = re.search(
            r'(?:preferred|nice.?to.?have|bonus|plus)[:\s]+(.*?)(?:\n\n|$)',
            text_lower, re.DOTALL
        )
        
        for skill in all_skills:
            skill_lower = skill.lower()
            in_required = required_section and skill_lower in required_section.group(1)
            in_preferred = preferred_section and skill_lower in preferred_section.group(1)
            
            if in_preferred:
                preferred.add(self._normalize_skill(skill))
            elif in_required:
                required.add(self._normalize_skill(skill))
            else:
                required.add(self._normalize_skill(skill))  # Default to required
        
        return list(required), list(preferred)
    
    def _normalize_skill(self, skill: str) -> str:
        """Normalize skill name to canonical form."""
        mapping = {
            'nodejs': 'Node.js',
            'node.js': 'Node.js',
            'nextjs': 'Next.js',
            'next.js': 'Next.js',
            'vue': 'Vue.js',
            'vue.js': 'Vue.js',
            'k8s': 'Kubernetes',
            'postgresql': 'PostgreSQL',
            'mysql': 'MySQL',
            'mongodb': 'MongoDB',
            'javascript': 'JavaScript',
            'typescript': 'TypeScript',
            'python': 'Python',
            'java': 'Java',
            'react': 'React',
            'angular': 'Angular',
            'docker': 'Docker',
            'kubernetes': 'Kubernetes',
            'aws': 'AWS',
            'azure': 'Azure',
            'gcp': 'GCP',
            'git': 'Git',
            'ci/cd': 'CI/CD',
            'rest api': 'REST API',
            'graphql': 'GraphQL',
            'llm': 'LLM',
            'rag': 'RAG',
            'langchain': 'LangChain',
            'ml': 'Machine Learning',
            'ai': 'AI',
            'nlp': 'NLP',
        }
        return mapping.get(skill.lower(), skill.title())
    
    def _extract_responsibilities(self, text: str) -> List[str]:
        """Extract job responsibilities."""
        responsibilities = []
        
        # Find responsibilities section
        resp_match = re.search(
            r'(?:responsibilities|what\s+you.?ll\s+do|duties|role)[:\s]+(.*?)(?:\n\n|requirements|qualifications|$)',
            text, re.IGNORECASE | re.DOTALL
        )
        
        if resp_match:
            section = resp_match.group(1)
            # Extract bullet points
            bullets = re.findall(r'[-•*]\s*([^\n]+)', section)
            responsibilities = [b.strip() for b in bullets if len(b.strip()) > 10]
        
        return responsibilities[:10]  # Limit to 10
    
    def _generate_keywords(
        self,
        text: str,
        required: List[str],
        preferred: List[str]
    ) -> List[str]:
        """Generate ATS keywords from job description."""
        keywords = set(required + preferred)
        
        # Add action verbs mentioned
        action_verbs = [
            'develop', 'build', 'design', 'implement', 'create', 'deploy',
            'manage', 'lead', 'collaborate', 'optimize', 'maintain'
        ]
        text_lower = text.lower()
        for verb in action_verbs:
            if verb in text_lower:
                keywords.add(verb)
        
        return list(keywords)
