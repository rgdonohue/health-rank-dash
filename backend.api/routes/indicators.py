# AI-Generated
"""
Indicators Routes

API endpoints for health indicator discovery and metadata.
"""

from fastapi import APIRouter, Depends
from typing import List, Dict, Any

from ..dependencies.data_service import get_data_service, DataService

router = APIRouter()


@router.get("/indicators", response_model=List[Dict[str, Any]])
async def get_indicators(
    data_service: DataService = Depends(get_data_service)
) -> List[Dict[str, Any]]:
    """
    Get list of all available health indicators.
    
    Returns:
        List of indicator objects with metadata including:
        - id: Indicator identifier (e.g., 'v001')
        - description: Human-readable description
        - has_confidence_intervals: Boolean indicating CI availability
        - complete: Boolean indicating data completeness
        - available_columns: List of available data columns
    """
    return data_service.get_indicators()