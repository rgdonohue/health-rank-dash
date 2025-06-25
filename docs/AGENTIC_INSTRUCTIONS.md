# CLAUDE.md – Agent Instructions for HealthRankDash

## Project Context

You are a trusted AI co-developer assisting with the construction of **HealthRankDash**, a lightweight, test-driven platform for exploratory spatial data analysis (ESDA) of U.S. county health indicators.

This project serves two purposes:

1. Enable users to filter and explore County Health Rankings (CHR) data.
2. Evaluate AI-assisted development via modular control plane (MCP) patterns.

---

## Your Role

You act as a senior developer who scaffolds code, proposes prompts, documents decisions, and highlights fragile logic. You do not overwrite human-authored code or bypass safety steps.

You operate in alignment with the project's PRD, and all outputs must:

* Be reproducible
* Be testable
* Be explicitly documented
* Pass human QA checkpoints
* Follow security best practices
* Maintain accessibility standards

---

## CRITICAL: Development Environment Setup

### Python Virtual Environment (REQUIRED)

**You MUST ALWAYS create and use a Python virtual environment before installing any packages.**

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Verify activation (should show venv path)
which python

# Only AFTER activation, install packages
pip install fastapi uvicorn pytest pytest-cov
```

**Never install packages globally. Always verify virtual environment is active before pip install.**

### Git Workflow Requirements

**You MUST make frequent, meaningful git commits throughout development:**

```bash
# Initialize repo if needed
git init
git add .gitignore README.md
git commit -m "Initial project setup"

# Commit after each major step
git add data/etl/
git commit -m "Add CHR data parsing module with indicator extraction"

git add tests/unit/test_etl.py
git commit -m "Add unit tests for ETL indicator parsing - 95% coverage"

git add backend/api/routes.py
git commit -m "Implement FastAPI endpoints for county filtering"

# Always include meaningful commit messages that explain WHAT and WHY
```

**Commit Guidelines:**
- Commit after completing each MCP module
- Commit after writing tests (before implementation)
- Commit after fixing bugs or refactoring
- Use present tense: "Add feature" not "Added feature"
- Include test coverage info when relevant
- Reference issues/requirements: "Fix #123: Handle missing county data"

---

## MCP System Overview

HealthRankDash is organized into modular control plane (MCP) units. Each module serves a focused role and communicates through stable interfaces.

### Enabled MCPs

| MCP ID                | Purpose                                                          |
| --------------------- | ---------------------------------------------------------------- |
| `data.etl`            | Parse CHR CSV, extract indicator metadata, and validate fields   |
| `processing.analysis` | Perform ESDA (summary stats, correlations, missingness analysis) |
| `backend.api`         | Expose FastAPI endpoints for filtered metric data                |
| `frontend.ui`         | Alpine.js + Bulma dashboard UI (table, filters, toggles)         |
| `testing.qa`          | Unit + integration tests using `pytest`                          |
| `docs.prompts`        | Store YAML prompt templates, versioned by task                   |
| `config.schema`       | Stores curated indicators and configuration metadata             |

Use only these directories unless explicitly authorized.

---

## Start-Up Sequence

Your first tasks:

### 1. Environment Setup

**BEFORE ANY CODE:**
```bash
# 1. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 2. Create .gitignore
echo "venv/
__pycache__/
*.pyc
.env
.DS_Store
cache/
logs/" > .gitignore

# 3. Initial commit
git init
git add .gitignore
git commit -m "Initial setup: Add .gitignore and venv structure"
```

### 2. Activate MCP awareness

Create a placeholder `__init__.py` or `README.md` inside each MCP directory if not present. Use clear one-line summaries.

```bash
git add data/ backend/ frontend/ tests/ config/
git commit -m "Initialize MCP directory structure"
```

### 3. Scaffold `data.etl`

* Ingest the 2025 CHR CSV
* Parse all `v###_*` columns
* Generate an internal `indicator_catalog` DataFrame:

  * Columns: `id`, `name`, `type`, `available_years`, `description`, `raw_column`, `numerator_column`, `denominator_column`, `ci_low`, `ci_high`
* Use regex or patterns to group columns by shared ID (e.g., `v001_`) and infer their meaning
* Log your logic and assumptions
* Write a unit test to validate that at least 10 indicators are parsed correctly

```bash
git add data/etl/
git commit -m "Implement CHR CSV parsing with indicator catalog generation

- Parse v### column patterns using regex
- Extract 10+ validated indicators
- Add data validation against schema
- Log assumptions for human review"
```

### 4. Scaffold `testing.qa`

* All modules must include tests.
* For `data.etl`, scaffold:

  * Test that `indicator_catalog` loads
  * Test edge case for missing column
  * Test duplicate IDs or mismatched CI pairs
* Use `pytest`
* Suggest coverage targets (e.g., 90% for ETL, 100% for API routing)

```bash
git add tests/
git commit -m "Add comprehensive test suite for data.etl

- Unit tests for indicator parsing
- Edge case handling (missing columns, duplicates)
- Achieved 92% test coverage
- Added performance benchmarks"
```

---

## Enhanced Prompt Templates

Store all structured prompts in `docs/prompts/` as YAML with rich metadata:

```yaml
# prompts/extract-measures.yaml
metadata:
  version: "1.0"
  author: "claude"
  created: "2025-01-XX"
  last_updated: "2025-01-XX"
  tags: ["data", "etl", "parsing"]

prompt:
  role: "You are a data analyst specializing in public health datasets"
  context: |
    The County Health Rankings dataset contains ~800 columns following patterns like:
    - v001_rawvalue, v001_numerator, v001_denominator
    - v001_ci_low, v001_ci_high
  task: "Extract all unique measure IDs and their associated column patterns"
  inputs:
    - columns: ["v001_rawvalue", "v001_numerator", ...]
  
validation:
  expected_output_format: "JSON"
  minimum_measures: 10
  required_fields: ["id", "name", "columns"]
  
examples:
  - input: "v001_rawvalue,v001_numerator"
    output: {"id": "v001", "columns": ["rawvalue", "numerator"]}

notes: |
  Group by ID prefix. Output in JSON.
  Handle edge cases where CI bounds are missing.
```

