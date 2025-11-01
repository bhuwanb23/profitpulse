"""
Tests for Capacity Planner Module
"""

import sys
import os
import unittest
import pandas as pd
import numpy as np
from datetime import datetime

# Add the src directory to the path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
sys.path.insert(0, src_path)

from src.models.demand_forecaster.capacity_planner import (
    ForecastMonitor,
    ModelDriftDetector,
    AlertSystem
)


class TestCapacityPlanner(unittest.TestCase):
    """Tests for capacity planner components"""
    
    def test_forecast_monitor_initialization(self):
        """Test ForecastMonitor initialization"""
        monitor = ForecastMonitor()
        self.assertIsNotNone(monitor)
    
    def test_model_drift_detector_initialization(self):
        """Test ModelDriftDetector initialization"""
        detector = ModelDriftDetector()
        self.assertIsNotNone(detector)
        self.assertTrue(hasattr(detector, 'threshold'))
    
    def test_alert_system_initialization(self):
        """Test AlertSystem initialization"""
        alert_system = AlertSystem()
        self.assertIsNotNone(alert_system)
        self.assertTrue(hasattr(alert_system, 'deviation_threshold'))
    
    def test_accuracy_metrics_calculation(self):
        """Test accuracy metrics calculation"""
        monitor = ForecastMonitor()
        
        # Create test data
        actual_values = [10.0, 15.0, 20.0, 25.0, 30.0]
        predicted_values = [12.0, 14.0, 18.0, 27.0, 32.0]
        
        # Calculate accuracy metrics
        result = monitor.calculate_accuracy_metrics(actual_values, predicted_values)
        
        self.assertTrue(isinstance(result, dict))
        self.assertIn('success', result)
        self.assertIn('metrics', result)
        
        if result['success']:
            metrics = result['metrics']
            self.assertIn('mae', metrics)
            self.assertIn('mse', metrics)
            self.assertIn('rmse', metrics)
    
    def test_model_performance_tracking(self):
        """Test model performance tracking"""
        monitor = ForecastMonitor()
        
        # Create test data
        actual_values = [10.0, 15.0, 20.0, 25.0, 30.0]
        predicted_values = [12.0, 14.0, 18.0, 27.0, 32.0]
        
        # Track performance
        result = monitor.track_model_performance(
            'test_model', actual_values, predicted_values, datetime.now()
        )
        
        self.assertTrue(isinstance(result, dict))
        self.assertIn('success', result)
        self.assertIn('performance_record', result)
    
    def test_drift_detection(self):
        """Test model drift detection"""
        detector = ModelDriftDetector(threshold=0.1)
        
        # Create test metrics
        current_metrics = {'mae': 5.0, 'rmse': 6.0, 'mape': 15.0}
        historical_metrics = {'mae': 4.0, 'rmse': 5.0, 'mape': 12.0}
        
        # Detect drift
        result = detector.detect_drift('test_model', current_metrics, historical_metrics)
        
        self.assertTrue(isinstance(result, dict))
        self.assertIn('success', result)
        self.assertIn('drift_result', result)


if __name__ == '__main__':
    unittest.main()