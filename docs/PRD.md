# Product Requirements Document (PRD)

## 1. Purpose

**Why are we building this?**

County Health Rankings (CHR) data is rich and underutilized. However, most existing tools for exploring this data (e.g., Tableau Public, CDC portals) are either gated, complex, or not tailored to offline, lightweight, and transparent exploration workflows.

**HealthRankDash** is a lightweight, test-driven spatial data platform enabling exploratory spatial data analysis (ESDA) on key health indicators. It is intended to serve both as a practical tool for analysts and as a research probe into agentic software development using AI co-agents.

**Strategic Priorities:**

* Build modular infrastructure for agentic ESDA pipelines.
* Validate AI-assisted backend-first development workflows.
* Empower data-informed exploration of social determinants of health.

## 2. Scope

### In-Scope (MVP):

* Parse and curate the 2025 CHR CSV
* Lightweight FastAPI backend with endpoints for state/year/metric filtering
* Alpine.js + Bulma dashboard UI to support table and metric filtering
* Backend-first TDD (pytest)
* AI-agent (Claude) assists with code scaffolding, test generation, and documentation, reflecting on logic and fragility

### Stretch Goals:

* Add CSV export of query results
* Add exploratory correlation matrix for 5–10 selected indicators
* Add confidence interval toggles per metric

### Explicitly Out:

* Persistent backend storage
* Interactive maps (until v0.2)
* Real-time dashboards or uploads

### Dependencies:

* County Health Rankings 2025 CSV
* Python + FastAPI + Pydantic
* Alpine.js + Bulma CSS

## 3. Personas / Target Users

### Persona 1: **Anna Ruiz** – Environmental Public Health Consultant

* Moderate technical skills
* Needs quick access to metrics for grant writing
* Seeks confidence in data reliability

### Persona 2: **Jordan Kim** – GIScience Student

* High technical fluency
* Exploring relationships and spatial patterns between indicators
* Wants reproducible workflows

### Persona 3: **Reggie Thorne** – County Planner

* Low technical fluency
* Interested in reliable, printable summary tables
* Needs results in under 3 clicks

**Accessibility Notes:**

* No login, minimal UI depth
* Screen-reader friendly table layout
* ARIA labels for all interactive elements
* Keyboard navigation support
* High contrast mode support
* Alternative "simplified view" for low-tech users

## 4. User Stories (Prioritized)

* **Must**: As a user, I want to select a year, state, county, and metric so I can see how counties compare.
* **Must**: As a planner, I want to export the table as a CSV so I can share it.
* **Should**: As a researcher, I want to view confidence intervals so I can assess data reliability.
* **Should**: As an analyst, I want to export data with metadata so I can understand collection methods.
* **Could**: As a student, I want to explore simple correlations between metrics so I can build hypotheses.
* **Could**: As a user, I want multiple export formats (JSON, Excel) so I can work with my preferred tools.
* **Won't**: This tool won't offer maps or uploads in v0.1

## 5. Functional Requirements

### Inputs:

* 2025 CHR CSV
* Frontend: dropdown filters for year, state, and curated metric list

### Processing:

* Parse `v###`-style columns into metadata
* Generate lookup table of validated indicators
* Slice/filter based on inputs
* Compute Pearson correlation matrix across selected indicators (stretch goal)

### Outputs:

* JSON API for data slices
* HTML table with toggleable CI columns
* CSV download endpoint (optional)
* Metadata export with data collection information
* Filtered export options (selected counties/metrics only)

## 6. Non-Functional Requirements

* Sub-500ms API latency on local
* Minimal RAM usage (<200MB preferred after profiling)
* Works offline (local-first)
* Open-source license (MIT or CC BY-SA)
* WCAG 2.1 AA accessibility compliance
* Mobile-responsive design (down to 320px width)

## 7. Data Requirements

* **Source**: County Health Rankings (2025)
* **Format**: Wide CSV with \~800 columns
* **Content**: Geographic descriptors, `v###`-style indicators (raw, numerator, denominator, CI bounds)
* **Frequency**: Annual
* **Validation**: JSON schema for expected CHR data structure
* **Error Handling**: Graceful degradation for malformed or missing data

## 8. Configuration Management

### Application Configuration (`config/settings.yaml`):

```yaml
app:
  name: "HealthRankDash"
  version: "0.1.0"
  environment: "development"

data:
  source_file: "data/analytic_data2025_v2.csv"
  cache_dir: "cache/"
  validation_schema: "config/chr_schema.json"

api:
  host: "localhost"
  port: 8000
  max_counties_per_request: 3142
  timeout_seconds: 30

logging:
  level: "INFO"
  format: "structured"
  file: "logs/healthrank.log"

ai:
  claude_model: "claude-3-sonnet"
  max_context_length: 200000
  safety_checks: true
```

## 9. Error Handling Strategy

### Data Validation Errors:
* Malformed CHR data → Load with warnings, flag problematic columns
* Missing required columns → Graceful degradation with user notification
* Invalid county codes → Skip invalid rows, log for review

### API Errors:
* Request timeout → Return partial results with continuation token
* Rate limiting → Queue requests with user feedback
* Invalid parameters → Return 400 with specific validation messages

### AI/MCP Tool Failures:
* Claude unavailable → Fall back to manual development mode
* MCP tools fail → Provide manual setup instructions
* Generated code fails validation → Require human review before integration

## 10. Data Validation Schema

### CHR Data Structure (`config/chr_schema.json`):

