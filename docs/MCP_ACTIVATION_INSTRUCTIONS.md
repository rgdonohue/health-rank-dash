# MCP Activation Instructions for Claude (Enhanced)

## Overview

To empower automated development with Claude Code CLI in the HealthRankDash project, the following Modular Control Plane (MCP) tools should be activated **immediately after running `/init`**. These external tools dramatically expand Claude's capacity to not just generate code—but execute, test, navigate, inspect, and reflect within your development environment.

This document outlines essential and optional tools, includes rationale, installation/config guidance, troubleshooting steps, and a recommended startup config file.

---

## 🚨 CRITICAL: Pre-Activation Checklist

### Environment Validation
Before activating MCPs, ensure:

```bash
# 1. Verify Python and virtual environment
python3 --version  # Should be 3.11+
python3 -m venv --help  # Should not error

# 2. Verify Git is configured
git --version
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 3. Check project structure
ls -la  # Should see docs/ and data/ directories
```

### Documentation Consistency Check

```bash
# Validate documentation files exist and are readable
ls -la docs/
wc -l docs/*.md  # All files should have content
```

---

## 🚀 Essential External Tools for Claude Code CLI (MCP-Compatible)

### 1. 📁 Filesystem MCP

* **Purpose**: Enables Claude to read, write, and navigate files and directories.
* **Why?**: Without it, Claude cannot directly create or edit `data.etl/`, `tests/`, etc.
* **Tool**: [`@anthropic-ai/claude-mcp-filesystem`](https://github.com/anthropics/claude-mcp-filesystem)
* **Command**:

```bash
claude mcp add filesystem --transport stdio ./mcp/fs
```

**Troubleshooting:**
- If `./mcp/fs` doesn't exist: `mkdir -p mcp && touch mcp/fs`
- If permission denied: `chmod +x mcp/fs`
- **Fallback**: Use manual file operations with explicit tool calls

### 2. 🧪 Process Execution Tool (Runner)

* **Purpose**: Lets Claude run scripts, tests, or shell commands (`pytest`, `python etl.py`, etc.).
* **Why?**: Enables real-time feedback on generated code, test success, or runtime behavior.
* **Tool**: Custom or generic MCP runner (e.g., shell runner wrapper)
* **Command**:

```bash
claude mcp add runner --transport stdio ./mcp/runner
```

**Troubleshooting:**
- If runner fails: Test with simple command first: `echo "Hello World"`
- If path issues: Use absolute paths: `/usr/bin/python3`
- **Fallback**: Manual command execution with copy-paste instructions

### 3. 📦 Prompt Template Directory

* **Purpose**: Stores and version-controls structured YAML prompts (e.g., `extract-measures.yaml`)
* **Why?**: Claude can retrieve reusable prompt templates and inject context dynamically.
* **How?**: Use Git-tracked `docs/prompts/` folder with filenames Claude understands
* **Tool**: No extra installation required—just directory discipline

**Setup:**
```bash
mkdir -p docs/prompts
touch docs/prompts/README.md
echo "# Prompt Templates Directory" > docs/prompts/README.md
```

---

## ⚙️ Optional Tools (For Enhanced UX / QA)

### 4. 🖥️ Puppeteer + Screenshot MCP

* **Purpose**: Lets Claude open and inspect frontend UI; captures screenshots or DOM inspections
* **Why?**: Helps visually validate table layouts or detect rendering bugs
* **Tool**: `claude-mcp-puppeteer`
* **Command**:

```bash
claude mcp add puppeteer --transport sse http://localhost:3000
```

**Prerequisites:**
```bash
# Install Node.js if needed
node --version  # Should be 16+
npm install -g puppeteer
```

**Troubleshooting:**
- If port 3000 busy: Change to different port in config
- If Chrome/Chromium missing: `npm install puppeteer` includes Chromium
- **Fallback**: Manual UI testing with screenshots

### 5. 🧹 Code Review Assistant

* **Purpose**: Run linters (e.g., `flake8`, `pylint`) and provide static diagnostics Claude can review
* **Why?**: Keeps the codebase clean and encourages reflective improvement
* **Tool**: CLI review output piped into Claude context with `/review`

**Setup:**
```bash
# In activated virtual environment
pip install flake8 black mypy pytest-cov safety
```

**Usage:**
```bash
flake8 --max-line-length=88 --extend-ignore=E203 .
black --check .
mypy --strict .
safety check
```

### 6. 🧪 Jupyter Kernel Executor (Experimental)

* **Purpose**: Run correlation pipelines or exploratory ESDA in a notebook context
* **Why?**: Useful for validating real analysis tasks beyond static files

**Setup:**
```bash
pip install jupyter notebook pandas matplotlib seaborn
jupyter kernelspec list  # Verify Python kernel available
```

---

## 🧩 Recommended Minimum Tooling Set

| Tool                | Required? | Enhances                      | Fallback Available? |
| ------------------- | --------- | ----------------------------- | ------------------- |
| Filesystem MCP      | ✅ Yes     | Code creation, file updates   | ✅ Manual file ops  |
| CLI Runner (Pytest) | ✅ Yes     | TDD, script validation        | ✅ Copy-paste cmds  |
| Prompt Template Dir | ✅ Yes     | Structured prompting          | ✅ Manual templates |
| Code Quality Tools  | ⚠️ Recommended | Linting, security checks  | ✅ Manual review    |
| Puppeteer MCP       | Optional  | Frontend QA / screenshot logs | ✅ Manual testing   |
| Notebook Kernel     | Optional  | ESDA exploration (stretch)    | ✅ Script analysis  |

---

## ✅ Enhanced `mcp-config.json`

Create this in your project root to auto-load all tools on Claude CLI launch:

```json
{
  "version": "1.0",
  "allowedTools": ["filesystem", "runner", "puppeteer", "linter"],
  "validation": {
    "requireVirtualEnv": true,
    "checkGitConfig": true,
    "validateDocs": true
  },
  "tools": {
    "filesystem": {
      "transport": "stdio",
      "path": "./mcp/fs",
      "permissions": ["read", "write", "create"],
      "restricted_paths": ["/etc", "/usr", "/var"]
    },
    "runner": {
      "transport": "stdio",
      "path": "./mcp/runner",
      "timeout": 30,
      "allowed_commands": ["python", "pytest", "pip", "git"],
      "working_directory": "."
    },
    "puppeteer": {
      "transport": "sse",
      "url": "http://localhost:3000",
      "timeout": 10,
      "viewport": {"width": 1280, "height": 720}
    },
    "linter": {
      "transport": "stdio",
      "tools": ["flake8", "black", "mypy", "safety"],
      "auto_fix": false
    }
  },
  "logging": {
    "level": "INFO",
    "file": "logs/mcp-activity.log"
  }
}
```

---

## 🔧 Activation Sequence with Validation

### Step 1: Pre-Flight Checks

```bash
# Run this script before MCP activation
#!/bin/bash
set -e

echo "🔍 Validating HealthRankDash environment..."

# Check Python version
python3 --version | grep -E "3\.(11|12)" || {
    echo "❌ Python 3.11+ required"
    exit 1
}

# Check virtual environment capability
python3 -m venv --help > /dev/null || {
    echo "❌ Virtual environment support missing"
    exit 1
}

# Check Git configuration
git config user.name > /dev/null || {
    echo "❌ Git user.name not configured"
    exit 1
}

# Validate documentation files
for file in docs/PRD.md docs/AGENTIC_INSTRUCTIONS.md; do
    [ -s "$file" ] || {
        echo "❌ Missing or empty: $file"
        exit 1
    }
done

# Check data file
[ -f "data/analytic_data2025_v2.csv" ] || {
    echo "⚠️  CHR data file not found - download required"
}

echo "✅ Environment validation passed"
```

### Step 2: MCP Activation with Fallbacks

```bash
#!/bin/bash
echo "🚀 Activating MCP tools..."

# Try to activate each tool with fallback
claude mcp add filesystem --transport stdio ./mcp/fs || {
    echo "⚠️  Filesystem MCP failed - using manual file operations"
    mkdir -p mcp && touch mcp/fs
}

claude mcp add runner --transport stdio ./mcp/runner || {
    echo "⚠️  Runner MCP failed - using manual command execution"
    mkdir -p mcp && touch mcp/runner
}

# Optional tools (non-blocking failures)
claude mcp add puppeteer --transport sse http://localhost:3000 || {
    echo "ℹ️  Puppeteer MCP skipped - manual UI testing available"
}

echo "✅ MCP activation complete (with fallbacks as needed)"
```

### Step 3: Verification

```bash
# Test MCP functionality
claude mcp list  # Should show active tools
claude mcp test filesystem  # Test file operations
claude mcp test runner  # Test command execution
```

---

## 🚨 Troubleshooting Guide

### Common Issues and Solutions

| Issue | Symptoms | Solution |
|-------|----------|----------|
| MCP tools not found | `command not found: claude` | Install Claude CLI: `pip install claude-cli` |
| Permission denied | `chmod: cannot access './mcp/fs'` | `sudo chmod +x ./mcp/fs` |
| Port already in use | `Error: listen EADDRINUSE :::3000` | Change port in config or kill process |
| Virtual env activation fails | `source: command not found` | Use `./venv/bin/activate` (not `source`) |
| Git config missing | `Please tell me who you are` | Set `git config --global user.*` |
| Documentation inconsistency | `File not found` errors | Run documentation validation script |

### Recovery Procedures

#### Complete MCP Reset:
```bash
claude mcp remove --all
rm -rf mcp/
mkdir -p mcp
# Re-run activation sequence
```

#### Fallback to Manual Mode:
```bash
echo "MANUAL_MODE=true" > .env
# Continue development without MCPs
# Use copy-paste for commands
# Use text editor for file operations
```

---

## 📋 Success Criteria

Before proceeding with development, verify:

- [ ] Virtual environment can be created and activated
- [ ] Git is configured and working
- [ ] All documentation files are readable and consistent
- [ ] At least Filesystem and Runner MCPs are functional (or fallbacks ready)
- [ ] Project structure matches expected layout
- [ ] CHR data file is accessible
- [ ] Code quality tools are available in venv

---

## Final Notes

Once MCPs are enabled (or fallbacks are ready):

* Use **filesystem** to scaffold modules (`data.etl`, `testing.qa`, etc.)
* Use **runner** to validate test coverage and ETL correctness
* Use **puppeteer** to validate frontend rendering if visual QA is required
* **Always verify** virtual environment activation before development
* **Make frequent git commits** with meaningful messages

Claude will log its usage of each MCP and reflect on effectiveness in its `CLAUDE.md` entries as outlined in the [Agentic Logging Guidelines](./AGENTIC_LOGGING_GUIDELINES.md).

### Emergency Contacts
- MCP tool issues: Continue with manual fallbacks
- Documentation problems: Fix consistency before development
- Environment setup failures: Validate Python/Git setup first

**Remember**: The project can succeed even with manual development workflows. MCPs are enhancement tools, not requirements for success.
