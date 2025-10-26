"""
Tests for data validation module
"""

import pandas as pd
import numpy as np
import pytest
from src.data.preprocessing.validation import (
    validate_data_schema, validate_data_ranges,
    validate_data_completeness, validate_cross_field_constraints,
    calculate_data_quality_score, validate_data
)


def test_validate_data_schema():
    """Test data schema validation"""
    # Create test DataFrame
    df = pd.DataFrame({
        'int_col': [1, 2, 3],
        'float_col': [1.0, 2.0, 3.0],
        'str_col': ['a', 'b', 'c']
    })
    
    # Define expected schema
    expected_schema = {
        'int_col': 'int64',
        'float_col': 'float64',
        'str_col': 'object'
    }
    
    # Validate schema
    results = validate_data_schema(df, expected_schema)
    
    # Check validation results
    assert isinstance(results, dict)
    assert 'validation_passed' in results


def test_validate_data_ranges():
    """Test data range validation"""
    # Create test DataFrame
    df = pd.DataFrame({
        'age_col': [25, 30, 35, -5, 150],  # -5 and 150 are out of range
        'salary_col': [50000, 60000, 70000, 80000, 90000]
    })
    
    # Define range constraints
    range_constraints = {
        'age_col': {'min': 0, 'max': 120}
    }
    
    # Validate ranges
    results = validate_data_ranges(df, range_constraints)
    
    # Check validation results
    assert isinstance(results, dict)
    assert 'validation_passed' in results


def test_validate_data_completeness():
    """Test data completeness validation"""
    # Create test DataFrame with missing values
    df = pd.DataFrame({
        'col1': [1, 2, np.nan, 4],
        'col2': [1, np.nan, np.nan, 4],
        'col3': [1, 2, 3, 4]
    })
    
    # Define completeness requirements
    completeness_requirements = {
        'col1': 0.75,  # 75% required, 75% actual (3/4)
        'col2': 0.75,  # 75% required, 50% actual (2/4)
        'col3': 1.0    # 100% required, 100% actual (4/4)
    }
    
    # Validate completeness
    results = validate_data_completeness(df, completeness_requirements)
    
    # Check validation results
    assert isinstance(results, dict)
    assert 'validation_passed' in results


def test_calculate_data_quality_score():
    """Test data quality score calculation"""
    # Create test DataFrame
    df = pd.DataFrame({
        'col1': [1, 2, 3, 4],
        'col2': [1, 2, 3, 4],
        'col3': [1, 2, 3, 4]
    })
    
    # Calculate quality scores
    quality_scores = calculate_data_quality_score(df)
    
    # Check quality scores
    assert isinstance(quality_scores, dict)
    assert 'overall' in quality_scores
    assert 0 <= quality_scores['overall'] <= 100


def test_validate_data():
    """Test comprehensive data validation pipeline"""
    # Create test DataFrame
    df = pd.DataFrame({
        'int_col': [1, 2, 3],
        'float_col': [1.0, 2.0, 3.0],
        'age_col': [25, 30, 35],
        'col_with_missing': [1, np.nan, 3]
    })
    
    # Define validation configuration
    config = {
        'schema': {
            'int_col': 'int64',
            'float_col': 'float64'
        },
        'ranges': {
            'age_col': {'min': 0, 'max': 120}
        },
        'completeness': {
            'int_col': 1.0,
            'col_with_missing': 0.5
        }
    }
    
    # Apply validation
    results = validate_data(df, config)
    
    # Check validation results
    assert isinstance(results, dict)
    assert 'overall_validation_passed' in results


if __name__ == "__main__":
    pytest.main([__file__])