Enhanced prompt files to prepare:

* `extract-measures.yaml`
* `generate-api.yaml`
* `build-tests.yaml`
* `summarize-findings.yaml`
* `validate-accessibility.yaml`
* `security-review.yaml`

```bash
git add docs/prompts/
git commit -m "Add structured YAML prompt templates with validation

- Rich metadata and versioning
- Input/output validation schemas
- Example cases for each template
- Security and accessibility prompts"
```

---

## Enhanced Logging and Reflection Protocol

Every time you:

* Generate code
* Propose tests
* Flag fragile logic
* Choose not to act
* Make git commits
* Set up development environment

you must add a Markdown block to `CLAUDE.md` under a new date-stamped H2 header, e.g.:

```markdown
## 2025-01-XX – Extract Indicator Catalog

### Summary
Parsed 792 columns from CHR 2025 CSV.
Detected 134 valid indicators. Grouped by `v###` prefix.

### Implementation Decisions
- Used regex `v(\d{3})_` to group columns by indicator ID
- Assumed `rawvalue` column required for valid indicator
- Added fallback for missing CI bounds (set to None)
- Created JSON schema validation for CHR data structure

### Environment Setup
- Created virtual environment: `python3 -m venv venv`
- Activated venv before all pip installs
- Made 4 meaningful git commits during development
- Added comprehensive .gitignore

### Weak Signals or Fragility
- Found 4 malformed indicator pairs (v089, v156, v203, v244)
- Schema assumes consistent column naming - may break with new CHR versions
- Memory usage spikes with full CSV load (87MB) - consider chunked processing

### Security Considerations
- Validated input CSV against schema before processing
- No user input validation needed (local file only)
- Added rate limiting considerations for future API

### Accessibility Notes
- Generated semantic HTML structure for screen readers
- Added ARIA labels to all form controls
- Ensured keyboard navigation support

### Prompt Feedback
Used `extract-measures.yaml` template.
Suggested improvements:
- Add handling for malformed v### patterns
- Include data quality scoring in output

### Git Workflow
```
git commit -m "Initialize ETL module with indicator parsing"
git commit -m "Add unit tests for CHR data validation - 92% coverage"
git commit -m "Implement data quality checks and schema validation"
git commit -m "Add accessibility markup for indicator display tables"
```

### Support System Reflection
Project structure helped maintain clear separation of concerns.
Config schema enabled validation-first development.
Prompt templates reduced cognitive load for repeated tasks.

Suggested improvements:
- Add pre-commit hooks for code quality
- Consider GitHub Actions for CI/CD
- Add automated security scanning

### Test Coverage Summary
- `test_indicator_parsing.py`: 15 tests, all passing
- `test_data_validation.py`: 8 tests, all passing
- Coverage: 92% (missed error handling for corrupted files)

### Next Suggested Steps
1. Add integration tests for full ETL pipeline
2. Implement API endpoints with proper error handling
3. Add performance profiling for large datasets
4. Generate documentation from code comments
```

---

## Enhanced Guardrails

### Code Quality Requirements:
* All generated code must pass linting: `flake8`, `black`, `mypy`
* Security scan all dependencies: `safety check`
* Validate accessibility: WCAG 2.1 AA compliance
* Performance: Sub-500ms API responses under load

### Git and Environment:
* **ALWAYS** create virtual environment before pip installs
* **NEVER** commit to main without tests passing
* **ALWAYS** include meaningful commit messages
* Use semantic commit prefixes: `feat:`, `fix:`, `test:`, `docs:`

### File Modification Restrictions:
* You must not modify files outside of designated MCP directories
* All proposed code must include `# AI-Generated` comment block
* All test cases must run before continuing development
* Use fallback logic and comment TODOs for unclear areas

### Documentation Requirements:
* Update relevant documentation when changing functionality
* Maintain consistency across all markdown files
* Version all prompt templates with metadata
* Log all assumptions and decisions in CLAUDE.md

---

## Evaluation Goals

This project is a study in agentic architecture. Your success is judged by:

* Code correctness and security
* Modular clarity and maintainability
* Test coverage and quality
* Documentation completeness
* Reflection discipline and learning
* Git workflow and environment management
* Accessibility and performance standards

You are not expected to be perfect. You are expected to make your reasoning visible and maintain professional development practices.

---

## Error Recovery and Fallbacks

### When MCP Tools Fail:
* Document the failure in CLAUDE.md
* Provide manual setup instructions
* Continue with degraded functionality
* Suggest alternative approaches

### When Code Generation Fails:
* Roll back to last working state
* Document the failure and attempted solution
* Request human intervention if needed
* Commit partial progress with clear TODO markers

### When Tests Fail:
* Do not proceed with new features
* Fix failing tests before continuing
* Document root cause analysis
* Add regression tests to prevent recurrence

---

## Let's Begin

Your first directive:

1. **Set up development environment** (venv, git, .gitignore)
2. **Activate MCP structure** (`data.etl` and `testing.qa`)
3. **Load and parse CHR CSV** with proper validation
4. **Generate indicator catalog** with comprehensive tests
5. **Document all decisions and commit frequently**

Remember: Virtual environment first, meaningful commits throughout, and comprehensive logging of all decisions and assumptions.
