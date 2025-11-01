"""
Tests for Demand Predictor Module
"""

import sys
import os
import unittest
import pandas as pd
import numpy as np

# Add the src directory to the path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
sys.path.insert(0, src_path)

from src.models.demand_forecaster.demand_predictor import (
    EnsembleForecaster,
    ResourcePlanner,
    CapacityPlanner,
    SeasonalAdjuster,
    UncertaintyQuantifier
)


class TestDemandPredictor(unittest.TestCase):
    """Tests for demand predictor components"""
    
    def test_ensemble_forecaster_initialization(self):
        """Test EnsembleForecaster initialization"""
        forecaster = EnsembleForecaster()
        self.assertIsNotNone(forecaster)
        self.assertEqual(forecaster.models, {})
        self.assertEqual(forecaster.weights, {})
    
    def test_resource_planner_initialization(self):
        """Test ResourcePlanner initialization"""
        planner = ResourcePlanner()
        self.assertIsNotNone(planner)
    
    def test_capacity_planner_initialization(self):
        """Test CapacityPlanner initialization"""
        planner = CapacityPlanner()
        self.assertIsNotNone(planner)
    
    def test_seasonal_adjuster_initialization(self):
        """Test SeasonalAdjuster initialization"""
        adjuster = SeasonalAdjuster()
        self.assertIsNotNone(adjuster)
    
    def test_uncertainty_quantifier_initialization(self):
        """Test UncertaintyQuantifier initialization"""
        quantifier = UncertaintyQuantifier()
        self.assertIsNotNone(quantifier)
    
    def test_ensemble_model_addition(self):
        """Test adding models to ensemble"""
        forecaster = EnsembleForecaster()
        
        # Create mock model
        class MockModel:
            def predict(self, data, steps):
                return {'success': True, 'predictions': [1.0] * steps}
        
        # Add model to ensemble
        forecaster.add_model('mock_model', MockModel(), weight=1.5)
        
        self.assertIn('mock_model', forecaster.models)
        self.assertEqual(forecaster.weights['mock_model'], 1.5)
    
    def test_resource_recommendations(self):
        """Test resource recommendation generation"""
        planner = ResourcePlanner()
        
        # Create mock data
        forecast = [10.0, 15.0, 20.0, 25.0, 30.0]
        capacity_data = pd.DataFrame({
            'resource_type': ['Developer', 'Designer'],
            'utilization_rate': [0.7, 0.6],
            'available_capacity_hours': [160, 120]
        })
        resource_types = ['Developer', 'Designer']
        
        # Generate recommendations
        result = planner.generate_resource_recommendations(forecast, capacity_data, resource_types)
        
        self.assertTrue(isinstance(result, dict))
        self.assertIn('success', result)
        self.assertIn('recommendations', result)


if __name__ == '__main__':
    unittest.main()