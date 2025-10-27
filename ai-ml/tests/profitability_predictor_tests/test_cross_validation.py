"""
Tests for CrossValidator
"""

import pandas as pd
import pytest
import numpy as np

try:
    from src.models.profitability_predictor.cross_validation import CrossValidator, perform_cross_validation, compare_cross_validation_methods
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("Skipping cross-validation tests - scikit-learn not available")


def create_test_data():
    """Create test data for cross-validation"""
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
def test_cross_validator_initialization():
    """Test CrossValidator initialization"""
    validator = CrossValidator()
    assert validator is not None


@pytest.mark.skipif(not SKLEARN_AVAILABLE, reason="scikit-learn not available")
def test_compare_cv_methods():
    """Test comparison of CV methods"""
    validator = CrossValidator()
    
    # Create test results
    cv_results = [
        {
            'cv_method': 'k-fold',
            'mean_score': 0.85,
            'std_score': 0.05,
            'scores': [0.80, 0.85, 0.90, 0.82, 0.88]
        },
        {
            'cv_method': 'stratified',
            'mean_score': 0.92,
            'std_score': 0.03,
            'scores': [0.89, 0.91, 0.93, 0.90, 0.92]
        }
    ]
    
    # Compare methods
    comparison = validator.compare_cv_methods(cv_results)
    
    assert isinstance(comparison, dict)
    assert 'best_method' in comparison
    assert 'all_methods' in comparison
    assert 'overall_statistics' in comparison
    assert 'method_comparison' in comparison
    assert comparison['best_method']['mean_score'] == 0.92


@pytest.mark.skipif(not SKLEARN_AVAILABLE, reason="scikit-learn not available")
def test_convenience_functions():
    """Test convenience functions"""
    # Create test results
    cv_results = [
        {
            'cv_method': 'k-fold',
            'mean_score': 0.85,
            'std_score': 0.05,
            'scores': [0.80, 0.85, 0.90, 0.82, 0.88]
        },
        {
            'cv_method': 'stratified',
            'mean_score': 0.92,
            'std_score': 0.03,
            'scores': [0.89, 0.91, 0.93, 0.90, 0.92]
        }
    ]
    
    # Test comparison function
    comparison = compare_cross_validation_methods(cv_results)
    assert isinstance(comparison, dict)
    assert 'best_method' in comparison
    assert comparison['best_method']['mean_score'] == 0.92


if __name__ == "__main__":
    if SKLEARN_AVAILABLE:
        pytest.main([__file__])
    else:
        print("Skipping tests - scikit-learn not available")