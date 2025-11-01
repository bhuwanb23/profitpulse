"""
Tests for Revenue Leak Detector Data Preparation Module
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.models.revenue_leak_detector.data_preparation import RevenueLeakDataPreparator


class TestDataPreparation:
    """Test cases for data preparation module"""
    
    def test_data_preparator_initialization(self):
        """Test that data preparator initializes correctly"""
        preparator = RevenueLeakDataPreparator()
        assert preparator is not None
        assert hasattr(preparator, 'db_path')
    
    def test_mock_invoice_data_generation(self):
        """Test generation of mock invoice data"""
        preparator = RevenueLeakDataPreparator()
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        
        # Test that we can generate mock data
        mock_data = preparator._generate_mock_invoice_data(start_date, end_date)
        assert isinstance(mock_data, pd.DataFrame)
        assert len(mock_data) > 0
        assert 'invoice_id' in mock_data.columns
        assert 'client_id' in mock_data.columns
        assert 'amount' in mock_data.columns
    
    def test_mock_time_log_data_generation(self):
        """Test generation of mock time log data"""
        preparator = RevenueLeakDataPreparator()
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        
        # Test that we can generate mock data
        mock_data = preparator._generate_mock_time_log_data(start_date, end_date)
        assert isinstance(mock_data, pd.DataFrame)
        assert len(mock_data) > 0
        assert 'time_log_id' in mock_data.columns
        assert 'technician_id' in mock_data.columns
        assert 'hours_logged' in mock_data.columns
    
    def test_mock_service_data_generation(self):
        """Test generation of mock service delivery data"""
        preparator = RevenueLeakDataPreparator()
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        
        # Test that we can generate mock data
        mock_data = preparator._generate_mock_service_data(start_date, end_date)
        assert isinstance(mock_data, pd.DataFrame)
        assert len(mock_data) > 0
        assert 'service_id' in mock_data.columns
        assert 'client_id' in mock_data.columns
        assert 'hours_billed' in mock_data.columns
    
    def test_feature_preparation(self):
        """Test feature preparation from mock data"""
        preparator = RevenueLeakDataPreparator()
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        
        # Generate mock data
        invoice_data = preparator._generate_mock_invoice_data(start_date, end_date)
        time_log_data = preparator._generate_mock_time_log_data(start_date, end_date)
        service_data = preparator._generate_mock_service_data(start_date, end_date)
        
        # Test feature preparation
        features = preparator.prepare_features(invoice_data, time_log_data, service_data)
        assert isinstance(features, pd.DataFrame)
        assert len(features) > 0
        assert 'client_id' in features.columns
        assert 'total_invoiced' in features.columns
        assert 'revenue_leak_score' in features.columns


if __name__ == "__main__":
    pytest.main([__file__])