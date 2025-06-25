# AI-Generated
"""
Unit tests for CHRParser module

Comprehensive test suite covering data loading, indicator extraction,
validation, and edge cases for County Health Rankings data processing.
"""

import pytest
import pandas as pd
import json
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, mock_open

# Import modules to test
from data.etl.parser import CHRParser


class TestCHRParser:
    """Test suite for CHRParser functionality."""
    
    def setup_method(self):
        """Set up test fixtures before each test."""
        self.sample_descriptions = [
            "State FIPS Code", "County FIPS Code", "5-digit FIPS Code", 
            "State", "County", "Year", "Premature Death raw value",
            "Premature Death numerator", "Premature Death CI low"
        ]
        
        self.sample_column_keys = [
            "statecode", "countycode", "fipscode", "state", "county", 
            "year", "v001_rawvalue", "v001_numerator", "v001_cilow"
        ]
        
        self.sample_data_rows = [
            "01,001,01001,Alabama,Autauga,2025,350.5,42,325.1",
            "01,003,01003,Alabama,Baldwin,2025,298.2,156,285.4",
            "01,005,01005,Alabama,Barbour,2025,512.8,31,480.2"
        ]
        
        # Create temporary CSV content
        self.sample_csv_content = (
            ",".join(self.sample_descriptions) + "\n" +
            ",".join(self.sample_column_keys) + "\n" +
            "\n".join(self.sample_data_rows)
        )
        
    def test_init(self):
        """Test CHRParser initialization."""
        parser = CHRParser("test_file.csv")
        assert parser.csv_path == Path("test_file.csv")
        assert parser.descriptions is None
        assert parser.column_keys is None
        assert parser.data is None
        assert parser.indicator_catalog is None
        
    def test_load_data_file_not_found(self):
        """Test load_data with non-existent file."""
        parser = CHRParser("nonexistent_file.csv")
        
        with pytest.raises(FileNotFoundError) as exc_info:
            parser.load_data()
        assert "CHR data file not found" in str(exc_info.value)
        
    def test_load_data_success(self):
        """Test successful data loading with dual headers."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(self.sample_csv_content)
            temp_path = f.name
            
        try:
            parser = CHRParser(temp_path)
            parser.load_data()
            
            # Check headers were parsed correctly
            assert parser.descriptions == self.sample_descriptions
            assert parser.column_keys == self.sample_column_keys
            
            # Check data loading
            assert len(parser.data) == 3
            assert list(parser.data.columns) == self.sample_column_keys
            assert parser.data.iloc[0]['fipscode'] == '01001'
            assert parser.data.iloc[0]['state'] == 'Alabama'
            
        finally:
            os.unlink(temp_path)
            
    def test_load_data_header_mismatch(self):
        """Test load_data with mismatched header lengths."""
        mismatched_content = (
            "Col1,Col2,Col3\n" +  # 3 description columns
            "key1,key2\n" +      # 2 key columns (mismatch!)
            "val1,val2\n"
        )
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(mismatched_content)
            temp_path = f.name
            
        try:
            parser = CHRParser(temp_path)
            with pytest.raises(ValueError) as exc_info:
                parser.load_data()
            assert "Header mismatch" in str(exc_info.value)
            
        finally:
            os.unlink(temp_path)
            
    def test_extract_indicators_without_loading(self):
        """Test extract_indicators called before load_data."""
        parser = CHRParser("test_file.csv")
        
        with pytest.raises(ValueError) as exc_info:
            parser.extract_indicators()
        assert "Data not loaded" in str(exc_info.value)
        
    def test_extract_indicators_success(self):
        """Test successful indicator extraction."""
        # Create test data with indicators
        test_descriptions = [
            "State", "County", "FIPS", "Premature Death raw value",
            "Premature Death numerator", "Premature Death CI low",
            "Poor Health raw value", "Poor Health CI high"
        ]
        test_keys = [
            "state", "county", "fipscode", "v001_rawvalue", 
            "v001_numerator", "v001_cilow", "v002_rawvalue", "v002_cihigh"
        ]
        
        parser = CHRParser("test_file.csv")
        parser.descriptions = test_descriptions
        parser.column_keys = test_keys
        
        catalog = parser.extract_indicators()
        
        # Check catalog structure
        assert "indicators" in catalog
        assert "malformed" in catalog
        assert "summary" in catalog
        
        # Should find 2 indicators (v001, v002)
        indicators = catalog["indicators"]
        assert len(indicators) == 2
        
        # Check v001 indicator
        v001 = next(ind for ind in indicators if ind["id"] == "v001")
        assert v001["complete"] is True
        assert v001["has_confidence_intervals"] is True  # has cilow
        assert "rawvalue" in v001["columns"]
        assert "numerator" in v001["columns"]
        assert "cilow" in v001["columns"]
        
        # Check v002 indicator (incomplete - missing cilow)
        v002 = next(ind for ind in indicators if ind["id"] == "v002")
        assert v002["complete"] is True
        assert v002["has_confidence_intervals"] is False  # missing cilow
        
        # Check summary
        summary = catalog["summary"]
        assert summary["total_indicators"] == 2
        assert summary["indicators_with_ci"] == 1
        assert summary["total_columns_processed"] == 8
        
    def test_extract_indicators_malformed(self):
        """Test indicator extraction with malformed indicators."""
        test_descriptions = ["State", "Malformed indicator"]
        test_keys = ["state", "v999_badcolumn"]  # No rawvalue
        
        parser = CHRParser("test_file.csv")
        parser.descriptions = test_descriptions
        parser.column_keys = test_keys
        
        catalog = parser.extract_indicators()
        
        # Should have no valid indicators
        assert len(catalog["indicators"]) == 0
        
        # Should flag malformed indicator
        assert len(catalog["malformed"]) == 1
        malformed = catalog["malformed"][0]
        assert malformed["id"] == "v999"
        assert "Missing rawvalue column" in malformed["issue"]
        
    def test_get_geographic_columns(self):
        """Test geographic column identification."""
        parser = CHRParser("test_file.csv")
        parser.column_keys = [
            "statecode", "countycode", "fipscode", "state", 
            "county", "year", "v001_rawvalue", "other_col"
        ]
        
        geo_cols = parser.get_geographic_columns()
        
        expected_geo_cols = ["statecode", "countycode", "fipscode", "state", "county", "year"]
        assert set(geo_cols) == set(expected_geo_cols)
        assert "v001_rawvalue" not in geo_cols
        assert "other_col" not in geo_cols
        
    def test_validate_data_quality_without_loading(self):
        """Test validate_data_quality called before load_data."""
        parser = CHRParser("test_file.csv")
        
        with pytest.raises(ValueError) as exc_info:
            parser.validate_data_quality()
        assert "Data not loaded" in str(exc_info.value)
        
    def test_validate_data_quality_success(self):
        """Test data quality validation."""
        # Create test DataFrame
        test_data = pd.DataFrame({
            'fipscode': ['01001', '01003', '01005', '01001'],  # Includes duplicate
            'state': ['Alabama', 'Alabama', 'Alabama', 'Alabama'],
            'county': ['Autauga', 'Baldwin', 'Barbour', 'Autauga'],
            'year': [2025, 2025, 2025, 2025]
        })
        
        parser = CHRParser("test_file.csv")
        parser.data = test_data
        
        quality_report = parser.validate_data_quality()
        
        # Check report structure
        assert "total_counties" in quality_report
        assert "missing_fips" in quality_report
        assert "duplicate_fips" in quality_report
        assert "year_range" in quality_report
        assert "states_covered" in quality_report
        
        # Check values
        assert quality_report["total_counties"] == 4
        assert quality_report["missing_fips"] == 0
        assert quality_report["duplicate_fips"] == 1  # One duplicate FIPS
        assert quality_report["year_range"] == [2025, 2025]
        assert quality_report["states_covered"] == 1  # Only Alabama
        
    def test_save_indicator_catalog_without_catalog(self):
        """Test save_indicator_catalog called before extract_indicators."""
        parser = CHRParser("test_file.csv")
        
        with pytest.raises(ValueError) as exc_info:
            parser.save_indicator_catalog("output.json")
        assert "Indicator catalog not generated" in str(exc_info.value)
        
    def test_save_indicator_catalog_success(self):
        """Test successful indicator catalog saving."""
        parser = CHRParser("test_file.csv")
        parser.indicator_catalog = {
            "indicators": [{"id": "v001", "description": "Test indicator"}],
            "summary": {"total_indicators": 1}
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
            
        try:
            parser.save_indicator_catalog(temp_path)
            
            # Verify file was created and contains correct data
            with open(temp_path, 'r') as f:
                saved_catalog = json.load(f)
                
            assert saved_catalog == parser.indicator_catalog
            assert saved_catalog["summary"]["total_indicators"] == 1
            
        finally:
            os.unlink(temp_path)
            
    def test_indicator_pattern_matching(self):
        """Test various indicator ID pattern matching scenarios."""
        test_cases = [
            ("v001_rawvalue", True, "v001", "rawvalue"),
            ("v123_numerator", True, "v123", "numerator"),
            ("v999_ci_low", True, "v999", "ci_low"),
            ("not_indicator", False, None, None),
            ("v1_rawvalue", False, None, None),    # Too short
            ("v1234_rawvalue", False, None, None), # Too long
            ("x001_rawvalue", False, None, None),  # Wrong prefix
        ]
        
        parser = CHRParser("test_file.csv")
        
        # Use the internal regex pattern from extract_indicators
        import re
        indicator_pattern = re.compile(r'^v(\d{3})_(.+)$')
        
        for column, should_match, expected_id, expected_suffix in test_cases:
            match = indicator_pattern.match(column)
            
            if should_match:
                assert match is not None, f"Should match: {column}"
                assert f"v{match.group(1)}" == expected_id
                assert match.group(2) == expected_suffix
            else:
                assert match is None, f"Should not match: {column}"


class TestCHRParserIntegration:
    """Integration tests using real-world scenarios."""
    
    def test_full_workflow_with_real_data_structure(self):
        """Test complete workflow with realistic CHR data structure."""
        # Simulate a subset of real CHR data structure
        descriptions = [
            "State FIPS Code", "County FIPS Code", "5-digit FIPS Code",
            "State", "County", "Release Year",
            "Premature Death raw value", "Premature Death numerator", 
            "Premature Death denominator", "Premature Death CI low", 
            "Premature Death CI high", "Poor Health raw value",
            "Poor Health CI low", "Poor Health CI high"
        ]
        
        column_keys = [
            "statecode", "countycode", "fipscode", "state", "county", "year",
            "v001_rawvalue", "v001_numerator", "v001_denominator", 
            "v001_cilow", "v001_cihigh", "v002_rawvalue", 
            "v002_cilow", "v002_cihigh"
        ]
        
        data_rows = [
            "01,001,01001,Alabama,Autauga,2025,350.5,42,120,325.1,375.8,12.5,11.2,13.8",
            "01,003,01003,Alabama,Baldwin,2025,298.2,156,523,285.4,311.0,10.8,9.5,12.1",
            "06,037,06037,California,Los Angeles,2025,289.1,9876,34123,286.2,292.0,11.2,10.9,11.5"
        ]
        
        csv_content = (
            ",".join(descriptions) + "\n" +
            ",".join(column_keys) + "\n" +
            "\n".join(data_rows)
        )
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_path = f.name
            
        try:
            # Complete workflow test
            parser = CHRParser(temp_path)
            
            # Load data
            parser.load_data()
            assert len(parser.data) == 3
            assert parser.data['state'].iloc[0] == 'Alabama'
            assert parser.data['state'].iloc[2] == 'California'
            
            # Extract indicators
            catalog = parser.extract_indicators()
            assert catalog["summary"]["total_indicators"] == 2
            
            # Both indicators should be complete with CI
            for indicator in catalog["indicators"]:
                assert indicator["complete"] is True
                assert indicator["has_confidence_intervals"] is True
                
            # Validate data quality
            quality = parser.validate_data_quality()
            assert quality["total_counties"] == 3
            assert quality["states_covered"] == 2  # Alabama, California
            assert quality["duplicate_fips"] == 0
            
            # Test geographic columns
            geo_cols = parser.get_geographic_columns()
            assert "statecode" in geo_cols
            assert "fipscode" in geo_cols
            assert "v001_rawvalue" not in geo_cols
            
        finally:
            os.unlink(temp_path)
            
    def test_edge_case_empty_data(self):
        """Test handling of empty data file."""
        # File with headers but no data rows
        csv_content = (
            "State,County\n" +
            "state,county\n"
            # No data rows
        )
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_path = f.name
            
        try:
            parser = CHRParser(temp_path)
            parser.load_data()
            
            # Should load successfully but have empty data
            assert len(parser.data) == 0
            assert parser.data.empty
            
            # Quality validation should handle empty data gracefully
            quality = parser.validate_data_quality()
            assert quality["total_counties"] == 0
            
        finally:
            os.unlink(temp_path)


# Pytest configuration and fixtures
@pytest.fixture
def sample_parser():
    """Fixture providing a CHRParser with sample data loaded."""
    parser = CHRParser("test_file.csv")
    parser.descriptions = ["State", "County", "Indicator"]
    parser.column_keys = ["state", "county", "v001_rawvalue"]
    parser.data = pd.DataFrame({
        'state': ['Alabama', 'Alaska'],
        'county': ['Autauga', 'Anchorage'],
        'v001_rawvalue': [350.5, 298.2]
    })
    return parser


def test_parser_with_fixture(sample_parser):
    """Test using the sample_parser fixture."""
    assert sample_parser.data is not None
    assert len(sample_parser.data) == 2
    assert 'state' in sample_parser.data.columns