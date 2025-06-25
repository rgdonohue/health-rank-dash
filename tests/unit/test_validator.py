# AI-Generated
"""
Unit tests for CHRDataValidator module

Comprehensive test suite covering data validation, schema compliance,
quality checks, and validation reporting functionality.
"""

import pytest
import pandas as pd
import numpy as np
import json
import tempfile
import os
from unittest.mock import patch, MagicMock

# Import modules to test
from data.etl.validator import CHRDataValidator, ValidationResult


class TestValidationResult:
    """Test ValidationResult dataclass."""
    
    def test_validation_result_creation(self):
        """Test ValidationResult initialization."""
        result = ValidationResult(
            is_valid=True,
            errors=["error1", "error2"],
            warnings=["warning1"],
            metrics={"count": 100}
        )
        
        assert result.is_valid is True
        assert result.errors == ["error1", "error2"]
        assert result.warnings == ["warning1"]
        assert result.metrics == {"count": 100}


class TestCHRDataValidator:
    """Test suite for CHRDataValidator functionality."""
    
    def setup_method(self):
        """Set up test fixtures before each test."""
        self.validator = CHRDataValidator()
        
        # Sample data for testing
        self.sample_data = pd.DataFrame({
            'fipscode': ['01001', '01003', '06037', '48201', '53033'],
            'state': ['Alabama', 'Alabama', 'California', 'Texas', 'Washington'],
            'county': ['Autauga', 'Baldwin', 'Los Angeles', 'Harris', 'King'],
            'year': [2025, 2025, 2025, 2025, 2025],
            'v001_rawvalue': [350.5, 298.2, 289.1, 312.4, 267.8],
            'v001_numerator': [42, 156, 9876, 1234, 89],
            'v001_denominator': [120, 523, 34123, 3951, 332],
            'v001_cilow': [325.1, 285.4, 286.2, 305.1, 261.2],
            'v001_cihigh': [375.8, 311.0, 292.0, 319.7, 274.4],
            'v002_rawvalue': [12.5, 10.8, 11.2, 13.1, 9.9],
            'v002_cilow': [11.2, 9.5, 10.9, 12.3, 9.1],
            'v002_cihigh': [13.8, 12.1, 11.5, 13.9, 10.7]
        })
        
        self.sample_columns = list(self.sample_data.columns)
        
        # Sample indicator catalog
        self.sample_catalog = {
            "indicators": [
                {
                    "id": "v001",
                    "columns": {
                        "rawvalue": "v001_rawvalue",
                        "numerator": "v001_numerator",
                        "denominator": "v001_denominator",
                        "cilow": "v001_cilow",
                        "cihigh": "v001_cihigh"
                    },
                    "complete": True,
                    "has_confidence_intervals": True
                },
                {
                    "id": "v002",
                    "columns": {
                        "rawvalue": "v002_rawvalue",
                        "cilow": "v002_cilow",
                        "cihigh": "v002_cihigh"
                    },
                    "complete": True,
                    "has_confidence_intervals": True
                }
            ],
            "malformed": [],
            "summary": {"total_indicators": 2}
        }
        
    def test_init_default_schema(self):
        """Test validator initialization with default schema."""
        validator = CHRDataValidator()
        
        assert "required_columns" in validator.schema
        assert "fipscode" in validator.schema["required_columns"]
        assert validator.schema["minimum_indicators"] == 10
        assert validator.schema["maximum_missing_rate"] == 0.8
        
    def test_init_custom_schema(self):
        """Test validator initialization with custom schema file."""
        custom_schema = {
            "required_columns": ["custom_col"],
            "minimum_indicators": 5
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(custom_schema, f)
            temp_path = f.name
            
        try:
            validator = CHRDataValidator(temp_path)
            
            # Should merge with default schema
            assert "custom_col" in validator.schema["required_columns"]
            assert validator.schema["minimum_indicators"] == 5  # Overridden
            assert "maximum_missing_rate" in validator.schema  # From default
            
        finally:
            os.unlink(temp_path)
            
    def test_validate_data_structure_success(self):
        """Test successful data structure validation."""
        result = self.validator.validate_data_structure(self.sample_data, self.sample_columns)
        
        assert result.is_valid is True
        assert len(result.errors) == 0
        assert result.metrics["indicator_count"] == 2  # v001, v002
        assert result.metrics["row_count"] == 5
        assert result.metrics["column_count"] == 12
        
    def test_validate_data_structure_missing_required_columns(self):
        """Test data structure validation with missing required columns."""
        # Remove required column
        data_missing_fips = self.sample_data.drop(columns=['fipscode'])
        columns_missing_fips = [col for col in self.sample_columns if col != 'fipscode']
        
        result = self.validator.validate_data_structure(data_missing_fips, columns_missing_fips)
        
        assert result.is_valid is False
        assert len(result.errors) == 1
        assert "Missing required columns" in result.errors[0]
        assert "fipscode" in result.errors[0]
        
    def test_validate_data_structure_insufficient_indicators(self):
        """Test data structure validation with too few indicators."""
        # Create data with only non-indicator columns
        minimal_data = self.sample_data[['fipscode', 'state', 'county', 'year']]
        minimal_columns = list(minimal_data.columns)
        
        result = self.validator.validate_data_structure(minimal_data, minimal_columns)
        
        assert result.is_valid is False
        assert len(result.errors) == 1
        assert "Insufficient indicators" in result.errors[0]
        assert result.metrics["indicator_count"] == 0
        
    def test_validate_data_structure_empty_data(self):
        """Test data structure validation with empty dataset."""
        empty_data = pd.DataFrame()
        
        result = self.validator.validate_data_structure(empty_data, [])
        
        assert result.is_valid is False
        assert "Dataset is empty" in result.errors[0]
        assert result.metrics["row_count"] == 0
        
    def test_validate_geographic_data_success(self):
        """Test successful geographic data validation."""
        result = self.validator.validate_geographic_data(self.sample_data)
        
        assert result.is_valid is True
        assert result.metrics["duplicate_fips_count"] == 0
        assert result.metrics["states_covered"] == 4  # AL, CA, TX, WA
        assert result.metrics["years_present"] == [2025]
        
    def test_validate_geographic_data_invalid_fips(self):
        """Test geographic validation with invalid FIPS codes."""
        # Add invalid FIPS codes
        invalid_data = self.sample_data.copy()
        invalid_data.loc[6] = ['123', 'InvalidState', 'InvalidCounty', 2025, 300, 50, 150, 290, 310, 12, 11, 13]  # 3-digit FIPS
        invalid_data.loc[7] = ['ABCDE', 'InvalidState2', 'InvalidCounty2', 2025, 280, 45, 160, 270, 290, 11, 10, 12]  # Non-numeric FIPS
        
        result = self.validator.validate_geographic_data(invalid_data)
        
        assert result.is_valid is True  # Geographic issues are warnings, not errors
        assert len(result.warnings) >= 1
        assert "invalid FIPS codes" in result.warnings[0]
        assert result.metrics["invalid_fips_count"] == 2
        
    def test_validate_geographic_data_duplicate_fips(self):
        """Test geographic validation with duplicate FIPS codes."""
        # Add duplicate FIPS
        duplicate_data = self.sample_data.copy()
        duplicate_data.loc[5] = ['01001', 'Alabama', 'Duplicate', 2025, 400, 60, 200, 380, 420, 15, 14, 16]  # Duplicate of row 0
        
        result = self.validator.validate_geographic_data(duplicate_data)
        
        assert result.is_valid is False  # Duplicates are errors
        assert "duplicate FIPS codes" in result.errors[0]
        assert result.metrics["duplicate_fips_count"] == 1
        
    def test_validate_geographic_data_low_state_coverage(self):
        """Test geographic validation with low state coverage."""
        # Create data with only 1 state (low coverage)
        low_coverage_data = self.sample_data.copy()
        low_coverage_data['state'] = 'Alabama'  # All same state
        
        result = self.validator.validate_geographic_data(low_coverage_data)
        
        assert result.is_valid is True
        assert any("Low state coverage" in warning for warning in result.warnings)
        assert result.metrics["states_covered"] == 1
        
    def test_validate_indicator_data_success(self):
        """Test successful indicator data validation."""
        result = self.validator.validate_indicator_data(self.sample_data, self.sample_catalog)
        
        assert result.is_valid is True
        assert len(result.errors) == 0
        
        # Check indicator metrics were calculated
        assert "indicator_validation" in result.metrics
        indicator_metrics = result.metrics["indicator_validation"]
        assert "v001" in indicator_metrics
        assert "v002" in indicator_metrics
        
        # Check v001 metrics
        v001_metrics = indicator_metrics["v001"]
        assert v001_metrics["total_values"] == 5
        assert v001_metrics["non_null_values"] == 5
        assert v001_metrics["missing_rate"] == 0.0
        assert v001_metrics["value_range"][0] == 267.8  # min
        assert v001_metrics["value_range"][1] == 350.5  # max
        
    def test_validate_indicator_data_high_missing_rate(self):
        """Test indicator validation with high missing rate."""
        # Create data with high missing rate for v001
        high_missing_data = self.sample_data.copy()
        high_missing_data.loc[1:4, 'v001_rawvalue'] = np.nan  # 80% missing (4 out of 5)
        
        result = self.validator.validate_indicator_data(high_missing_data, self.sample_catalog)
        
        assert result.is_valid is True  # High missing rate is a warning
        assert any("High missing rate" in warning for warning in result.warnings)
        
    def test_validate_indicator_data_invalid_ci_bounds(self):
        """Test indicator validation with invalid confidence intervals."""
        # Make CI low > CI high for some rows
        invalid_ci_data = self.sample_data.copy()
        invalid_ci_data.loc[0, 'v001_cilow'] = 400  # Higher than cihigh (375.8)
        invalid_ci_data.loc[1, 'v001_cilow'] = 350  # Higher than cihigh (311.0)
        
        result = self.validator.validate_indicator_data(invalid_ci_data, self.sample_catalog)
        
        assert result.is_valid is False  # Invalid CI is an error
        assert any("invalid confidence intervals" in error for error in result.errors)
        
    def test_validate_indicator_data_values_outside_ci(self):
        """Test indicator validation with values outside confidence intervals."""
        # Make rawvalue outside CI bounds
        outside_ci_data = self.sample_data.copy()
        outside_ci_data.loc[0, 'v001_rawvalue'] = 400  # Above cihigh (375.8)
        outside_ci_data.loc[1, 'v001_rawvalue'] = 200  # Below cilow (285.4)
        
        result = self.validator.validate_indicator_data(outside_ci_data, self.sample_catalog)
        
        assert result.is_valid is True  # Values outside CI are warnings
        assert any("values outside confidence intervals" in warning for warning in result.warnings)
        
    def test_validate_completeness_high_completeness(self):
        """Test completeness validation with high completeness."""
        # All data complete
        result = self.validator.validate_completeness(self.sample_data)
        
        assert result.is_valid is True
        assert result.metrics["completeness_rate"] == 1.0  # 100% complete
        assert result.metrics["null_cells"] == 0
        
    def test_validate_completeness_low_completeness(self):
        """Test completeness validation with low completeness."""
        # Create data with many missing values
        low_complete_data = self.sample_data.copy()
        
        # Make 60% of cells missing
        for col in ['v001_rawvalue', 'v001_numerator', 'v001_denominator', 'v001_cilow', 'v001_cihigh']:
            low_complete_data.loc[1:4, col] = np.nan
            
        for col in ['v002_rawvalue', 'v002_cilow', 'v002_cihigh']:
            low_complete_data.loc[0:3, col] = np.nan
            
        result = self.validator.validate_completeness(low_complete_data)
        
        assert result.is_valid is True  # Low completeness is warning, not error
        assert result.metrics["completeness_rate"] < 0.5
        assert any("Low overall completeness" in warning for warning in result.warnings)
        
    def test_validate_completeness_severely_missing_columns(self):
        """Test completeness validation with severely missing columns."""
        # Create data where some columns are almost entirely missing
        severe_missing_data = self.sample_data.copy()
        
        # Make v002_rawvalue 95% missing (only 1 out of 5 values)
        severe_missing_data.loc[1:4, 'v002_rawvalue'] = np.nan
        
        result = self.validator.validate_completeness(severe_missing_data)
        
        assert result.is_valid is True
        assert any("Columns with <10% completeness" in warning for warning in result.warnings)
        
    def test_run_comprehensive_validation(self):
        """Test running all validation checks together."""
        validation_results = self.validator.run_comprehensive_validation(
            self.sample_data, self.sample_columns, self.sample_catalog
        )
        
        # Check all validation types are present
        expected_checks = ["structure", "geographic", "indicators", "completeness"]
        assert set(validation_results.keys()) == set(expected_checks)
        
        # All should pass with good test data
        for check_name, result in validation_results.items():
            assert isinstance(result, ValidationResult)
            assert result.is_valid is True, f"{check_name} validation failed"
            
    def test_generate_validation_report_all_pass(self):
        """Test validation report generation with all checks passing."""
        # Create mock validation results (all passing)
        mock_results = {
            "structure": ValidationResult(True, [], [], {"row_count": 100}),
            "geographic": ValidationResult(True, [], ["Minor warning"], {"states": 50}),
            "indicators": ValidationResult(True, [], [], {}),
            "completeness": ValidationResult(True, [], [], {"completeness_rate": 0.95})
        }
        
        report = self.validator.generate_validation_report(mock_results)
        
        assert "OVERALL VALIDATION: ✅ VALID" in report
        assert "STRUCTURE VALIDATION: ✅ PASS" in report
        assert "GEOGRAPHIC VALIDATION: ✅ PASS" in report
        assert "Total Errors: 0" in report
        assert "Total Warnings: 1" in report
        
    def test_generate_validation_report_with_failures(self):
        """Test validation report generation with some failures."""
        # Create mock validation results (some failing)
        mock_results = {
            "structure": ValidationResult(False, ["Missing columns"], [], {}),
            "geographic": ValidationResult(True, [], ["Low coverage"], {}),
            "indicators": ValidationResult(False, ["Invalid CI"], ["High missing"], {}),
            "completeness": ValidationResult(True, [], [], {})
        }
        
        report = self.validator.generate_validation_report(mock_results)
        
        assert "OVERALL VALIDATION: ❌ INVALID" in report
        assert "STRUCTURE VALIDATION: ❌ FAIL" in report
        assert "INDICATORS VALIDATION: ❌ FAIL" in report
        assert "Total Errors: 2" in report
        assert "Total Warnings: 2" in report
        assert "Missing columns" in report
        assert "Invalid CI" in report
        
    def test_schema_customization(self):
        """Test validator with custom schema requirements."""
        custom_validator = CHRDataValidator()
        custom_validator.schema.update({
            "minimum_indicators": 1,  # Lower requirement
            "maximum_missing_rate": 0.5,  # Stricter missing rate
            "expected_states": 2  # Lower state requirement
        })
        
        # Test with data that meets custom requirements
        result = custom_validator.validate_data_structure(self.sample_data, self.sample_columns)
        assert result.is_valid is True  # Should pass with 2 indicators (> 1)
        
        # Test indicator validation with stricter missing rate
        high_missing_data = self.sample_data.copy()
        high_missing_data.loc[2:4, 'v001_rawvalue'] = np.nan  # 60% missing
        
        result = custom_validator.validate_indicator_data(high_missing_data, self.sample_catalog)
        # Should warn about high missing rate (60% > 50% threshold)
        assert any("High missing rate" in warning for warning in result.warnings)


class TestValidatorEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_empty_dataframe_validation(self):
        """Test validator with completely empty DataFrame."""
        validator = CHRDataValidator()
        empty_df = pd.DataFrame()
        
        # Structure validation
        result = validator.validate_data_structure(empty_df, [])
        assert result.is_valid is False
        assert "Dataset is empty" in result.errors[0]
        
        # Geographic validation
        result = validator.validate_geographic_data(empty_df)
        assert result.is_valid is True  # Empty data has no geographic errors
        
        # Completeness validation
        result = validator.validate_completeness(empty_df)
        assert result.is_valid is True  # No cells to be incomplete
        
    def test_single_row_validation(self):
        """Test validator with single row of data."""
        validator = CHRDataValidator()
        single_row_df = pd.DataFrame({
            'fipscode': ['01001'],
            'state': ['Alabama'],
            'county': ['Autauga'],
            'year': [2025],
            'v001_rawvalue': [350.5]
        })
        
        result = validator.validate_geographic_data(single_row_df)
        assert result.is_valid is True
        assert result.metrics["duplicate_fips_count"] == 0
        assert result.metrics["states_covered"] == 1
        
    def test_missing_columns_in_catalog(self):
        """Test indicator validation when catalog references non-existent columns."""
        validator = CHRDataValidator()
        
        # Catalog references columns not in data
        bad_catalog = {
            "indicators": [{
                "id": "v999",
                "columns": {
                    "rawvalue": "v999_rawvalue",  # Column doesn't exist
                    "cilow": "v999_cilow",
                    "cihigh": "v999_cihigh"
                },
                "complete": True,
                "has_confidence_intervals": True
            }]
        }
        
        simple_data = pd.DataFrame({
            'fipscode': ['01001'],
            'v001_rawvalue': [350.5]
        })
        
        # Should handle gracefully without crashing
        result = validator.validate_indicator_data(simple_data, bad_catalog)
        assert result.is_valid is True  # No errors for missing columns, just no validation


# Pytest fixtures for integration testing
@pytest.fixture
def sample_validator():
    """Fixture providing a CHRDataValidator with test data."""
    validator = CHRDataValidator()
    return validator


@pytest.fixture
def sample_complete_data():
    """Fixture providing complete, valid test data."""
    return pd.DataFrame({
        'fipscode': ['01001', '01003', '06037'],
        'state': ['Alabama', 'Alabama', 'California'],
        'county': ['Autauga', 'Baldwin', 'Los Angeles'],
        'year': [2025, 2025, 2025],
        'v001_rawvalue': [350.5, 298.2, 289.1],
        'v001_cilow': [325.1, 285.4, 286.2],
        'v001_cihigh': [375.8, 311.0, 292.0]
    })


def test_integration_with_fixtures(sample_validator, sample_complete_data):
    """Test validator using fixtures."""
    columns = list(sample_complete_data.columns)
    result = sample_validator.validate_data_structure(sample_complete_data, columns)
    
    assert result.is_valid is True
    assert result.metrics["row_count"] == 3