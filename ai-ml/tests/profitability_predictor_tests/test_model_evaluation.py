"""
Tests for ProfitabilityModelEvaluator
"""

import pandas as pd
import pytest
import numpy as np

try:
    from src.models.profitability_predictor.model_evaluation import ProfitabilityModelEvaluator, calculate_profitability_metrics, evaluate_profitability_model
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("Skipping model evaluation tests - scikit-learn not available")


@pytest.mark.skipif(not SKLEARN_AVAILABLE, reason="scikit-learn not available")
def test_model_evaluator_initialization():
    """Test ProfitabilityModelEvaluator initialization"""
    evaluator = ProfitabilityModelEvaluator()
    assert evaluator is not None


@pytest.mark.skipif(not SKLEARN_AVAILABLE, reason="scikit-learn not available")
def test_calculate_r2_score():
    """Test R² score calculation"""
    evaluator = ProfitabilityModelEvaluator()
    
    # Create test data
    y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    y_pred = np.array([1.1, 2.1, 2.9, 4.1, 4.9])
    
    # Calculate R² score
    r2 = evaluator.calculate_r2_score(y_true, y_pred)
    
    # Check result (should be close to 1.0 for good predictions)
    assert isinstance(r2, float)
    assert r2 >= 0.9


@pytest.mark.skipif(not SKLEARN_AVAILABLE, reason="scikit-learn not available")
def test_calculate_mae():
    """Test MAE calculation"""
    evaluator = ProfitabilityModelEvaluator()
    
    # Create test data
    y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    y_pred = np.array([1.1, 2.1, 2.9, 4.1, 4.9])
    
    # Calculate MAE
    mae = evaluator.calculate_mae(y_true, y_pred)
    
    # Check result (should be small for good predictions)
    assert isinstance(mae, float)
    assert mae > 0
    assert mae < 1.0


@pytest.mark.skipif(not SKLEARN_AVAILABLE, reason="scikit-learn not available")
def test_calculate_rmse():
    """Test RMSE calculation"""
    evaluator = ProfitabilityModelEvaluator()
    
    # Create test data
    y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    y_pred = np.array([1.1, 2.1, 2.9, 4.1, 4.9])
    
    # Calculate RMSE
    rmse = evaluator.calculate_rmse(y_true, y_pred)
    
    # Check result (should be small for good predictions)
    assert isinstance(rmse, float)
    assert rmse > 0
    assert rmse < 1.0


@pytest.mark.skipif(not SKLEARN_AVAILABLE, reason="scikit-learn not available")
def test_calculate_mape():
    """Test MAPE calculation"""
    evaluator = ProfitabilityModelEvaluator()
    
    # Create test data
    y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    y_pred = np.array([1.1, 2.1, 2.9, 4.1, 4.9])
    
    # Calculate MAPE
    mape = evaluator.calculate_mape(y_true, y_pred)
    
    # Check result (should be small for good predictions)
    assert isinstance(mape, float)
    assert mape > 0
    assert mape < 0.5  # 50% error would be very high


@pytest.mark.skipif(not SKLEARN_AVAILABLE, reason="scikit-learn not available")
def test_calculate_all_metrics():
    """Test calculation of all metrics"""
    evaluator = ProfitabilityModelEvaluator()
    
    # Create test data
    y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    y_pred = np.array([1.1, 2.1, 2.9, 4.1, 4.9])
    
    # Calculate all metrics
    metrics = evaluator.calculate_all_metrics(y_true, y_pred)
    
    # Check results
    assert isinstance(metrics, dict)
    assert 'r2' in metrics
    assert 'mae' in metrics
    assert 'rmse' in metrics
    assert 'mape' in metrics
    assert all(isinstance(v, float) for v in metrics.values())


@pytest.mark.skipif(not SKLEARN_AVAILABLE, reason="scikit-learn not available")
def test_evaluate_model_performance():
    """Test model performance evaluation"""
    evaluator = ProfitabilityModelEvaluator()
    
    # Create test data
    y_true = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    y_pred = np.array([0.11, 0.19, 0.31, 0.39, 0.51, 0.59, 0.71, 0.79, 0.91, 0.99])
    
    # Evaluate model performance
    evaluation = evaluator.evaluate_model_performance(y_true, y_pred, "Test Model")
    
    # Check results
    assert isinstance(evaluation, dict)
    assert 'model_name' in evaluation
    assert 'metrics' in evaluation
    assert 'residual_statistics' in evaluation
    assert 'performance_level' in evaluation
    assert 'sample_size' in evaluation
    assert evaluation['model_name'] == "Test Model"
    assert evaluation['sample_size'] == len(y_true)
    assert evaluation['performance_level'] in ["Excellent", "Good", "Fair", "Poor"]


@pytest.mark.skipif(not SKLEARN_AVAILABLE, reason="scikit-learn not available")
def test_convenience_functions():
    """Test convenience functions"""
    # Create test data
    y_true = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
    y_pred = np.array([0.11, 0.19, 0.31, 0.39, 0.51])
    
    # Test metrics calculation function
    metrics = calculate_profitability_metrics(y_true, y_pred)
    assert isinstance(metrics, dict)
    assert 'r2' in metrics
    assert 'mae' in metrics
    assert 'rmse' in metrics
    assert 'mape' in metrics
    
    # Test model evaluation function
    evaluation = evaluate_profitability_model(y_true, y_pred, "Convenience Test")
    assert isinstance(evaluation, dict)
    assert 'model_name' in evaluation
    assert 'metrics' in evaluation
    assert evaluation['model_name'] == "Convenience Test"


if __name__ == "__main__":
    if SKLEARN_AVAILABLE:
        pytest.main([__file__])
    else:
        print("Skipping tests - scikit-learn not available")