/**
 * HealthRankDash Alpine.js Application
 * 
 * Main application logic for the County Health Rankings dashboard.
 * Handles API integration, data filtering, sorting, and CSV export.
 */

// API Configuration
const API_BASE_URL = 'http://localhost:8000/api/v1';

// Alpine.js Main Application Component
function healthDashboard() {
    return {
        // State Management
        isLoading: false,
        error: null,
        
        // Filter State
        selectedYear: '2025',
        selectedState: '',
        selectedCounty: '',
        selectedIndicator: '',
        
        // Data Arrays
        availableYears: ['2025', '2024', '2023'],
        states: [],
        counties: [],
        indicators: [],
        tableData: [],
        
        // Display Options
        showConfidenceIntervals: false,
        
        // Sorting State
        sortField: 'county',
        sortDirection: 'asc',
        
        /**
         * Initialize the application
         */
        async init() {
            console.log('🚀 Initializing HealthRankDash...');
            await this.loadInitialData();
        },
        
        /**
         * Load initial data (states and indicators)
         */
        async loadInitialData() {
            this.isLoading = true;
            this.error = null;
            
            try {
                // Load states and indicators in parallel
                const [statesResponse, indicatorsResponse] = await Promise.all([
                    this.fetchWithErrorHandling('/states'),
                    this.fetchWithErrorHandling('/indicators')
                ]);
                
                this.states = statesResponse || [];
                this.indicators = indicatorsResponse || [];
                
                console.log(`✅ Loaded ${this.states.length} states and ${this.indicators.length} indicators`);
                this.announceToScreenReader(`Loaded ${this.states.length} states and ${this.indicators.length} health indicators`);
                
            } catch (error) {
                this.handleError('Failed to load initial data', error);
            } finally {
                this.isLoading = false;
            }
        },
        
        /**
         * Load counties for selected state
         */
        async loadCounties() {
            if (!this.selectedState) {
                this.counties = [];
                this.selectedCounty = '';
                return;
            }
            
            this.isLoading = true;
            
            try {
                const counties = await this.fetchWithErrorHandling(`/counties/${encodeURIComponent(this.selectedState)}`);
                this.counties = counties || [];
                this.selectedCounty = ''; // Reset county selection
                
                console.log(`✅ Loaded ${this.counties.length} counties for ${this.selectedState}`);
                this.announceToScreenReader(`Loaded ${this.counties.length} counties for ${this.selectedState}`);
                
            } catch (error) {
                this.handleError(`Failed to load counties for ${this.selectedState}`, error);
                this.counties = [];
            } finally {
                this.isLoading = false;
            }
        },
        
        /**
         * Load health data based on current filters
         */
        async loadData() {
            if (!this.canLoadData) {
                this.announceToScreenReader('Please select required filters before loading data');
                return;
            }
            
            this.isLoading = true;
            this.error = null;
            
            try {
                // Build query parameters
                const params = new URLSearchParams();
                
                if (this.selectedYear) params.append('year', this.selectedYear);
                if (this.selectedState) params.append('state', this.selectedState);
                if (this.selectedCounty) params.append('county', this.selectedCounty);
                if (this.selectedIndicator) params.append('indicator', this.selectedIndicator);
                
                const data = await this.fetchWithErrorHandling(`/data?${params.toString()}`);
                this.tableData = data || [];
                
                // Reset sorting when new data loads
                this.sortField = 'county';
                this.sortDirection = 'asc';
                
                const resultCount = this.tableData.length;
                const message = `Loaded ${resultCount} ${resultCount === 1 ? 'county' : 'counties'}`;
                console.log(`✅ ${message}`);
                this.announceToScreenReader(message);
                
            } catch (error) {
                this.handleError('Failed to load health data', error);
                this.tableData = [];
            } finally {
                this.isLoading = false;
            }
        },
        
        /**
         * Check if data can be loaded (minimum required filters)
         */
        get canLoadData() {
            return this.selectedState && this.selectedIndicator;
        },
        
        /**
         * Handle filter changes
         */
        onFilterChange() {
            // Clear existing data when filters change
            if (this.tableData.length > 0) {
                this.tableData = [];
            }
        },
        
        /**
         * Clear all filters and data
         */
        clearFilters() {
            this.selectedYear = '2025';
            this.selectedState = '';
            this.selectedCounty = '';
            this.selectedIndicator = '';
            this.counties = [];
            this.tableData = [];
            this.error = null;
            
            this.announceToScreenReader('All filters cleared');
        },
        
        /**
         * Sort data by specified field
         */
        sortBy(field) {
            if (this.sortField === field) {
                // Toggle direction if same field
                this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
            } else {
                // New field, default to ascending
                this.sortField = field;
                this.sortDirection = 'asc';
            }
            
            this.announceToScreenReader(`Sorted by ${field} ${this.sortDirection}ending`);
        },
        
        /**
         * Get sorted data for display
         */
        get sortedData() {
            if (!this.tableData.length) return [];
            
            return [...this.tableData].sort((a, b) => {
                let aVal = a[this.sortField];
                let bVal = b[this.sortField];
                
                // Handle null/undefined values
                if (aVal == null && bVal == null) return 0;
                if (aVal == null) return 1;
                if (bVal == null) return -1;
                
                // Convert to appropriate types for comparison
                if (typeof aVal === 'string') {
                    aVal = aVal.toLowerCase();
                    bVal = bVal.toLowerCase();
                } else if (typeof aVal === 'number') {
                    // Numbers are already comparable
                } else {
                    // Convert to string for comparison
                    aVal = String(aVal).toLowerCase();
                    bVal = String(bVal).toLowerCase();
                }
                
                let result;
                if (aVal < bVal) result = -1;
                else if (aVal > bVal) result = 1;
                else result = 0;
                
                return this.sortDirection === 'desc' ? -result : result;
            });
        },
        
        /**
         * Get sort direction for ARIA
         */
        getSortDirection(field) {
            if (this.sortField !== field) return 'none';
            return this.sortDirection === 'asc' ? 'ascending' : 'descending';
        },
        
        /**
         * Get sort icon class
         */
        getSortIcon(field) {
            if (this.sortField !== field) return 'fas fa-sort';
            return this.sortDirection === 'asc' ? 'fas fa-sort-up' : 'fas fa-sort-down';
        },
        
        /**
         * Format values for display
         */
        formatValue(value) {
            if (value == null || value === '') return 'N/A';
            if (typeof value === 'number') {
                return value.toLocaleString('en-US', { maximumFractionDigits: 2 });
            }
            return value;
        },
        
        /**
         * Export data as CSV
         */
        exportCSV() {
            if (!this.tableData.length) {
                this.announceToScreenReader('No data available to export');
                return;
            }
            
            try {
                // Prepare CSV headers
                const headers = ['County', 'State', 'Value'];
                if (this.showConfidenceIntervals) {
                    headers.push('CI Low', 'CI High');
                }
                
                // Prepare CSV rows
                const rows = this.sortedData.map(row => {
                    const csvRow = [
                        this.escapeCSV(row.county || ''),
                        this.escapeCSV(row.state || ''),
                        row.rawvalue || ''
                    ];
                    
                    if (this.showConfidenceIntervals) {
                        csvRow.push(row.ci_low || '');
                        csvRow.push(row.ci_high || '');
                    }
                    
                    return csvRow.join(',');
                });
                
                // Combine headers and rows
                const csvContent = [headers.join(','), ...rows].join('\n');
                
                // Create and trigger download
                const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
                const link = document.createElement('a');
                const url = URL.createObjectURL(blob);
                
                link.setAttribute('href', url);
                link.setAttribute('download', this.generateCSVFilename());
                link.style.visibility = 'hidden';
                
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                URL.revokeObjectURL(url);
                
                this.announceToScreenReader(`Exported ${this.tableData.length} records to CSV`);
                
            } catch (error) {
                this.handleError('Failed to export CSV', error);
            }
        },
        
        /**
         * Generate CSV filename with current filters
         */
        generateCSVFilename() {
            const parts = ['healthrank-data'];
            
            if (this.selectedState) parts.push(this.selectedState.replace(/\s+/g, '-'));
            if (this.selectedIndicator) parts.push(this.selectedIndicator);
            if (this.selectedYear) parts.push(this.selectedYear);
            
            const timestamp = new Date().toISOString().slice(0, 10);
            parts.push(timestamp);
            
            return parts.join('_') + '.csv';
        },
        
        /**
         * Escape CSV values
         */
        escapeCSV(value) {
            if (typeof value !== 'string') return value;
            if (value.includes(',') || value.includes('"') || value.includes('\n')) {
                return `"${value.replace(/"/g, '""')}"`;
            }
            return value;
        },
        
        /**
         * Generic fetch with error handling
         */
        async fetchWithErrorHandling(endpoint) {
            const url = `${API_BASE_URL}${endpoint}`;
            
            try {
                const response = await fetch(url);
                
                if (!response.ok) {
                    const errorData = await response.json().catch(() => null);
                    throw new Error(errorData?.message || `HTTP ${response.status}: ${response.statusText}`);
                }
                
                return await response.json();
                
            } catch (error) {
                if (error.name === 'TypeError' && error.message.includes('fetch')) {
                    throw new Error('Unable to connect to API. Please ensure the backend server is running.');
                }
                throw error;
            }
        },
        
        /**
         * Handle errors with user feedback
         */
        handleError(message, error) {
            console.error(`❌ ${message}:`, error);
            this.error = `${message}: ${error.message || 'Unknown error'}`;
            this.announceToScreenReader(`Error: ${message}`);
        },
        
        /**
         * Announce messages to screen readers
         */
        announceToScreenReader(message) {
            const announcements = document.getElementById('announcements');
            if (announcements) {
                announcements.textContent = message;
                
                // Clear after a delay to prepare for next announcement
                setTimeout(() => {
                    announcements.textContent = '';
                }, 1000);
            }
        }
    };
}

// Progressive Enhancement: Fallback for browsers without JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Add noscript warning if JavaScript is disabled
    if (!window.Alpine) {
        const noscriptWarning = document.createElement('div');
        noscriptWarning.className = 'notification is-warning';
        noscriptWarning.innerHTML = `
            <strong>JavaScript Required:</strong> 
            This application requires JavaScript to function properly. 
            Please enable JavaScript in your browser settings.
        `;
        
        const main = document.getElementById('main-content');
        if (main) {
            main.insertBefore(noscriptWarning, main.firstChild);
        }
    }
});

// Global error handling for unhandled promises
window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
    
    // Find the Alpine.js component and set error
    const dashboard = window.Alpine?.findClosest(document.body, x => x.healthDashboard);
    if (dashboard) {
        dashboard.error = 'An unexpected error occurred. Please refresh the page and try again.';
    }
});

console.log('📊 HealthRankDash frontend loaded successfully');