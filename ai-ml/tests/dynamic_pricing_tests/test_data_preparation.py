"""
Tests for Dynamic Pricing Data Preparation Module
"""

import sys
import os
import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'models'))

class TestPricingDataPreparator(unittest.TestCase):
    """Test cases for PricingDataPreparator class"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        from dynamic_pricing.data_preparation import PricingDataPreparator
        self.preparator = PricingDataPreparator()
    
    def test_basic_functionality(self):
        """Test basic functionality of the data preparator"""
        # Test that the preparator can be instantiated
        self.assertIsNotNone(self.preparator)
        
        # Test that data directory exists
        self.assertTrue(hasattr(self.preparator, 'data_dir'))
    
    def test_dataframe_creation(self):
        """Test that mock dataframes can be created"""
        # Test market rate data generation
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        
        market_data = self.preparator._generate_mock_market_rate_data(start_date, end_date)
        self.assertIsInstance(market_data, pd.DataFrame)
        self.assertGreater(len(market_data), 0)
        self.assertIn('date', market_data.columns)
        self.assertIn('market_rate', market_data.columns)
        
        # Test client value data generation
        client_data = self.preparator._generate_mock_client_value_data(start_date, end_date)
        self.assertIsInstance(client_data, pd.DataFrame)
        self.assertGreater(len(client_data), 0)
        self.assertIn('client_id', client_data.columns)
        self.assertIn('revenue_contribution', client_data.columns)
        
        # Test service complexity data generation
        service_data = self.preparator._generate_mock_service_complexity_data(start_date, end_date)
        self.assertIsInstance(service_data, pd.DataFrame)
        self.assertGreater(len(service_data), 0)
        self.assertIn('service_id', service_data.columns)
        self.assertIn('technical_complexity', service_data.columns)

if __name__ == '__main__':
    unittest.main()