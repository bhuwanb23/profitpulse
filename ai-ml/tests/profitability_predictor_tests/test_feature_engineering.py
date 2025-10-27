"""
Tests for ProfitabilityFeatureEngineer
"""

import pandas as pd
import pytest
import tempfile
import sqlite3
import os
from datetime import datetime

from src.models.profitability_predictor.feature_engineering import ProfitabilityFeatureEngineer, engineer_profitability_features


def create_test_financial_data():
    """Create test financial data"""
    # Create sample financial data
    data = {
        'id': ['client_1', 'client_2', 'client_3'],
        'name': ['Acme Corp', 'TechStart Inc', 'Global Solutions'],
        'industry': ['Manufacturing', 'Technology', 'Finance'],
        'contract_type': ['annual', 'monthly', 'quarterly'],
        'contract_value': [50000.0, 5000.0, 25000.0],
        'start_date': ['2023-01-01', '2023-03-01', '2023-02-01'],
        'end_date': ['2023-12-31', None, '2023-11-30'],
        'is_active': [True, True, False],
        'total_revenue': [45000.0, 6000.0, 20000.0],
        'total_costs': [30000.0, 4000.0, 15000.0],
        'profit': [15000.0, 2000.0, 5000.0],
        'profit_margin': [0.33, 0.33, 0.25],
        'service_count': [10, 5, 8],
        'total_service_value': [10000.0, 5000.0, 8000.0],
        'total_quantity': [100, 50, 80],
        'revenue_per_service': [4500.0, 1200.0, 2500.0],
        'cost_per_service': [3000.0, 800.0, 1875.0]
    }
    
    return pd.DataFrame(data)


def test_feature_engineer_initialization():
    """Test ProfitabilityFeatureEngineer initialization"""
    engineer = ProfitabilityFeatureEngineer()
    assert engineer.db_path == "../../database/superhack.db"
    
    engineer = ProfitabilityFeatureEngineer("/custom/path.db")
    assert engineer.db_path == "/custom/path.db"


def test_create_financial_features():
    """Test creating financial features"""
    # Create test data
    financial_data = create_test_financial_data()
    
    # Create feature engineer
    engineer = ProfitabilityFeatureEngineer()
    
    # Create financial features
    features_df = engineer.create_financial_features(financial_data)
    
    # Check results
    assert isinstance(features_df, pd.DataFrame)
    assert len(features_df) == len(financial_data)
    assert 'revenue_to_contract_value_ratio' in features_df.columns
    assert 'cost_to_revenue_ratio' in features_df.columns
    assert 'revenue_stability_score' in features_df.columns
    assert 'contract_value_efficiency' in features_df.columns
    assert 'avg_service_profitability' in features_df.columns
    assert 'revenue_concentration_risk' in features_df.columns
    
    # Check specific calculations
    client_1_data = features_df[features_df['id'] == 'client_1'].iloc[0]
    assert client_1_data['revenue_to_contract_value_ratio'] == 45000.0 / 50000.0
    assert client_1_data['cost_to_revenue_ratio'] == 30000.0 / 45000.0


def test_create_operational_features():
    """Test creating operational features"""
    # Create test data
    financial_data = create_test_financial_data()
    
    # Create feature engineer
    engineer = ProfitabilityFeatureEngineer()
    
    # Create operational features
    features_df = engineer.create_operational_features(financial_data)
    
    # Check results
    assert isinstance(features_df, pd.DataFrame)
    assert len(features_df) == len(financial_data)
    assert 'service_utilization_efficiency' in features_df.columns
    assert 'cost_efficiency_per_service' in features_df.columns
    assert 'revenue_efficiency_per_service' in features_df.columns


def test_create_temporal_features():
    """Test creating temporal features"""
    # Create test data
    financial_data = create_test_financial_data()
    
    # Create feature engineer
    engineer = ProfitabilityFeatureEngineer()
    
    # Create temporal features
    features_df = engineer.create_temporal_features(financial_data)
    
    # Check results
    assert isinstance(features_df, pd.DataFrame)
    assert len(features_df) == len(financial_data)
    assert 'contract_duration_days' in features_df.columns
    assert 'contract_age_days' in features_df.columns
    assert 'days_until_contract_end' in features_df.columns
    assert 'revenue_velocity' in features_df.columns


def test_create_categorical_features():
    """Test creating categorical features"""
    # Create test data
    financial_data = create_test_financial_data()
    
    # Create feature engineer
    engineer = ProfitabilityFeatureEngineer()
    
    # Create categorical features
    features_df = engineer.create_categorical_features(financial_data)
    
    # Check results
    assert isinstance(features_df, pd.DataFrame)
    assert len(features_df) == len(financial_data)
    assert 'contract_type_annual' in features_df.columns
    assert 'contract_type_monthly' in features_df.columns
    assert 'contract_type_quarterly' in features_df.columns
    assert 'industry_Manufacturing' in features_df.columns
    assert 'industry_Technology' in features_df.columns
    assert 'industry_Finance' in features_df.columns
    assert 'is_active_binary' in features_df.columns


def test_create_interaction_features():
    """Test creating interaction features"""
    # Create test data
    financial_data = create_test_financial_data()
    
    # Create feature engineer
    engineer = ProfitabilityFeatureEngineer()
    
    # Create interaction features
    features_df = engineer.create_interaction_features(financial_data)
    
    # Check results
    assert isinstance(features_df, pd.DataFrame)
    assert len(features_df) == len(financial_data)
    assert 'revenue_cost_interaction' in features_df.columns
    assert 'profit_contract_interaction' in features_df.columns
    assert 'margin_service_interaction' in features_df.columns


def test_engineer_features():
    """Test complete feature engineering pipeline"""
    # Create test data
    financial_data = create_test_financial_data()
    
    # Create feature engineer
    engineer = ProfitabilityFeatureEngineer()
    
    # Engineer all features
    features_df = engineer.engineer_features(financial_data)
    
    # Check results
    assert isinstance(features_df, pd.DataFrame)
    assert len(features_df) == len(financial_data)
    # Check that we have more features than original columns
    assert len(features_df.columns) > len(financial_data.columns)
    
    # Check that all expected feature types are present
    expected_feature_types = [
        'revenue_to_contract_value_ratio',  # Financial
        'service_utilization_efficiency',   # Operational
        'contract_duration_days',           # Temporal
        'contract_type_annual',             # Categorical
        'revenue_cost_interaction'          # Interaction
    ]
    
    for feature in expected_feature_types:
        assert feature in features_df.columns


def test_convenience_function():
    """Test the convenience function"""
    # Create test data
    financial_data = create_test_financial_data()
    
    # Test convenience function
    features_df = engineer_profitability_features(financial_data)
    
    # Check results
    assert isinstance(features_df, pd.DataFrame)
    assert len(features_df) == len(financial_data)
    assert len(features_df.columns) > len(financial_data.columns)


if __name__ == "__main__":
    pytest.main([__file__])