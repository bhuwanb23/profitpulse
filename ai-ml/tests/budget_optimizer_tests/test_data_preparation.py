"""
Tests for Budget Data Preparation Module
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

# Import the module directly
from src.models.budget_optimizer.data_preparation import BudgetDataPreparator


class TestBudgetDataPreparation(unittest.TestCase):
    """Tests for BudgetDataPreparator class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.preparator = BudgetDataPreparator()
    
    def test_basic_functionality(self):
        """Test basic functionality of BudgetDataPreparator"""
        self.assertIsNotNone(self.preparator)
        self.assertTrue(hasattr(self.preparator, 'data_dir'))
    
    def test_dataframe_creation(self):
        """Test that mock dataframes can be created"""
        from datetime import datetime
        
        # Test budget data generation
        budget_data = self.preparator._generate_mock_budget_data(datetime(2024, 1, 1), datetime(2024, 12, 31))
        self.assertIsInstance(budget_data, pd.DataFrame)
        self.assertGreater(len(budget_data), 0)
        self.assertIn('budget_id', budget_data.columns)
        
        # Test service cost data generation
        service_data = self.preparator._generate_mock_service_cost_data(datetime(2024, 1, 1), datetime(2024, 12, 31))
        self.assertIsInstance(service_data, pd.DataFrame)
        self.assertGreater(len(service_data), 0)
        self.assertIn('service_id', service_data.columns)
        
        # Test client priority data generation
        client_data = self.preparator._generate_mock_client_priority_data(datetime(2024, 1, 1), datetime(2024, 12, 31))
        self.assertIsInstance(client_data, pd.DataFrame)
        self.assertGreater(len(client_data), 0)
        self.assertIn('client_id', client_data.columns)
        
        # Test ROI data generation
        roi_data = self.preparator._generate_mock_roi_data(datetime(2024, 1, 1), datetime(2024, 12, 31))
        self.assertIsInstance(roi_data, pd.DataFrame)
        self.assertGreater(len(roi_data), 0)
        self.assertIn('item_id', roi_data.columns)
        
        # Test resource data generation
        resource_data = self.preparator._generate_mock_resource_data(datetime(2024, 1, 1), datetime(2024, 12, 31))
        self.assertIsInstance(resource_data, pd.DataFrame)
        self.assertGreater(len(resource_data), 0)
        self.assertIn('resource_id', resource_data.columns)


if __name__ == '__main__':
    unittest.main()