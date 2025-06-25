# AI-Generated
"""
Response Models

Pydantic models for API response validation and documentation.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class HealthCheckResponse(BaseModel):
    """Response model for health check endpoint."""
    
    status: str = Field(..., description="API health status")
    timestamp: float = Field(..., description="Response timestamp")
    response_time_ms: float = Field(..., description="Response time in milliseconds")
    data_service: Dict[str, Any] = Field(..., description="Data service status")
    api_version: str = Field(..., description="API version")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": 1672531200.0,
                "response_time_ms": 45.67,
                "data_service": {
                    "status": "healthy",
                    "error": None,
                    "counties_loaded": 3204,
                    "indicators_available": 90
                },
                "api_version": "0.1.0"
            }
        }


class IndicatorResponse(BaseModel):
    """Response model for a single health indicator."""
    
    id: str = Field(..., description="Indicator ID (e.g., 'v001')")
    description: str = Field(..., description="Human-readable description")
    has_confidence_intervals: bool = Field(..., description="Whether CI data is available")
    complete: bool = Field(..., description="Whether indicator data is complete")
    available_columns: List[str] = Field(..., description="Available data columns")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "id": "v001",
                "description": "Premature Death",
                "has_confidence_intervals": True,
                "complete": True,
                "available_columns": ["rawvalue", "numerator", "denominator", "cilow", "cihigh"]
            }
        }


class CountyResponse(BaseModel):
    """Response model for county information."""
    
    fipscode: str = Field(..., description="5-digit FIPS code")
    county: str = Field(..., description="County name")
    state: str = Field(..., description="State name")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "fipscode": "39001",
                "county": "Adams",
                "state": "Ohio"
            }
        }


class DataRecord(BaseModel):
    """Response model for a data record with flexible fields."""
    
    fipscode: Optional[str] = Field(None, description="5-digit FIPS code")
    state: Optional[str] = Field(None, description="State name")
    county: Optional[str] = Field(None, description="County name")
    year: Optional[int] = Field(None, description="Data year")
    
    class Config:
        """Pydantic configuration."""
        extra = "allow"  # Allow additional fields for indicator data
        schema_extra = {
            "example": {
                "fipscode": "39001",
                "state": "Ohio",
                "county": "Adams",
                "year": 2025,
                "v001_rawvalue": 350.5,
                "v001_cilow": 325.1,
                "v001_cihigh": 375.8
            }
        }


class ErrorResponse(BaseModel):
    """Response model for API errors."""
    
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "error": "validation_error",
                "message": "Invalid FIPS code format",
                "details": {
                    "field": "fipscode",
                    "provided_value": "123",
                    "expected_format": "12345"
                }
            }
        }


class APIInfoResponse(BaseModel):
    """Response model for API root endpoint."""
    
    name: str = Field(..., description="API name")
    version: str = Field(..., description="API version")
    description: str = Field(..., description="API description")
    docs_url: str = Field(..., description="Documentation URL")
    health_check: str = Field(..., description="Health check URL")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "name": "HealthRankDash API",
                "version": "0.1.0",
                "description": "County Health Rankings data exploration API",
                "docs_url": "/docs",
                "health_check": "/api/v1/health"
            }
        }