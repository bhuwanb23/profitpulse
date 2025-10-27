"""
Tests for Profitability Predictor
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime
import asyncio

# Add src to path for imports
src_path = os.path.join(os.path.dirname(__file__), '..', '..', 'src')
sys.path.insert(0, src_path)

# Conditional imports
try:
    from src.models.profitability_predictor.profitability_predictor import (
        ProfitabilityPredictor,
        ModelVersionManager,
        ABTestingFramework
    )
    PREDICTOR_AVAILABLE = True
except ImportError as e:
    print(f"Import error: {e}")
    try:
        # Try direct import
        from models.profitability_predictor.profitability_predictor import (
            ProfitabilityPredictor,
            ModelVersionManager,
            ABTestingFramework
        )
        PREDICTOR_AVAILABLE = True
    except ImportError as e2:
        print(f"Direct import error: {e2}")
        PREDICTOR_AVAILABLE = False


def create_test_client_data():
    """Create test client data"""
    return {
        'client_id': 'test_client_1',
        'contract_value': 50000.0,
        'hours_logged': 100.0,
        'billing_amount': 45000.0,
        'ticket_count': 20,
        'satisfaction_score': 4.2,
        'last_contact_days': 5,
        'service_types': ['support', 'maintenance']
    }


@pytest.mark.skipif(not PREDICTOR_AVAILABLE, reason="Profitability predictor module not available")
def test_profitability_predictor_initialization():
    """Test profitability predictor initialization"""
    predictor = ProfitabilityPredictor()
    assert predictor.model_path == "./models"
    assert predictor.db_path == "../../database/superhack.db"
    assert predictor.xgboost_model is None
    assert predictor.random_forest_model is None
    assert predictor.feature_names == []
    assert predictor.is_initialized == False
    assert predictor.active_model == "xgboost"


@pytest.mark.skipif(not PREDICTOR_AVAILABLE, reason="Profitability predictor module not available")
def test_prepare_features():
    """Test feature preparation"""
    predictor = ProfitabilityPredictor()
    
    # Create test data
    client_data = create_test_client_data()
    
    # Prepare features (this will use mock features since models aren't loaded)
    features = predictor.prepare_features(client_data)
    
    # Check results
    assert isinstance(features, pd.DataFrame)
    assert len(features) == 1  # One client


@pytest.mark.skipif(not PREDICTOR_AVAILABLE, reason="Profitability predictor module not available")
def test_model_version_manager_initialization():
    """Test model version manager initialization"""
    version_manager = ModelVersionManager()
    assert version_manager.model_registry_path == "./model_registry"
    assert isinstance(version_manager.versions, dict)
    assert isinstance(version_manager.active_versions, dict)


@pytest.mark.skipif(not PREDICTOR_AVAILABLE, reason="Profitability predictor module not available")
def test_ab_testing_framework_initialization():
    """Test A/B testing framework initialization"""
    ab_testing = ABTestingFramework()
    assert isinstance(ab_testing.experiments, dict)
    assert isinstance(ab_testing.results, dict)


@pytest.mark.skipif(not PREDICTOR_AVAILABLE, reason="Profitability predictor module not available")
def test_predict_mock():
    """Test mock prediction"""
    predictor = ProfitabilityPredictor()
    
    # Create test data
    client_data = create_test_client_data()
    
    # Make prediction (will use mock since no real models are loaded)
    result = asyncio.run(predictor.predict(client_data))
    
    # Check results
    assert isinstance(result, dict)
    assert 'prediction' in result
    assert 'model_type' in result
    assert 'prediction_time_ms' in result
    assert 'timestamp' in result
    # Prediction should be between 0 and 1 for profit margin
    assert 0 <= result['prediction'] <= 1


@pytest.mark.skipif(not PREDICTOR_AVAILABLE, reason="Profitability predictor module not available")
def test_batch_predict():
    """Test batch prediction"""
    predictor = ProfitabilityPredictor()
    
    # Create test data
    clients_data = [create_test_client_data() for _ in range(3)]
    
    # Make batch predictions
    results = asyncio.run(predictor.batch_predict(clients_data))
    
    # Check results
    assert isinstance(results, list)
    assert len(results) == 3
    for result in results:
        assert isinstance(result, dict)
        assert 'prediction' in result
        assert 0 <= result['prediction'] <= 1


@pytest.mark.skipif(not PREDICTOR_AVAILABLE, reason="Profitability predictor module not available")
def test_get_model_info():
    """Test getting model info"""
    predictor = ProfitabilityPredictor()
    
    # Get model info
    info = asyncio.run(predictor.get_model_info())
    
    # Check results
    assert isinstance(info, dict)
    assert 'models_available' in info
    assert 'active_model' in info
    assert 'feature_count' in info


@pytest.mark.skipif(not PREDICTOR_AVAILABLE, reason="Profitability predictor module not available")
def test_register_model_version():
    """Test registering model version"""
    version_manager = ModelVersionManager()
    
    # Register a model version
    success = asyncio.run(version_manager.register_model_version(
        "test_model", 
        "1.0.0", 
        "/path/to/model", 
        {"accuracy": 0.95}
    ))
    
    # Check results
    assert success == True
    assert "test_model" in version_manager.versions
    assert "1.0.0" in version_manager.versions["test_model"]


@pytest.mark.skipif(not PREDICTOR_AVAILABLE, reason="Profitability predictor module not available")
def test_create_ab_experiment():
    """Test creating A/B test experiment"""
    ab_testing = ABTestingFramework()
    
    # Create experiment
    success = asyncio.run(ab_testing.create_experiment(
        "test_experiment",
        "model_a", "1.0.0",
        "model_b", "1.0.1",
        0.5
    ))
    
    # Check results
    assert success == True
    assert "test_experiment" in ab_testing.experiments


if __name__ == "__main__":
    pytest.main([__file__])