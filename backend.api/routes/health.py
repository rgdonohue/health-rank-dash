# AI-Generated
"""
Health Check Routes

Provides API health monitoring and status endpoints.
"""

from fastapi import APIRouter, Depends
from typing import Dict, Any
import time

from backend.api.dependencies.data_service import get_data_service, DataService

router = APIRouter()


@router.get("/health")
async def health_check(
    data_service: DataService = Depends(get_data_service)
) -> Dict[str, Any]:
    """
    API health check endpoint.
    
    Returns:
        Dict containing API status, data service status, and basic metrics
    """
    start_time = time.time()
    
    # Check data service health
    try:
        data = data_service.get_data()
        indicators = data_service.get_indicator_catalog()
        data_healthy = True
        data_error = None
    except Exception as e:
        data_healthy = False
        data_error = str(e)
        
    response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    
    return {
        "status": "healthy" if data_healthy else "unhealthy",
        "timestamp": time.time(),
        "response_time_ms": round(response_time, 2),
        "data_service": {
            "status": "healthy" if data_healthy else "error",
            "error": data_error,
            "counties_loaded": len(data) if data_healthy else 0,
            "indicators_available": indicators["summary"]["total_indicators"] if data_healthy else 0
        },
        "api_version": "0.1.0"
    }