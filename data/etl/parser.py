# AI-Generated
"""
CHR Data Parser Module

Parses County Health Rankings CSV with dual-header structure:
- Row 1: Human-readable descriptions 
- Row 2: Machine-readable column keys (v###_suffix patterns)

Implements extract-measures.yaml template for indicator catalog generation.
"""

import pandas as pd
import re
import json
from typing import Dict, List, Tuple, Optional
from pathlib import Path


class CHRParser:
    """County Health Rankings data parser with dual-header support."""
    
    def __init__(self, csv_path: str):
        """Initialize parser with CHR CSV file path."""
        self.csv_path = Path(csv_path)
        self.descriptions = None  # Row 1: Human-readable descriptions
        self.column_keys = None   # Row 2: Machine-readable keys
        self.data = None         # Actual data rows
        self.indicator_catalog = None
        
    def load_data(self) -> None:
        """Load CHR CSV with dual-header structure."""
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CHR data file not found: {self.csv_path}")
            
        # Read first two rows to get headers
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            self.descriptions = f.readline().strip().split(',')
            self.column_keys = f.readline().strip().split(',')
            
        # Validate header consistency
        if len(self.descriptions) != len(self.column_keys):
            raise ValueError(f"Header mismatch: {len(self.descriptions)} descriptions vs {len(self.column_keys)} keys")
            
        # Load data using column keys as headers, skipping first two rows
        self.data = pd.read_csv(self.csv_path, skiprows=2, names=self.column_keys, low_memory=False)
        
        print(f"✅ Loaded CHR data: {len(self.data)} counties, {len(self.column_keys)} columns")
        
    def extract_indicators(self) -> Dict:
        """
        Extract health indicators using v###_suffix pattern matching.
        
        Returns indicator catalog following extract-measures.yaml template format.
        """
        if self.column_keys is None:
            raise ValueError("Data not loaded. Call load_data() first.")
            
        indicators = {}
        malformed = []
        
        # Regex pattern for v###_suffix matching
        indicator_pattern = re.compile(r'^v(\d{3})_(.+)$')
        
        # Group columns by indicator ID
        for i, col_key in enumerate(self.column_keys):
            match = indicator_pattern.match(col_key)
            if match:
                indicator_id = f"v{match.group(1)}"
                suffix = match.group(2)
                description = self.descriptions[i] if i < len(self.descriptions) else ""
                
                if indicator_id not in indicators:
                    indicators[indicator_id] = {
                        "id": indicator_id,
                        "columns": {},
                        "description": "",
                        "complete": False,
                        "has_confidence_intervals": False
                    }
                    
                # Map suffix to column
                indicators[indicator_id]["columns"][suffix] = col_key
                
                # Use first description found for this indicator
                if not indicators[indicator_id]["description"] and "rawvalue" in suffix:
                    indicators[indicator_id]["description"] = description.strip('"')
                    
        # Validate and flag indicators
        valid_indicators = []
        for indicator_id, indicator in indicators.items():
            columns = indicator["columns"]
            
            # Must have rawvalue to be considered valid
            if "rawvalue" in columns:
                indicator["complete"] = True
                
                # Check for confidence intervals
                if "cilow" in columns and "cihigh" in columns:
                    indicator["has_confidence_intervals"] = True
                    
                # Check for numerator/denominator pair consistency
                has_num = "numerator" in columns
                has_denom = "denominator" in columns
                if has_num != has_denom:  # Should have both or neither
                    malformed.append({
                        "id": indicator_id,
                        "issue": "Mismatched numerator/denominator pair",
                        "columns": list(columns.keys())
                    })
                    
                valid_indicators.append(indicator)
                
            else:
                malformed.append({
                    "id": indicator_id,
                    "issue": "Missing rawvalue column - incomplete indicator",
                    "columns": list(columns.keys())
                })
                
        # Generate summary statistics
        ci_count = sum(1 for ind in valid_indicators if ind["has_confidence_intervals"])
        
        catalog = {
            "indicators": valid_indicators,
            "malformed": malformed,
            "summary": {
                "total_indicators": len(valid_indicators),
                "complete_indicators": len(valid_indicators),
                "indicators_with_ci": ci_count,
                "malformed_count": len(malformed),
                "total_columns_processed": len(self.column_keys)
            }
        }
        
        self.indicator_catalog = catalog
        return catalog
        
    def get_geographic_columns(self) -> List[str]:
        """Return list of geographic identifier columns."""
        geo_cols = []
        for col in self.column_keys:
            if col in ['statecode', 'countycode', 'fipscode', 'state', 'county', 'year']:
                geo_cols.append(col)
        return geo_cols
        
    def validate_data_quality(self) -> Dict:
        """Validate CHR data quality and flag issues."""
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")
            
        quality_report = {
            "total_counties": len(self.data),
            "missing_fips": self.data['fipscode'].isna().sum(),
            "duplicate_fips": self.data['fipscode'].duplicated().sum(),
            "year_range": [self.data['year'].min(), self.data['year'].max()] if 'year' in self.data.columns else None,
            "states_covered": self.data['state'].nunique() if 'state' in self.data.columns else 0
        }
        
        return quality_report
        
    def save_indicator_catalog(self, output_path: str) -> None:
        """Save indicator catalog to JSON file."""
        if self.indicator_catalog is None:
            raise ValueError("Indicator catalog not generated. Call extract_indicators() first.")
            
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.indicator_catalog, f, indent=2)
            
        print(f"✅ Saved indicator catalog to: {output_path}")


def main():
    """CLI entry point for CHR data parsing."""
    parser = CHRParser("data/analytic_data2025_v2.csv")
    
    try:
        # Load and parse CHR data
        parser.load_data()
        
        # Extract indicator catalog
        catalog = parser.extract_indicators()
        
        # Display summary
        summary = catalog["summary"]
        print(f"\n📊 CHR Indicator Analysis Summary:")
        print(f"   • Total indicators found: {summary['total_indicators']}")
        print(f"   • Indicators with confidence intervals: {summary['indicators_with_ci']}")
        print(f"   • Malformed indicators: {summary['malformed_count']}")
        print(f"   • Total columns processed: {summary['total_columns_processed']}")
        
        # Validate data quality
        quality = parser.validate_data_quality()
        print(f"\n🔍 Data Quality Report:")
        print(f"   • Total counties: {quality['total_counties']}")
        print(f"   • States covered: {quality['states_covered']}")
        print(f"   • Year range: {quality['year_range']}")
        print(f"   • Missing FIPS codes: {quality['missing_fips']}")
        print(f"   • Duplicate FIPS codes: {quality['duplicate_fips']}")
        
        # Save catalog
        parser.save_indicator_catalog("config/indicator_catalog.json")
        
        # Display sample indicators
        print(f"\n📋 Sample Indicators:")
        for i, indicator in enumerate(catalog["indicators"][:5]):
            print(f"   {i+1}. {indicator['id']}: {indicator['description'][:50]}...")
            
        if catalog["malformed"]:
            print(f"\n⚠️  Malformed Indicators Flagged:")
            for malformed in catalog["malformed"][:3]:
                print(f"   • {malformed['id']}: {malformed['issue']}")
                
    except Exception as e:
        print(f"❌ Error processing CHR data: {e}")
        raise


if __name__ == "__main__":
    main()