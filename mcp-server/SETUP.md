# MCP Server Setup Guide

## Quick Start

### 1. Install Dependencies

```powershell
cd E:\LatexCv\mcp-server
npm install
```

### 2. Test the Server

```powershell
npm start
```

You should see: `CV Data MCP server running on stdio`

### 3. Configure GitHub Copilot (VS Code)

**Location**: `.vscode/settings.json` in your workspace (already created for you)

**Configuration added**:
```json
{
  "github.copilot.chat.mcp": {
    "enabled": true,
    "servers": {
      "cv-data": {
        "command": "node",
        "args": ["E:\\LatexCv\\mcp-server\\index.js"]
      }
    }
  }
}
```

**Important**: 
- MCP support in Copilot requires VS Code version 1.95+ and Copilot Chat extension
- Reload VS Code window after configuration changes: `Ctrl+Shift+P` → "Developer: Reload Window"
- Use double backslashes `\\` in Windows paths

### 4. Verify in GitHub Copilot Chat

After reloading VS Code:
1. Open Copilot Chat panel (`Ctrl+Alt+I`)
2. Type: `@workspace Use the cv-data MCP server to validate if I have Docker`
3. Copilot should respond using the MCP server tools
4. You can also ask: "List my verified skills using get_verified_skills"

### Alternative: Configure Claude Desktop

If you also want Claude Desktop integration:

**Location**: `%APPDATA%\Claude\claude_desktop_config.json`

**Add this configuration**:
```json
{
  "mcpServers": {
    "cv-data": {
      "command": "node",
      "args": ["E:\\LatexCv\\mcp-server\\index.js"],
      "env": {}
    }
  }
}
```

Restart Claude Desktop after config changes.

## Usage Examples

### Example 1: Validate Skills Before Adding to CV

```
You: I'm applying for a job that requires React, Docker, and .NET. 
     Use validate_skill to check which of these I actually have.

Claude: [Uses MCP server]
- React: ✓ Verified (frontend category)
- Docker: ✓ Verified (devops category)  
- .NET: ✗ NOT VERIFIED - Do not add to CV
```

### Example 2: Reorder Skills for Job Application

```
You: Reorder my skills for a job requiring: Python, MongoDB, Docker, React

Claude: [Uses suggest_skill_reordering]
Suggested order:
- Backend: Python, Flask
- Frontend: React, ReactJS
- Databases: MongoDB
- DevOps: Docker, CI/CD
```

### Example 3: Get All Experience

```
You: Show me my complete work history using the MCP server

Claude: [Uses get_canonical_experience]
Returns: IT Serv, IronByte, Ooredoo internships with verified bullets
```

## Manual Testing (PowerShell)

Test MCP server responses:

```powershell
# List available tools
$request = '{"jsonrpc":"2.0","method":"tools/list","id":1}'
echo $request | node E:\LatexCv\mcp-server\index.js

# Validate a skill
$request = '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"validate_skill","arguments":{"skill":"Docker"}},"id":2}'
echo $request | node E:\LatexCv\mcp-server\index.js
```

## Common Issues

### Issue: Claude Desktop doesn't show MCP server

**Solution**:
1. Check config file exists: `%APPDATA%\Claude\claude_desktop_config.json`
2. Verify JSON syntax (use JSON validator)
3. Ensure Node.js is installed: `node --version`
4. Restart Claude Desktop completely (not just close window)

### Issue: "Module not found" error

**Solution**:
```powershell
cd E:\LatexCv\mcp-server
Remove-Item -Recurse -Force node_modules
npm install
```

### Issue: Server starts but no response

**Solution**:
- Check `cv-data.js` syntax: `node -c E:\LatexCv\mcp-server\cv-data.js`
- Look for console errors when server starts
- Verify export statement in `cv-data.js`

## Updating Your Data

When you gain new experience or skills:

1. **Edit `cv-data.js`**:
```javascript
experience: [
  {
    title: 'New Position',
    company: 'New Company',
    // ... add complete data
    verified: true,
  },
  // ... existing experience
],
```

2. **Update skills**:
```javascript
skills: {
  programming: ['C++', 'Python', 'NewLanguage'], // Add here
  // ...
}
```

3. **Update metadata**:
```javascript
metadata: {
  last_updated: '2025-12-03', // Today's date
  // ...
}
```

4. **Restart** Claude Desktop or reload MCP connection

## Best Practices for AI Prompts

### ✅ Good Prompts

```
"Use get_verified_skills to see what technologies I know, 
then adapt my CV for this [job description]"

"Validate each skill in this job posting against my verified 
skills inventory before suggesting CV changes"

"Get my canonical experience and reorder bullets to emphasize 
Docker and Python for this DevOps role"
```

### ❌ Bad Prompts

```
"Add Kubernetes experience to my CV"
// Without validation - might add unverified skill

"Create a CV showing 5 years of .NET experience"
// Fabricates experience not in canonical data

"List skills I should learn for this job"
// Different purpose - this is ok, but clarify you're 
// asking what to LEARN, not what to ADD to CV
```

## Integration with CV Generation Workflow

Recommended workflow:

1. **Paste job description** to AI
2. **AI queries MCP server** for verified data
3. **AI validates** required skills exist
4. **AI reorders** existing skills to prioritize matches
5. **AI generates** CV using only verified data
6. **You review** - check no fabricated content

## Next Steps

After MCP server is working:

1. **Test validation** with various skills
2. **Practice prompts** for CV adaptation
3. **Update cv-data.js** with any missing verified skills
4. **Create prompt templates** for common job types
5. **Consider** web app integration (Phase 2)

## Support

If you encounter issues:
1. Check Node.js version: `node --version` (should be 18+)
2. Review server logs in terminal
3. Test with manual PowerShell commands above
4. Verify config file JSON syntax
5. Restart everything (terminal, Claude Desktop)
