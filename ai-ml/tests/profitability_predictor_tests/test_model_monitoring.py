"""
Tests for Model Performance Monitoring
"""

import pytest
import numpy as np
import pandas as pd
import sys
import os
from datetime import datetime, timedelta

# Add src to path for imports
src_path = os.path.join(os.path.dirname(__file__), '..', '..', 'src')
sys.path.insert(0, src_path)

# Conditional imports
MONITORING_AVAILABLE = False
try:
    from src.models.profitability_predictor.model_monitoring import (
        ProfitabilityModelMonitor, 
        FeatureImportanceAnalyzer
    )
    MONITORING_AVAILABLE = True
except ImportError as e:
    print(f"Import error: {e}")
    try:
        # Try direct import
        from models.profitability_predictor.model_monitoring import (
            ProfitabilityModelMonitor, 
            FeatureImportanceAnalyzer
        )
        MONITORING_AVAILABLE = True
    except ImportError as e2:
        print(f"Direct import error: {e2}")
        MONITORING_AVAILABLE = False


@pytest.mark.skipif(not MONITORING_AVAILABLE, reason="Model monitoring module not available")
def test_model_monitor_initialization():
    """Test model monitor initialization"""
    monitor = ProfitabilityModelMonitor()
    assert monitor.initialized == True
    assert isinstance(monitor.performance_history, list)
    assert isinstance(monitor.alerts, list)


@pytest.mark.skipif(not MONITORING_AVAILABLE, reason="Model monitoring module not available")
def test_performance_metrics_calculation():
    """Test performance metrics calculation"""
    monitor = ProfitabilityModelMonitor()
    
    # Create test data
    y_true = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
    y_pred = np.array([0.12, 0.18, 0.32, 0.38, 0.52])
    
    # Calculate metrics
    metrics = monitor.calculate_performance_metrics(y_true, y_pred)
    
    # Check results
    assert isinstance(metrics, dict)
    assert 'r2' in metrics
    assert 'mae' in metrics
    assert 'rmse' in metrics
    assert 'mape' in metrics
    
    # Check that metrics are reasonable
    assert -1 <= metrics['r2'] <= 1  # R² should be between -1 and 1
    assert metrics['mae'] >= 0  # MAE should be non-negative
    assert metrics['rmse'] >= 0  # RMSE should be non-negative
    assert metrics['mape'] >= 0  # MAPE should be non-negative


@pytest.mark.skipif(not MONITORING_AVAILABLE, reason="Model monitoring module not available")
def test_performance_drift_detection():
    """Test performance drift detection"""
    monitor = ProfitabilityModelMonitor()
    
    # Create baseline and current metrics
    baseline_metrics = {
        'r2': 0.90,
        'mae': 0.05,
        'rmse': 0.08
    }
    
    current_metrics = {
        'r2': 0.85,  # Slight degradation
        'mae': 0.06,  # Slight increase
        'rmse': 0.09   # Slight increase
    }
    
    # Detect drift
    drift_results = monitor.detect_performance_drift(current_metrics, baseline_metrics)
    
    # Check results
    assert isinstance(drift_results, dict)
    assert 'drift_detected' in drift_results
    assert 'drift_details' in drift_results
    assert 'recommendations' in drift_results


@pytest.mark.skipif(not MONITORING_AVAILABLE, reason="Model monitoring module not available")
def test_prediction_quality_monitoring():
    """Test prediction quality monitoring"""
    monitor = ProfitabilityModelMonitor()
    
    # Create test predictions
    predictions = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
    
    # Monitor quality without actuals
    quality_report = monitor.monitor_prediction_quality(predictions)
    
    # Check results
    assert isinstance(quality_report, dict)
    assert 'prediction_count' in quality_report
    assert 'prediction_stats' in quality_report
    assert quality_report['prediction_count'] == len(predictions)
    
    # Monitor quality with actuals
    actuals = np.array([0.12, 0.18, 0.32, 0.38, 0.52, 0.58, 0.72, 0.78, 0.88])
    quality_report_with_actuals = monitor.monitor_prediction_quality(predictions, actuals)
    
    # Check results
    assert isinstance(quality_report_with_actuals, dict)
    assert 'accuracy_metrics' in quality_report_with_actuals


@pytest.mark.skipif(not MONITORING_AVAILABLE, reason="Model monitoring module not available")
def test_performance_report_generation():
    """Test performance report generation"""
    monitor = ProfitabilityModelMonitor()
    
    # Add some performance history
    monitor.performance_history = [
        {
            'timestamp': datetime.now() - timedelta(days=2),
            'metrics': {'r2': 0.85, 'mae': 0.06, 'rmse': 0.09}
        },
        {
            'timestamp': datetime.now() - timedelta(days=1),
            'metrics': {'r2': 0.87, 'mae': 0.05, 'rmse': 0.08}
        },
        {
            'timestamp': datetime.now(),
            'metrics': {'r2': 0.88, 'mae': 0.04, 'rmse': 0.07}
        }
    ]
    
    # Generate report
    report = monitor.generate_performance_report(period_days=7)
    
    # Check results
    assert isinstance(report, dict)
    assert 'report_period' in report
    assert 'performance_trends' in report
    assert 'recent_performance' in report


@pytest.mark.skipif(not MONITORING_AVAILABLE, reason="Model monitoring module not available")
def test_feature_importance_analyzer_initialization():
    """Test feature importance analyzer initialization"""
    analyzer = FeatureImportanceAnalyzer()
    assert isinstance(analyzer.feature_importance_history, list)
    assert isinstance(analyzer.baseline_importance, dict)


@pytest.mark.skipif(not MONITORING_AVAILABLE, reason="Model monitoring module not available")
def test_feature_importance_analysis():
    """Test feature importance analysis"""
    analyzer = FeatureImportanceAnalyzer()
    
    # Create mock model with feature importances
    class MockModel:
        def __init__(self):
            self.feature_importances_ = np.array([0.3, 0.25, 0.2, 0.15, 0.1])
    
    model = MockModel()
    feature_names = ['feature1', 'feature2', 'feature3', 'feature4', 'feature5']
    
    # Analyze feature importance
    analysis = analyzer.analyze_feature_importance(model, feature_names)
    
    # Check results
    assert isinstance(analysis, dict)
    assert 'feature_importance' in analysis
    assert 'top_features' in analysis
    assert 'feature_stats' in analysis
    assert len(analysis['feature_importance']) == len(feature_names)


@pytest.mark.skipif(not MONITORING_AVAILABLE, reason="Model monitoring module not available")
def test_feature_importance_comparison():
    """Test feature importance comparison"""
    analyzer = FeatureImportanceAnalyzer()
    
    # Create current and baseline importance
    current_importance = {
        'feature1': 0.35,
        'feature2': 0.25,
        'feature3': 0.20,
        'feature4': 0.10,
        'feature5': 0.10
    }
    
    baseline_importance = {
        'feature1': 0.30,
        'feature2': 0.25,
        'feature3': 0.25,
        'feature4': 0.10,
        'feature5': 0.10
    }
    
    # Compare importance
    comparison = analyzer.compare_feature_importance(current_importance, baseline_importance)
    
    # Check results
    assert isinstance(comparison, dict)
    assert 'significant_changes' in comparison
    assert 'new_features' in comparison
    assert 'removed_features' in comparison
    assert 'stable_features' in comparison


if __name__ == "__main__":
    pytest.main([__file__])