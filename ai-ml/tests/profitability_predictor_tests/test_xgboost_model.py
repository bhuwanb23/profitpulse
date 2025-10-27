"""
Tests for XGBoostProfitabilityModel
"""

import pandas as pd
import pytest
import numpy as np
import tempfile
import os

try:
    from src.models.profitability_predictor.xgboost_model import XGBoostProfitabilityModel, train_xgboost_profitability_model, predict_with_xgboost_model
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("Skipping XGBoost tests - XGBoost not available")


def create_test_data():
    """Create test data for model training"""
    np.random.seed(42)
    n_samples = 100
    
    data = {
        'id': [f'client_{i}' for i in range(n_samples)],
        'contract_value': np.random.uniform(1000, 50000, n_samples),
        'total_revenue': np.random.uniform(500, 45000, n_samples),
        'total_costs': np.random.uniform(100, 30000, n_samples),
        'service_count': np.random.randint(1, 20, n_samples),
        'contract_type': np.random.choice(['annual', 'monthly', 'quarterly'], n_samples),
        'industry': np.random.choice(['Technology', 'Finance', 'Healthcare', 'Manufacturing'], n_samples),
        'is_active': np.random.choice([True, False], n_samples)
    }
    
    # Create target variable with some relationship to features
    data['profit_margin'] = (
        0.1 + 
        0.2 * (data['total_revenue'] / np.maximum(data['contract_value'], 1)) +
        0.1 * (data['service_count'] / 20) +
        np.random.normal(0, 0.05, n_samples)
    )
    # Ensure profit margin is between 0 and 1
    data['profit_margin'] = np.clip(data['profit_margin'], 0, 1)
    
    return pd.DataFrame(data)


@pytest.mark.skipif(not XGBOOST_AVAILABLE, reason="XGBoost not available")
def test_xgboost_model_initialization():
    """Test XGBoostProfitabilityModel initialization"""
    model = XGBoostProfitabilityModel()
    assert model is not None
    assert not model.is_trained


@pytest.mark.skipif(not XGBOOST_AVAILABLE, reason="XGBoost not available")
def test_prepare_features():
    """Test feature preparation"""
    # Create test data
    data = create_test_data().head(10)
    
    # Create model
    model = XGBoostProfitabilityModel()
    
    # Prepare features
    features_df = model.prepare_features(data)
    
    # Check results
    assert isinstance(features_df, pd.DataFrame)
    assert len(features_df) == len(data)
    # Check that non-feature columns were removed
    assert 'id' not in features_df.columns
    assert 'name' not in features_df.columns
    # Check that categorical variables were encoded
    assert 'contract_type_annual' in features_df.columns or len(features_df.select_dtypes(include=['object']).columns) == 0


@pytest.mark.skipif(not XGBOOST_AVAILABLE, reason="XGBoost not available")
def test_model_training():
    """Test model training"""
    # Create test data
    data = create_test_data()
    train_data = data.head(80)
    val_data = data.tail(20)
    
    # Create model
    model = XGBoostProfitabilityModel()
    
    # Train model
    results = model.train(train_data, 'profit_margin', val_data)
    
    # Check results
    assert model.is_trained
    assert 'training_metrics' in results
    assert 'validation_metrics' in results
    assert results['training_metrics']['r2'] >= 0  # R² should be non-negative
    assert results['validation_metrics']['r2'] >= 0  # R² should be non-negative


@pytest.mark.skipif(not XGBOOST_AVAILABLE, reason="XGBoost not available")
def test_model_prediction():
    """Test model prediction"""
    # Create test data
    data = create_test_data()
    train_data = data.head(80)
    test_data = data.tail(20)
    
    # Create and train model
    model = XGBoostProfitabilityModel()
    model.train(train_data, 'profit_margin')
    
    # Make predictions
    predictions = model.predict(test_data)
    
    # Check results
    assert isinstance(predictions, np.ndarray)
    assert len(predictions) == len(test_data)
    # Check that predictions are reasonable (between 0 and 1 for profit margin)
    assert np.all(predictions >= 0)
    assert np.all(predictions <= 1)


@pytest.mark.skipif(not XGBOOST_AVAILABLE, reason="XGBoost not available")
def test_feature_importance():
    """Test feature importance extraction"""
    # Create test data
    data = create_test_data()
    train_data = data.head(80)
    
    # Create and train model
    model = XGBoostProfitabilityModel()
    model.train(train_data, 'profit_margin')
    
    # Get feature importance
    importance = model.get_feature_importance()
    
    # Check results
    assert isinstance(importance, dict)
    # Should have some features with importance scores
    assert len(importance) > 0


@pytest.mark.skipif(not XGBOOST_AVAILABLE, reason="XGBoost not available")
def test_model_save_load():
    """Test model saving and loading"""
    # Create test data
    data = create_test_data()
    train_data = data.head(80)
    
    # Create and train model
    model = XGBoostProfitabilityModel()
    model.train(train_data, 'profit_margin')
    
    # Save model
    temp_file = tempfile.NamedTemporaryFile(suffix='.pkl', delete=False)
    temp_file.close()
    
    try:
        model.save_model(temp_file.name)
        assert os.path.exists(temp_file.name)
        
        # Load model
        loaded_model = XGBoostProfitabilityModel(temp_file.name)
        assert loaded_model.is_trained
        
        # Test that loaded model can make predictions
        test_data = data.tail(10)
        predictions = loaded_model.predict(test_data)
        assert isinstance(predictions, np.ndarray)
        assert len(predictions) == len(test_data)
        
    finally:
        # Clean up
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)


@pytest.mark.skipif(not XGBOOST_AVAILABLE, reason="XGBoost not available")
def test_convenience_functions():
    """Test convenience functions"""
    # Create test data
    data = create_test_data()
    train_data = data.head(80)
    val_data = data.tail(20)
    
    # Test training function
    temp_file = tempfile.NamedTemporaryFile(suffix='.pkl', delete=False)
    temp_file.close()
    
    try:
        model, results = train_xgboost_profitability_model(
            train_data, 
            'profit_margin', 
            val_data,
            model_path=temp_file.name
        )
        
        # Check results
        assert model.is_trained
        assert 'training_metrics' in results
        assert os.path.exists(temp_file.name)
        
        # Test prediction function
        predictions = predict_with_xgboost_model(temp_file.name, val_data.head(5))
        assert isinstance(predictions, np.ndarray)
        assert len(predictions) == 5
        
    finally:
        # Clean up
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)


if __name__ == "__main__":
    if XGBOOST_AVAILABLE:
        pytest.main([__file__])
    else:
        print("Skipping tests - XGBoost not available")