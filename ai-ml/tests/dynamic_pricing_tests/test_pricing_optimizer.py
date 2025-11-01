"""
Tests for Dynamic Pricing Optimizer Module
"""

import sys
import os
import unittest
import pandas as pd
import numpy as np

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'models'))

class TestPricingOptimizer(unittest.TestCase):
    """Test cases for pricing optimizer components"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        from dynamic_pricing.pricing_optimizer import PriceRecommendationEngine, ROICalculator
        self.recommendation_engine = PriceRecommendationEngine()
        self.roi_calculator = ROICalculator()
    
    def test_price_recommendation_engine_initialization(self):
        """Test price recommendation engine initialization"""
        self.assertIsNotNone(self.recommendation_engine)
    
    def test_roi_calculator_initialization(self):
        """Test ROI calculator initialization"""
        self.assertIsNotNone(self.roi_calculator)
    
    def test_base_price_calculation(self):
        """Test base price calculation"""
        # Create mock data
        client_data = pd.DataFrame([{
            'client_id': 'CLIENT-001',
            'revenue_contribution': 10000,
            'profit_margin': 0.3,
            'loyalty_score': 75
        }])
        
        service_data = pd.DataFrame([{
            'service_id': 'SERVICE-001',
            'technical_complexity': 7.5
        }])
        
        market_data = pd.DataFrame([{
            'date': pd.Timestamp.now(),
            'market_rate': 100.0
        }])
        
        # Test base price calculation
        base_price = self.recommendation_engine._calculate_base_price(
            client_data.iloc[0], service_data, market_data)
        self.assertIsInstance(base_price, float)
        self.assertGreater(base_price, 0)

if __name__ == '__main__':
    unittest.main()