#!/usr/bin/env python3
"""
Simple FastAPI server to get the frontend working
This serves the basic endpoints that the frontend expects
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import List, Dict, Any

app = FastAPI(
    title="HealthRankDash Simple API",
    description="Simple API to get frontend working",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, be more specific
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Mock data
MOCK_STATES = [
    {"id": "AL", "name": "Alabama"},
    {"id": "AK", "name": "Alaska"},
    {"id": "AZ", "name": "Arizona"},
    {"id": "AR", "name": "Arkansas"},
    {"id": "CA", "name": "California"},
    {"id": "CO", "name": "Colorado"},
    {"id": "CT", "name": "Connecticut"},
    {"id": "DE", "name": "Delaware"},
    {"id": "FL", "name": "Florida"},
    {"id": "GA", "name": "Georgia"}
]

MOCK_INDICATORS = [
    {"id": "v001", "name": "Length of Life", "description": "Premature death rate"},
    {"id": "v002", "name": "Quality of Life", "description": "Poor or fair health rate"},
    {"id": "v003", "name": "Health Behaviors", "description": "Adult smoking rate"},
    {"id": "v004", "name": "Clinical Care", "description": "Uninsured rate"},
    {"id": "v005", "name": "Social & Economic", "description": "Children in poverty rate"}
]

MOCK_COUNTIES = {
    "Colorado": [
        {"id": "08001", "name": "Adams County", "state": "Colorado"},
        {"id": "08005", "name": "Arapahoe County", "state": "Colorado"},
        {"id": "08013", "name": "Boulder County", "state": "Colorado"}
    ]
}

MOCK_DATA = [
    {"county_id": "08001", "county_name": "Adams County", "state": "Colorado", "indicator": "v003", "value": 15.2, "year": 2025},
    {"county_id": "08005", "county_name": "Arapahoe County", "state": "Colorado", "indicator": "v003", "value": 12.8, "year": 2025},
    {"county_id": "08013", "county_name": "Boulder County", "state": "Colorado", "indicator": "v003", "value": 8.9, "year": 2025}
]

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "HealthRankDash Simple API",
        "version": "0.1.0",
        "status": "running"
    }

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": "2025-01-19T12:00:00Z"}

@app.get("/api/v1/states")
async def get_states():
    """Get list of states"""
    return {"states": MOCK_STATES}

@app.get("/api/v1/indicators")
async def get_indicators():
    """Get list of indicators"""
    return {"indicators": MOCK_INDICATORS}

@app.get("/api/v1/counties/{state}")
async def get_counties(state: str):
    """Get counties for a state"""
    counties = MOCK_COUNTIES.get(state, [])
    return {"counties": counties, "state": state}

@app.get("/api/v1/data")
async def get_data(year: int = 2025, state: str = None, indicator: str = None):
    """Get health data with filters"""
    data = MOCK_DATA.copy()
    
    # Apply filters
    if state:
        data = [d for d in data if d["state"] == state]
    if indicator:
        data = [d for d in data if d["indicator"] == indicator]
    if year:
        data = [d for d in data if d["year"] == year]
    
    return {
        "data": data,
        "filters": {"year": year, "state": state, "indicator": indicator},
        "count": len(data)
    }

if __name__ == "__main__":
    print("🚀 Starting HealthRankDash Simple API...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 