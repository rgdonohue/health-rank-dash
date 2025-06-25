# AI-Generated
"""
API Unit Tests

Comprehensive test suite for FastAPI endpoints with 100% coverage goal.
Tests all endpoints, error conditions, and performance requirements.
"""

import pytest
import pandas as pd
import json
import tempfile
import os
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
import time

# Import the simplified test API
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_test import app


class TestHealthRankDashAPI:
    """Test suite for HealthRankDash API endpoints."""
    
    @pytest.fixture
    def client(self):
        """FastAPI test client fixture."""
        return TestClient(app)
        
    @pytest.fixture
    def mock_data_service(self):
        """Mock data service for testing."""
        mock_data = pd.DataFrame({
            'fipscode': ['01001', '01003', '06037'],
            'state': ['Alabama', 'Alabama', 'California'],
            'county': ['Autauga', 'Baldwin', 'Los Angeles'],
            'year': [2025, 2025, 2025],
            'v001_rawvalue': [350.5, 298.2, 289.1],
            'v001_cilow': [325.1, 285.4, 286.2],
            'v001_cihigh': [375.8, 311.0, 292.0]
        })
        
        mock_catalog = {
            "indicators": [
                {
                    "id": "v001",
                    "description": "Premature Death",
                    "has_confidence_intervals": True,
                    "complete": True
                },
                {
                    "id": "v002",
                    "description": "Poor Health", 
                    "has_confidence_intervals": False,
                    "complete": True
                }
            ],
            "summary": {"total_indicators": 2}
        }
        
        return {
            'data': mock_data,
            'catalog': mock_catalog
        }
        
    def test_root_endpoint(self, client):
        """Test API root endpoint."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "HealthRankDash API"
        assert data["version"] == "0.1.0"
        assert "docs_url" in data
        assert "health_check" in data
        
    def test_health_endpoint_without_data_service(self, client):
        """Test health endpoint when data service is not initialized."""
        # Ensure data_service is None by patching
        with patch('api_test.data_service', None):
            response = client.get("/api/v1/health")
            assert response.status_code == 503
            assert "Data service not initialized" in response.json()["detail"]
            
    def test_health_endpoint_with_data_service(self, client, mock_data_service):
        """Test health endpoint when data service is initialized."""
        with patch('api_test.data_service', mock_data_service):
            response = client.get("/api/v1/health")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["counties_loaded"] == 3
            assert data["indicators_available"] == 2
            assert data["api_version"] == "0.1.0"
            
    def test_indicators_endpoint_without_data_service(self, client):
        """Test indicators endpoint when data service is not initialized."""
        with patch('api_test.data_service', None):
            response = client.get("/api/v1/indicators")
            assert response.status_code == 503
            
    def test_indicators_endpoint_success(self, client, mock_data_service):
        """Test indicators endpoint returns correct data."""
        with patch('api_test.data_service', mock_data_service):
            response = client.get("/api/v1/indicators")
            
            assert response.status_code == 200
            indicators = response.json()
            
            assert len(indicators) == 2
            assert indicators[0]["id"] == "v001"
            assert indicators[0]["description"] == "Premature Death"
            assert indicators[0]["has_confidence_intervals"] is True
            assert indicators[1]["id"] == "v002"
            assert indicators[1]["has_confidence_intervals"] is False
            
    def test_states_endpoint_without_data_service(self, client):
        """Test states endpoint when data service is not initialized."""
        with patch('api_test.data_service', None):
            response = client.get("/api/v1/states")
            assert response.status_code == 503
            
    def test_states_endpoint_success(self, client, mock_data_service):
        """Test states endpoint returns sorted states."""
        with patch('api_test.data_service', mock_data_service):
            response = client.get("/api/v1/states")
            
            assert response.status_code == 200
            states = response.json()
            
            assert len(states) == 2
            assert states == ["Alabama", "California"]  # Should be sorted
            
    def test_counties_endpoint_without_data_service(self, client):
        """Test counties endpoint when data service is not initialized."""
        with patch('api_test.data_service', None):
            response = client.get("/api/v1/counties/Alabama")
            assert response.status_code == 503
            
    def test_counties_endpoint_valid_state(self, client, mock_data_service):
        """Test counties endpoint with valid state."""
        with patch('api_test.data_service', mock_data_service):
            response = client.get("/api/v1/counties/Alabama")
            
            assert response.status_code == 200
            counties = response.json()
            
            assert len(counties) == 2
            assert counties[0]["county"] == "Autauga"  # Should be sorted
            assert counties[1]["county"] == "Baldwin"
            assert all(c["state"] == "Alabama" for c in counties)
            assert all("fipscode" in c for c in counties)
            
    def test_counties_endpoint_case_insensitive(self, client, mock_data_service):
        """Test counties endpoint is case insensitive."""
        with patch('api_test.data_service', mock_data_service):
            response = client.get("/api/v1/counties/alabama")  # lowercase
            
            assert response.status_code == 200
            counties = response.json()
            assert len(counties) == 2
            
    def test_counties_endpoint_invalid_state(self, client, mock_data_service):
        """Test counties endpoint with invalid state."""
        with patch('api_test.data_service', mock_data_service):
            response = client.get("/api/v1/counties/InvalidState")
            
            assert response.status_code == 404
            assert "not found" in response.json()["detail"]
            
    def test_data_endpoint_without_data_service(self, client):
        """Test data endpoint when data service is not initialized."""
        with patch('api_test.data_service', None):
            response = client.get("/api/v1/data?state=Alabama")
            assert response.status_code == 503
            
    def test_data_endpoint_no_filters(self, client, mock_data_service):
        """Test data endpoint requires at least one filter."""
        with patch('api_test.data_service', mock_data_service):
            response = client.get("/api/v1/data")
            
            assert response.status_code == 400
            assert "At least one filter parameter is required" in response.json()["detail"]
            
    def test_data_endpoint_filter_by_state(self, client, mock_data_service):
        """Test data endpoint filtering by state."""
        with patch('api_test.data_service', mock_data_service):
            response = client.get("/api/v1/data?state=Alabama")
            
            assert response.status_code == 200
            data = response.json()
            
            assert len(data) == 2  # Two Alabama counties
            assert all(record["state"] == "Alabama" for record in data)
            assert data[0]["fipscode"] == "01001"
            assert data[1]["fipscode"] == "01003"
            
    def test_data_endpoint_filter_by_fipscode(self, client, mock_data_service):
        """Test data endpoint filtering by FIPS code."""
        with patch('api_test.data_service', mock_data_service):
            response = client.get("/api/v1/data?fipscode=01001")
            
            assert response.status_code == 200
            data = response.json()
            
            assert len(data) == 1
            assert data[0]["fipscode"] == "01001"
            assert data[0]["county"] == "Autauga"
            
    def test_data_endpoint_filter_by_year(self, client, mock_data_service):
        """Test data endpoint filtering by year."""
        with patch('api_test.data_service', mock_data_service):
            response = client.get("/api/v1/data?year=2025")
            
            assert response.status_code == 200
            data = response.json()
            
            assert len(data) == 3  # All records are 2025
            assert all(record["year"] == 2025 for record in data)
            
    def test_data_endpoint_combined_filters(self, client, mock_data_service):
        """Test data endpoint with multiple filters."""
        with patch('api_test.data_service', mock_data_service):
            response = client.get("/api/v1/data?state=Alabama&year=2025")
            
            assert response.status_code == 200
            data = response.json()
            
            assert len(data) == 2
            assert all(record["state"] == "Alabama" and record["year"] == 2025 for record in data)
            
    def test_data_endpoint_with_limit(self, client, mock_data_service):
        """Test data endpoint with result limit."""
        with patch('api_test.data_service', mock_data_service):
            response = client.get("/api/v1/data?year=2025&limit=1")
            
            assert response.status_code == 200
            data = response.json()
            
            assert len(data) == 1  # Limited to 1 result
            
    def test_data_endpoint_no_results(self, client, mock_data_service):
        """Test data endpoint returns empty list when no data matches."""
        with patch('api_test.data_service', mock_data_service):
            response = client.get("/api/v1/data?state=NonExistentState")
            
            assert response.status_code == 200
            data = response.json()
            
            assert len(data) == 0
            assert data == []
            
    def test_data_endpoint_case_insensitive_state(self, client, mock_data_service):
        """Test data endpoint state filter is case insensitive."""
        with patch('api_test.data_service', mock_data_service):
            response = client.get("/api/v1/data?state=california")  # lowercase
            
            assert response.status_code == 200
            data = response.json()
            
            assert len(data) == 1
            assert data[0]["state"] == "California"


class TestAPIPerformance:
    """Performance tests for API endpoints."""
    
    @pytest.fixture
    def client(self):
        """FastAPI test client fixture."""
        return TestClient(app)
        
    @pytest.fixture
    def large_mock_data_service(self):
        """Mock data service with larger dataset for performance testing."""
        # Create larger dataset (1000 records)
        mock_data = pd.DataFrame({
            'fipscode': [f"{i:05d}" for i in range(1000, 2000)],
            'state': ['TestState'] * 1000,
            'county': [f'County_{i}' for i in range(1000)],
            'year': [2025] * 1000,
            'v001_rawvalue': [300.0 + i for i in range(1000)]
        })
        
        mock_catalog = {
            "indicators": [{"id": "v001", "description": "Test", "has_confidence_intervals": False, "complete": True}],
            "summary": {"total_indicators": 1}
        }
        
        return {'data': mock_data, 'catalog': mock_catalog}
        
    def test_health_endpoint_response_time(self, client, large_mock_data_service):
        """Test health endpoint meets performance requirements (<500ms)."""
        with patch('api_test.data_service', large_mock_data_service):
            start_time = time.time()
            response = client.get("/api/v1/health")
            response_time = (time.time() - start_time) * 1000  # Convert to ms
            
            assert response.status_code == 200
            assert response_time < 500, f"Health endpoint took {response_time:.2f}ms (>500ms)"
            
    def test_data_endpoint_response_time_with_limit(self, client, large_mock_data_service):
        """Test data endpoint performance with large dataset and limit."""
        with patch('api_test.data_service', large_mock_data_service):
            start_time = time.time()
            response = client.get("/api/v1/data?state=TestState&limit=100")
            response_time = (time.time() - start_time) * 1000
            
            assert response.status_code == 200
            assert response_time < 500, f"Data endpoint took {response_time:.2f}ms (>500ms)"
            assert len(response.json()) == 100
            
    def test_states_endpoint_response_time(self, client, large_mock_data_service):
        """Test states endpoint performance."""
        with patch('api_test.data_service', large_mock_data_service):
            start_time = time.time()
            response = client.get("/api/v1/states")
            response_time = (time.time() - start_time) * 1000
            
            assert response.status_code == 200
            assert response_time < 500, f"States endpoint took {response_time:.2f}ms (>500ms)"


class TestAPIErrorHandling:
    """Test error handling and edge cases."""
    
    @pytest.fixture
    def client(self):
        """FastAPI test client fixture."""
        return TestClient(app)
        
    def test_invalid_http_methods(self, client):
        """Test that invalid HTTP methods return 405."""
        # Test POST on GET-only endpoints
        response = client.post("/api/v1/health")
        assert response.status_code == 405
        
        response = client.put("/api/v1/states")
        assert response.status_code == 405
        
        response = client.delete("/api/v1/indicators")
        assert response.status_code == 405
        
    def test_nonexistent_endpoints(self, client):
        """Test that nonexistent endpoints return 404."""
        response = client.get("/api/v1/nonexistent")
        assert response.status_code == 404
        
        response = client.get("/api/v2/health")  # Wrong version
        assert response.status_code == 404
        
    def test_malformed_query_parameters(self, client, mock_data_service):
        """Test handling of malformed query parameters."""
        with patch('api_test.data_service', mock_data_service):
            # Invalid year (string instead of int)
            response = client.get("/api/v1/data?year=invalid&state=Alabama")
            assert response.status_code == 422  # Validation error
            
            # Invalid limit (negative number)
            response = client.get("/api/v1/data?state=Alabama&limit=-1")
            assert response.status_code == 422
            
    @pytest.fixture
    def mock_data_service(self):
        """Mock data service for error testing."""
        return {
            'data': pd.DataFrame({
                'fipscode': ['01001'],
                'state': ['Alabama'],
                'county': ['Test'],
                'year': [2025]
            }),
            'catalog': {
                "indicators": [],
                "summary": {"total_indicators": 0}
            }
        }


class TestAPIDocumentation:
    """Test API documentation and OpenAPI schema."""
    
    @pytest.fixture
    def client(self):
        """FastAPI test client fixture."""
        return TestClient(app)
        
    def test_openapi_schema_available(self, client):
        """Test that OpenAPI schema is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert schema["info"]["title"] == "HealthRankDash API"
        assert schema["info"]["version"] == "0.1.0"
        
    def test_docs_endpoints_available(self, client):
        """Test that documentation endpoints are available."""
        # Swagger UI
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        
        # ReDoc
        response = client.get("/redoc")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        
    def test_api_endpoint_documentation(self, client):
        """Test that API endpoints are properly documented in OpenAPI schema."""
        response = client.get("/openapi.json")
        schema = response.json()
        
        paths = schema.get("paths", {})
        
        # Check that all our endpoints are documented
        expected_paths = [
            "/",
            "/api/v1/health",
            "/api/v1/indicators", 
            "/api/v1/states",
            "/api/v1/counties/{state}",
            "/api/v1/data"
        ]
        
        for path in expected_paths:
            assert path in paths, f"Endpoint {path} not found in OpenAPI schema"
            
        # Check that endpoints have proper descriptions
        assert "summary" in paths["/api/v1/health"]["get"]
        assert "summary" in paths["/api/v1/data"]["get"]


# Pytest configuration and test runner
if __name__ == "__main__":
    # Run tests with coverage
    pytest.main([
        __file__,
        "-v",
        "--cov=api_test",
        "--cov-report=term",
        "--cov-report=html:htmlcov_api"
    ])