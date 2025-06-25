# AI-Generated
"""
Geography Routes

API endpoints for geographic data discovery (states, counties).
"""

from fastapi import APIRouter, Depends, Path
from typing import List, Dict, Any

from backend.api.dependencies.data_service import get_data_service, DataService

router = APIRouter()


@router.get("/states", response_model=List[str])
async def get_states(
    data_service: DataService = Depends(get_data_service)
) -> List[str]:
    """
    Get list of all available states.
    
    Returns:
        Sorted list of state names
    """
    return data_service.get_states()


@router.get("/counties/{state}", response_model=List[Dict[str, Any]])
async def get_counties_by_state(
    state: str = Path(..., description="State name"),
    data_service: DataService = Depends(get_data_service)
) -> List[Dict[str, Any]]:
    """
    Get list of counties for a given state.
    
    Args:
        state: State name (case-insensitive)
        
    Returns:
        List of county objects with:
        - fipscode: 5-digit FIPS code
        - county: County name
        - state: State name
    """
    return data_service.get_counties_by_state(state)