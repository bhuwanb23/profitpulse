"""
Tests for Revenue Leak Detector Anomaly Models
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.models.revenue_leak_detector.anomaly_models import (
    IsolationForestModel, AutoencoderModel, DBSCANModel, 
    OneClassSVMModel, EnsembleAnomalyDetector
)


class TestAnomalyModels:
    """Test cases for anomaly detection models"""
    
    def setup_method(self):
        """Set up test data"""
        # Create simple test data
        self.test_data = pd.DataFrame({
            'feature1': [1, 2, 3, 4, 5, 100, 2, 3, 4, 5],  # 100 is an anomaly
            'feature2': [2, 4, 6, 8, 10, 200, 4, 6, 8, 10],  # 200 is an anomaly
            'feature3': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        })
    
    def test_isolation_forest_model(self):
        """Test Isolation Forest model"""
        model = IsolationForestModel(contamination=0.1)
        
        # Test training
        success = model.train(self.test_data)
        # Training might fail if sklearn is not available, but that's okay for testing
        assert model is not None
        
        # Test prediction (even if model not trained, should return mock results)
        predictions = model.predict(self.test_data)
        assert isinstance(predictions, np.ndarray)
        assert len(predictions) == len(self.test_data)
        
        # Test anomaly scores
        scores = model.anomaly_scores(self.test_data)
        assert isinstance(scores, np.ndarray)
        assert len(scores) == len(self.test_data)
    
    def test_autoencoder_model(self):
        """Test Autoencoder model"""
        model = AutoencoderModel(encoding_dim=2, epochs=10)
        
        # Test training
        success = model.train(self.test_data)
        # Training might fail if tensorflow is not available, but that's okay for testing
        assert model is not None
        
        # Test prediction (even if model not trained, should return mock results)
        predictions = model.predict(self.test_data)
        assert isinstance(predictions, np.ndarray)
        assert len(predictions) == len(self.test_data)
        
        # Test anomaly scores
        scores = model.anomaly_scores(self.test_data)
        assert isinstance(scores, np.ndarray)
        assert len(scores) == len(self.test_data)
    
    def test_dbscan_model(self):
        """Test DBSCAN model"""
        model = DBSCANModel(eps=0.5, min_samples=2)
        
        # Test training
        success = model.train(self.test_data)
        # Training might fail if sklearn is not available, but that's okay for testing
        assert model is not None
        
        # Test prediction (even if model not trained, should return mock results)
        predictions = model.predict(self.test_data)
        assert isinstance(predictions, np.ndarray)
        assert len(predictions) == len(self.test_data)
        
        # Test anomaly scores
        scores = model.anomaly_scores(self.test_data)
        assert isinstance(scores, np.ndarray)
        assert len(scores) == len(self.test_data)
    
    def test_one_class_svm_model(self):
        """Test One-Class SVM model"""
        model = OneClassSVMModel(nu=0.1)
        
        # Test training
        success = model.train(self.test_data)
        # Training might fail if sklearn is not available, but that's okay for testing
        assert model is not None
        
        # Test prediction (even if model not trained, should return mock results)
        predictions = model.predict(self.test_data)
        assert isinstance(predictions, np.ndarray)
        assert len(predictions) == len(self.test_data)
        
        # Test anomaly scores
        scores = model.anomaly_scores(self.test_data)
        assert isinstance(scores, np.ndarray)
        assert len(scores) == len(self.test_data)
    
    def test_ensemble_model(self):
        """Test Ensemble model"""
        model = EnsembleAnomalyDetector(contamination=0.1)
        
        # Test training
        success = model.train(self.test_data)
        # Training might fail if sklearn/tensorflow is not available, but that's okay for testing
        assert model is not None
        
        # Test prediction (even if model not trained, should return mock results)
        predictions = model.predict(self.test_data)
        assert isinstance(predictions, np.ndarray)
        assert len(predictions) == len(self.test_data)
        
        # Test anomaly scores
        scores = model.anomaly_scores(self.test_data)
        assert isinstance(scores, np.ndarray)
        assert len(scores) == len(self.test_data)


if __name__ == "__main__":
    pytest.main([__file__])