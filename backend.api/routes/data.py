# AI-Generated
"""
Data Routes

Main data query endpoints for CHR data with filtering capabilities.
"""

from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any, Optional

from backend.api.dependencies.data_service import get_data_service, DataService
from backend.api.core.exceptions import BadRequestError

router = APIRouter()


@router.get("/data", response_model=List[Dict[str, Any]])
async def get_data(
    state: Optional[str] = Query(None, description="Filter by state name"),
    fipscode: Optional[str] = Query(None, description="Filter by 5-digit FIPS code"),
    indicator: Optional[str] = Query(None, description="Filter by indicator ID (e.g., 'v001')"),
    year: Optional[int] = Query(None, description="Filter by year"),
    limit: Optional[int] = Query(None, description="Maximum number of results", ge=1, le=10000),
    data_service: DataService = Depends(get_data_service)
) -> List[Dict[str, Any]]:
    """
    Get CHR data with optional filtering.
    
    Query Parameters:
        - state: Filter by state name (case-insensitive)
        - fipscode: Filter by specific 5-digit FIPS code
        - indicator: Filter by indicator ID (e.g., 'v001')
        - year: Filter by year
        - limit: Maximum number of results (1-10000)
        
    Examples:
        - /data?state=Ohio&year=2025&indicator=v001
        - /data?fipscode=39001&year=2025&indicator=v023
        - /data?state=Ohio&year=2025 (all indicators)
        
    Returns:
        List of data records matching the filter criteria
    """
    # Validate that at least one filter is provided for performance
    if not any([state, fipscode, indicator, year]):
        raise BadRequestError(
            "At least one filter parameter is required (state, fipscode, indicator, or year)",
            details={"available_filters": ["state", "fipscode", "indicator", "year"]}
        )
    
    # Validate FIPS code format if provided
    if fipscode and (len(fipscode) != 5 or not fipscode.isdigit()):
        raise BadRequestError(
            "FIPS code must be exactly 5 digits",
            details={"provided_fipscode": fipscode, "expected_format": "12345"}
        )
    
    # Query data with filters
    results = data_service.query_data(
        state=state,
        fipscode=fipscode,
        indicator=indicator,
        year=year,
        limit=limit
    )
    
    return results