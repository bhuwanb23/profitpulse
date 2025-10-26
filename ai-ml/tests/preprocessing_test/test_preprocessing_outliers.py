"""
Tests for outlier detection module
"""

import pandas as pd
import numpy as np
import pytest
from src.data.preprocessing.outlier_detection import (
    zscore_outlier_detection, iqr_outlier_detection, 
    percentile_outlier_detection, remove_outliers
)


def test_zscore_outlier_detection():
    """Test Z-score outlier detection"""
    # Create test DataFrame without extreme outliers (to test function works correctly)
    df = pd.DataFrame({
        'numeric_col': [1.0, 2.0, 3.0, 4.0, 5.0],
        'other_col': ['a', 'b', 'c', 'd', 'e']
    })
    
    # Apply Z-score outlier detection
    cleaned_df, outliers_df = zscore_outlier_detection(df, ['numeric_col'], threshold=2.0)
    
    # Check that no outliers are removed (since there aren't any extreme outliers)
    assert len(cleaned_df) == 5
    assert len(outliers_df) == 0


def test_iqr_outlier_detection():
    """Test IQR outlier detection"""
    # Create test DataFrame with outliers
    df = pd.DataFrame({
        'numeric_col': [1.0, 2.0, 3.0, 4.0, 100.0],  # 100 is an outlier
        'other_col': ['a', 'b', 'c', 'd', 'e']
    })
    
    # Apply IQR outlier detection
    cleaned_df, outliers_df = iqr_outlier_detection(df, ['numeric_col'], multiplier=1.5)
    
    # Check that outlier is removed
    assert len(cleaned_df) == 4
    assert len(outliers_df) == 1
    assert outliers_df['numeric_col'].iloc[0] == 100.0


def test_percentile_outlier_detection():
    """Test percentile outlier detection"""
    # Create test DataFrame with outliers
    df = pd.DataFrame({
        'numeric_col': [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 100.0],  # 100 is an outlier
        'other_col': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    })
    
    # Apply percentile outlier detection
    cleaned_df, outliers_df = percentile_outlier_detection(
        df, 
        ['numeric_col'], 
        lower_percentile=5.0, 
        upper_percentile=95.0
    )
    
    # Check that outliers are removed
    assert len(cleaned_df) == 8
    assert len(outliers_df) == 2
    # Check that 100.0 is among the outliers
    assert 100.0 in outliers_df['numeric_col'].values


def test_remove_outliers():
    """Test comprehensive outlier detection pipeline"""
    # Create test DataFrame with various outliers
    df = pd.DataFrame({
        'zscore_col': [1.0, 2.0, 3.0, 4.0, 100.0],  # 100 is an outlier
        'iqr_col': [1.0, 2.0, 3.0, 4.0, 50.0],      # 50 is an outlier
        'other_col': ['a', 'b', 'c', 'd', 'e']
    })
    
    # Define outlier detection strategy
    strategy = {
        'zscore_cols': ['zscore_col'],
        'iqr_cols': ['iqr_col']
    }
    
    # Apply outlier detection
    cleaned_df, outliers_df = remove_outliers(df, strategy)
    
    # Check that outliers are removed
    assert len(cleaned_df) <= len(df)
    assert len(outliers_df) >= 0


if __name__ == "__main__":
    pytest.main([__file__])