```json
{
  "required_columns": [
    "fipscode", "state", "county", "year"
  ],
  "indicator_pattern": "^v\\d{3}_",
  "expected_suffixes": [
    "_rawvalue", "_numerator", "_denominator", 
    "_ci_low", "_ci_high"
  ],
  "minimum_indicators": 10,
  "maximum_missing_rate": 0.8
}
```

## 11. Design + UX

### Key Interactions:

* Select year > Select state > Select metric → View table
* (Stretch) Toggle correlation explorer
* (Stretch) Click column header to sort counties

### UI Components:

* Filters: year, state, metric
* Output table: counties + values + CI toggles
* Export button (optional)
* Accessibility: Skip links, ARIA labels, keyboard navigation

### Design Constraints:

* Bulma + Alpine.js only (no complex JS state)
* Minimalist, responsive, printable
* WCAG 2.1 AA compliant
* Works without JavaScript (progressive enhancement)

## 12. Architecture + Technical Stack

### Frontend:

* HTML + Alpine.js
* Bulma CSS
* Progressive Web App features

### Backend:

* Python 3.11
* FastAPI + Pydantic
* Pytest + Coverage
* Virtual environment management

### Hosting:

* Local + Git-based; no Docker or DB
* CI/CD with GitHub Actions

### Testing Strategy:

```
tests/
├── unit/           # Individual function tests
├── integration/    # API endpoint tests  
├── data/          # CHR data validation tests
├── ai/            # Claude-generated code validation
├── performance/   # Sub-500ms response time tests
└── accessibility/ # WCAG compliance tests
```

## 13. Milestones & Timeline

| Phase                   | Target Date | Owner          |
| ----------------------- | ----------- | -------------- |
| Environment Setup       | Minute 1       | Human + Claude |
| ETL + Validation        | Hour 1      | Human + Claude |
| TDD API Development     | Hour 2      | Human          |
| Frontend Implementation | Hour 3      | Human          |
| Correlation + Export    | Hour 4      | Human + Claude |
| Accessibility QA        | Hour 5      | Human          |

## 14. Metrics & Success Criteria

### Functional Metrics:
* 100% test coverage on backend routes and parsers
* Validated indicator table generated with >= 10 usable metrics
* Frontend loads and filters in <1s for 3,000+ counties
* 2+ documented statistical findings (e.g., correlations > |0.5|)

### Quality Metrics:
* WCAG 2.1 AA accessibility compliance
* Lighthouse performance score > 90
* Zero critical security vulnerabilities
* <5% error rate in AI-generated code

### AI Effectiveness Metrics:
* Code generation time vs manual development
* Test coverage achieved by AI vs human
* Number of human edits required per AI contribution
* Bug introduction rate (AI vs human-written code)

## 15. Risks & Mitigations

| Risk                              | Mitigation                                           |
| --------------------------------- | ---------------------------------------------------- |
| Inconsistent CHR schema           | Parse columns dynamically, validate in `data.etl`    |
| AI hallucination or fragile logic | Claude must log decisions and test coverage enforced |
| Over-scoped frontend complexity   | Freeze scope to static HTML + Alpine.js              |
| Accessibility compliance failure  | Early testing with screen readers and WAVE tool     |
| Performance degradation           | Continuous performance monitoring and profiling     |
| Security vulnerabilities         | Regular dependency updates and security scanning    |

## 16. Open Questions

* How do we define and validate ESDA insights?
* Should we allow toggling normalized vs raw metrics?
* Should we prototype correlation UX before building full UI?
* What baseline metrics should we establish for AI vs human development comparison?

## 17. AI / Agentic Considerations

### Enhanced Prompt Templates:

* `extract-measures.yaml` – identify and validate metric columns
* `build-tests.yaml` – suggest test coverage for API + ETL
* `summarize-findings.yaml` – propose correlation descriptions
* `validate-accessibility.yaml` – check WCAG compliance
* `optimize-performance.yaml` – suggest performance improvements

### Claude Roles:

* Reflect on decisions and suggest fragility in `CLAUDE.md`
* Scaffold test cases before implementation
* Highlight ambiguous field mappings or schema assumptions
* Generate accessibility-compliant UI components
* Validate code against security best practices

### Enhanced Safeguards:

* Claude cannot write to production files directly
* All agentic steps must emit commentary and fallback code
* AI-generated code must pass linting (flake8, black, mypy)
* Automated review of AI test cases for completeness
* Security scan of all AI-generated dependencies

### AI Effectiveness Measurement:

```python
# ai_metrics.py
metrics = {
    "code_generation_time_seconds": float,
    "test_coverage_percentage": float, 
    "human_edits_required": int,
    "bugs_introduced_count": int,
    "documentation_completeness_score": float,
    "security_vulnerabilities_introduced": int,
    "accessibility_compliance_score": float
}
```

## 18. Versioning

* PRD v0.3 — June 2025 (Enhanced with implementation suggestions)
* CLAUDE.md versioned in Git with each agentic decision
* All prompt templates versioned with metadata

## 19. Post-Launch Plan

* Archive curated indicators + filtered slices
* Publish reproducible correlation insights
* Offer map layer as upgrade path (v0.2)
* Document AI-agent role performance (case study follow-up)
* Publish accessibility and performance benchmarks
* Open source the AI-assisted development methodology

## 20. Continuous Integration

### GitHub Actions Workflow:

* Automated testing on push/PR
* Code quality checks (linting, type checking)
* Security vulnerability scanning
* Performance regression testing
* Accessibility compliance validation
* AI-generated code review automation

### Documentation Validation:

* Check for broken internal links
* Validate YAML prompt templates
* Ensure documentation consistency across files
* Generate coverage reports for documentation completeness
