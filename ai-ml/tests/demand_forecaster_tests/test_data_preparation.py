"""
Tests for Demand Data Preparation Module
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

from src.models.demand_forecaster.data_preparation import DemandDataPreparator


class TestDemandDataPreparation(unittest.TestCase):
    """Tests for DemandDataPreparator class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.preparator = DemandDataPreparator()
    
    def test_basic_functionality(self):
        """Test basic functionality of DemandDataPreparator"""
        self.assertIsNotNone(self.preparator)
        self.assertTrue(hasattr(self.preparator, 'data_dir'))
    
    def test_dataframe_creation(self):
        """Test that mock dataframes can be created"""
        from datetime import datetime
        
        # Test ticket data generation
        ticket_data = self.preparator._generate_mock_ticket_data(datetime(2024, 1, 1), datetime(2024, 1, 31))
        self.assertIsInstance(ticket_data, pd.DataFrame)
        self.assertGreater(len(ticket_data), 0)
        self.assertIn('date', ticket_data.columns)
        self.assertIn('ticket_count', ticket_data.columns)
        
        # Test client growth data generation
        client_data = self.preparator._generate_mock_client_growth_data(datetime(2024, 1, 1), datetime(2024, 12, 31))
        self.assertIsInstance(client_data, pd.DataFrame)
        self.assertGreater(len(client_data), 0)
        self.assertIn('date', client_data.columns)
        self.assertIn('total_clients', client_data.columns)
        
        # Test seasonal pattern data generation
        seasonal_data = self.preparator._generate_mock_seasonal_data(datetime(2024, 1, 1), datetime(2024, 12, 31))
        self.assertIsInstance(seasonal_data, pd.DataFrame)
        self.assertGreater(len(seasonal_data), 0)
        self.assertIn('date', seasonal_data.columns)
        self.assertIn('monthly_seasonality', seasonal_data.columns)
        
        # Test external factor data generation
        external_data = self.preparator._generate_mock_external_factor_data(datetime(2024, 1, 1), datetime(2024, 1, 31))
        self.assertIsInstance(external_data, pd.DataFrame)
        self.assertGreater(len(external_data), 0)
        self.assertIn('date', external_data.columns)
        self.assertIn('gdp_growth_rate', external_data.columns)
        
        # Test resource capacity data generation
        capacity_data = self.preparator._generate_mock_resource_capacity_data(datetime(2024, 1, 1), datetime(2024, 12, 31))
        self.assertIsInstance(capacity_data, pd.DataFrame)
        self.assertGreater(len(capacity_data), 0)
        self.assertIn('date', capacity_data.columns)
        self.assertIn('resource_type', capacity_data.columns)


if __name__ == '__main__':
    unittest.main()