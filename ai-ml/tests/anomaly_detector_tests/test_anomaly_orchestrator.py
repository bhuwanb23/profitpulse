"""
Unit tests for anomaly detector orchestrator
"""

import unittest
import numpy as np
import pandas as pd
from datetime import datetime
import asyncio

from src.models.anomaly_detector.anomaly_orchestrator import (
    AnomalyDetectorOrchestrator,
    get_anomaly_orchestrator
)


class TestAnomalyDetectorOrchestrator(unittest.TestCase):
    """Test cases for AnomalyDetectorOrchestrator"""
    
    def setUp(self):
        """Set up test data"""
        # Create orchestrator with test configuration
        self.config = {
            'streaming_port': 8766,
            'update_interval': 1,  # Fast updates for testing
            'buffer_size': 100
        }
        self.orchestrator = AnomalyDetectorOrchestrator(self.config)
        
        # Sample training data
        self.sample_training_data = pd.DataFrame({
            'feature1': np.random.normal(0, 1, 100),
            'feature2': np.random.normal(0, 1, 100),
            'feature3': np.random.normal(0, 1, 100)
        })
        
        # Sample test data
        self.sample_test_data = pd.DataFrame({
            'feature1': np.random.normal(0, 1, 20),
            'feature2': np.random.normal(0, 1, 20),
            'feature3': np.random.normal(0, 1, 20)
        })
    
    def test_initialization(self):
        """Test orchestrator initialization"""
        self.assertIsNotNone(self.orchestrator)
        self.assertEqual(self.orchestrator.config, self.config)
        self.assertFalse(self.orchestrator.is_running)
        
        # Check that components were initialized
        self.assertIsNotNone(self.orchestrator.one_class_svm)
        self.assertIsNotNone(self.orchestrator.dbscan)
        self.assertIsNotNone(self.orchestrator.statistical_detector)
        self.assertIsNotNone(self.orchestrator.ml_detector)
        self.assertIsNotNone(self.orchestrator.ensemble_detector)
        self.assertIsNotNone(self.orchestrator.data_processor)
        self.assertIsNotNone(self.orchestrator.streaming_service)
        self.assertIsNotNone(self.orchestrator.alert_generator)
        self.assertIsNotNone(self.orchestrator.escalation_system)
    
    def test_train_models(self):
        """Test model training"""
        # This might fail if dependencies are not available, but should not crash
        result = self.orchestrator.train_models(self.sample_training_data)
        self.assertIsInstance(result, bool)
    
    def test_detect_anomalies(self):
        """Test anomaly detection"""
        # Train models first
        self.orchestrator.train_models(self.sample_training_data)
        
        # Detect anomalies
        results = self.orchestrator.detect_anomalies(self.sample_test_data)
        
        # Results should be a dictionary
        self.assertIsInstance(results, dict)
        
        # Check for expected keys
        self.assertIn('anomalies', results)
        self.assertIn('results', results)
        self.assertIn('anomaly_data', results)
        self.assertIn('severities', results)
        self.assertIn('impacts', results)
        self.assertIn('timestamp', results)
    
    def test_get_system_status(self):
        """Test system status retrieval"""
        status = self.orchestrator.get_system_status()
        
        # Status should be a dictionary
        self.assertIsInstance(status, dict)
        
        # Check for expected keys
        self.assertIn('is_running', status)
        self.assertIn('models_trained', status)
        self.assertIn('streaming_active', status)
        self.assertIn('processed_count', status)
        self.assertIn('error_count', status)
        self.assertIn('alert_count', status)
        
        # Check initial values
        self.assertFalse(status['is_running'])
        self.assertEqual(status['processed_count'], 0)
        self.assertEqual(status['error_count'], 0)
        self.assertEqual(status['alert_count'], 0)
    
    def test_load_sample_data(self):
        """Test loading sample data"""
        # This will fail since the file doesn't exist, but should not crash
        try:
            data = self.orchestrator.load_sample_data("nonexistent_file.csv")
            # If it doesn't raise an exception, it should return an empty DataFrame
            self.assertIsInstance(data, pd.DataFrame)
        except FileNotFoundError:
            # This is expected
            pass


class TestSingletonFunction(unittest.TestCase):
    """Test cases for singleton function"""
    
    def test_get_anomaly_orchestrator(self):
        """Test getting orchestrator singleton"""
        config = {'test': True}
        orchestrator1 = get_anomaly_orchestrator(config)
        orchestrator2 = get_anomaly_orchestrator(config)
        
        # Should return the same instance
        self.assertIs(orchestrator1, orchestrator2)
        
        # Should be an instance of AnomalyDetectorOrchestrator
        self.assertIsInstance(orchestrator1, AnomalyDetectorOrchestrator)


if __name__ == '__main__':
    unittest.main()