# 🛠 Agentic Backend Playbook

**For AI-Augmented Development of Data Pipelines, APIs, and Stateful Systems**

---

## 🔍 Why This Playbook Exists

Drawing from the successes and failures of *Tilecraft*, *No-SQL Atlas*, and the recent *HealthRankDash* documentation experiments, this playbook offers a refined methodology for backend-heavy agentic workflows. It integrates:

* Architectural patterns from production case studies
* Behavioral insights from AI system testing
* Lessons on documentation overload
* Measurement frameworks for empirical benchmarking

---

## 🧱 Foundational Principles

### 1. **AI ≠ Engineer. It’s a Junior Teammate.**

Give it clear boundaries and tools, not vague autonomy.

### 2. **Backend Requires Explicit Staging**

AI cannot reason well across multi-layer data flows unless scaffolded in stages.

### 3. **Documentation Is a Cost. Minimize It.**

Avoid meta-work until functionality exists.

### 4. **Test First or Fail Later**

AI won't write tests unless required. Bake tests into every step.

---

## 📦 Architecture Blueprint

### 🔁 Dual-Loop Architecture

* **Human Loop**: Plan → Edit → Review → Commit
* **AI Loop**: Prompt → Generate → Evaluate → Retry
* **Shared State**: YAML Configs, Prompt Templates, Structured Logs

### 📁 Directory Layout

```
/backend
  ├── schema/             # Pydantic schemas
  ├── processors/         # Data transformation logic
  ├── integration/        # API, CLI, routing
  ├── test/               # Mirror structure of implementation
  ├── config/             # Staged YAML with diff-check tools
  └── logs/               # AI prompt/response logs
```

---

## 🔃 Agentic Backend Workflow

### Stage 1: Schema & Validation

* AI Task: Generate Pydantic model from data spec
* Prompt Template:

```yaml
role: "You are a Python backend engineer."
task: "Define a schema for county health indicators."
inputs:
  - field: county_name
  - field: fips_code
  - field: obesity_rate
notes: "Use strict validation for fips_code format."
```

* Test Requirement: Valid + malformed input tests

### Stage 2: Processor Layer

* AI Task: Build function to normalize fields
* Human Action: Seed test cases first
* Logging: Include input, output, error trace

### Stage 3: Integration Layer

* AI Task: Wire schema + processor into FastAPI
* Human Action: Inject health checks, dependency injection pattern
* Prompt Addendum: "Use dependency overrides for testability"

### Stage 4: Test Harness

* Mirror file structure in `/test/`
* Use AI to scaffold, human to fill edge cases
* Example prompt: "Write pytest for processor\_x using mock input"

### Stage 5: Observability & Fallbacks

* Only introduced **after** functional milestone reached
* Add structured logging, fallback defaults, API stubs

---

## 📘 Documentation Strategy

### 🎯 Goal: Optimize Guidance-to-Cognition Ratio

### 🔹 Minimal Viable Documentation (MVD)

* `CORE_REQUIREMENTS.md` — essential user stories + constraints (≤2KB)
* `QUICK_START.md` — setup + first agentic task (≤1KB)
* `API_SPEC.md` — schemas + endpoints (≤1KB)

### 🔹 Just-In-Time Documentation

* Inject instruction into prompt templates rather than linking to `INSTRUCTIONS.md`
* Reveal logging protocols *only when logging is implemented*

### 🔹 Avoid:

* Frontloaded reflection protocols
* Unused meta-guidelines
* Process compliance before functional output

---

## 🧪 Metrics + Measurement

### Quantitative Tracking (from MEASUREMENT\_METHODOLOGY.md)

#### Time-Based Metrics

* **Setup Time** → Git timestamp analysis
* **Time-to-First-Test-Pass**
* **Debug Cycle Duration** → From failure to green test

#### Output Quality

* **Test Coverage** → `pytest --cov`
* **Code Complexity** → `radon`
* **Security** → `safety check`
* **Performance** → `curl`, `ab`, `lighthouse`

#### AI Cognitive Load

* **Questions Asked / Feature**
* **Context Tokens Used**
* **Prompt Length / Effectiveness Ratio**

#### Process Compliance

* **Commit Activity**
* **Semantic Git Messages**
* **Churn Metrics** → `git diff --stat`

### A/B Testing Protocol

* **Test A**: MVD + JIT documentation
* **Test B**: Full instruction set
* Compare on time, coverage, output completeness, and cognitive load

---

## ✅ Final Checklist per Backend Component

| Stage       | Artifact          | AI Prompt Required? | Test Coverage? | Human Review? |
| ----------- | ----------------- | ------------------- | -------------- | ------------- |
| Schema      | Pydantic model    | ✅                   | ✅              | ✅             |
| Processor   | Field transformer | ✅                   | ✅              | ✅             |
| Integration | API / CLI         | ✅                   | ✅              | ✅             |
| Test Suite  | Pytest module     | ✅ scaffold only     | ✅ manual cases | ✅             |
| Docs        | README, MVD only  | ✅ (auto-summary)    | n/a            | ✅             |

---

## 🚫 Common Pitfalls

* “Build the pipeline” single-shot prompts → hallucinated glue code
* Test-after-the-fact → flaky or missing coverage
* Overloaded context windows → reduced AI precision
* Documentation-as-obstacle → time sink with no velocity gain
* AI writing logging/config before logic → wasted effort

---

## 🧭 Evolution Strategy

* Use versioned playbook per project phase
* Embed quality gates via CI for test, coverage, lint, and semantic commit enforcement
* Run weekly dashboard reporting from `metrics_*.json`
* Revisit documentation-to-performance ratio quarterly
* Expand prompt templates only when reuse proves ROI

---

## Final Word

Backend-heavy agentic development **can** work—but only with:

* Narrowly scoped AI tasks
* Mandatory test scaffolding
* Minimal documentation volume
* Clear observability
* Human judgment at every integration point

Use this playbook not as dogma—but as insulation from chaos.
