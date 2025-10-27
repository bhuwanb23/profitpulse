"""
Tests for HyperparameterTuner
"""

import pandas as pd
import pytest
import numpy as np

try:
    from src.models.profitability_predictor.hyperparameter_tuning import HyperparameterTuner, tune_profitability_model, compare_model_tuning_results
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("Skipping hyperparameter tuning tests - scikit-learn not available")


def create_test_data():
    """Create test data for model tuning"""
    np.random.seed(42)
    n_samples = 50  # Smaller dataset for faster testing
    
    X = pd.DataFrame({
        'feature_1': np.random.uniform(0, 1, n_samples),
        'feature_2': np.random.uniform(0, 1, n_samples),
        'feature_3': np.random.uniform(0, 1, n_samples),
        'feature_4': np.random.uniform(0, 1, n_samples)
    })
    
    y = np.random.uniform(0, 1, n_samples)
    
    return X, y


@pytest.mark.skipif(not SKLEARN_AVAILABLE, reason="scikit-learn not available")
def test_hyperparameter_tuner_initialization():
    """Test HyperparameterTuner initialization"""
    tuner = HyperparameterTuner()
    assert tuner is not None


@pytest.mark.skipif(not SKLEARN_AVAILABLE, reason="scikit-learn not available")
def test_create_xgboost_param_grid():
    """Test XGBoost parameter grid creation"""
    tuner = HyperparameterTuner()
    param_grid = tuner.create_xgboost_param_grid()
    
    assert isinstance(param_grid, dict)
    assert 'n_estimators' in param_grid
    assert 'max_depth' in param_grid
    assert 'learning_rate' in param_grid
    assert len(param_grid) >= 5


@pytest.mark.skipif(not SKLEARN_AVAILABLE, reason="scikit-learn not available")
def test_create_random_forest_param_grid():
    """Test Random Forest parameter grid creation"""
    tuner = HyperparameterTuner()
    param_grid = tuner.create_random_forest_param_grid()
    
    assert isinstance(param_grid, dict)
    assert 'n_estimators' in param_grid
    assert 'max_depth' in param_grid
    assert 'min_samples_split' in param_grid
    assert len(param_grid) >= 5


@pytest.mark.skipif(not SKLEARN_AVAILABLE, reason="scikit-learn not available")
def test_compare_tuning_results():
    """Test comparison of tuning results"""
    tuner = HyperparameterTuner()
    
    # Create test results
    results_list = [
        {
            'model_name': 'Model 1',
            'best_score': 0.85,
            'best_params': {'param1': 1}
        },
        {
            'model_name': 'Model 2',
            'best_score': 0.92,
            'best_params': {'param1': 2}
        },
        {
            'model_name': 'Model 3',
            'best_score': 0.78,
            'best_params': {'param1': 3}
        }
    ]
    
    # Compare results
    comparison = tuner.compare_tuning_results(results_list)
    
    assert isinstance(comparison, dict)
    assert 'best_result' in comparison
    assert 'total_experiments' in comparison
    assert 'score_range' in comparison
    assert 'all_results' in comparison
    assert comparison['best_result']['best_score'] == 0.92


@pytest.mark.skipif(not SKLEARN_AVAILABLE, reason="scikit-learn not available")
def test_convenience_functions():
    """Test convenience functions"""
    # Create test results
    results_list = [
        {
            'model_name': 'Model 1',
            'best_score': 0.85,
            'best_params': {'param1': 1}
        },
        {
            'model_name': 'Model 2',
            'best_score': 0.92,
            'best_params': {'param1': 2}
        }
    ]
    
    # Test comparison function
    comparison = compare_model_tuning_results(results_list)
    assert isinstance(comparison, dict)
    assert 'best_result' in comparison
    assert comparison['best_result']['best_score'] == 0.92


if __name__ == "__main__":
    if SKLEARN_AVAILABLE:
        pytest.main([__file__])
    else:
        print("Skipping tests - scikit-learn not available")