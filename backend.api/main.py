# AI-Generated
"""
HealthRankDash FastAPI Application

Main application entry point with dependency injection configuration
for County Health Rankings data API.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import uvicorn
from typing import Dict, Any

from .core.config import get_settings
from .core.exceptions import HealthRankException
from .dependencies.data_service import get_data_service
from .routes import health, indicators, geography, data

# Application settings
settings = get_settings()

# FastAPI application with metadata
app = FastAPI(
    title="HealthRankDash API",
    description="County Health Rankings data exploration API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Request timing middleware for performance monitoring
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add response time header for performance monitoring."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    # Log slow requests (>500ms as per requirements)
    if process_time > 0.5:
        print(f"⚠️  Slow request: {request.url} took {process_time:.3f}s")
    
    return response

# Global exception handler
@app.exception_handler(HealthRankException)
async def health_rank_exception_handler(request: Request, exc: HealthRankException):
    """Handle custom HealthRank exceptions with proper HTTP status codes."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_type,
            "message": exc.message,
            "details": exc.details
        }
    )

# Include API routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(indicators.router, prefix="/api/v1", tags=["indicators"])
app.include_router(geography.router, prefix="/api/v1", tags=["geography"])
app.include_router(data.router, prefix="/api/v1", tags=["data"])

# Root endpoint
@app.get("/")
async def root() -> Dict[str, Any]:
    """API root endpoint with basic information."""
    return {
        "name": "HealthRankDash API",
        "version": "0.1.0",
        "description": "County Health Rankings data exploration API",
        "docs_url": "/docs",
        "health_check": "/api/v1/health"
    }

# Application startup event
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    print("🚀 HealthRankDash API starting up...")
    
    # Initialize data service (ETL components)
    try:
        data_service = get_data_service()
        await data_service.initialize()
        print("✅ Data service initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize data service: {e}")
        raise

# Application shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    print("⏹️  HealthRankDash API shutting down...")

# Development server entry point
if __name__ == "__main__":
    uvicorn.run(
        "backend.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )