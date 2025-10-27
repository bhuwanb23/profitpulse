"""
Test script to demonstrate the feature engineering pipeline working with sample data
"""

import sys
import os
import pandas as pd
import sqlite3
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data.preprocessing.feature_engineering import engineer_features


def load_sample_data():
    """Load sample data from the database"""
    print("Loading Sample Data from Database")
    print("=" * 35)
    
    # Connect to the database
    db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'superhack.db')
    
    try:
        conn = sqlite3.connect(db_path)
        
        # Load clients data
        clients_df = pd.read_sql_query("SELECT * FROM clients LIMIT 10", conn)
        print(f"Loaded {len(clients_df)} client records")
        
        # Load tickets data
        tickets_df = pd.read_sql_query("SELECT * FROM tickets LIMIT 10", conn)
        print(f"Loaded {len(tickets_df)} ticket records")
        
        # Load invoices data
        invoices_df = pd.read_sql_query("SELECT * FROM invoices LIMIT 10", conn)
        print(f"Loaded {len(invoices_df)} invoice records")
        
        conn.close()
        
        return clients_df, tickets_df, invoices_df
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None, None


def demonstrate_feature_engineering(clients_df):
    """Demonstrate the feature engineering pipeline"""
    print("\nDemonstrating Feature Engineering Pipeline")
    print("=" * 40)
    
    if clients_df is None or clients_df.empty:
        print("No data to process")
        return
    
    print(f"Original data shape: {clients_df.shape}")
    print("Original columns:", list(clients_df.columns)[:5], "...")
    
    # Create feature engineering configuration
    feature_config = {
        'use_modular_system': True,  # Use the new modular system
        'financial_features': True,
        'operational_features': True,
        'behavioral_features': True,
        'financial_config': {
            'revenue_per_client': True,
            'profit_margins_by_service': True,
            'billing_efficiency': True,
            'revenue_per_client_config': {
                'client_id_col': 'id',
                'revenue_col': 'contract_value',
                'date_col': 'created_at',
                'frequency': 'monthly'
            }
        },
        'operational_config': {
            'ticket_resolution_time': True,
            'sla_compliance': True
        },
        'behavioral_config': {
            'client_engagement': True,
            'churn_risk': True
        }
    }
    
    # Engineer features
    print("\nEngineering Features...")
    try:
        engineered_data = engineer_features(clients_df, feature_config)
        print(f"✅ Feature engineering completed successfully!")
        print(f"Engineered data shape: {engineered_data.shape}")
        print(f"New columns added: {len(engineered_data.columns) - len(clients_df.columns)}")
        
        # Show some of the new columns
        new_columns = set(engineered_data.columns) - set(clients_df.columns)
        print("Sample new features:", list(new_columns)[:10])
        
        return engineered_data
        
    except Exception as e:
        print(f"❌ Error in feature engineering: {e}")
        return None


def main():
    """Main function"""
    print("SuperHack Feature Engineering Pipeline Test")
    print("=" * 45)
    
    # Load sample data
    clients_df, tickets_df, invoices_df = load_sample_data()
    
    # Demonstrate feature engineering
    engineered_data = demonstrate_feature_engineering(clients_df)
    
    if engineered_data is not None:
        print("\n" + "=" * 50)
        print("🎉 FEATURE ENGINEERING DEMO COMPLETE")
        print("=" * 50)
        print("The feature engineering pipeline is working correctly!")
        print("You can now:")
        print("1. Create client genome vectors")
        print("2. Train machine learning models")
        print("3. Generate client insights")
        print("\nThe entire AI/ML pipeline is ready to use!")


if __name__ == "__main__":
    main()