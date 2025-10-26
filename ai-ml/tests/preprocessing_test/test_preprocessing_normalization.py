"""
Tests for data normalization module
"""

import pandas as pd
import numpy as np
import pytest
from src.data.preprocessing.normalization import (
    min_max_scaling, standard_scaling, robust_scaling,
    unit_vector_scaling, normalize_data
)


def test_min_max_scaling():
    """Test Min-Max scaling"""
    # Create test DataFrame with numerical columns
    df = pd.DataFrame({
        'numeric_col': [1.0, 2.0, 3.0, 4.0, 5.0],
        'other_col': ['a', 'b', 'c', 'd', 'e']
    })
    
    # Apply Min-Max scaling
    scaled_df = min_max_scaling(df, ['numeric_col'], feature_range=(0, 1))
    
    # Check that values are scaled to [0, 1] range
    assert scaled_df['numeric_col'].min() >= 0.0
    assert scaled_df['numeric_col'].max() <= 1.0


def test_standard_scaling():
    """Test Standard scaling (Z-score normalization)"""
    # Create test DataFrame with numerical columns
    df = pd.DataFrame({
        'numeric_col': [1.0, 2.0, 3.0, 4.0, 5.0],
        'other_col': ['a', 'b', 'c', 'd', 'e']
    })
    
    # Apply Standard scaling
    scaled_df = standard_scaling(df, ['numeric_col'])
    
    # Check that values are standardized (mean ≈ 0, std ≈ 1)
    assert abs(scaled_df['numeric_col'].mean()) < 0.1
    assert abs(scaled_df['numeric_col'].std() - 1.0) < 0.2


def test_robust_scaling():
    """Test Robust scaling"""
    # Create test DataFrame with numerical columns
    df = pd.DataFrame({
        'numeric_col': [1.0, 2.0, 3.0, 4.0, 5.0],
        'other_col': ['a', 'b', 'c', 'd', 'e']
    })
    
    # Apply Robust scaling
    scaled_df = robust_scaling(df, ['numeric_col'])
    
    # Check that scaling is applied
    assert len(scaled_df) == len(df)


def test_unit_vector_scaling():
    """Test Unit Vector scaling"""
    # Create test DataFrame with numerical columns
    df = pd.DataFrame({
        'numeric_col1': [1.0, 2.0, 3.0],
        'numeric_col2': [4.0, 5.0, 6.0],
        'other_col': ['a', 'b', 'c']
    })
    
    # Apply Unit Vector scaling
    scaled_df = unit_vector_scaling(df, ['numeric_col1', 'numeric_col2'], norm='l2')
    
    # Check that scaling is applied
    assert len(scaled_df) == len(df)


def test_normalize_data():
    """Test comprehensive data normalization pipeline"""
    # Create test DataFrame with various numerical columns
    df = pd.DataFrame({
        'minmax_col': [1.0, 2.0, 3.0, 4.0, 5.0],
        'standard_col': [10.0, 20.0, 30.0, 40.0, 50.0],
        'robust_col': [100.0, 200.0, 300.0, 400.0, 500.0],
        'other_col': ['a', 'b', 'c', 'd', 'e']
    })
    
    # Define normalization configuration
    config = {
        'min_max_cols': ['minmax_col'],
        'standard_cols': ['standard_col'],
        'robust_cols': ['robust_col']
    }
    
    # Apply normalization
    normalized_df = normalize_data(df, config)
    
    # Check that normalization is applied
    assert len(normalized_df) == len(df)
    assert normalized_df['minmax_col'].min() >= 0.0
    assert normalized_df['minmax_col'].max() <= 1.0


if __name__ == "__main__":
    pytest.main([__file__])