"""
Tests for Forecasting Models Module
"""

import sys
import os
import unittest
import pandas as pd
import numpy as np

# Add the src directory to the path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
sys.path.insert(0, src_path)

from src.models.demand_forecaster.forecasting_models import (
    LSTMForecaster,
    ARIMAForecaster,
    ProphetForecaster,
    SeasonalDecomposer
)


class TestForecastingModels(unittest.TestCase):
    """Tests for forecasting models"""
    
    def test_lstm_forecaster_initialization(self):
        """Test LSTM forecaster initialization"""
        forecaster = LSTMForecaster()
        self.assertIsNotNone(forecaster)
        self.assertTrue(hasattr(forecaster, 'sequence_length'))
        self.assertTrue(hasattr(forecaster, 'epochs'))
    
    def test_arima_forecaster_initialization(self):
        """Test ARIMA forecaster initialization"""
        forecaster = ARIMAForecaster()
        self.assertIsNotNone(forecaster)
        self.assertTrue(hasattr(forecaster, 'order'))
    
    def test_prophet_forecaster_initialization(self):
        """Test Prophet forecaster initialization"""
        forecaster = ProphetForecaster()
        self.assertIsNotNone(forecaster)
    
    def test_seasonal_decomposer_initialization(self):
        """Test seasonal decomposer initialization"""
        decomposer = SeasonalDecomposer()
        self.assertIsNotNone(decomposer)
        self.assertTrue(hasattr(decomposer, 'model'))
        self.assertTrue(hasattr(decomposer, 'period'))
    
    def test_lstm_prepare_data(self):
        """Test LSTM data preparation"""
        forecaster = LSTMForecaster(sequence_length=5)
        
        # Create test data
        data = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        
        # Test data preparation
        X, y = forecaster.prepare_data(data)
        
        # Check if the forecaster is available (has required libraries)
        if forecaster.available:
            # Check shapes when libraries are available
            self.assertEqual(X.shape[0], y.shape[0])
            self.assertEqual(X.shape[1], 5)  # sequence_length
        else:
            # When libraries are not available, we expect empty arrays
            self.assertEqual(len(X), 0)
            self.assertEqual(len(y), 0)
    
    def test_arima_model_building(self):
        """Test ARIMA model building"""
        forecaster = ARIMAForecaster(order=(1, 1, 1))
        
        # Create test data
        data = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        
        # Test model training (will fail without statsmodels, but shouldn't crash)
        result = forecaster.train(data)
        self.assertTrue(isinstance(result, dict))
        self.assertIn('success', result)


if __name__ == '__main__':
    unittest.main()