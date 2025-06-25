# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**HealthRankDash** is a lightweight, test-driven platform for exploratory spatial data analysis (ESDA) of U.S. county health indicators using County Health Rankings (CHR) data. The project serves dual purposes: enabling data exploration and evaluating AI-assisted development workflows using modular control plane (MCP) patterns.

## Development Environment Setup

### Python Virtual Environment (CRITICAL)

**ALWAYS create and activate a Python virtual environment before any development:**

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Verify activation (should show venv path)
which python

# Install core dependencies
pip install fastapi uvicorn pytest pytest-cov flake8 black mypy safety
```

### Git Workflow Requirements

Make frequent, meaningful commits throughout development:

```bash
# Initialize if needed
git init
echo "venv/\n__pycache__/\n*.pyc\n.env\n.DS_Store\ncache/\nlogs/" > .gitignore
git add .gitignore
git commit -m "Initial setup: Add .gitignore and venv structure"

# Commit after each major step with descriptive messages
git commit -m "Add CHR data parsing module with indicator extraction"
git commit -m "Add unit tests for ETL indicator parsing - 95% coverage"
git commit -m "Implement FastAPI endpoints for county filtering"
```

## Architecture

### Modular Control Plane (MCP) Structure

```
health-rank-dash/
├── data/                   # CHR CSV data file
│   └── analytic_data2025_v2.csv
├── docs/                   # Complete documentation suite
│   ├── PRD.md             # Product requirements
│   ├── AGENTIC_INSTRUCTIONS.md  # AI development guidelines
│   ├── AGENTIC_LOGGING_GUIDELINES.md
│   └── prompts/           # YAML prompt templates
│       └── extract-measures.yaml
└── [Future MCP modules to be created:]
    ├── data.etl/          # CHR CSV parsing and validation
    ├── processing.analysis/ # Statistical analysis and correlations
    ├── backend.api/       # FastAPI endpoints
    ├── frontend.ui/       # Alpine.js + Bulma dashboard
    ├── testing.qa/        # Comprehensive test suite
    └── config.schema/     # Configuration and metadata
```

### Technology Stack

- **Backend**: Python 3.11+ | FastAPI | Pydantic
- **Frontend**: HTML | Alpine.js | Bulma CSS
- **Testing**: pytest | pytest-cov
- **Data**: County Health Rankings 2025 CSV (~800 columns)
- **Quality**: flake8, black, mypy, safety

## Common Development Commands

Since this is an early-stage project, standard commands will be established as development progresses:

```bash
# Environment management
python3 -m venv venv
source venv/bin/activate

# Development dependencies
pip install fastapi uvicorn pytest pytest-cov flake8 black mypy safety

# Future commands (to be implemented):
# python -m pytest tests/ --cov=src --cov-report=html
# flake8 src/ tests/
# black src/ tests/
# mypy src/
# safety check
```

## Data Processing

### CHR Data Structure

The County Health Rankings CSV contains ~800 columns following patterns:
- `v###_rawvalue` - Primary metric values
- `v###_numerator`, `v###_denominator` - Rate components  
- `v###_ci_low`, `v###_ci_high` - 95% confidence intervals
- Geographic identifiers: `fipscode`, `state`, `county`, `year`

### Indicator Parsing Strategy

Use regex pattern `v(\d{3})_(.+)` to extract indicator IDs and group related columns. The `docs/prompts/extract-measures.yaml` template provides detailed specifications for building the indicator catalog.

## Quality Standards

### Code Quality Requirements
- All code must pass: flake8, black, mypy
- Security scan dependencies: safety check
- Minimum test coverage: 90% for ETL, 100% for API
- Performance target: sub-500ms API responses

### Accessibility Requirements
- WCAG 2.1 AA compliance mandatory
- Screen reader compatibility
- Keyboard navigation support
- Progressive enhancement (works without JavaScript)

### Git and Documentation Standards
- Commit after each MCP module completion
- Include test coverage info in commit messages
- Update documentation with functional changes
- Log all assumptions and decisions

## AI Development Guidelines

### Environment Setup Checklist
1. Create and activate virtual environment FIRST
2. Install dependencies only after venv activation
3. Initialize git with comprehensive .gitignore
4. Create MCP directory structure with README files

### Development Workflow
1. **TDD Approach**: Write tests before implementation
2. **Modular Development**: Focus on one MCP module at a time
3. **Frequent Commits**: Commit after each logical completion
4. **Comprehensive Logging**: Document all decisions and assumptions
5. **Quality Gates**: All code must pass linting and security scans

### Structured Prompts
Use YAML templates in `docs/prompts/` for consistent AI interactions:
- `extract-measures.yaml` - CHR indicator parsing
- Future templates for API generation, testing, and validation

## Success Metrics

### Functional Targets
- 100% backend test coverage
- 10+ validated health indicators parsed
- <1s frontend load times
- WCAG 2.1 AA accessibility compliance
- Zero critical security vulnerabilities

### AI Effectiveness Tracking
- Code generation time vs manual development
- Test coverage achieved by AI vs human
- Number of human edits required per AI contribution
- Bug introduction rate comparison

## Key Implementation Notes

### Critical Requirements
- **Virtual Environment**: NEVER install packages globally
- **Git Discipline**: Meaningful commits with context
- **Testing First**: TDD methodology throughout
- **Documentation**: Update with every functional change
- **Security**: Regular dependency scanning and validation

### Project Constraints
- Local-first (no external databases)
- Lightweight and fast (<200MB RAM preferred)
- Works offline
- Accessible to users with varying technical skills

This project emphasizes quality, maintainability, and systematic AI-assisted development practices while building a practical tool for health data exploration.