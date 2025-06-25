# HealthRankDash Documentation

## Overview

This directory contains all documentation for **HealthRankDash**, a lightweight, test-driven platform for exploratory spatial data analysis (ESDA) of U.S. county health indicators. The project serves as both a practical data analysis tool and a research probe into AI-assisted software development using agentic patterns.

---

## 📁 Documentation Structure

| File | Purpose | Audience |
|------|---------|----------|
| **[PRD.md](./PRD.md)** | Complete product requirements document | All stakeholders |
| **[AGENTIC_INSTRUCTIONS.md](./AGENTIC_INSTRUCTIONS.md)** | Instructions for Claude AI co-developer | AI agent |
| **[AGENTIC_LOGGING_GUIDELINES.md](./AGENTIC_LOGGING_GUIDELINES.md)** | Logging and reflection protocols | AI agent, researchers |
| **[MCP_ACTIVATION_INSTRUCTIONS.md](./MCP_ACTIVATION_INSTRUCTIONS.md)** | Setup guide for AI development tools | Human developers |

---

## 🚀 Quick Start

### For Human Developers

1. **Read the PRD**: Start with [PRD.md](./PRD.md) to understand project goals and requirements
2. **Set up environment**: Follow [MCP_ACTIVATION_INSTRUCTIONS.md](./MCP_ACTIVATION_INSTRUCTIONS.md) for AI tool setup
3. **Review AI protocols**: Understand [AGENTIC_INSTRUCTIONS.md](./AGENTIC_INSTRUCTIONS.md) for AI collaboration patterns

### For AI Agents (Claude)

1. **Read all documentation files** to understand project context
2. **Follow setup requirements** in [AGENTIC_INSTRUCTIONS.md](./AGENTIC_INSTRUCTIONS.md)
3. **Implement logging protocols** from [AGENTIC_LOGGING_GUIDELINES.md](./AGENTIC_LOGGING_GUIDELINES.md)
4. **ALWAYS create virtual environment and make frequent git commits**

---

## 🎯 Project Goals

### Primary Objectives
- **Data Analysis Tool**: Enable exploration of County Health Rankings data
- **AI Research**: Evaluate AI-assisted development workflows
- **Accessibility**: Ensure WCAG 2.1 AA compliance
- **Performance**: Achieve sub-500ms API response times

### Success Metrics
- ✅ 100% backend test coverage
- ✅ 10+ validated health indicators
- ✅ <1s frontend load times
- ✅ WCAG 2.1 AA accessibility compliance
- ✅ Zero critical security vulnerabilities

---

## 🏗️ Architecture Overview

### Modular Control Plane (MCP) Structure
```
health-rank-dash/
├── data.etl/           # CHR CSV parsing and validation
├── processing.analysis/ # Statistical analysis and correlations
├── backend.api/        # FastAPI endpoints
├── frontend.ui/        # Alpine.js + Bulma dashboard
├── testing.qa/         # Comprehensive test suite
├── docs.prompts/       # AI prompt templates
└── config.schema/      # Configuration and metadata
```

### Technology Stack
- **Backend**: Python 3.11+ | FastAPI | Pydantic
- **Frontend**: HTML | Alpine.js | Bulma CSS
- **Testing**: pytest | pytest-cov
- **AI Tools**: Claude | MCP tools | Structured prompts
- **Data**: County Health Rankings 2025 CSV

---

## 🧪 Development Workflow

### Environment Setup (REQUIRED)
```bash
# 1. Create virtual environment (ALWAYS FIRST)
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Verify activation
which python  # Should show venv path

# 3. Install dependencies
pip install fastapi uvicorn pytest pytest-cov flake8 black mypy safety

# 4. Set up git
git init
echo "venv/\n__pycache__/\n*.pyc\n.env\n.DS_Store" > .gitignore
git add .gitignore
git commit -m "Initial setup: Add .gitignore and venv structure"
```

### AI Development Guidelines
- **Virtual Environment**: ALWAYS activate before pip install
- **Git Commits**: Frequent, meaningful commits with test coverage info
- **Testing**: Write tests before implementation (TDD)
- **Documentation**: Update docs with every functional change
- **Quality**: All code must pass linting and security scans

---

## 📊 Quality Standards

### Code Quality
- **Linting**: flake8, black, mypy must pass
- **Security**: safety check for vulnerabilities
- **Testing**: Minimum 90% coverage for ETL, 100% for API
- **Performance**: Sub-500ms API responses

### Accessibility
- **WCAG 2.1 AA**: Full compliance required
- **Screen Readers**: Test with actual assistive technology
- **Keyboard Navigation**: All functionality accessible via keyboard
- **Progressive Enhancement**: Works without JavaScript

### Documentation
- **Consistency**: All markdown files must be internally consistent
- **Completeness**: Every feature requires documentation
- **Versioning**: Track changes with meaningful version numbers
- **Cross-References**: Validate links between documents

---

## 🔍 AI Effectiveness Tracking

### Quantitative Metrics
Track these metrics for AI vs manual development comparison:
- Code generation time
- Test coverage achieved
- Bugs introduced
- Human edits required
- Documentation completeness
- Security compliance

### Qualitative Assessment
- Architecture clarity and maintainability
- Learning curve for new developers
- Problem-solving approach effectiveness
- Communication clarity in documentation

---

## 🚨 Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| Virtual env not activating | Use full path: `./venv/bin/activate` |
| MCP tools failing | Use manual fallbacks (see MCP instructions) |
| Tests failing | Fix tests before proceeding with features |
| Documentation inconsistency | Run validation script before commits |
| Performance regression | Profile and benchmark before optimization |

### Emergency Procedures
- **MCP Failure**: Continue with manual development mode
- **Test Failures**: Roll back to last working state
- **Security Issues**: Stop development, address immediately
- **Accessibility Violations**: Fix before feature completion

---

## 📈 Research Objectives

This project studies:
- **AI-Assisted Development**: Effectiveness of AI co-development patterns
- **Agentic Architecture**: Modular control plane effectiveness
- **Quality Maintenance**: Can AI maintain professional standards?
- **Documentation Discipline**: Impact on long-term maintainability

### Expected Outputs
- Quantitative comparison of AI vs manual development
- Best practices for AI-human collaboration
- Accessibility compliance patterns for AI-generated code
- Performance optimization strategies for AI workflows

---

## 🔄 Version History

- **v0.3** (January 2025): Enhanced documentation with implementation suggestions
- **v0.2** (June 2025): Post-feedback revision
- **v0.1** (Initial): Basic project structure and requirements

---

## 📞 Support

### For Implementation Issues
- Check troubleshooting section above
- Review relevant documentation files
- Ensure environment setup is complete
- Validate all tools are properly configured

### For AI Agent Issues
- Follow fallback procedures in MCP instructions
- Document all issues in CLAUDE.md
- Continue with manual development if needed
- Request human intervention when necessary

---

## 🎓 Learning Resources

### Understanding the Project
1. Read PRD.md for complete context
2. Review personas and user stories
3. Understand accessibility requirements
4. Study the MCP architecture pattern

### AI Development Best Practices
1. Study the agentic instructions carefully
2. Practice the logging template format
3. Understand git workflow requirements
4. Learn the prompt template structure

### Quality Assurance
1. Learn WCAG 2.1 AA requirements
2. Understand security scanning tools
3. Practice TDD methodology
4. Study performance optimization techniques

Remember: The goal is not just to build software, but to understand how AI can effectively participate in professional software development workflows while maintaining high standards for quality, accessibility, and maintainability. 