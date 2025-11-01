"""
Tests for Main Demand Forecaster Module
"""

import sys
import os
import unittest
import pandas as pd
import numpy as np
import asyncio

# Add the src directory to the path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
sys.path.insert(0, src_path)

from src.models.demand_forecaster.demand_forecaster import DemandForecaster


class TestDemandForecaster(unittest.TestCase):
    """Tests for DemandForecaster class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.forecaster = DemandForecaster()
    
    def test_engine_initialization(self):
        """Test demand forecaster engine initialization"""
        self.assertIsNotNone(self.forecaster)
        # Check that components are initialized
        self.assertTrue(hasattr(self.forecaster, 'data_preparator'))
        self.assertTrue(hasattr(self.forecaster, 'lstm_forecaster'))
        self.assertTrue(hasattr(self.forecaster, 'arima_forecaster'))
    
    def test_component_initialization_methods(self):
        """Test component initialization methods"""
        # Test that initialization methods exist
        self.assertTrue(hasattr(self.forecaster, '_initialize_components'))
        self.assertTrue(hasattr(self.forecaster, 'initialize_data_preparator'))
        self.assertTrue(hasattr(self.forecaster, 'initialize_forecasting_models'))
        self.assertTrue(hasattr(self.forecaster, 'initialize_demand_prediction_engines'))
        self.assertTrue(hasattr(self.forecaster, 'initialize_monitoring_engines'))
    
    def test_data_preparation_initialization(self):
        """Test data preparator initialization"""
        # This is an async method, so we need to run it in an event loop
        async def test_async():
            await self.forecaster.initialize_data_preparator()
            self.assertIsNotNone(self.forecaster.data_preparator)
        
        # Run the async test
        asyncio.run(test_async())
    
    def test_forecasting_models_initialization(self):
        """Test forecasting models initialization"""
        # This is an async method, so we need to run it in an event loop
        async def test_async():
            await self.forecaster.initialize_forecasting_models()
            self.assertIsNotNone(self.forecaster.lstm_forecaster)
            self.assertIsNotNone(self.forecaster.arima_forecaster)
            self.assertIsNotNone(self.forecaster.prophet_forecaster)
            self.assertIsNotNone(self.forecaster.seasonal_decomposer)
        
        # Run the async test
        asyncio.run(test_async())
    
    def test_demand_prediction_engines_initialization(self):
        """Test demand prediction engines initialization"""
        # This is an async method, so we need to run it in an event loop
        async def test_async():
            await self.forecaster.initialize_demand_prediction_engines()
            self.assertIsNotNone(self.forecaster.ensemble_forecaster)
            self.assertIsNotNone(self.forecaster.resource_planner)
            self.assertIsNotNone(self.forecaster.capacity_planner)
            self.assertIsNotNone(self.forecaster.seasonal_adjuster)
            self.assertIsNotNone(self.forecaster.uncertainty_quantifier)
        
        # Run the async test
        asyncio.run(test_async())
    
    def test_monitoring_engines_initialization(self):
        """Test monitoring engines initialization"""
        # This is an async method, so we need to run it in an event loop
        async def test_async():
            await self.forecaster.initialize_monitoring_engines()
            self.assertIsNotNone(self.forecaster.forecast_monitor)
            self.assertIsNotNone(self.forecaster.drift_detector)
            self.assertIsNotNone(self.forecaster.alert_system)
        
        # Run the async test
        asyncio.run(test_async())


if __name__ == '__main__':
    unittest.main()