# Claude Startup Prompt (Post-Init)

Copy and paste this prompt to Claude after running `/init`:

---

## 🚀 HealthRankDash Development - Ready to Begin

You've just completed `/init` and should now have full context of the HealthRankDash project. This is a lightweight, test-driven platform for County Health Rankings data analysis that serves as both a practical tool and AI development research project.

## ⚡ ACCELERATED TIMELINE - Hour 1 Target: ETL + Validation Complete

### 🚨 CRITICAL FIRST STEPS (Do These IMMEDIATELY):

1. **Create Virtual Environment (REQUIRED)**:
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
which python  # Verify venv is active
```

2. **Set Up Git Repository**:
```bash
git init
echo "venv/
__pycache__/
*.pyc
.env
.DS_Store
cache/
logs/" > .gitignore
git add .gitignore docs/
git commit -m "Initial setup: Add documentation and venv structure

- Complete project documentation in place
- Virtual environment ready for dependencies
- Git workflow established for AI development"
```

3. **Install Core Dependencies**:
```bash
pip install fastapi uvicorn pytest pytest-cov pandas flake8 black mypy safety
git add requirements.txt  # if generated
git commit -m "Add core Python dependencies for ETL and API development"
```

## 🎯 YOUR IMMEDIATE MISSION (Next 60 Minutes):

### Phase 1: MCP Structure (5 minutes)
- Create the modular directory structure: `data/etl/`, `tests/unit/`, `config/`
- Add placeholder `__init__.py` files with clear purposes
- **Git commit**: "Initialize MCP directory structure for health data processing"

### Phase 2: CHR Data Analysis (15 minutes)
- Load and inspect `data/analytic_data2025_v2.csv`
- Use the **`docs/prompts/extract-measures.yaml`** template to parse indicator columns
- Generate a complete indicator catalog with validation
- **Git commit**: "Parse CHR data and generate indicator catalog with [X] measures"

### Phase 3: ETL Implementation (25 minutes)  
- Create `data/etl/parser.py` with robust CHR parsing
- Implement data validation against the schema we defined
- Add error handling for malformed data
- **Git commit**: "Implement CHR ETL pipeline with validation and error handling"

### Phase 4: Comprehensive Testing (15 minutes)
- Write unit tests for all ETL functions using pytest
- Achieve 90%+ test coverage
- Test edge cases (missing columns, malformed data)
- **Git commit**: "Add comprehensive test suite - [X]% coverage achieved"

## 📋 SUCCESS CRITERIA FOR HOUR 1:

- [ ] Virtual environment created and active
- [ ] Git repository with meaningful commits every 10-15 minutes
- [ ] CHR CSV successfully parsed with 10+ validated indicators
- [ ] Complete ETL pipeline with error handling
- [ ] 90%+ test coverage on all data processing code
- [ ] Detailed logging in CLAUDE.md following the enhanced template

## 🧭 KEY RESOURCES TO USE:

1. **Prompt Template**: `docs/prompts/extract-measures.yaml` for CHR parsing
2. **Logging Template**: Enhanced format in `docs/AGENTIC_LOGGING_GUIDELINES.md`
3. **Requirements**: All specs in `docs/PRD.md` sections 5-7
4. **Error Handling**: Patterns defined in PRD section 9

## ⚠️ CRITICAL REMINDERS:

- **NEVER** install packages without activating venv first
- **ALWAYS** make git commits with meaningful messages including test coverage
- **USE** the structured YAML prompt templates for consistency
- **LOG** everything in CLAUDE.md using the enhanced template format
- **VALIDATE** data quality and flag any issues for human review

## 🔧 IF MCP TOOLS FAIL:
Use the fallback procedures in `docs/MCP_ACTIVATION_INSTRUCTIONS.md` - continue with manual file operations and copy-paste commands. The project can succeed with or without MCP tools.

## 📊 TRACK THESE METRICS:
- Time to complete each phase
- Lines of code generated
- Test coverage percentage  
- Number of git commits made
- Issues/edge cases discovered

## 🎯 START NOW:

Begin with environment setup, then dive into the CHR data analysis. You have all the documentation, templates, and requirements needed. The goal is to have a working, tested ETL pipeline processing real County Health Rankings data within the next hour.

**Remember**: Quality over speed, but we're aiming for both. Use the enhanced logging template to document every decision and assumption you make.

Ready to build something amazing? Let's go! 🚀 