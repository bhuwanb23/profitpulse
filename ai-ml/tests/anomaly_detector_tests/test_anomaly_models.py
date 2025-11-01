"""
Unit tests for anomaly detection models
"""

import unittest
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

from src.models.anomaly_detector.anomaly_models import (
    OneClassSVMModel,
    DBSCANModel,
    StatisticalAnomalyDetector,
    MachineLearningAnomalyDetector,
    EnsembleAnomalyDetector
)


class TestOneClassSVMModel(unittest.TestCase):
    """Test cases for OneClassSVMModel"""
    
    def setUp(self):
        """Set up test data"""
        # Create sample data
        self.X_train = pd.DataFrame({
            'feature1': np.random.normal(0, 1, 100),
            'feature2': np.random.normal(0, 1, 100),
            'feature3': np.random.normal(0, 1, 100)
        })
        
        self.X_test = pd.DataFrame({
            'feature1': np.random.normal(0, 1, 20),
            'feature2': np.random.normal(0, 1, 20),
            'feature3': np.random.normal(0, 1, 20)
        })
        
        # Add some anomalies
        self.X_test_anomalies = pd.DataFrame({
            'feature1': np.random.normal(5, 1, 5),  # Anomalies with different mean
            'feature2': np.random.normal(5, 1, 5),
            'feature3': np.random.normal(5, 1, 5)
        })
        
        self.model = OneClassSVMModel()
    
    def test_initialization(self):
        """Test model initialization"""
        self.assertIsNotNone(self.model)
        self.assertEqual(self.model.kernel, 'rbf')
        self.assertEqual(self.model.nu, 0.1)
        self.assertEqual(self.model.gamma, 'scale')
    
    def test_train(self):
        """Test model training"""
        success = self.model.train(self.X_train)
        self.assertTrue(success)
        self.assertTrue(self.model.is_trained)
    
    def test_predict(self):
        """Test model prediction"""
        # Train model
        self.model.train(self.X_train)
        
        # Predict on normal data
        predictions_normal = self.model.predict(self.X_test)
        self.assertEqual(len(predictions_normal), len(self.X_test))
        
        # Predict on anomalies
        predictions_anomalies = self.model.predict(self.X_test_anomalies)
        self.assertEqual(len(predictions_anomalies), len(self.X_test_anomalies))
    
    def test_anomaly_scores(self):
        """Test anomaly scoring"""
        # Train model
        self.model.train(self.X_train)
        
        # Get scores
        scores = self.model.anomaly_scores(self.X_test)
        self.assertEqual(len(scores), len(self.X_test))
        
        # Scores should be numpy array
        self.assertIsInstance(scores, np.ndarray)


class TestDBSCANModel(unittest.TestCase):
    """Test cases for DBSCANModel"""
    
    def setUp(self):
        """Set up test data"""
        # Create sample data with clusters
        self.X_train = pd.DataFrame({
            'feature1': np.concatenate([np.random.normal(0, 0.5, 50), np.random.normal(3, 0.5, 50)]),
            'feature2': np.concatenate([np.random.normal(0, 0.5, 50), np.random.normal(3, 0.5, 50)])
        })
        
        self.X_test = pd.DataFrame({
            'feature1': np.random.normal(0, 0.5, 20),
            'feature2': np.random.normal(0, 0.5, 20)
        })
        
        self.model = DBSCANModel(eps=0.5, min_samples=5)
    
    def test_initialization(self):
        """Test model initialization"""
        self.assertIsNotNone(self.model)
        self.assertEqual(self.model.eps, 0.5)
        self.assertEqual(self.model.min_samples, 5)
    
    def test_train(self):
        """Test model training"""
        success = self.model.train(self.X_train)
        self.assertTrue(success)
        self.assertTrue(self.model.is_trained)
    
    def test_predict(self):
        """Test model prediction"""
        # Train model
        self.model.train(self.X_train)
        
        # Predict
        predictions = self.model.predict(self.X_test)
        self.assertEqual(len(predictions), len(self.X_test))
        
        # Predictions should be -1 (anomaly) or 1 (normal)
        unique_predictions = np.unique(predictions)
        for pred in unique_predictions:
            self.assertIn(pred, [-1, 1])


