# 🚀 Using the CV Data MCP Server with GitHub Copilot

## ✅ Setup Complete!

Your MCP server is now configured and ready to use with GitHub Copilot in VS Code.

## 🔍 How to Use It

### 1. Reload VS Code
Press `Ctrl+Shift+P` → Type "Developer: Reload Window" → Enter

### 2. Open Copilot Chat
Press `Ctrl+Alt+I` or click the Copilot Chat icon

### 3. Start Using MCP Server Commands

#### Example 1: Validate Skills Before Adding to CV
```
@workspace I'm applying to a job that requires React, Docker, Kubernetes, and AWS. 
Use the cv-data MCP server's validate_skill tool to check which of these I actually have.
```

**Expected Response:**
- ✅ React: Verified (frontend skills)
- ✅ Docker: Verified (devops skills)
- ❌ Kubernetes: FORBIDDEN - not in your verified skills
- ❌ AWS: FORBIDDEN - not in your verified skills

#### Example 2: Get All Verified Skills
```
@workspace Use the cv-data MCP server to list all my verified skills by category
```

#### Example 3: Adapt CV for Job (Safe Mode)
```
@workspace I'm applying for this job: [paste job description]

Before making ANY changes:
1. Use get_verified_skills from cv-data MCP server
2. Use validate_skill for each technology in the job description
3. Only reorder existing skills - DO NOT add unverified ones
4. Update CV_Yosr_BenNagra_English_ATS.tex
```

#### Example 4: Get Experience Details
```
@workspace Use get_canonical_experience from cv-data MCP server to show my work history
```

#### Example 5: Check Projects
```
@workspace Use get_projects from cv-data MCP server to list my verified projects
```

## 🎯 Best Practices

### ✅ DO:
- **Always validate skills** before adding to CV using `validate_skill`
- **Query verified data** using MCP server tools
- **Reorder existing skills** to prioritize job requirements
- **Ask for confirmation** if a skill isn't in the verified list

### ❌ DON'T:
- Add skills from the forbidden list (Kubernetes, AWS, Azure, etc.)
- Fabricate experience or projects
- Assume you have a technology without validation
- Modify experience bullet points (they are locked)

## 📋 Available MCP Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `get_verified_skills` | List all verified skills by category | "Show me all my backend skills" |
| `validate_skill` | Check if a specific skill exists | "Do I have Docker?" |
| `get_canonical_experience` | Get work history with verified bullets | "What did I do at IT Serv?" |
| `get_projects` | List verified projects | "Show my personal projects" |
| `get_education` | Get education credentials | "What's my degree?" |
| `suggest_skill_reordering` | Get skill prioritization suggestions | "Reorder for React/Node/MongoDB job" |

## 🧪 Test Results

Your MCP server correctly identifies:
- ✅ **Verified Skills**: Docker, React, Python, TypeScript, NestJS, Flask, MongoDB, etc.
- ❌ **Forbidden Skills**: Kubernetes, AWS, Azure, Terraform, Kafka, Redis, etc.

## 🔄 Workflow for Job Applications

1. **Paste job description** to Copilot Chat
2. **Copilot queries MCP server** to validate requirements
3. **Copilot shows you** which skills match (✅) and which don't (❌)
4. **You decide** whether to proceed or skip the job
5. **Copilot reorders** existing skills to prioritize matches
6. **CV gets updated** with ONLY verified data

## 💡 Example Prompts

### Safe CV Adaptation
```
@workspace Adapt my CV for this Software Engineer position requiring:
- Python, React, Docker, PostgreSQL (use MCP to verify)
- CI/CD, Git, RESTful APIs (validate these too)

Steps:
1. Validate each skill using cv-data MCP server
2. Reorder skills section to prioritize verified matches
3. Update role/title and summary
4. Keep experience unchanged
```

### Checking for Missing Skills
```
@workspace This job requires Go, Kubernetes, and Terraform. 
Use validate_skill to check if I have these.
If not, what related skills do I have?
```

### Learning Roadmap (Safe)
```
@workspace Based on my verified skills in cv-data MCP server, 
what skills should I learn to become a DevOps engineer?
(This is for learning, not for adding to CV)
```

## 🛠️ Troubleshooting

### Copilot Not Using MCP Server?
1. Check `.vscode/settings.json` exists with MCP config
2. Reload VS Code window completely
3. Check VS Code version is 1.95+
4. Try: `@workspace Use the cv-data MCP server to validate Docker`

### Can't See MCP Tools?
- Update GitHub Copilot Chat extension
- Update VS Code to latest version
- Restart VS Code completely (close all windows)

### MCP Server Not Starting?
```powershell
cd E:\LatexCv\mcp-server
npm start
```
Should show: "CV Data MCP server running on stdio"

## 📚 What's in the MCP Server?

### ✅ Verified Data (FROM YOUR ACTUAL CV):
- **3 Internships**: IT Serv, IronByte, Ooredoo Tunisie
- **4 Projects**: n8n Automation, Shape Blaster, Collaborative Platform, Construction Management
- **16 Skill Categories**: 90+ verified technologies
- **Education**: ESPRIT Bachelor's in Computer Science
- **Languages**: Arabic (Native), English (Fluent), French (Fluent)

### ❌ Forbidden Skills (NEVER ADD):
Kubernetes, AWS, Azure, GCP, Terraform, Kafka, Redis, React Native, Flutter, Vue.js, and 15+ more

## 🎉 You're Ready!

From now on, when you paste a job description, I'll:
1. **Automatically query** the MCP server
2. **Validate** every skill requirement
3. **Show you** what matches and what doesn't
4. **Only add** verified skills to your CV
5. **Never fabricate** experience or technologies

Try it now! Paste a job description and I'll demonstrate the MCP validation workflow.
