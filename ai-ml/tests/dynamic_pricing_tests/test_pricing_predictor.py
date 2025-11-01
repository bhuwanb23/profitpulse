"""
Tests for Dynamic Pricing Predictor Module
"""

import sys
import os
import unittest
import pandas as pd
import numpy as np

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'models'))

class TestPricingPredictor(unittest.TestCase):
    """Test cases for pricing predictor components"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        from dynamic_pricing.pricing_predictor import ClientAcceptancePredictor, PricingStrategyValidator
        self.acceptance_predictor = ClientAcceptancePredictor()
        self.strategy_validator = PricingStrategyValidator()
    
    def test_client_acceptance_predictor_initialization(self):
        """Test client acceptance predictor initialization"""
        self.assertIsNotNone(self.acceptance_predictor)
    
    def test_pricing_strategy_validator_initialization(self):
        """Test pricing strategy validator initialization"""
        self.assertIsNotNone(self.strategy_validator)
    
    def test_acceptance_probability_calculation(self):
        """Test acceptance probability calculation"""
        # Create mock client data
        client = pd.Series({
            'client_id': 'CLIENT-001',
            'price_sensitivity': 50,
            'loyalty_score': 75,
            'satisfaction_score': 8,
            'current_price': 100.0
        })
        
        proposed_price = 110.0
        
        # Test acceptance probability calculation
        acceptance_prob = self.acceptance_predictor._calculate_acceptance_probability(
            client, proposed_price)
        self.assertIsInstance(acceptance_prob, float)
        self.assertGreaterEqual(acceptance_prob, 0.0)
        self.assertLessEqual(acceptance_prob, 1.0)

if __name__ == '__main__':
    unittest.main()