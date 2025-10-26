"""
Tests for missing value imputation module
"""

import pandas as pd
import numpy as np
import pytest
from src.data.preprocessing.imputation import (
    mean_imputation, median_imputation, mode_imputation, 
    forward_fill_imputation, knn_imputation, impute_missing_values
)


def test_mean_imputation():
    """Test mean imputation for numerical columns"""
    # Create test DataFrame with missing values
    df = pd.DataFrame({
        'numeric_col': [1.0, 2.0, np.nan, 4.0, 5.0],
        'other_col': ['a', 'b', 'c', 'd', 'e']
    })
    
    # Apply mean imputation
    imputed_df = mean_imputation(df, ['numeric_col'])
    
    # Check that missing values are filled with mean (3.0)
    assert imputed_df['numeric_col'].isnull().sum() == 0
    assert imputed_df['numeric_col'].iloc[2] == 3.0


def test_median_imputation():
    """Test median imputation for numerical columns"""
    # Create test DataFrame with missing values
    df = pd.DataFrame({
        'numeric_col': [1.0, 2.0, np.nan, 4.0, 5.0],
        'other_col': ['a', 'b', 'c', 'd', 'e']
    })
    
    # Apply median imputation
    imputed_df = median_imputation(df, ['numeric_col'])
    
    # Check that missing values are filled with median (3.0)
    assert imputed_df['numeric_col'].isnull().sum() == 0
    assert imputed_df['numeric_col'].iloc[2] == 3.0


def test_mode_imputation():
    """Test mode imputation for categorical columns"""
    # Create test DataFrame with missing values
    df = pd.DataFrame({
        'categorical_col': ['a', 'b', 'a', np.nan, 'a'],
        'other_col': [1, 2, 3, 4, 5]
    })
    
    # Apply mode imputation
    imputed_df = mode_imputation(df, ['categorical_col'])
    
    # Check that missing values are filled with mode ('a')
    assert imputed_df['categorical_col'].isnull().sum() == 0
    assert imputed_df['categorical_col'].iloc[3] == 'a'


def test_forward_fill_imputation():
    """Test forward fill imputation"""
    # Create test DataFrame with missing values
    df = pd.DataFrame({
        'time_series_col': [1.0, np.nan, np.nan, 4.0, 5.0],
        'other_col': ['a', 'b', 'c', 'd', 'e']
    })
    
    # Apply forward fill imputation
    imputed_df = forward_fill_imputation(df, ['time_series_col'])
    
    # Check that missing values are filled with forward fill
    assert imputed_df['time_series_col'].isnull().sum() == 0
    assert imputed_df['time_series_col'].iloc[1] == 1.0
    assert imputed_df['time_series_col'].iloc[2] == 1.0


def test_impute_missing_values():
    """Test comprehensive missing value imputation pipeline"""
    # Create test DataFrame with various missing values
    df = pd.DataFrame({
        'mean_col': [1.0, 2.0, np.nan, 4.0, 5.0],
        'median_col': [1.0, 2.0, np.nan, 4.0, 5.0],
        'mode_col': ['a', 'b', 'a', np.nan, 'a'],
        'other_col': [1, 2, 3, 4, 5]
    })
    
    # Define imputation strategy
    strategy = {
        'mean_cols': ['mean_col'],
        'median_cols': ['median_col'],
        'mode_cols': ['mode_col']
    }
    
    # Apply imputation
    imputed_df = impute_missing_values(df, strategy)
    
    # Check that all missing values are filled
    assert imputed_df['mean_col'].isnull().sum() == 0
    assert imputed_df['median_col'].isnull().sum() == 0
    assert imputed_df['mode_col'].isnull().sum() == 0


if __name__ == "__main__":
    pytest.main([__file__])