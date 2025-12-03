import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { cvData } from './cv-data.js';

const server = new Server(
  {
    name: 'cv-data-server',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
      resources: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'get_canonical_experience',
        description: 'Get verified work experience data. CRITICAL: Only use this data - never fabricate or add unverified experience.',
        inputSchema: {
          type: 'object',
          properties: {
            company: {
              type: 'string',
              description: 'Optional: Filter by company name',
            },
          },
        },
      },
      {
        name: 'get_verified_skills',
        description: 'Get verified technical skills organized by category. CRITICAL: Only use these skills - never add skills not listed here.',
        inputSchema: {
          type: 'object',
          properties: {
            category: {
              type: 'string',
              description: 'Optional: Filter by category (programming, frontend, backend, databases, devops, etc.)',
            },
          },
        },
      },
      {
        name: 'get_projects',
        description: 'Get verified project portfolio. CRITICAL: Only use these projects - never fabricate projects.',
        inputSchema: {
          type: 'object',
          properties: {
            type: {
              type: 'string',
              description: 'Optional: Filter by type (personal, academic, professional)',
            },
          },
        },
      },
      {
        name: 'get_education',
        description: 'Get verified education credentials and certifications.',
        inputSchema: {
          type: 'object',
          properties: {},
        },
      },
      {
        name: 'validate_skill',
        description: 'Validate if a skill exists in the verified skills inventory. Use this before adding any skill to CV.',
        inputSchema: {
          type: 'object',
          properties: {
            skill: {
              type: 'string',
              description: 'The skill to validate',
            },
          },
          required: ['skill'],
        },
      },
      {
        name: 'suggest_skill_reordering',
        description: 'Get suggestions for reordering existing skills based on job requirements. Only reorders existing skills, never adds new ones.',
        inputSchema: {
          type: 'object',
          properties: {
            job_requirements: {
              type: 'string',
              description: 'Key technologies from job description',
            },
          },
          required: ['job_requirements'],
        },
      },
    ],
  };
});

// List available resources
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  return {
    resources: [
      {
        uri: 'cv://personal/info',
        name: 'Personal Information',
        mimeType: 'application/json',
        description: 'Contact details and personal information',
      },
      {
        uri: 'cv://experience/all',
        name: 'All Work Experience',
        mimeType: 'application/json',
        description: 'Complete work experience history',
      },
      {
        uri: 'cv://skills/inventory',
        name: 'Skills Inventory',
        mimeType: 'application/json',
        description: 'Comprehensive verified skills inventory',
      },
      {
        uri: 'cv://projects/all',
        name: 'All Projects',
        mimeType: 'application/json',
        description: 'Complete project portfolio',
      },
      {
        uri: 'cv://education/all',
        name: 'Education History',
        mimeType: 'application/json',
        description: 'Academic credentials and certifications',
      },
    ],
  };
});

// Read resource handler
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const uri = request.params.uri;

  if (uri === 'cv://personal/info') {
    return {
      contents: [
        {
          uri,
          mimeType: 'application/json',
          text: JSON.stringify(cvData.personal, null, 2),
        },
      ],
    };
  }

  if (uri === 'cv://experience/all') {
    return {
      contents: [
        {
          uri,
          mimeType: 'application/json',
          text: JSON.stringify(cvData.experience, null, 2),
        },
      ],
    };
  }

  if (uri === 'cv://skills/inventory') {
    return {
      contents: [
        {
          uri,
          mimeType: 'application/json',
          text: JSON.stringify(cvData.skills, null, 2),
        },
      ],
    };
  }

  if (uri === 'cv://projects/all') {
    return {
      contents: [
        {
          uri,
          mimeType: 'application/json',
          text: JSON.stringify(cvData.projects, null, 2),
        },
      ],
    };
  }

  if (uri === 'cv://education/all') {
    return {
      contents: [
        {
          uri,
          mimeType: 'application/json',
          text: JSON.stringify(cvData.education, null, 2),
        },
      ],
    };
  }

  throw new Error(`Resource not found: ${uri}`);
});

// Tool execution handler
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === 'get_canonical_experience') {
    const experiences = cvData.experience;
    if (args.company) {
      const filtered = experiences.filter((exp) =>
        exp.company.toLowerCase().includes(args.company.toLowerCase())
      );
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(filtered, null, 2),
          },
        ],
      };
    }
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(experiences, null, 2),
        },
      ],
    };
  }

  if (name === 'get_verified_skills') {
    if (args.category) {
      const categorySkills = cvData.skills[args.category.toLowerCase()];
      if (!categorySkills) {
        return {
          content: [
            {
              type: 'text',
              text: `Category "${args.category}" not found. Available categories: ${Object.keys(cvData.skills).join(', ')}`,
            },
          ],
        };
      }
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({ [args.category]: categorySkills }, null, 2),
          },
        ],
      };
    }
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(cvData.skills, null, 2),
        },
      ],
    };
  }

  if (name === 'get_projects') {
    const projects = cvData.projects;
    if (args.type) {
      const filtered = projects.filter((proj) => proj.type === args.type);
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(filtered, null, 2),
          },
        ],
      };
    }
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(projects, null, 2),
        },
      ],
    };
  }

  if (name === 'get_education') {
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(
            {
              education: cvData.education,
              certifications: cvData.certifications || [],
            },
            null,
            2
          ),
        },
      ],
    };
  }

  if (name === 'validate_skill') {
    const skillToValidate = args.skill.toLowerCase();
    let found = false;
    let category = null;

    // Search through all skill categories
    for (const [cat, skills] of Object.entries(cvData.skills)) {
      if (Array.isArray(skills)) {
        if (skills.some((s) => s.toLowerCase().includes(skillToValidate))) {
          found = true;
          category = cat;
          break;
        }
      }
    }

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(
            {
              skill: args.skill,
              verified: found,
              category: category,
              message: found
                ? `✓ Verified: "${args.skill}" exists in ${category} skills`
                : `✗ NOT VERIFIED: "${args.skill}" not found in skills inventory. DO NOT ADD TO CV.`,
            },
            null,
            2
          ),
        },
      ],
    };
  }

  if (name === 'suggest_skill_reordering') {
    const jobReqs = args.job_requirements.toLowerCase();
    const allSkills = cvData.skills;
    const suggestions = {
      matched_skills: [],
      suggested_order: {},
    };

    // Find skills that match job requirements
    for (const [category, skills] of Object.entries(allSkills)) {
      const matched = skills.filter((skill) =>
        jobReqs.includes(skill.toLowerCase())
      );
      if (matched.length > 0) {
        suggestions.matched_skills.push(...matched);
        suggestions.suggested_order[category] = matched;
      }
    }

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(
            {
              job_requirements: args.job_requirements,
              suggestions,
              instruction:
                'Reorder skills to prioritize matched_skills. Only use skills from the verified inventory.',
            },
            null,
            2
          ),
        },
      ],
    };
  }

  throw new Error(`Unknown tool: ${name}`);
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('CV Data MCP server running on stdio');
}

main().catch((error) => {
  console.error('Server error:', error);
  process.exit(1);
});
