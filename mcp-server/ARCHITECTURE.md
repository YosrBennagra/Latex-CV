# MCP Server Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         YOUR CV PROJECT                          │
│                      E:\LatexCv\                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────┐         ┌──────────────────┐               │
│  │  LaTeX CVs     │         │  MCP Server      │               │
│  │                │         │                  │               │
│  │  • English ATS │◄────────┤  cv-data.js      │               │
│  │  • French ATS  │  reads  │  (SOURCE OF      │               │
│  │  • OVRSEA      │  data   │   TRUTH)         │               │
│  │  • Tradeweb    │  from   │                  │               │
│  └────────────────┘         │  • 3 experiences │               │
│                             │  • 4 projects    │               │
│                             │  • 90+ skills    │               │
│                             │  • 25 forbidden  │               │
│                             └────────┬─────────┘               │
│                                      │                          │
│                                      │ provides                 │
│                                      │ verified                 │
│                                      │ data to                  │
│                                      ▼                          │
│                             ┌─────────────────┐                │
│                             │  GitHub Copilot │                │
│                             │                 │                │
│                             │  Queries MCP    │                │
│                             │  before adding  │                │
│                             │  any skill      │                │
│                             └─────────────────┘                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow: Safe CV Adaptation

```
1. USER PASTES JOB DESCRIPTION
   │
   │ Job requires: React, Python, Kubernetes, AWS
   │
   ▼
2. GITHUB COPILOT RECEIVES REQUEST
   │
   │ "Adapt CV for this job"
   │
   ▼
3. COPILOT QUERIES MCP SERVER
   │
   ├─► validate_skill("React")      → ✅ VERIFIED (frontend)
   ├─► validate_skill("Python")     → ✅ VERIFIED (programming)
   ├─► validate_skill("Kubernetes") → ❌ FORBIDDEN (in forbidden list)
   └─► validate_skill("AWS")        → ❌ FORBIDDEN (in forbidden list)
   │
   ▼
4. MCP SERVER RESPONDS
   │
   │ {
   │   "React": { verified: true, category: "frontend" },
   │   "Python": { verified: true, category: "programming" },
   │   "Kubernetes": { verified: false, forbidden: true },
   │   "AWS": { verified: false, forbidden: true }
   │ }
   │
   ▼
5. COPILOT SHOWS YOU RESULTS
   │
   │ "You have: React ✅, Python ✅"
   │ "You DON'T have: Kubernetes ❌, AWS ❌"
   │ "I can reorder skills to emphasize React and Python"
   │
   ▼
6. YOU APPROVE
   │
   │ "Yes, proceed"
   │
   ▼
7. COPILOT SAFELY UPDATES CV
   │
   ├─► Reorders skills: React, Python at top
   ├─► Updates role/title: "Full Stack Developer"
   ├─► Rewrites summary: mentions React, Python
   └─► DOES NOT ADD: Kubernetes, AWS
   │
   ▼
8. CV UPDATED WITH ONLY VERIFIED DATA ✅
```

## MCP Server Components

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP SERVER (index.js)                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────┐          │
│  │             TOOLS (6 available)              │          │
│  ├──────────────────────────────────────────────┤          │
│  │                                              │          │
│  │  1. get_verified_skills                     │          │
│  │     → Returns all skills by category        │          │
│  │                                              │          │
│  │  2. validate_skill                          │          │
│  │     → Checks if skill exists                │          │
│  │     → Returns: verified (true/false)        │          │
│  │                                              │          │
│  │  3. get_canonical_experience                │          │
│  │     → Returns locked work history           │          │
│  │                                              │          │
│  │  4. get_projects                            │          │
│  │     → Returns verified project portfolio    │          │
│  │                                              │          │
│  │  5. get_education                           │          │
│  │     → Returns education credentials         │          │
│  │                                              │          │
│  │  6. suggest_skill_reordering                │          │
│  │     → Smart prioritization based on job     │          │
│  │                                              │          │
│  └──────────────────────────────────────────────┘          │
│                                                              │
│  ┌──────────────────────────────────────────────┐          │
│  │            RESOURCES (5 available)           │          │
│  ├──────────────────────────────────────────────┤          │
│  │                                              │          │
│  │  • cv://personal/info                       │          │
│  │  • cv://experience/all                      │          │
│  │  • cv://skills/inventory                    │          │
│  │  • cv://projects/all                        │          │
│  │  • cv://education/all                       │          │
│  │                                              │          │
│  └──────────────────────────────────────────────┘          │
│                                                              │
│  ┌──────────────────────────────────────────────┐          │
│  │           DATA SOURCE (cv-data.js)           │          │
│  ├──────────────────────────────────────────────┤          │
│  │                                              │          │
│  │  ✅ Verified Skills (90+)                   │          │
│  │  ✅ Experience (3 internships)              │          │
│  │  ✅ Projects (4 verified)                   │          │
│  │  ✅ Education (ESPRIT)                      │          │
│  │  ❌ Forbidden Skills (25)                   │          │
│  │                                              │          │
│  └──────────────────────────────────────────────┘          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Skills Inventory Structure

