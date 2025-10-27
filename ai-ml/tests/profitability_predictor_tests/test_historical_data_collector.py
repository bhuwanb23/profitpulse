"""
Tests for HistoricalDataCollector
"""

import pandas as pd
import pytest
import tempfile
import sqlite3
import os
from datetime import datetime

from src.models.profitability_predictor.historical_data_collector import HistoricalDataCollector, collect_historical_financial_data


def create_test_database():
    """Create a test database with sample data"""
    # Create a temporary database
    temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
    temp_db.close()
    
    # Connect to the database
    conn = sqlite3.connect(temp_db.name)
    
    # Create tables and insert sample data
    # Clients table
    conn.execute("""
        CREATE TABLE clients (
            id TEXT PRIMARY KEY,
            name TEXT,
            industry TEXT,
            contract_type TEXT,
            contract_value REAL,
            start_date TEXT,
            end_date TEXT,
            is_active BOOLEAN
        )
    """)
    
    # Invoices table
    conn.execute("""
        CREATE TABLE invoices (
            client_id TEXT,
            invoice_date TEXT,
            total_amount REAL,
            status TEXT
        )
    """)
    
    # Tickets table
    conn.execute("""
        CREATE TABLE tickets (
            client_id TEXT,
            time_spent REAL,
            billable_hours REAL,
            hourly_rate REAL
        )
    """)
    
    # Services table
    conn.execute("""
        CREATE TABLE services (
            id TEXT PRIMARY KEY,
            category TEXT
        )
    """)
    
    # Client services table
    conn.execute("""
        CREATE TABLE client_services (
            client_id TEXT,
            service_id TEXT,
            custom_price REAL,
            quantity INTEGER
        )
    """)
    
    # Insert sample data
    conn.execute("""
        INSERT INTO clients VALUES 
        ('client_1', 'Acme Corp', 'Manufacturing', 'annual', 50000.0, '2023-01-01', '2023-12-31', 1),
        ('client_2', 'TechStart Inc', 'Technology', 'monthly', 5000.0, '2023-03-01', NULL, 1)
    """)
    
    conn.execute("""
        INSERT INTO invoices VALUES 
        ('client_1', '2023-01-31', 10000.0, 'paid'),
        ('client_1', '2023-02-28', 12000.0, 'paid'),
        ('client_2', '2023-03-31', 5000.0, 'sent')
    """)
    
    conn.execute("""
        INSERT INTO tickets VALUES 
        ('client_1', 20.0, 20.0, 100.0),
        ('client_1', 15.0, 15.0, 100.0),
        ('client_2', 5.0, 5.0, 80.0)
    """)
    
    conn.execute("""
        INSERT INTO services VALUES 
        ('service_1', 'Help Desk'),
        ('service_2', 'Network Monitoring')
    """)
    
    conn.execute("""
        INSERT INTO client_services VALUES 
        ('client_1', 'service_1', 1000.0, 20),
        ('client_1', 'service_2', 2000.0, 10),
        ('client_2', 'service_1', 500.0, 10)
    """)
    
    conn.commit()
    conn.close()
    
    return temp_db.name


def test_historical_data_collector_initialization():
    """Test HistoricalDataCollector initialization"""
    collector = HistoricalDataCollector()
    assert collector.db_path == "../../database/superhack.db"
    
    collector = HistoricalDataCollector("/custom/path.db")
    assert collector.db_path == "/custom/path.db"


def test_collect_historical_financial_data():
    """Test collecting and aggregating historical financial data"""
    # Create test database
    db_path = create_test_database()
    
    try:
        # Collect data
        collector = HistoricalDataCollector(db_path)
        financial_data = collector.aggregate_financial_metrics()
        
        # Check results
        assert isinstance(financial_data, pd.DataFrame)
        assert len(financial_data) == 2
        assert 'id' in financial_data.columns
        assert 'total_revenue' in financial_data.columns
        assert 'total_costs' in financial_data.columns
        assert 'profit' in financial_data.columns
        assert 'profit_margin' in financial_data.columns
        
        # Check specific client data
        client_1_data = financial_data[financial_data['id'] == 'client_1'].iloc[0]
        assert client_1_data['total_revenue'] == 22000.0  # 10000 + 12000
        assert client_1_data['total_costs'] == 3500.0  # (20*100) + (15*100)
        assert client_1_data['profit'] == 18500.0  # 22000 - 3500
        assert client_1_data['profit_margin'] == 18500.0 / 22000.0
        
    finally:
        # Clean up - wait a moment to ensure file is not locked
        import time
        time.sleep(0.1)
        try:
            os.unlink(db_path)
        except PermissionError:
            # If file is still locked, that's okay for the test
            pass


def test_convenience_function():
    """Test the convenience function"""
    # Create test database
    db_path = create_test_database()
    
    try:
        # Test convenience function
        financial_data = collect_historical_financial_data(db_path)
        
        # Check results
        assert isinstance(financial_data, pd.DataFrame)
        assert len(financial_data) == 2
        
    finally:
        # Clean up - wait a moment to ensure file is not locked
        import time
        time.sleep(0.1)
        try:
            os.unlink(db_path)
        except PermissionError:
            # If file is still locked, that's okay for the test
            pass


if __name__ == "__main__":
    pytest.main([__file__])