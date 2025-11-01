"""
Test script to verify that the CSV data files can be loaded correctly
"""

import pandas as pd
import sys
import os

# Add the src directory to the path so we can import the data preparation module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models.revenue_leak_detector.data_preparation import RevenueLeakDataPreparator

def test_csv_loading():
    """Test that CSV data files load correctly"""
    # Test invoice data
    invoice_df = pd.read_csv('invoice_data.csv')
    print(f"Invoice data: {len(invoice_df)} rows, columns: {list(invoice_df.columns)}")
    
    # Test time log data
    time_log_df = pd.read_csv('time_log_data.csv')
    print(f"Time log data: {len(time_log_df)} rows, columns: {list(time_log_df.columns)}")
    
    # Test service data
    service_df = pd.read_csv('service_data.csv')
    print(f"Service data: {len(service_df)} rows, columns: {list(service_df.columns)}")
    
    print("All CSV files loaded successfully!")

def test_data_preparator():
    """Test that the data preparator can load data from CSV files"""
    preparator = RevenueLeakDataPreparator()
    
    # Test that the data directory is set correctly
    print(f"Data directory: {preparator.data_dir}")
    
    # Check if CSV files exist
    import os
    invoice_path = os.path.join(os.path.dirname(__file__), 'invoice_data.csv')
    time_log_path = os.path.join(os.path.dirname(__file__), 'time_log_data.csv')
    service_path = os.path.join(os.path.dirname(__file__), 'service_data.csv')
    
    print(f"Invoice CSV exists: {os.path.exists(invoice_path)}")
    print(f"Time log CSV exists: {os.path.exists(time_log_path)}")
    print(f"Service CSV exists: {os.path.exists(service_path)}")

if __name__ == "__main__":
    print("Testing CSV data loading...")
    test_csv_loading()
    print("\nTesting data preparator...")
    test_data_preparator()