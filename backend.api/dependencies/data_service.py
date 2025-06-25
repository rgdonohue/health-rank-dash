# AI-Generated
"""
Data Service Dependency Injection

Provides singleton data service instance with ETL components
for FastAPI dependency injection pattern.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from functools import lru_cache
import pandas as pd

from data.etl.parser import CHRParser
from data.etl.validator import CHRDataValidator
from ..core.config import get_settings
from ..core.exceptions import DataProcessingError, NotFoundError


class DataService:
    """
    Data service providing access to parsed CHR data and indicators.
    
    Implements singleton pattern for efficient memory usage and
    fast API response times.
    """
    
    def __init__(self):
        self.settings = get_settings()
        self.parser: Optional[CHRParser] = None
        self.validator: Optional[CHRDataValidator] = None
        self.data: Optional[pd.DataFrame] = None
        self.indicator_catalog: Optional[Dict] = None
        self.is_initialized = False
        
    async def initialize(self) -> None:
        """Initialize data service with ETL components."""
        try:
            # Initialize parser and load data
            self.parser = CHRParser(str(self.settings.data_file_path_resolved))
            self.parser.load_data()
            self.data = self.parser.data
            
            # Load indicator catalog
            if self.settings.indicator_catalog_path_resolved.exists():
                with open(self.settings.indicator_catalog_path_resolved, 'r') as f:
                    self.indicator_catalog = json.load(f)
            else:
                # Generate catalog if not exists
                self.indicator_catalog = self.parser.extract_indicators()
                
            # Initialize validator
            self.validator = CHRDataValidator()
            
            self.is_initialized = True
            print(f"✅ Data service initialized: {len(self.data)} counties, "
                  f"{self.indicator_catalog['summary']['total_indicators']} indicators")
                  
        except Exception as e:
            raise DataProcessingError(f"Failed to initialize data service: {str(e)}")
            
    def get_data(self) -> pd.DataFrame:
        """Get the main CHR dataset."""
        if not self.is_initialized:
            raise DataProcessingError("Data service not initialized")
        return self.data
        
    def get_indicator_catalog(self) -> Dict:
        """Get the indicator catalog."""
        if not self.is_initialized:
            raise DataProcessingError("Data service not initialized")
        return self.indicator_catalog
        
    def get_states(self) -> List[str]:
        """Get list of all available states."""
        data = self.get_data()
        return sorted(data['state'].unique().tolist())
        
    def get_counties_by_state(self, state: str) -> List[Dict[str, Any]]:
        """Get list of counties for a given state."""
        data = self.get_data()
        state_data = data[data['state'].str.lower() == state.lower()]
        
        if state_data.empty:
            raise NotFoundError(f"State '{state}' not found", "state")
            
        counties = []
        for _, row in state_data.iterrows():
            counties.append({
                "fipscode": row['fipscode'],
                "county": row['county'],
                "state": row['state']
            })
            
        return sorted(counties, key=lambda x: x['county'])
        
    def get_indicators(self) -> List[Dict[str, Any]]:
        """Get list of all available indicators with metadata."""
        catalog = self.get_indicator_catalog()
        indicators = []
        
        for indicator in catalog.get("indicators", []):
            indicators.append({
                "id": indicator["id"],
                "description": indicator.get("description", ""),
                "has_confidence_intervals": indicator.get("has_confidence_intervals", False),
                "complete": indicator.get("complete", False),
                "available_columns": list(indicator.get("columns", {}).keys())
            })
            
        return sorted(indicators, key=lambda x: x['id'])
        
    def query_data(
        self,
        state: Optional[str] = None,
        fipscode: Optional[str] = None,
        indicator: Optional[str] = None,
        year: Optional[int] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Query CHR data with filtering parameters.
        
        Args:
            state: Filter by state name
            fipscode: Filter by specific FIPS code
            indicator: Filter by indicator ID
            year: Filter by year
            limit: Maximum number of results
            
        Returns:
            List of matching data records
        """
        data = self.get_data()
        
        # Apply filters
        if state:
            data = data[data['state'].str.lower() == state.lower()]
            
        if fipscode:
            data = data[data['fipscode'] == fipscode]
            
        if year:
            data = data[data['year'] == year]
            
        if data.empty:
            return []
            
        # Select columns based on indicator
        if indicator:
            # Get indicator columns from catalog
            catalog = self.get_indicator_catalog()
            indicator_info = None
            
            for ind in catalog.get("indicators", []):
                if ind["id"] == indicator:
                    indicator_info = ind
                    break
                    
            if not indicator_info:
                raise NotFoundError(f"Indicator '{indicator}' not found", "indicator")
                
            # Base geographic columns
            base_columns = ['fipscode', 'state', 'county', 'year']
            
            # Add indicator-specific columns
            indicator_columns = list(indicator_info.get("columns", {}).values())
            selected_columns = base_columns + [col for col in indicator_columns if col in data.columns]
            
        else:
            # Return all columns if no specific indicator requested
            selected_columns = data.columns.tolist()
            
        # Select and limit data
        result_data = data[selected_columns]
        
        if limit:
            result_data = result_data.head(limit)
            
        # Convert to list of dictionaries
        results = []
        for _, row in result_data.iterrows():
            record = {}
            for col in selected_columns:
                value = row[col]
                # Handle NaN values
                if pd.isna(value):
                    record[col] = None
                else:
                    record[col] = value
            results.append(record)
            
        return results


# Singleton instance
_data_service: Optional[DataService] = None


async def get_data_service() -> DataService:
    """Dependency injection function for FastAPI."""
    global _data_service
    
    if _data_service is None:
        _data_service = DataService()
        
    if not _data_service.is_initialized:
        await _data_service.initialize()
        
    return _data_service