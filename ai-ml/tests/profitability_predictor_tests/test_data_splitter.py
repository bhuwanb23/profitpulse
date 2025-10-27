"""
Tests for ProfitabilityDataSplitter
"""

import pandas as pd
import pytest
import numpy as np
from datetime import datetime, timedelta

from src.models.profitability_predictor.data_splitter import ProfitabilityDataSplitter, split_profitability_data


def create_test_features():
    """Create test features data"""
    # Create sample data with dates for time-based splitting
    dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
    
    data = {
        'id': [f'client_{i}' for i in range(100)],
        'start_date': dates.strftime('%Y-%m-%d').tolist(),
        'profit_margin': np.random.normal(0.25, 0.1, 100),  # Normal distribution around 25% margin
        'total_revenue': np.random.uniform(1000, 50000, 100),
        'total_costs': np.random.uniform(500, 30000, 100),
        'feature_1': np.random.uniform(0, 1, 100),
        'feature_2': np.random.uniform(0, 1, 100),
        'feature_3': np.random.uniform(0, 1, 100)
    }
    
    return pd.DataFrame(data)


def test_data_splitter_initialization():
    """Test ProfitabilityDataSplitter initialization"""
    splitter = ProfitabilityDataSplitter()
    assert splitter is not None


def test_time_based_split():
    """Test time-based data splitting"""
    # Create test data
    features = create_test_features()
    
    # Create data splitter
    splitter = ProfitabilityDataSplitter()
    
    # Perform time-based split
    train_df, validation_df, test_df = splitter.time_based_split(
        features, 
        test_size=0.15, 
        validation_size=0.15
    )
    
    # Check results
    assert isinstance(train_df, pd.DataFrame)
    assert isinstance(validation_df, pd.DataFrame)
    assert isinstance(test_df, pd.DataFrame)
    
    # Check sizes (approximately)
    total_rows = len(features)
    expected_test_rows = int(total_rows * 0.15)
    expected_validation_rows = int(total_rows * 0.15)
    expected_train_rows = total_rows - expected_test_rows - expected_validation_rows
    
    # Allow for some flexibility in actual vs expected
    assert abs(len(test_df) - expected_test_rows) <= 1
    assert abs(len(validation_df) - expected_validation_rows) <= 1
    assert abs(len(train_df) - expected_train_rows) <= 1
    
    # Check that all data is accounted for
    assert len(train_df) + len(validation_df) + len(test_df) == total_rows
    
    # Check time-based ordering (most recent should be in test)
    train_dates = pd.to_datetime(train_df['start_date'])
    test_dates = pd.to_datetime(test_df['start_date'])
    
    assert train_dates.max() <= test_dates.min()


def test_stratified_split():
    """Test stratified data splitting"""
    # Create test data
    features = create_test_features()
    
    # Create data splitter
    splitter = ProfitabilityDataSplitter()
    
    # Perform stratified split
    train_df, validation_df, test_df = splitter.stratified_split(
        features, 
        target_column='profit_margin',
        test_size=0.2, 
        validation_size=0.2,
        random_state=42
    )
    
    # Check results
    assert isinstance(train_df, pd.DataFrame)
    assert isinstance(validation_df, pd.DataFrame)
    assert isinstance(test_df, pd.DataFrame)
    
    # Check sizes (approximately)
    total_rows = len(features)
    expected_test_rows = int(total_rows * 0.2)
    expected_validation_rows = int(total_rows * 0.2)
    expected_train_rows = total_rows - expected_test_rows - expected_validation_rows
    
    # Allow for some flexibility in actual vs expected
    assert abs(len(test_df) - expected_test_rows) <= 2
    assert abs(len(validation_df) - expected_validation_rows) <= 2
    assert abs(len(train_df) - expected_train_rows) <= 2
    
    # Check that all data is accounted for
    assert len(train_df) + len(validation_df) + len(test_df) == total_rows


def test_split_dataset():
    """Test complete dataset splitting"""
    # Create test data
    features = create_test_features()
    
    # Create data splitter
    splitter = ProfitabilityDataSplitter()
    
    # Test stratified split via main method
    train_df, validation_df, test_df = splitter.split_dataset(
        features, 
        target_column='profit_margin',
        split_method='stratified',
        test_size=0.15, 
        validation_size=0.15,
        random_state=42
    )
    
    # Check results
    assert isinstance(train_df, pd.DataFrame)
    assert isinstance(validation_df, pd.DataFrame)
    assert isinstance(test_df, pd.DataFrame)
    
    # Check that all data is accounted for
    assert len(train_df) + len(validation_df) + len(test_df) == len(features)


def test_convenience_function():
    """Test the convenience function"""
    # Create test data
    features = create_test_features()
    
    # Test convenience function
    train_df, validation_df, test_df = split_profitability_data(
        features, 
        target_column='profit_margin',
        split_method='stratified',
        test_size=0.2, 
        validation_size=0.2,
        random_state=42
    )
    
    # Check results
    assert isinstance(train_df, pd.DataFrame)
    assert isinstance(validation_df, pd.DataFrame)
    assert isinstance(test_df, pd.DataFrame)
    
    # Check that all data is accounted for
    assert len(train_df) + len(validation_df) + len(test_df) == len(features)


def test_invalid_split_method():
    """Test error handling for invalid split method"""
    # Create test data
    features = create_test_features()
    
    # Create data splitter
    splitter = ProfitabilityDataSplitter()
    
    # Test invalid split method
    with pytest.raises(ValueError):
        splitter.split_dataset(
            features, 
            split_method='invalid_method'
        )


if __name__ == "__main__":
    pytest.main([__file__])