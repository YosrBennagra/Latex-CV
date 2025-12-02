# CV Data MCP Server

This MCP (Model Context Protocol) server provides canonical CV data to AI agents, preventing hallucination and ensuring only verified information is used when adapting CVs.

## Purpose

**CRITICAL**: This server is the **source of truth** for all CV-related data. AI agents (Claude, ChatGPT, Copilot, etc.) MUST:
- ✅ Only use skills, experience, and projects listed in `cv-data.js`
- ✅ Reorder and rephrase existing data to match job requirements
- ❌ NEVER fabricate or add unverified skills/experience
- ❌ NEVER claim technologies not in the verified inventory

## Installation

```powershell
cd E:\LatexCv\mcp-server
npm install
```

## Configuration

### For Claude Desktop

Add to your Claude Desktop config file (`%APPDATA%\Claude\claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "cv-data": {
      "command": "node",
      "args": ["E:\\LatexCv\\mcp-server\\index.js"]
    }
  }
}
```

### For GitHub Copilot / VS Code

Add to your VS Code settings (`.vscode/settings.json` or User Settings):

```json
{
  "github.copilot.advanced": {
    "mcpServers": {
      "cv-data": {
        "command": "node",
        "args": ["E:\\LatexCv\\mcp-server\\index.js"]
      }
    }
  }
}
```

## Available Tools

### 1. `get_canonical_experience`
Get verified work experience data.
```javascript
// Optional: filter by company
{ "company": "IT Serv" }
```

### 2. `get_verified_skills`
Get verified technical skills by category.
```javascript
// Optional: filter by category
{ "category": "programming" }
// Categories: programming, frontend, backend, databases, devops, cloud, tools, ai_automation, testing, methodologies, systems
```

### 3. `get_projects`
Get verified project portfolio.
```javascript
// Optional: filter by type
{ "type": "personal" }
// Types: personal, academic, professional
```

### 4. `get_education`
Get verified education credentials.

### 5. `validate_skill`
Validate if a skill exists before adding to CV.
```javascript
{ "skill": "Docker" }
// Returns: { verified: true/false, category: "...", message: "..." }
```

### 6. `suggest_skill_reordering`
Get suggestions for reordering existing skills based on job requirements.
```javascript
{ "job_requirements": "React, Python, Docker, MongoDB" }
// Returns matched skills and suggested ordering
```

## Available Resources

- `cv://personal/info` - Contact details
- `cv://experience/all` - Complete work history
- `cv://skills/inventory` - Comprehensive skills inventory
- `cv://projects/all` - Project portfolio
- `cv://education/all` - Academic credentials

## Usage in AI Prompts

When adapting CV for a job, AI agents should:

1. **First**, query verified data:
```
Use get_verified_skills to see what technologies I actually know
Use get_canonical_experience to see my real work history
```

2. **Then**, validate job requirements:
```
For each skill in job description, use validate_skill to check if I have it
```

3. **Finally**, reorder existing skills:
```
Use suggest_skill_reordering with job requirements to prioritize relevant skills
```

## Updating CV Data

To add new verified skills or experience:

1. Edit `cv-data.js`
2. Add to appropriate section with `verified: true`
3. Update `metadata.last_updated`
4. Restart MCP server (Claude Desktop will auto-reload)

## Running the Server

```powershell
# Production
npm start

# Development (auto-reload on changes)
npm run dev
```

## Testing

Test the server with:

```powershell
# In PowerShell
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | node index.js
```

## Security

- All data is local to your machine
- No external API calls
- No data leaves your system
- MCP communication over stdio (local process)

## Troubleshooting

### Claude Desktop not seeing MCP server
1. Check config file path: `%APPDATA%\Claude\claude_desktop_config.json`
2. Verify absolute path to `index.js` is correct
3. Restart Claude Desktop completely

### VS Code Copilot not connecting
1. MCP support in Copilot may require specific extensions
2. Check VS Code output panel for MCP logs
3. Ensure Node.js is in PATH

### Validation errors
- Check `cv-data.js` syntax with `node -c cv-data.js`
- Verify all arrays and objects are properly formatted
- Check console for error messages

## Best Practices

1. **Always validate** before adding skills to CV
2. **Reorder, don't fabricate** - prioritize existing skills
3. **Update cv-data.js** when you gain new verified experience
4. **Test prompts** with `validate_skill` before bulk CV generation
5. **Keep metadata current** - update `last_updated` field

## Architecture

```
MCP Server (stdio)
    ↓
CV Data (cv-data.js) - Source of Truth
    ↓
AI Agent (Claude/Copilot/ChatGPT)
    ↓
CV Generation (LaTeX files)
```

The MCP server acts as a gatekeeper, ensuring AI agents can only access verified data and preventing hallucination.
