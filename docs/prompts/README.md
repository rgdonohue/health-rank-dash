# AI Prompt Templates Directory

## Overview

This directory contains structured YAML prompt templates for the HealthRankDash project. These templates enable consistent, versioned, and validated AI interactions throughout the development process.

---

## 📁 Template Structure

All prompt templates follow this enhanced YAML structure:

```yaml
metadata:
  version: "1.0"
  author: "claude|human"
  created: "YYYY-MM-DD"
  last_updated: "YYYY-MM-DD"
  tags: ["category", "task-type", "module"]
  
prompt:
  role: "You are a [specific expert role]"
  context: |
    Multi-line context about the specific domain,
    data structures, and constraints.
  task: "Clear, specific task description"
  inputs:
    - input_name: "Description of expected input"
  
validation:
  expected_output_format: "JSON|Markdown|Code"
  minimum_requirements: ["list", "of", "requirements"]
  required_fields: ["field1", "field2"]
  
examples:
  - input: "Example input data"
    output: "Expected output format"
    
notes: |
  Additional guidance, edge cases, and
  special considerations.
```

---

## 🚀 Available Templates

### Data Processing
- **[extract-measures.yaml](./extract-measures.yaml)** - Parse CHR indicator columns
- **[validate-data.yaml](./validate-data.yaml)** - Data quality checks and validation
- **[schema-generation.yaml](./schema-generation.yaml)** - Generate JSON schemas

### Testing & Quality
- **[build-tests.yaml](./build-tests.yaml)** - Generate comprehensive test suites
- **[security-review.yaml](./security-review.yaml)** - Security vulnerability assessment
- **[performance-analysis.yaml](./performance-analysis.yaml)** - Performance optimization

### Frontend & Accessibility
- **[validate-accessibility.yaml](./validate-accessibility.yaml)** - WCAG 2.1 AA compliance
- **[generate-ui.yaml](./generate-ui.yaml)** - Accessible UI component generation
- **[responsive-design.yaml](./responsive-design.yaml)** - Mobile-responsive implementation

### Analysis & Insights
- **[summarize-findings.yaml](./summarize-findings.yaml)** - Statistical analysis summaries
- **[correlation-analysis.yaml](./correlation-analysis.yaml)** - Explore data relationships
- **[data-insights.yaml](./data-insights.yaml)** - Generate meaningful insights

---

## 🧪 Usage Guidelines

### Template Selection
1. Choose the template that best matches your current task
2. Review the metadata to ensure version compatibility
3. Check examples to understand expected inputs/outputs
4. Customize the context section for your specific use case

### Version Management
- Always update `last_updated` when modifying templates
- Increment version numbers for significant changes
- Tag templates with relevant categories for easy discovery
- Document changes in git commits

### Validation Requirements
- All outputs must meet the specified format requirements
- Check minimum requirements before considering task complete
- Validate required fields are present in outputs
- Test examples to ensure template effectiveness

---

## 📊 Template Effectiveness Tracking

Track these metrics for each template usage:

```yaml
usage_metrics:
  template_name: "extract-measures.yaml"
  version_used: "1.0"
  task_completion_time: "15 minutes"
  output_quality_score: 4.2  # 1-5 scale
  human_edits_required: 2
  template_effectiveness: "high"  # low|medium|high
  suggested_improvements: 
    - "Add handling for malformed v### patterns"
    - "Include data quality scoring in output"
```

---

## 🔧 Template Development

### Creating New Templates

1. **Identify the need**: What specific, repeatable task needs a template?
2. **Research requirements**: What are the inputs, constraints, and expected outputs?
3. **Draft structure**: Use the standard YAML format above
4. **Test with examples**: Validate the template works with real data
5. **Document and version**: Add to this directory with proper metadata

### Template Improvement Process

1. **Collect usage feedback**: Track effectiveness metrics
2. **Identify patterns**: What modifications are commonly needed?
3. **Update template**: Improve based on common issues
4. **Version increment**: Update version and last_updated fields
5. **Test changes**: Validate improvements with existing use cases

---

## 🚨 Quality Standards

### Required Elements
- [ ] Complete metadata section
- [ ] Clear role and context definition
- [ ] Specific, actionable task description
- [ ] Input/output validation criteria
- [ ] At least one working example
- [ ] Edge case considerations in notes

### Best Practices
- Use specific domain language (e.g., "public health analyst" not "developer")
- Include relevant constraints and limitations
- Provide realistic examples with actual data patterns
- Document assumptions and edge cases
- Keep templates focused on single, specific tasks

---

## 🔄 Template Lifecycle

1. **Draft** - Initial template creation and testing
2. **Active** - In regular use with effectiveness tracking
3. **Deprecated** - Superseded by newer versions
4. **Archived** - No longer relevant but kept for reference

### Maintenance Schedule
- **Weekly**: Review usage metrics and feedback
- **Monthly**: Update templates based on common modifications
- **Quarterly**: Major version updates and lifecycle management
- **Annually**: Complete template library review and cleanup

---

## 📈 Research Value

These templates contribute to research objectives by:

- **Standardizing AI interactions** for consistent quality measurement
- **Tracking effectiveness** across different types of development tasks
- **Enabling reproducibility** of AI-assisted development workflows
- **Documenting best practices** for AI-human collaboration

---

## 🎯 Success Metrics

Evaluate template effectiveness using:

- **Task completion time** compared to manual approaches
- **Output quality scores** from human reviewers
- **Reduction in human edits** required after AI generation
- **Consistency of results** across multiple uses
- **Learning curve** for new users adopting templates

---

Remember: Good templates reduce cognitive load, increase consistency, and enable effective measurement of AI capabilities. They should be living documents that improve based on usage experience and changing project needs. 