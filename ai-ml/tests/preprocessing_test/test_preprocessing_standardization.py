"""
Tests for data standardization module
"""

import pandas as pd
import numpy as np
import pytest
from src.data.preprocessing.standardization import (
    standardize_datetime_columns, standardize_currency_columns,
    standardize_categorical_values, standardize_text_columns,
    standardize_data
)


def test_standardize_datetime_columns():
    """Test datetime column standardization"""
    # Create test DataFrame with datetime columns
    df = pd.DataFrame({
        'date_col': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'other_col': [1, 2, 3]
    })
    
    # Apply datetime standardization
    standardized_df = standardize_datetime_columns(
        df, 
        {'date_col': '%Y-%m-%d'}
    )
    
    # Check that datetime is standardized (converted to string format)
    assert isinstance(standardized_df['date_col'].iloc[0], str)
    assert standardized_df['date_col'].iloc[0] == '2023-01-01'


def test_standardize_currency_columns():
    """Test currency column standardization"""
    # Create test DataFrame with currency columns
    df = pd.DataFrame({
        'amount_col': ['$100.50', '€200.75', '£300.25'],
        'other_col': [1, 2, 3]
    })
    
    # Apply currency standardization
    standardized_df = standardize_currency_columns(df, ['amount_col'])
    
    # Check that currency is standardized to float
    assert standardized_df['amount_col'].dtype in [np.float64, np.float32]
    assert standardized_df['amount_col'].isnull().sum() == 0


def test_standardize_categorical_values():
    """Test categorical value standardization"""
    # Create test DataFrame with categorical columns
    df = pd.DataFrame({
        'status_col': ['active', 'inactive', 'Active', 'INACTIVE'],
        'other_col': [1, 2, 3, 4]
    })
    
    # Apply categorical standardization
    mappings = {'status_col': {'active': 'Active', 'inactive': 'Inactive', 'Active': 'Active', 'INACTIVE': 'Inactive'}}
    standardized_df = standardize_categorical_values(df, mappings)
    
    # Check that categorical values are standardized
    expected_values = ['Active', 'Inactive', 'Active', 'Inactive']
    assert list(standardized_df['status_col']) == expected_values


def test_standardize_text_columns():
    """Test text column standardization"""
    # Create test DataFrame with text columns
    df = pd.DataFrame({
        'text_col': ['  Hello World  ', '  TEST  ', '  lowercase  '],
        'other_col': [1, 2, 3]
    })
    
    # Apply text standardization
    standardized_df = standardize_text_columns(df, ['text_col'])
    
    # Check that text is standardized
    expected_values = ['Hello World', 'Test', 'Lowercase']
    assert list(standardized_df['text_col']) == expected_values


def test_standardize_data():
    """Test comprehensive data standardization pipeline"""
    # Create test DataFrame with various data types
    df = pd.DataFrame({
        'date_col': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'amount_col': ['$100.50', '€200.75', '£300.25'],
        'status_col': ['active', 'inactive', 'Active'],
        'text_col': ['  Hello World  ', '  TEST  ', '  lowercase  ']
    })
    
    # Define standardization configuration
    config = {
        'datetime_columns': {'date_col': '%Y-%m-%d'},
        'currency_columns': ['amount_col'],
        'categorical_mappings': {'status_col': {'active': 'Active', 'inactive': 'Inactive', 'Active': 'Active'}},
        'text_columns': ['text_col']
    }
    
    # Apply standardization
    standardized_df = standardize_data(df, config)
    
    # Check that data is standardized (datetime converted to string format)
    assert isinstance(standardized_df['date_col'].iloc[0], str)
    assert standardized_df['date_col'].iloc[0] == '2023-01-01'
    assert standardized_df['amount_col'].dtype in [np.float64, np.float32]
    assert list(standardized_df['status_col']) == ['Active', 'Inactive', 'Active']
    assert list(standardized_df['text_col']) == ['Hello World', 'Test', 'Lowercase']


if __name__ == "__main__":
    pytest.main([__file__])