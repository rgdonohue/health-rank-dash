# AI-Generated
"""
FastAPI Test Runner

Quick test script to validate API functionality and run test server.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException, Query
from fastapi import Path as FastAPIPath
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
import uvicorn
import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

# Import our ETL components
from data.etl.parser import CHRParser
from data.etl.validator import CHRDataValidator

# Simple FastAPI app for testing
app = FastAPI(
    title="HealthRankDash API",
    description="County Health Rankings data exploration API",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Global data storage (simplified for testing)
data_service = None

@app.on_event("startup")
async def startup_event():
    """Initialize data on startup."""
    global data_service
    try:
        print("🚀 Initializing data service...")
        parser = CHRParser("data/analytic_data2025_v2.csv")
        parser.load_data()
        
        # Load indicator catalog
        catalog_path = Path("config/indicator_catalog.json")
        if catalog_path.exists():
            with open(catalog_path, 'r') as f:
                catalog = json.load(f)
        else:
            catalog = parser.extract_indicators()
            
        data_service = {
            'data': parser.data,
            'catalog': catalog,
            'parser': parser
        }
        
        print(f"✅ Data service initialized: {len(parser.data)} counties, {catalog['summary']['total_indicators']} indicators")
        
    except Exception as e:
        print(f"❌ Failed to initialize data service: {e}")
        raise

# Health check endpoint
@app.get("/api/v1/health")
async def health_check():
    """API health check."""
    if data_service is None:
        raise HTTPException(status_code=503, detail="Data service not initialized")
        
    return {
        "status": "healthy",
        "counties_loaded": len(data_service['data']),
        "indicators_available": data_service['catalog']['summary']['total_indicators'],
        "api_version": "0.1.0"
    }

# Get all indicators
@app.get("/api/v1/indicators")
async def get_indicators():
    """Get all available indicators."""
    if data_service is None:
        raise HTTPException(status_code=503, detail="Data service not initialized")
        
    indicators = []
    for indicator in data_service['catalog'].get("indicators", []):
        indicators.append({
            "id": indicator["id"],
            "description": indicator.get("description", ""),
            "has_confidence_intervals": indicator.get("has_confidence_intervals", False),
            "complete": indicator.get("complete", False)
        })
        
    return sorted(indicators, key=lambda x: x['id'])

# Get all states
@app.get("/api/v1/states")
async def get_states():
    """Get all available states."""
    if data_service is None:
        raise HTTPException(status_code=503, detail="Data service not initialized")
        
    return sorted(data_service['data']['state'].unique().tolist())

# Get counties by state with validation
@app.get("/api/v1/counties/{state}")
async def get_counties_by_state(
    state: str = FastAPIPath(..., description="State name", min_length=2, max_length=50)
):
    """Get counties for a given state."""
    if data_service is None:
        raise HTTPException(status_code=503, detail="Data service not initialized")
        
    data = data_service['data']
    state_data = data[data['state'].str.lower() == state.lower()]
    
    if state_data.empty:
        raise HTTPException(status_code=404, detail=f"State '{state}' not found")
        
    counties = []
    for _, row in state_data.iterrows():
        counties.append({
            "fipscode": row['fipscode'],
            "county": row['county'],
            "state": row['state']
        })
        
    return sorted(counties, key=lambda x: x['county'])

# Main data endpoint with proper validation
@app.get("/api/v1/data")
async def get_data(
    state: Optional[str] = Query(None, description="Filter by state name", min_length=2, max_length=50),
    fipscode: Optional[str] = Query(None, description="Filter by 5-digit FIPS code", regex=r"^\d{5}$"),
    indicator: Optional[str] = Query(None, description="Filter by indicator ID", regex=r"^v\d{3}$"),
    year: Optional[int] = Query(None, description="Filter by year", ge=2000, le=2030),
    limit: Optional[int] = Query(None, description="Maximum results", ge=1, le=10000)
):
    """Get CHR data with filtering."""
    if data_service is None:
        raise HTTPException(status_code=503, detail="Data service not initialized")
        
    # Require at least one filter
    if not any([state, fipscode, indicator, year]):
        raise HTTPException(
            status_code=400, 
            detail="At least one filter parameter is required"
        )
        
    data = data_service['data']
    
    # Apply filters
    if state:
        data = data[data['state'].str.lower() == state.lower()]
    if fipscode:
        data = data[data['fipscode'] == fipscode]
    if year:
        data = data[data['year'] == year]
        
    if data.empty:
        return []
        
    # Limit results
    if limit:
        data = data.head(limit)
        
    # Convert to list of dicts
    results = []
    for _, row in data.iterrows():
        record = {}
        for col in data.columns:
            value = row[col]
            record[col] = None if pd.isna(value) else value
        results.append(record)
        
    return results

# Root endpoint
@app.get("/")
async def root():
    """API root."""
    return {
        "name": "HealthRankDash API",
        "version": "0.1.0",
        "docs_url": "/docs",
        "health_check": "/api/v1/health"
    }

if __name__ == "__main__":
    print("🚀 Starting HealthRankDash API server...")
    uvicorn.run(app, host="127.0.0.1", port=8001, reload=True)