```
cvData.skills {
  programming: [
    "JavaScript", "TypeScript", "Python", 
    "Java", "C#", "C++", "SQL"
  ],
  frontend: [
    "React", "Angular", "HTML5", "CSS3", 
    "Responsive Design"
  ],
  backend: [
    "Node.js", "NestJS", "Express", 
    "Spring Boot", "Flask", "Django",
    "RESTful APIs", "GraphQL"
  ],
  databases: [
    "MongoDB", "PostgreSQL", "MySQL", 
    "Oracle", "SQL Server"
  ],
  devops: [
    "Docker", "Jenkins", "GitHub Actions", 
    "GitLab CI", "CI/CD", "Vercel"
  ],
  ai_automation: [
    "Hugging Face", "RAG", "AI Model Fine-Tuning",
    "n8n", "GitHub Copilot", "AI Agents"
  ],
  testing: [
    "Jest", "JUnit", "Unit Testing", 
    "Integration Testing"
  ],
  ... (16 categories total)
}

cvData.forbidden_skills [
  "Kubernetes", "AWS", "Azure", "GCP",
  "Terraform", "Kafka", "Redis",
  "React Native", "Flutter", "Vue.js",
  ... (25 total)
]
```

## Validation Logic

```javascript
// When Copilot asks: "Do I have Docker?"

function validate_skill(skill_name) {
  // Step 1: Check if skill is in forbidden list
  if (cvData.forbidden_skills.includes(skill_name)) {
    return {
      verified: false,
      forbidden: true,
      message: "❌ FORBIDDEN - Do NOT add to CV"
    };
  }
  
  // Step 2: Search through all skill categories
  for (category in cvData.skills) {
    if (cvData.skills[category].includes(skill_name)) {
      return {
        verified: true,
        category: category,
        message: `✅ Verified in ${category} skills`
      };
    }
  }
  
  // Step 3: Skill not found anywhere
  return {
    verified: false,
    message: "⚠️ NOT FOUND - Ask user before adding"
  };
}

// Example: validate_skill("Docker")
// Returns: { verified: true, category: "devops", message: "✅ Verified in devops skills" }

// Example: validate_skill("Kubernetes")
// Returns: { verified: false, forbidden: true, message: "❌ FORBIDDEN - Do NOT add to CV" }
```

## Integration Points

```
┌────────────────────────────────────────────────────────────┐
│              VS Code Configuration                          │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  .vscode/settings.json                                     │
│  {                                                          │
│    "github.copilot.chat.mcp": {                           │
│      "enabled": true,                                      │
│      "servers": {                                          │
│        "cv-data": {                                        │
│          "command": "node",                                │
│          "args": ["E:\\LatexCv\\mcp-server\\index.js"]   │
│        }                                                    │
│      }                                                      │
│    }                                                        │
│  }                                                          │
│                                                             │
└────────────────────────────────────────────────────────────┘
          │
          │ Copilot uses this config to connect
          │
          ▼
┌────────────────────────────────────────────────────────────┐
│              MCP Server Process                             │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  node E:\LatexCv\mcp-server\index.js                      │
│                                                             │
│  → Starts server on stdio                                  │
│  → Loads cv-data.js                                        │
│  → Registers 6 tools + 5 resources                         │
│  → Waits for Copilot queries                               │
│                                                             │
└────────────────────────────────────────────────────────────┘
          │
          │ Copilot sends JSON-RPC requests
          │
          ▼
┌────────────────────────────────────────────────────────────┐
│              Response to Copilot                            │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  {                                                          │
│    "tool": "validate_skill",                               │
│    "input": { "skill": "Docker" },                         │
│    "result": {                                              │
│      "verified": true,                                      │
│      "category": "devops",                                  │
│      "message": "✅ Verified in devops skills"            │
│    }                                                        │
│  }                                                          │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

## Security Model

```
┌─────────────────────────────────────────────┐
│         All Data Stays Local                 │
├─────────────────────────────────────────────┤
│                                              │
│  • MCP server runs on YOUR machine          │
│  • No external API calls                    │
│  • No data sent to cloud                    │
│  • Communication over stdio (local)         │
│  • cv-data.js is YOUR verified truth        │
│                                              │
└─────────────────────────────────────────────┘
```
