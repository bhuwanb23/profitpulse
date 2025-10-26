"""
Tests for feature engineering module
"""

import pandas as pd
import numpy as np
import pytest
from src.data.preprocessing.feature_engineering import (
    one_hot_encoding, label_encoding, create_time_based_features,
    create_ratio_features, create_polynomial_features,
    create_interaction_features, engineer_features
)


def test_one_hot_encoding():
    """Test one-hot encoding"""
    # Create test DataFrame with categorical columns
    df = pd.DataFrame({
        'category_col': ['A', 'B', 'A', 'C'],
        'numeric_col': [1, 2, 3, 4]
    })
    
    # Apply one-hot encoding
    encoded_df = one_hot_encoding(df, ['category_col'], drop_first=True)
    
    # Check that one-hot encoding is applied
    assert len(encoded_df) == len(df)
    assert 'category_col_A' in encoded_df.columns or 'category_col_B' in encoded_df.columns


def test_label_encoding():
    """Test label encoding"""
    # Create test DataFrame with categorical columns
    df = pd.DataFrame({
        'category_col': ['A', 'B', 'A', 'C'],
        'numeric_col': [1, 2, 3, 4]
    })
    
    # Apply label encoding
    encoded_df = label_encoding(df, ['category_col'])
    
    # Check that label encoding is applied
    assert len(encoded_df) == len(df)
    assert encoded_df['category_col'].dtype in [np.int64, np.int32]


def test_create_time_based_features():
    """Test time-based feature creation"""
    # Create test DataFrame with datetime column
    df = pd.DataFrame({
        'datetime_col': pd.date_range('2023-01-01', periods=4, freq='D'),
        'numeric_col': [1, 2, 3, 4]
    })
    
    # Create time-based features
    feature_df = create_time_based_features(df, 'datetime_col')
    
    # Check that time-based features are created
    assert len(feature_df) == len(df)
    assert 'datetime_col_year' in feature_df.columns
    assert 'datetime_col_month' in feature_df.columns


def test_create_ratio_features():
    """Test ratio feature creation"""
    # Create test DataFrame with numerical columns
    df = pd.DataFrame({
        'numerator_col': [10.0, 20.0, 30.0, 40.0],
        'denominator_col': [2.0, 4.0, 5.0, 8.0],
        'other_col': ['a', 'b', 'c', 'd']
    })
    
    # Create ratio features
    ratio_pairs = [('numerator_col', 'denominator_col', 'ratio_col')]
    feature_df = create_ratio_features(df, ratio_pairs)
    
    # Check that ratio features are created
    assert len(feature_df) == len(df)
    assert 'ratio_col' in feature_df.columns
    # Check first ratio: 10.0 / 2.0 = 5.0
    assert feature_df['ratio_col'].iloc[0] == 5.0


def test_create_polynomial_features():
    """Test polynomial feature creation"""
    # Create test DataFrame with numerical columns
    df = pd.DataFrame({
        'numeric_col': [1.0, 2.0, 3.0, 4.0],
        'other_col': ['a', 'b', 'c', 'd']
    })
    
    # Create polynomial features
    feature_df = create_polynomial_features(df, ['numeric_col'], degree=2)
    
    # Check that polynomial features are created
    assert len(feature_df) == len(df)
    assert 'numeric_col_pow_2' in feature_df.columns
    # Check first squared value: 1.0^2 = 1.0
    assert feature_df['numeric_col_pow_2'].iloc[0] == 1.0


def test_create_interaction_features():
    """Test interaction feature creation"""
    # Create test DataFrame with numerical columns
    df = pd.DataFrame({
        'col1': [1.0, 2.0, 3.0, 4.0],
        'col2': [2.0, 3.0, 4.0, 5.0],
        'other_col': ['a', 'b', 'c', 'd']
    })
    
    # Create interaction features
    interaction_pairs = [('col1', 'col2', 'interaction_col')]
    feature_df = create_interaction_features(df, interaction_pairs)
    
    # Check that interaction features are created
    assert len(feature_df) == len(df)
    assert 'interaction_col' in feature_df.columns
    # Check first interaction: 1.0 * 2.0 = 2.0
    assert feature_df['interaction_col'].iloc[0] == 2.0


def test_engineer_features():
    """Test comprehensive feature engineering pipeline"""
    # Create test DataFrame with various columns
    df = pd.DataFrame({
        'category_col': ['A', 'B', 'A', 'C'],
        'datetime_col': pd.date_range('2023-01-01', periods=4, freq='D'),
        'numerator_col': [10.0, 20.0, 30.0, 40.0],
        'denominator_col': [2.0, 4.0, 5.0, 8.0],
        'numeric_col': [1.0, 2.0, 3.0, 4.0]
    })
    
    # Define feature engineering configuration
    config = {
        'one_hot_cols': ['category_col'],
        'time_based_features': {'datetime_col': 'datetime_col'},
        'ratio_features': [('numerator_col', 'denominator_col', 'ratio_col')],
        'polynomial_features': {'cols': ['numeric_col'], 'degree': 2}
    }
    
    # Apply feature engineering
    engineered_df = engineer_features(df, config)
    
    # Check that features are engineered
    assert len(engineered_df) == len(df)
    assert 'ratio_col' in engineered_df.columns
    assert 'numeric_col_pow_2' in engineered_df.columns


if __name__ == "__main__":
    pytest.main([__file__])