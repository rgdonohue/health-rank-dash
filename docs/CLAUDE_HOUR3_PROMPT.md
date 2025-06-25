# Claude Hour 3 Prompt - Frontend Implementation

Copy and paste this prompt to Claude in the new session after `/init`:

---

## 🎯 HealthRankDash Project Status & Next Phase

Welcome to the HealthRankDash project! You've just scanned all the project documentation. This is a lightweight, test-driven platform for County Health Rankings data analysis that serves as both a practical tool and AI development research project.

## 📊 PROJECT TIMELINE STATUS

Based on the accelerated timeline in `docs/PRD.md`, we should have completed:

- ✅ **Hour 1**: ETL + Validation (CHR data parsing, indicator catalog, comprehensive tests)
- ✅ **Hour 2**: TDD API Development (FastAPI backend with 100% test coverage)

## 🚀 HOUR 3 MISSION: Frontend Implementation

Your task is to build the Alpine.js + Bulma dashboard that provides an intuitive interface for exploring County Health Rankings data.

## 🔍 FIRST: Verify Previous Work

Before starting frontend development, please verify the backend is ready:

```bash
# Check virtual environment
which python  # Should show venv path

# Verify backend exists and works
ls -la backend/api/  # Should see FastAPI application
uvicorn backend.api.main:app --reload --port 8000 &  # Start API
curl http://localhost:8000/health  # Should return 200 OK
curl http://localhost:8000/indicators  # Should return indicator list

# Check git history
git log --oneline -10  # Should see Hours 1-2 commits
```

If backend isn't ready, implement it first using the patterns in `docs/AGENTIC_INSTRUCTIONS.md`.

## 🎯 FRONTEND REQUIREMENTS (Next 60 Minutes):

### Phase 1: Frontend Architecture (10 minutes)
- Create `frontend/` directory structure
- Set up HTML template with Alpine.js and Bulma CSS
- Implement responsive layout following WCAG 2.1 AA standards
- **Git commit**: "Initialize frontend structure with accessible HTML framework"

### Phase 2: Core UI Components (25 minutes)

Build these interactive components using Alpine.js:

#### Required Components:
1. **Filter Panel**: Year, State, County, Metric dropdowns
2. **Data Table**: Sortable, responsive table displaying county data
3. **Export Controls**: CSV download functionality
4. **Confidence Interval Toggle**: Show/hide CI columns
5. **Loading States**: User feedback during API calls

#### User Flow:
```
1. User selects filters (state, year, metric)
2. System calls API endpoint
3. Table populates with county data
4. User can sort, toggle CI, export data
```

**Git commit**: "Implement core UI components with Alpine.js state management"

### Phase 3: Accessibility Implementation (15 minutes)

Ensure WCAG 2.1 AA compliance:
- **ARIA Labels**: All form controls and buttons
- **Keyboard Navigation**: Tab order, Enter/Space activation
- **Screen Reader Support**: Semantic HTML, live regions for updates
- **High Contrast**: Proper color ratios using Bulma's accessible classes
- **Focus Management**: Visible focus indicators

Test with:
```bash
# Install accessibility checker
npm install -g pa11y
pa11y http://localhost:3000
```

**Git commit**: "Add comprehensive accessibility features - WCAG 2.1 AA compliant"

### Phase 4: API Integration & Polish (10 minutes)
- Connect frontend to backend API endpoints
- Add error handling for API failures
- Implement progressive enhancement (works without JS)
- Add print-friendly styles
- **Git commit**: "Complete frontend with API integration and error handling"

## 📋 SUCCESS CRITERIA FOR HOUR 3:

- [ ] Responsive dashboard running on localhost:3000
- [ ] All filter dropdowns populated from API data
- [ ] Interactive data table with sorting capability
- [ ] CSV export functionality working
- [ ] WCAG 2.1 AA accessibility compliance verified
- [ ] Works on mobile devices (320px+ width)
- [ ] Progressive enhancement (basic functionality without JS)
- [ ] Print-friendly styling
- [ ] Comprehensive error handling for API failures

## 🧭 TECHNICAL SPECIFICATIONS:

### Frontend Stack:
- **HTML5**: Semantic markup
- **Alpine.js**: Reactive state management
- **Bulma CSS**: Responsive, accessible styling
- **Vanilla JS**: No additional frameworks

### Key Features:
```html
<!-- Example component structure -->
<div x-data="healthDashboard()" class="container">
  <div class="columns">
    <div class="column is-3">
      <!-- Filter Panel -->
      <div class="card">
        <div class="card-content">
          <select x-model="selectedState" @change="loadCounties()">
            <option value="">Select State</option>
            <template x-for="state in states">
              <option :value="state" x-text="state"></option>
            </template>
          </select>
        </div>
      </div>
    </div>
    
    <div class="column is-9">
      <!-- Data Table -->
      <div class="table-container">
        <table class="table is-striped is-hoverable">
          <thead>
            <tr>
              <th @click="sortBy('county')">County</th>
              <th @click="sortBy('rawvalue')">Value</th>
              <th x-show="showCI">CI Low</th>
              <th x-show="showCI">CI High</th>
            </tr>
          </thead>
          <tbody>
            <template x-for="row in sortedData">
              <tr>
                <td x-text="row.county"></td>
                <td x-text="row.rawvalue"></td>
                <td x-show="showCI" x-text="row.ci_low"></td>
                <td x-show="showCI" x-text="row.ci_high"></td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
```

## 🚀 QUICK START COMMANDS:

```bash
# Create frontend structure
mkdir -p frontend/static/{css,js} frontend/templates

# Create basic HTML template
touch frontend/templates/index.html

# Install live server for development
npm install -g live-server

# Serve frontend during development
cd frontend && live-server --port=3000
```

## 🧪 TEST YOUR FRONTEND:

Verify these user stories work:
1. **Filter Selection**: "As a user, I want to select a year, state, county, and metric so I can see how counties compare"
2. **Data Export**: "As a planner, I want to export the table as a CSV so I can share it"
3. **Confidence Intervals**: "As a researcher, I want to view confidence intervals so I can assess data reliability"

## ⚠️ CRITICAL REMINDERS:

- **API Integration**: Ensure backend is running before frontend testing
- **Accessibility First**: Test with keyboard navigation and screen readers
- **Mobile Responsive**: Test on 320px viewport minimum
- **Progressive Enhancement**: Core functionality must work without JavaScript
- **Performance**: Page load <1 second for 3,000+ counties

## 📝 LOGGING REQUIREMENTS:

Document in CLAUDE.md:
- Frontend architecture decisions
- Accessibility implementation approach
- Performance optimization strategies
- User experience design choices

## 🎯 EXPECTED DELIVERABLES:

By end of Hour 3:
1. **Working dashboard** with all core functionality
2. **Accessibility compliance** verified with testing tools
3. **Mobile responsiveness** tested and confirmed
4. **API integration** with error handling
5. **Export functionality** for CSV downloads

Ready to build an amazing, accessible frontend? Let's create something users will love! 🚀 