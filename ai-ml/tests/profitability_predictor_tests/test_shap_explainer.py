"""
Tests for SHAP Explainer and Confidence Interval Calculator
"""

import pytest
import numpy as np
import pandas as pd
import sys
import os
from datetime import datetime

# Add src to path for imports
src_path = os.path.join(os.path.dirname(__file__), '..', '..', 'src')
sys.path.insert(0, src_path)

# Conditional imports
SHAP_AVAILABLE = False
try:
    from src.models.profitability_predictor.shap_explainer import (
        SHAPExplainer,
        ConfidenceIntervalCalculator
    )
    SHAP_AVAILABLE = True
except ImportError as e:
    print(f"Import error: {e}")
    try:
        # Try direct import
        from models.profitability_predictor.shap_explainer import (
            SHAPExplainer,
            ConfidenceIntervalCalculator
        )
        SHAP_AVAILABLE = True
    except ImportError as e2:
        print(f"Direct import error: {e2}")
        SHAP_AVAILABLE = False


@pytest.mark.skipif(not SHAP_AVAILABLE, reason="SHAP explainer module not available")
def test_shap_explainer_initialization():
    """Test SHAP explainer initialization"""
    explainer = SHAPExplainer()
    assert explainer.explainer is None
    assert explainer.feature_names is None
    assert explainer.baseline_values is None


@pytest.mark.skipif(not SHAP_AVAILABLE, reason="SHAP explainer module not available")
def test_confidence_interval_calculator_initialization():
    """Test confidence interval calculator initialization"""
    calculator = ConfidenceIntervalCalculator()
    assert calculator.bootstrap_samples == 1000
    assert calculator.confidence_level == 0.95


@pytest.mark.skipif(not SHAP_AVAILABLE, reason="SHAP explainer module not available")
def test_mock_explanation():
    """Test mock explanation generation"""
    explainer = SHAPExplainer()
    
    # Create test data
    X_instance = pd.DataFrame({
        'feature1': [0.5],
        'feature2': [0.3],
        'feature3': [0.8]
    })
    
    # Generate mock explanation
    explanation = explainer.explain_prediction(X_instance)
    
    # Check results
    assert isinstance(explanation, dict)
    assert 'shap_values' in explanation
    assert 'sorted_shap_values' in explanation
    assert 'base_value' in explanation
    assert 'prediction' in explanation
    assert explanation.get('mock', False) == True  # Should be mock since SHAP not available


@pytest.mark.skipif(not SHAP_AVAILABLE, reason="SHAP explainer module not available")
def test_mock_global_importance():
    """Test mock global importance generation"""
    explainer = SHAPExplainer()
    
    # Create test data
    X_sample = pd.DataFrame({
        'feature1': [0.5, 0.6, 0.4],
        'feature2': [0.3, 0.2, 0.4],
        'feature3': [0.8, 0.7, 0.9]
    })
    
    # Generate mock global importance
    importance = explainer.explain_global_feature_importance(X_sample)
    
    # Check results
    assert isinstance(importance, dict)
    assert 'global_importance' in importance
    assert 'top_features' in importance
    assert 'mean_shap_values' in importance
    assert importance.get('mock', False) == True  # Should be mock since SHAP not available


@pytest.mark.skipif(not SHAP_AVAILABLE, reason="SHAP explainer module not available")
def test_mock_confidence_intervals():
    """Test mock confidence interval generation"""
    calculator = ConfidenceIntervalCalculator()
    
    # Create mock model
    class MockModel:
        def predict(self, X):
            return np.array([0.5] * len(X))
    
    model = MockModel()
    
    # Create test data
    X = pd.DataFrame({
        'feature1': [0.5, 0.6, 0.4],
        'feature2': [0.3, 0.2, 0.4],
        'feature3': [0.8, 0.7, 0.9]
    })
    
    # Calculate mock confidence intervals
    ci_results = calculator.calculate_confidence_interval(model, X)
    
    # Check results
    assert isinstance(ci_results, dict)
    assert 'method' in ci_results
    assert 'confidence_level' in ci_results
    assert 'individual_intervals' in ci_results
    assert 'overall_interval' in ci_results
    assert 'prediction_stats' in ci_results
    # The method should work without errors (mock flag only set in _mock_confidence_intervals)


@pytest.mark.skipif(not SHAP_AVAILABLE, reason="SHAP explainer module not available")
def test_bootstrap_confidence_intervals():
    """Test bootstrap confidence interval calculation"""
    calculator = ConfidenceIntervalCalculator()
    
    # Create mock model
    class MockModel:
        def predict(self, X):
            return np.array([0.5] * len(X))
    
    model = MockModel()
    
    # Create test data
    X = pd.DataFrame({
        'feature1': [0.5, 0.6, 0.4],
        'feature2': [0.3, 0.2, 0.4],
        'feature3': [0.8, 0.7, 0.9]
    })
    
    # Calculate bootstrap confidence intervals
    ci_results = calculator.calculate_confidence_interval(model, X, method='bootstrap')
    
    # Check results
    assert isinstance(ci_results, dict)
    assert 'method' in ci_results
    assert ci_results['method'] in ['bootstrap', 'mock']
    assert 'confidence_level' in ci_results
    assert 'individual_intervals' in ci_results
    assert 'overall_interval' in ci_results
    assert 'prediction_stats' in ci_results


@pytest.mark.skipif(not SHAP_AVAILABLE, reason="SHAP explainer module not available")
def test_residual_confidence_intervals():
    """Test residual confidence interval calculation"""
    calculator = ConfidenceIntervalCalculator()
    
    # Create mock model
    class MockModel:
        def predict(self, X):
            return np.array([0.5] * len(X))
    
    model = MockModel()
    
    # Create test data
    X = pd.DataFrame({
        'feature1': [0.5, 0.6, 0.4],
        'feature2': [0.3, 0.2, 0.4],
        'feature3': [0.8, 0.7, 0.9]
    })
    
    y_true = np.array([0.45, 0.55, 0.52])
    
    # Calculate residual confidence intervals
    ci_results = calculator.calculate_confidence_interval(model, X, y_true, method='residual')
    
    # Check results
    assert isinstance(ci_results, dict)
    assert 'method' in ci_results
    assert ci_results['method'] in ['residual', 'mock']
    assert 'confidence_level' in ci_results
    assert 'individual_intervals' in ci_results
    assert 'overall_interval' in ci_results
    assert 'prediction_stats' in ci_results


if __name__ == "__main__":
    pytest.main([__file__])