# MCP Dependencies Setup Guide

This guide helps you ensure all dependencies are available to run your `claude_desktop_config.json` with MCP servers.

## Prerequisites Overview

Your configuration requires:
- **Node.js** (JavaScript runtime)
- **mcp-remote** npm package (MCP proxy tool)

---

## macOS Setup

### 1. Install Homebrew (if not already installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Node.js

```bash
brew install node
```

### 3. Verify Node.js Installation

```bash
node --version
which node
```

Expected output should show version (e.g., `v20.x.x`) and path (e.g., `/opt/homebrew/bin/node` or `/usr/local/bin/node`)

### 4. Install mcp-remote Package

```bash
npm install -g mcp-remote
```

### 5. Verify mcp-remote Installation

```bash
npm list -g mcp-remote
which mcp-remote
```

### 6. Locate Your Installation Paths

Find your Node.js path:
```bash
which node
```

Find your mcp-remote proxy.js path:
```bash
npm root -g
```

The `proxy.js` file will be at: `<npm-root>/mcp-remote/dist/proxy.js`

### 7. Update claude_desktop_config.json for macOS

Location: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "hello-world": {
      "command": "/opt/homebrew/bin/node",
      "args": [
        "/opt/homebrew/lib/node_modules/mcp-remote/dist/proxy.js",
        "https://mcp-helloworld-production.up.railway.app/mcp"
      ]
    }
  }
}
```

**Note:** Your actual paths may vary. Common paths:
- Intel Mac: `/usr/local/bin/node` and `/usr/local/lib/node_modules/...`
- Apple Silicon: `/opt/homebrew/bin/node` and `/opt/homebrew/lib/node_modules/...`

### 8. Verify Configuration Works

Test the command directly:
```bash
/opt/homebrew/bin/node /opt/homebrew/lib/node_modules/mcp-remote/dist/proxy.js https://mcp-helloworld-production.up.railway.app/mcp
```

---

## Windows Setup

### 1. Install Node.js

1. Download the Windows installer from: https://nodejs.org/
2. Run the installer (choose LTS version recommended)
3. Follow installation wizard (accept defaults)
4. Restart your terminal/command prompt

### 2. Verify Node.js Installation

Open Command Prompt or PowerShell:
```cmd
node --version
where node
```

Expected output should show version and path (e.g., `C:\Program Files\nodejs\node.exe`)

### 3. Install mcp-remote Package

```cmd
npm install -g mcp-remote
```

### 4. Verify mcp-remote Installation

```cmd
npm list -g mcp-remote
```

### 5. Locate Your Installation Paths

Find your Node.js path:
```cmd
where node
```

Find your npm global root:
```cmd
npm root -g
```

The `proxy.js` file will be at: `<npm-root>\mcp-remote\dist\proxy.js`

Example: `C:\Users\YourUsername\AppData\Roaming\npm\node_modules\mcp-remote\dist\proxy.js`

### 6. Update claude_desktop_config.json for Windows

Location: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "hello-world": {
      "command": "C:\\Program Files\\nodejs\\node.exe",
      "args": [
        "C:\\Users\\YourUsername\\AppData\\Roaming\\npm\\node_modules\\mcp-remote\\dist\\proxy.js",
        "https://mcp-helloworld-production.up.railway.app/mcp"
      ]
    }
  }
}
```

**Important:** 
- Use double backslashes (`\\`) in JSON strings
- Replace `YourUsername` with your actual Windows username
- Your paths may vary based on installation choices

### 7. Verify Configuration Works

Test the command directly in PowerShell:
```powershell
& "C:\Program Files\nodejs\node.exe" "C:\Users\YourUsername\AppData\Roaming\npm\node_modules\mcp-remote\dist\proxy.js" "https://mcp-helloworld-production.up.railway.app/mcp"
```

---

## Common Issues & Troubleshooting

### Issue: "command not found" or "is not recognized"

**Solution:** Node.js is not in your PATH
- macOS: Run `echo $PATH` and ensure Node.js bin directory is listed
- Windows: Restart terminal after installing Node.js, or manually add to PATH

### Issue: Cannot find proxy.js file

**Solution:** Run `npm list -g mcp-remote` to verify installation, then reinstall if needed:
```bash
npm uninstall -g mcp-remote
npm install -g mcp-remote
```

### Issue: Permission errors during npm install (macOS/Linux)

**Solution:** Either use sudo (not recommended) or fix npm permissions:
```bash
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.zshrc
source ~/.zshrc
```

### Issue: Claude Desktop doesn't recognize the MCP server

**Solution:** 
1. Verify JSON syntax is valid (no trailing commas, proper escaping)
2. Restart Claude Desktop completely
3. Check Claude Desktop logs for errors

### Issue: MCP server URL is unreachable

**Solution:**
- Test the URL in a browser: `https://mcp-helloworld-production.up.railway.app/mcp`
- Check your internet connection
- Verify the server is running

---

## Quick Validation Checklist

- [ ] Node.js installed and in PATH
- [ ] `node --version` shows version number
- [ ] mcp-remote installed globally
- [ ] `npm list -g mcp-remote` shows package
- [ ] Paths in config match actual file locations
- [ ] JSON syntax is valid (use a JSON validator)
- [ ] Claude Desktop has been restarted
- [ ] Test command runs successfully in terminal

---

## Additional Resources

- Node.js Documentation: https://nodejs.org/docs/
- npm Documentation: https://docs.npmjs.com/
- Claude Desktop Documentation: https://docs.claude.com/
- MCP Documentation: https://modelcontextprotocol.io/
