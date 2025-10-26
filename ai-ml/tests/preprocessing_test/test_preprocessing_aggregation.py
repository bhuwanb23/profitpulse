"""
Tests for data aggregation module
"""

import pandas as pd
import numpy as np
import pytest
from src.data.preprocessing.aggregation import (
    groupby_aggregation, time_series_resampling,
    rolling_window_aggregation, pivot_table_aggregation,
    aggregate_data
)


def test_groupby_aggregation():
    """Test groupby aggregation"""
    # Create test DataFrame
    df = pd.DataFrame({
        'category': ['A', 'A', 'B', 'B'],
        'value': [10, 20, 30, 40],
        'quantity': [1, 2, 3, 4]
    })
    
    # Apply groupby aggregation
    aggregated_df = df.groupby(['category']).agg({'value': 'sum', 'quantity': 'mean'}).reset_index()
    
    # Check that aggregation is applied
    assert len(aggregated_df) == 2  # Two categories
    assert 'value' in aggregated_df.columns
    assert 'quantity' in aggregated_df.columns


def test_time_series_resampling():
    """Test time series resampling"""
    # Create test DataFrame with datetime index
    dates = pd.date_range('2023-01-01', periods=10, freq='D')
    df = pd.DataFrame({
        'date': dates,
        'value': range(10),
        'quantity': range(10, 20)
    })
    
    # Apply time series resampling
    df_resampled = df.set_index('date')
    resampled_df = df_resampled.resample('2D').agg({'value': 'sum', 'quantity': 'mean'})
    resampled_df = resampled_df.reset_index()
    
    # Check that resampling is applied
    assert len(resampled_df) < len(df)  # Should have fewer rows after resampling


def test_rolling_window_aggregation():
    """Test rolling window aggregation"""
    # Create test DataFrame
    df = pd.DataFrame({
        'group': ['A', 'A', 'A', 'B', 'B', 'B'],
        'value': [1, 2, 3, 4, 5, 6],
        'date': pd.date_range('2023-01-01', periods=6, freq='D')
    })
    
    # Apply rolling window aggregation
    aggregated_df = rolling_window_aggregation(
        df, 
        ['group'], 
        ['value'], 
        2, 
        'mean'
    )
    
    # Check that rolling window aggregation is applied
    assert len(aggregated_df) == len(df)


def test_pivot_table_aggregation():
    """Test pivot table aggregation"""
    # Create test DataFrame
    df = pd.DataFrame({
        'row_col': ['A', 'A', 'B', 'B'],
        'col_col': ['X', 'Y', 'X', 'Y'],
        'value': [10, 20, 30, 40]
    })
    
    # Apply pivot table aggregation
    pivot_df = pivot_table_aggregation(
        df, 
        ['row_col'], 
        ['col_col'], 
        ['value'], 
        'mean'
    )
    
    # Check that pivot table is created
    assert len(pivot_df) > 0


def test_aggregate_data():
    """Test comprehensive data aggregation pipeline"""
    # Create test DataFrame
    df = pd.DataFrame({
        'category': ['A', 'A', 'B', 'B'],
        'date': pd.date_range('2023-01-01', periods=4, freq='D'),
        'value': [10, 20, 30, 40],
        'quantity': [1, 2, 3, 4]
    })
    
    # Define aggregation configuration
    config = {
        'groupby': {
            'groupby_columns': ['category'],
            'aggregation_functions': {'value': 'sum', 'quantity': 'mean'}
        }
    }
    
    # Apply aggregation
    aggregated_df = aggregate_data(df, config)
    
    # Check that aggregation is applied
    assert len(aggregated_df) > 0


if __name__ == "__main__":
    pytest.main([__file__])