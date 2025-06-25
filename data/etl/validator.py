# AI-Generated
"""
CHR Data Validation Module

Implements comprehensive validation schemas and data quality checks
for County Health Rankings data processing pipeline.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import json
import jsonschema
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Container for validation results."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    metrics: Dict[str, Any]


class CHRDataValidator:
    """Comprehensive validator for CHR data quality and schema compliance."""
    
    def __init__(self, schema_path: Optional[str] = None):
        """Initialize validator with optional schema file."""
        self.schema = self._load_default_schema()
        if schema_path and Path(schema_path).exists():
            with open(schema_path, 'r') as f:
                self.schema.update(json.load(f))
                
    def _load_default_schema(self) -> Dict:
        """Load default CHR validation schema."""
        return {
            "required_columns": [
                "fipscode", "state", "county", "year"
            ],
            "indicator_pattern": r"^v\d{3}_",
            "expected_suffixes": [
                "_rawvalue", "_numerator", "_denominator", 
                "_cilow", "_cihigh", "_flag"
            ],
            "minimum_indicators": 10,
            "maximum_missing_rate": 0.8,
            "expected_states": 50,  # Plus DC and territories
            "year_range": [2020, 2030],
            "fips_pattern": r"^\d{5}$"
        }
        
    def validate_data_structure(self, data: pd.DataFrame, column_keys: List[str]) -> ValidationResult:
        """Validate overall data structure and schema compliance."""
        errors = []
        warnings = []
        metrics = {}
        
        # Check required columns
        missing_required = []
        for col in self.schema["required_columns"]:
            if col not in column_keys:
                missing_required.append(col)
                
        if missing_required:
            errors.append(f"Missing required columns: {missing_required}")
            
        # Check for minimum number of indicators
        indicator_cols = [col for col in column_keys if col.startswith('v') and '_' in col]
        unique_indicators = set()
        for col in indicator_cols:
            if '_' in col:
                indicator_id = col.split('_')[0]
                unique_indicators.add(indicator_id)
                
        metrics["indicator_count"] = len(unique_indicators)
        if len(unique_indicators) < self.schema["minimum_indicators"]:
            errors.append(f"Insufficient indicators: {len(unique_indicators)} < {self.schema['minimum_indicators']}")
            
        # Validate data dimensions
        metrics["row_count"] = len(data)
        metrics["column_count"] = len(column_keys)
        
        if len(data) == 0:
            errors.append("Dataset is empty")
            
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            metrics=metrics
        )
        
    def validate_geographic_data(self, data: pd.DataFrame) -> ValidationResult:
        """Validate geographic identifiers and coverage."""
        errors = []
        warnings = []
        metrics = {}
        
        # FIPS code validation
        if 'fipscode' in data.columns:
            invalid_fips = data[~data['fipscode'].astype(str).str.match(r'^\d{5}$', na=False)]
            metrics["invalid_fips_count"] = len(invalid_fips)
            
            if len(invalid_fips) > 0:
                warnings.append(f"Found {len(invalid_fips)} invalid FIPS codes")
                
            # Check for duplicates
            duplicates = data['fipscode'].duplicated().sum()
            metrics["duplicate_fips_count"] = duplicates
            if duplicates > 0:
                errors.append(f"Found {duplicates} duplicate FIPS codes")
                
        # State coverage validation
        if 'state' in data.columns:
            unique_states = data['state'].nunique()
            metrics["states_covered"] = unique_states
            
            if unique_states < 40:  # Arbitrary threshold for coverage
                warnings.append(f"Low state coverage: only {unique_states} states")
                
        # Year validation
        if 'year' in data.columns:
            years = data['year'].dropna().unique()
            metrics["years_present"] = sorted(years.tolist())
            
            min_year, max_year = self.schema["year_range"]
            invalid_years = [y for y in years if y < min_year or y > max_year]
            if invalid_years:
                warnings.append(f"Years outside expected range: {invalid_years}")
                
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            metrics=metrics
        )
        
    def validate_indicator_data(self, data: pd.DataFrame, indicator_catalog: Dict) -> ValidationResult:
        """Validate indicator data quality and consistency."""
        errors = []
        warnings = []
        metrics = {}
        
        indicator_metrics = {}
        
        for indicator in indicator_catalog.get("indicators", []):
            indicator_id = indicator["id"]
            columns = indicator["columns"]
            
            # Check if rawvalue exists and has data
            rawvalue_col = columns.get("rawvalue")
            if rawvalue_col and rawvalue_col in data.columns:
                raw_data = data[rawvalue_col].dropna()
                
                indicator_metrics[indicator_id] = {
                    "total_values": len(data),
                    "non_null_values": len(raw_data),
                    "missing_rate": 1 - (len(raw_data) / len(data)),
                    "value_range": [raw_data.min(), raw_data.max()] if len(raw_data) > 0 else [None, None]
                }
                
                # Check missing rate
                missing_rate = 1 - (len(raw_data) / len(data))
                if missing_rate > self.schema["maximum_missing_rate"]:
                    warnings.append(f"{indicator_id}: High missing rate {missing_rate:.2%}")
                    
                # Validate confidence intervals if present
                if "cilow" in columns and "cihigh" in columns:
                    cilow_col = columns["cilow"]
                    cihigh_col = columns["cihigh"]
                    
                    if cilow_col in data.columns and cihigh_col in data.columns:
                        # Check CI consistency (low <= high)
                        ci_data = data[[rawvalue_col, cilow_col, cihigh_col]].dropna()
                        invalid_ci = ci_data[ci_data[cilow_col] > ci_data[cihigh_col]]
                        
                        if len(invalid_ci) > 0:
                            errors.append(f"{indicator_id}: {len(invalid_ci)} invalid confidence intervals (low > high)")
                            
                        # Check if rawvalue is within CI bounds
                        outside_ci = ci_data[
                            (ci_data[rawvalue_col] < ci_data[cilow_col]) | 
                            (ci_data[rawvalue_col] > ci_data[cihigh_col])
                        ]
                        
                        if len(outside_ci) > 0:
                            warnings.append(f"{indicator_id}: {len(outside_ci)} values outside confidence intervals")
                            
        metrics["indicator_validation"] = indicator_metrics
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            metrics=metrics
        )
        
    def validate_completeness(self, data: pd.DataFrame) -> ValidationResult:
        """Validate data completeness across all dimensions."""
        errors = []
        warnings = []
        metrics = {}
        
        # Overall completeness
        total_cells = data.size
        null_cells = data.isnull().sum().sum()
        completeness_rate = 1 - (null_cells / total_cells)
        
        metrics["completeness_rate"] = completeness_rate
        metrics["total_cells"] = total_cells
        metrics["null_cells"] = null_cells
        
        if completeness_rate < 0.5:  # 50% threshold
            warnings.append(f"Low overall completeness: {completeness_rate:.2%}")
            
        # Per-column completeness
        column_completeness = {}
        for col in data.columns:
            col_completeness = 1 - (data[col].isnull().sum() / len(data))
            column_completeness[col] = col_completeness
            
        metrics["column_completeness"] = column_completeness
        
        # Identify columns with severe missingness
        severely_missing = [col for col, rate in column_completeness.items() 
                          if rate < 0.1]  # Less than 10% complete
        
        if severely_missing:
            warnings.append(f"Columns with <10% completeness: {len(severely_missing)} columns")
            
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            metrics=metrics
        )
        
    def run_comprehensive_validation(self, data: pd.DataFrame, column_keys: List[str], 
                                   indicator_catalog: Dict) -> Dict[str, ValidationResult]:
        """Run all validation checks and return comprehensive report."""
        
        validation_results = {
            "structure": self.validate_data_structure(data, column_keys),
            "geographic": self.validate_geographic_data(data),
            "indicators": self.validate_indicator_data(data, indicator_catalog),
            "completeness": self.validate_completeness(data)
        }
        
        return validation_results
        
    def generate_validation_report(self, validation_results: Dict[str, ValidationResult]) -> str:
        """Generate human-readable validation report."""
        report_lines = ["🔍 CHR Data Validation Report", "=" * 50]
        
        overall_valid = True
        total_errors = 0
        total_warnings = 0
        
        for check_name, result in validation_results.items():
            status = "✅ PASS" if result.is_valid else "❌ FAIL"
            report_lines.append(f"\n{check_name.upper()} VALIDATION: {status}")
            
            if not result.is_valid:
                overall_valid = False
                
            total_errors += len(result.errors)
            total_warnings += len(result.warnings)
            
            if result.errors:
                report_lines.append("  Errors:")
                for error in result.errors:
                    report_lines.append(f"    • {error}")
                    
            if result.warnings:
                report_lines.append("  Warnings:")
                for warning in result.warnings:
                    report_lines.append(f"    • {warning}")
                    
            # Add key metrics
            if result.metrics:
                report_lines.append("  Key Metrics:")
                for metric, value in result.metrics.items():
                    if metric != "indicator_validation":  # Skip detailed indicator metrics
                        report_lines.append(f"    • {metric}: {value}")
                        
        # Overall summary
        overall_status = "✅ VALID" if overall_valid else "❌ INVALID"
        report_lines.extend([
            "\n" + "=" * 50,
            f"OVERALL VALIDATION: {overall_status}",
            f"Total Errors: {total_errors}",
            f"Total Warnings: {total_warnings}"
        ])
        
        return "\n".join(report_lines)


def main():
    """CLI entry point for data validation."""
    from .parser import CHRParser
    
    parser = CHRParser("data/analytic_data2025_v2.csv")
    validator = CHRDataValidator()
    
    try:
        # Load data and extract indicators
        parser.load_data()
        catalog = parser.extract_indicators()
        
        # Run comprehensive validation
        validation_results = validator.run_comprehensive_validation(
            parser.data, parser.column_keys, catalog
        )
        
        # Generate and display report
        report = validator.generate_validation_report(validation_results)
        print(report)
        
        # Save validation results
        validation_summary = {
            check: {
                "is_valid": result.is_valid,
                "error_count": len(result.errors),
                "warning_count": len(result.warnings),
                "errors": result.errors,
                "warnings": result.warnings
            }
            for check, result in validation_results.items()
        }
        
        with open("config/validation_report.json", "w") as f:
            json.dump(validation_summary, f, indent=2)
            
        print(f"\n✅ Validation report saved to: config/validation_report.json")
        
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        raise


if __name__ == "__main__":
    main()