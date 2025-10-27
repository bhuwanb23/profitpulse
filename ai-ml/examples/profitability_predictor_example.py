"""
Example usage of the Client Profitability Predictor modules
"""

import pandas as pd
import numpy as np
import sys
import os

# Add the ai-ml directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.models.profitability_predictor.historical_data_collector import collect_historical_financial_data
from src.models.profitability_predictor.feature_engineering import engineer_profitability_features
from src.models.profitability_predictor.data_splitter import split_profitability_data
from src.models.profitability_predictor.data_quality import assess_profitability_data_quality
from src.models.profitability_predictor.data_preparation import prepare_profitability_data


def create_sample_database():
    """Create a sample database for demonstration"""
    import sqlite3
    import tempfile
    
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
            name TEXT
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
        ('client_2', 'TechStart Inc', 'Technology', 'monthly', 5000.0, '2023-03-01', NULL, 1),
        ('client_3', 'Global Solutions', 'Finance', 'quarterly', 25000.0, '2023-02-01', '2023-11-30', 0)
    """)
    
    conn.execute("""
        INSERT INTO invoices VALUES 
        ('client_1', '2023-01-31', 10000.0, 'paid'),
        ('client_1', '2023-02-28', 12000.0, 'paid'),
        ('client_2', '2023-03-31', 5000.0, 'sent'),
        ('client_3', '2023-02-28', 8000.0, 'paid'),
        ('client_3', '2023-03-31', 7000.0, 'paid')
    """)
    
    conn.execute("""
        INSERT INTO tickets VALUES 
        ('client_1', 20.0, 20.0, 100.0),
        ('client_1', 15.0, 15.0, 100.0),
        ('client_2', 5.0, 5.0, 80.0),
        ('client_3', 10.0, 10.0, 120.0)
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
        ('client_2', 'service_1', 500.0, 10),
        ('client_3', 'service_1', 750.0, 15),
        ('client_3', 'service_2', 1500.0, 5)
    """)
    
    conn.commit()
    conn.close()
    
    return temp_db.name


def main():
    """Main example function"""
    print("=== Client Profitability Predictor Example ===")
    
    # Create sample database
    db_path = create_sample_database()
    print(f"Created sample database at: {db_path}")
    
    try:
        # 1. Collect historical financial data
        print("\n1. Collecting historical financial data...")
        financial_data = collect_historical_financial_data(db_path)
        print(f"Collected data for {len(financial_data)} clients")
        print("Sample data:")
        print(financial_data.head())
        
        # 2. Engineer features
        print("\n2. Engineering features...")
        features_df = engineer_profitability_features(financial_data, db_path)
        print(f"Engineered {len(features_df.columns)} features for {len(features_df)} clients")
        print("Feature columns:", list(features_df.columns))
        
        # 3. Assess data quality
        print("\n3. Assessing data quality...")
        quality_report = assess_profitability_data_quality(features_df)
        print("Data quality summary:")
        print(f"  - Total records: {quality_report['summary']['total_records']}")
        print(f"  - Total features: {quality_report['summary']['total_columns']}")
        print(f"  - Columns with missing values: {quality_report['summary']['columns_with_missing']}")
        print(f"  - Duplicate rows: {quality_report['summary']['duplicate_rows']}")
        
        # 4. Split data
        print("\n4. Splitting data...")
        train_df, validation_df, test_df = split_profitability_data(
            features_df, 
            target_column='profit_margin',
            split_method='stratified',
            test_size=0.2, 
            validation_size=0.2,
            random_state=42
        )
        print(f"Data split - Train: {len(train_df)}, Validation: {len(validation_df)}, Test: {len(test_df)}")
        
        # 5. Complete preparation pipeline
        print("\n5. Running complete preparation pipeline...")
        train_df, validation_df, test_df, quality_report = prepare_profitability_data(db_path)
        print("Complete pipeline results:")
        print(f"  - Train set: {len(train_df)} records")
        print(f"  - Validation set: {len(validation_df)} records")
        print(f"  - Test set: {len(test_df)} records")
        
        print("\n=== Example completed successfully ===")
        
    finally:
        # Clean up
        import os
        os.unlink(db_path)
        print(f"Cleaned up temporary database: {db_path}")


if __name__ == "__main__":
    main()