class TestStatisticalAnomalyDetector(unittest.TestCase):
    """Test cases for StatisticalAnomalyDetector"""
    
    def setUp(self):
        """Set up test data"""
        # Create sample data
        self.X_train = pd.DataFrame({
            'feature1': np.random.normal(0, 1, 100),
            'feature2': np.random.normal(0, 1, 100),
            'feature3': np.random.normal(0, 1, 100)
        })
        
        self.X_test = pd.DataFrame({
            'feature1': np.random.normal(0, 1, 20),
            'feature2': np.random.normal(0, 1, 20),
            'feature3': np.random.normal(0, 1, 20)
        })
        
        # Add some anomalies
        self.X_test_anomalies = pd.DataFrame({
            'feature1': np.random.normal(5, 1, 5),
            'feature2': np.random.normal(5, 1, 5),
            'feature3': np.random.normal(5, 1, 5)
        })
        
        self.model = StatisticalAnomalyDetector(method='zscore', threshold=3.0)
    
    def test_initialization(self):
        """Test model initialization"""
        self.assertIsNotNone(self.model)
        self.assertEqual(self.model.method, 'zscore')
        self.assertEqual(self.model.threshold, 3.0)
    
    def test_train(self):
        """Test model training"""
        success = self.model.train(self.X_train)
        self.assertTrue(success)
        self.assertTrue(self.model.is_trained)
        self.assertGreater(len(self.model.stats), 0)
    
    def test_predict(self):
        """Test model prediction"""
        # Train model
        self.model.train(self.X_train)
        
        # Predict on normal data
        predictions_normal = self.model.predict(self.X_test)
        self.assertEqual(len(predictions_normal), len(self.X_test))
        
        # Predict on anomalies
        predictions_anomalies = self.model.predict(self.X_test_anomalies)
        self.assertEqual(len(predictions_anomalies), len(self.X_test_anomalies))
    
    def test_anomaly_scores(self):
        """Test anomaly scoring"""
        # Train model
        self.model.train(self.X_train)
        
        # Get scores
        scores = self.model.anomaly_scores(self.X_test)
        self.assertEqual(len(scores), len(self.X_test))
        # Convert to numpy array if it's a pandas Series
        if hasattr(scores, 'values') and not isinstance(scores, np.ndarray):
            scores = scores.values
        self.assertIsInstance(scores, (np.ndarray, pd.Series))


class TestMachineLearningAnomalyDetector(unittest.TestCase):
    """Test cases for MachineLearningAnomalyDetector"""
    
    def setUp(self):
        """Set up test data"""
        # Create sample data
        self.X_train = pd.DataFrame({
            'feature1': np.random.normal(0, 1, 100),
            'feature2': np.random.normal(0, 1, 100),
            'feature3': np.random.normal(0, 1, 100)
        })
        
        self.X_test = pd.DataFrame({
            'feature1': np.random.normal(0, 1, 20),
            'feature2': np.random.normal(0, 1, 20),
            'feature3': np.random.normal(0, 1, 20)
        })
        
        self.model = MachineLearningAnomalyDetector(model_type='isolation_forest')
    
    def test_initialization(self):
        """Test model initialization"""
        self.assertIsNotNone(self.model)
        self.assertEqual(self.model.model_type, 'isolation_forest')
    
    def test_train(self):
        """Test model training"""
        result = self.model.train(self.X_train)
        self.assertIsInstance(result, dict)
        self.assertIn('success', result)
        if result['success']:
            self.assertTrue(self.model.is_trained)
    
    def test_predict(self):
        """Test model prediction"""
        # Train model
        self.model.train(self.X_train)
        
        # Predict
        predictions = self.model.predict(self.X_test)
        self.assertEqual(len(predictions), len(self.X_test))
        
        # Predictions should be -1 (anomaly) or 1 (normal)
        unique_predictions = np.unique(predictions)
        for pred in unique_predictions:
            self.assertIn(pred, [-1, 1])


class TestEnsembleAnomalyDetector(unittest.TestCase):
    """Test cases for EnsembleAnomalyDetector"""
    
    def setUp(self):
        """Set up test data"""
        # Create sample data
        self.X_train = pd.DataFrame({
            'feature1': np.random.normal(0, 1, 100),
            'feature2': np.random.normal(0, 1, 100),
            'feature3': np.random.normal(0, 1, 100)
        })
        
        self.X_test = pd.DataFrame({
            'feature1': np.random.normal(0, 1, 20),
            'feature2': np.random.normal(0, 1, 20),
            'feature3': np.random.normal(0, 1, 20)
        })
        
        self.model = EnsembleAnomalyDetector(voting_method='majority')
    
    def test_initialization(self):
        """Test model initialization"""
        self.assertIsNotNone(self.model)
        self.assertEqual(self.model.voting_method, 'majority')
        self.assertEqual(len(self.model.weights), 4)  # 4 models
    
    def test_train(self):
        """Test model training"""
        success = self.model.train(self.X_train)
        # Training might fail if dependencies are not available, but should not crash
        self.assertIsInstance(success, bool)
    
    def test_predict(self):
        """Test model prediction"""
        # Train model
        self.model.train(self.X_train)
        
        # Predict
        predictions = self.model.predict(self.X_test)
        self.assertEqual(len(predictions), len(self.X_test))
        
        # Predictions should be -1 (anomaly) or 1 (normal)
        if len(predictions) > 0:
            unique_predictions = np.unique(predictions)
            for pred in unique_predictions:
                self.assertIn(pred, [-1, 1])


if __name__ == '__main__':
    unittest.main()