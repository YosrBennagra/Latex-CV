"""
MCP Server
==========

Model Context Protocol server for CV optimization.
Provides tools for AI assistants to interact with the CV agent.
"""

import json
import logging
from typing import Dict, Any
from pathlib import Path

from ..domain import is_skill_verified, is_skill_forbidden, VERIFIED_SKILLS, VERIFIED_EXPERIENCES, VERIFIED_PROJECTS

logger = logging.getLogger(__name__)


class MCPServer:
    """
    MCP server for CV optimization tools.
    
    Available tools:
    - get_verified_skills: List all verified skills
    - validate_skill: Check if a skill is verified
    - get_canonical_experience: Get verified experience bullets
    - get_projects: Get verified projects
    - optimize_cv: Run CV optimization
    - score_cv: Score CV for ATS compatibility
    """
    
    def __init__(self):
        """Initialize MCP server."""
        self.tools = {
            'get_verified_skills': self._get_verified_skills,
            'validate_skill': self._validate_skill,
            'get_canonical_experience': self._get_canonical_experience,
            'get_projects': self._get_projects,
        }
    
    def handle_request(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle an MCP tool request.
        
        Args:
            tool_name: Name of the tool to invoke
            params: Tool parameters
            
        Returns:
            Tool response
        """
        logger.info(f"MCP request: {tool_name}")
        
        if tool_name not in self.tools:
            return {'error': f"Unknown tool: {tool_name}"}
        
        try:
            result = self.tools[tool_name](params)
            return {'success': True, 'result': result}
        except Exception as e:
            logger.error(f"MCP error: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_tool_definitions(self) -> list:
        """Get MCP tool definitions for registration."""
        return [
            {
                'name': 'get_verified_skills',
                'description': 'Get list of all verified skills that can be claimed in CVs',
                'parameters': {}
            },
            {
                'name': 'validate_skill',
                'description': 'Check if a specific skill is in the verified inventory',
                'parameters': {
                    'skill_name': {'type': 'string', 'description': 'Skill to validate'}
                }
            },
            {
                'name': 'get_canonical_experience',
                'description': 'Get verified experience bullets for a company',
                'parameters': {
                    'company': {'type': 'string', 'description': 'Company name'}
                }
            },
            {
                'name': 'get_projects',
                'description': 'Get list of verified projects',
                'parameters': {}
            },
        ]
    
    def _get_verified_skills(self, params: Dict) -> Dict:
        """Get all verified skills."""
        return {
            'skills': sorted(list(VERIFIED_SKILLS)),
            'count': len(VERIFIED_SKILLS)
        }
    
    def _validate_skill(self, params: Dict) -> Dict:
        """Validate a specific skill."""
        skill = params.get('skill_name', '')
        
        if not skill:
            return {'error': 'skill_name is required'}
        
        verified = is_skill_verified(skill)
        forbidden = is_skill_forbidden(skill)
        
        return {
            'skill': skill,
            'verified': verified,
            'forbidden': forbidden,
            'can_use': verified and not forbidden,
            'message': self._get_skill_message(skill, verified, forbidden)
        }
    
    def _get_canonical_experience(self, params: Dict) -> Dict:
        """Get canonical experience for a company."""
        company = params.get('company', '')
        
        if not company:
            return {'error': 'company is required'}
        
        company_lower = company.lower()
        
        for exp in VERIFIED_EXPERIENCES:
            if company_lower in exp.company.lower():
                return {
                    'found': True,
                    'company': exp.company,
                    'title': exp.title,
                    'dates': exp.dates,
                    'location': exp.location,
                    'bullets': list(exp.bullets),
                    'technologies': list(exp.technologies)
                }
        
        return {
            'found': False,
            'message': f"No verified experience for '{company}'"
        }
    
    def _get_projects(self, params: Dict) -> Dict:
        """Get all verified projects."""
        projects = []
        
        for proj in VERIFIED_PROJECTS:
            projects.append({
                'name': proj.name,
                'description': proj.description,
                'technologies': list(proj.technologies),
                'achievements': list(proj.achievements)
            })
        
        return {
            'projects': projects,
            'count': len(projects)
        }
    
    def _get_skill_message(self, skill: str, verified: bool, forbidden: bool) -> str:
        """Generate message for skill validation."""
        if forbidden:
            return f"❌ '{skill}' is FORBIDDEN - cannot be added to CV"
        elif verified:
            return f"✓ '{skill}' is verified and can be used"
        else:
            return f"⚠ '{skill}' is not in verified inventory - verify before using"
