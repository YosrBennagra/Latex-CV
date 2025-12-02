# 📋 MCP Server Quick Reference

## Verified Skills Summary

### ✅ YOU HAVE (90+ skills across 16 categories):

**Programming**: JavaScript, TypeScript, Python, Java, C#, C++, SQL  
**Frontend**: React, Angular, HTML5, CSS3, Responsive Design  
**Backend**: Node.js, NestJS, Express, Spring Boot, Flask, Django, RESTful APIs, GraphQL  
**Databases**: MongoDB, PostgreSQL, MySQL, Oracle, SQL Server  
**DevOps**: Docker, Jenkins, GitHub Actions, GitLab CI, CI/CD, Vercel  
**AI/Automation**: Hugging Face, RAG, AI Model Fine-Tuning, n8n, GitHub Copilot  
**Testing**: Jest, JUnit, Unit Testing, Integration Testing  
**Game Dev**: Unity, C#, Mobile Game Development  
**Desktop**: Qt, C++

### ❌ YOU DON'T HAVE (25 forbidden skills):

Kubernetes, AWS, AWS Lambda, Azure, GCP, Terraform, Kafka, Redis, React Native, Flutter, Vue.js, FastAPI, Cypress, Playwright, and more

## Quick Commands

### Validate a Single Skill
```
@workspace Use cv-data MCP validate_skill to check: Docker
```

### Get All Skills
```
@workspace Use cv-data MCP get_verified_skills
```

### Validate Job Requirements
```
@workspace Job requires: React, Python, Kubernetes, AWS
Use cv-data MCP validate_skill for each technology
```

### Safe CV Adaptation
```
@workspace Adapt CV for [job title]:
1. Query cv-data MCP server for verified skills
2. Validate each job requirement
3. Reorder skills (no new additions)
4. Update role/summary only
```

## MCP Server Status

**Location**: `E:\LatexCv\mcp-server\`  
**Data File**: `cv-data.js` (your verified CV data)  
**Config**: `.vscode/settings.json` (Copilot integration)  
**Test**: Run `node test.js` to verify data

## Workflow

```
Job Description → MCP Server Validation → Skill Matching → CV Reordering
                     ↓
            [Verified Skills Only]
                     ↓
              Safe CV Update
```

## Experience (LOCKED - Never Modify)

1. **IT Serv** (Feb 2025 - Aug 2025) - Full-Stack + AI + DevOps
2. **IronByte** (Jun 2024 - Aug 2024) - NestJS + React + MongoDB
3. **Ooredoo Tunisie** (Jul 2023 - Sep 2023) - Spring Boot + Angular

## Projects (LOCKED - Never Modify)

1. **n8n Workflow Automation** - AI agents, email/Discord pipelines
2. **Shape Blaster** - Unity C# mobile game with AI-assisted dev
3. **Collaborative Platform** - React + NestJS + WebSockets
4. **Construction Management** - Qt + C++ desktop app

## Remember

- ✅ Reorder existing skills = OK
- ✅ Rephrase bullets = OK  
- ✅ Update role/title/summary = OK
- ❌ Add unverified skills = FORBIDDEN
- ❌ Modify experience dates/companies = FORBIDDEN
- ❌ Fabricate projects = FORBIDDEN

## Support

- Full docs: [mcp-server/README.md](README.md)
- Setup guide: [mcp-server/SETUP.md](SETUP.md)
- Usage guide: [mcp-server/USAGE_GUIDE.md](USAGE_GUIDE.md)
