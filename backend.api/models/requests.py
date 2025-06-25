# AI-Generated
"""
Request Models

Pydantic models for API request validation and documentation.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
import re


class DataQueryRequest(BaseModel):
    """Request model for data endpoint query parameters."""
    
    state: Optional[str] = Field(
        None, 
        description="Filter by state name (case-insensitive)",
        min_length=2,
        max_length=50
    )
    
    fipscode: Optional[str] = Field(
        None,
        description="Filter by 5-digit FIPS code",
        regex=r"^\d{5}$"
    )
    
    indicator: Optional[str] = Field(
        None,
        description="Filter by indicator ID (e.g., 'v001')",
        regex=r"^v\d{3}$"
    )
    
    year: Optional[int] = Field(
        None,
        description="Filter by year",
        ge=2000,
        le=2030
    )
    
    limit: Optional[int] = Field(
        None,
        description="Maximum number of results",
        ge=1,
        le=10000
    )
    
    @validator('state')
    def validate_state(cls, v):
        """Validate state name format."""
        if v is not None:
            # Remove extra whitespace and validate characters
            v = v.strip()
            if not re.match(r'^[a-zA-Z\s]+$', v):
                raise ValueError('State name must contain only letters and spaces')
        return v
        
    @validator('fipscode')
    def validate_fipscode(cls, v):
        """Validate FIPS code format."""
        if v is not None and (len(v) != 5 or not v.isdigit()):
            raise ValueError('FIPS code must be exactly 5 digits')
        return v
        
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "state": "Ohio",
                "year": 2025,
                "indicator": "v001",
                "limit": 100
            }
        }


class CountyStateRequest(BaseModel):
    """Request model for county lookup by state."""
    
    state: str = Field(
        ...,
        description="State name (case-insensitive)",
        min_length=2,
        max_length=50
    )
    
    @validator('state')
    def validate_state(cls, v):
        """Validate state name format."""
        v = v.strip()
        if not re.match(r'^[a-zA-Z\s]+$', v):
            raise ValueError('State name must contain only letters and spaces')
        return v
        
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "state": "California"
            }
        }