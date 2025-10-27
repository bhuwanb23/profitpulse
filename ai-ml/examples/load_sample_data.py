"""
Example showing how to load sample data and start working with AI/ML models
"""

import sys
import os
import sqlite3
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
from datetime import datetime


def load_sample_data():
    """Load sample data into the database"""
    print("Loading Sample Data for AI/ML Development")
    print("=" * 45)
    
    # Connect to the database
    db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'superhack.db')
    print(f"Database path: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        print("✅ Connected to database successfully")
        
        # Check if we have sample data tables
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Existing tables: {[table[0] for table in tables]}")
        
        # Close connection
        conn.close()
        print("✅ Database connection closed")
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Note: This is expected if you haven't set up the database yet")


def show_sample_data_structure():
    """Show the structure of sample data we can work with"""
    print("\n📊 Sample Data Structure Available:")
    print("=" * 40)
    
    # Client data structure
    print("\n1. Client Data:")
    client_data = pd.DataFrame({
        'client_id': ['client_1', 'client_2', 'client_3'],
        'name': ['Acme Corp', 'TechStart Inc', 'RetailMax'],
        'industry': ['Manufacturing', 'Technology', 'Retail'],
        'contract_value': [50000.00, 5000.00, 75000.00],
        'contract_type': ['annual', 'monthly', 'annual']
    })
    print(client_data.to_string(index=False))
    
    # Ticket data structure
    print("\n2. Ticket Data:")
    ticket_data = pd.DataFrame({
        'ticket_id': ['TKT-001', 'TKT-002', 'TKT-003'],
        'client_id': ['client_1', 'client_2', 'client_3'],
        'priority': ['high', 'medium', 'low'],
        'status': ['resolved', 'in_progress', 'open'],
        'time_spent': [2.5, 1.0, 0.0],
        'billable_hours': [2.5, 1.0, 0.0]
    })
    print(ticket_data.to_string(index=False))
    
    # Financial data structure
    print("\n3. Financial Data:")
    financial_data = pd.DataFrame({
        'client_id': ['client_1', 'client_2', 'client_3'],
        'revenue': [50000, 1500, 6400],
        'cost': [35000, 1000, 4500],
        'profit_margin': [0.30, 0.33, 0.29]
    })
    print(financial_data.to_string(index=False))


def demonstrate_data_pipeline():
    """Demonstrate how the data flows through our pipeline"""
    print("\n🔄 Data Pipeline Flow:")
    print("=" * 25)
    
    print("1. Raw Data Sources:")
    print("   ├── Internal Database (SQLite)")
    print("   ├── SuperOps API (tickets, SLA metrics)")
    print("   └── QuickBooks API (financial data)")
    
    print("\n2. Data Extraction:")
    print("   └── src/data/ingestion/comprehensive_extractor.py")
    
    print("\n3. Data Preprocessing:")
    print("   ├── src/data/preprocessing/cleaning.py")
    print("   ├── src/data/preprocessing/imputation.py")
    print("   ├── src/data/preprocessing/outlier_detection.py")
    print("   ├── src/data/preprocessing/standardization.py")
    print("   └── src/data/preprocessing/normalization.py")
    
    print("\n4. Feature Engineering:")
    print("   ├── Financial Features (revenue, margins, billing)")
    print("   ├── Operational Features (SLA, resolution times)")
    print("   └── Behavioral Features (engagement, usage)")
    
    print("\n5. Client Profitability Genome:")
    print("   └── 50-dimensional client vectors")
    print("       ├── Financial Health (0-9)")
    print("       ├── Operational Efficiency (10-19)")
    print("       ├── Engagement Level (20-29)")
    print("       ├── Growth Potential (30-39)")
    print("       └── Risk Factors (40-49)")
    
    print("\n6. Model Training:")
    print("   ├── Profitability Prediction Models")
    print("   ├── Revenue Leak Detection")
    print("   ├── Churn Prediction")
    print("   ├── Dynamic Pricing Engine")
    print("   └── Budget Optimization")


def next_steps():
    """Show what you need to do to start working with real data"""
    print("\n📋 Next Steps to Work with Real Data:")
    print("=" * 40)
    
    print("\n1. Set Up Database:")
    print("   ├── Run database initialization scripts")
    print("   ├── Load sample data for testing")
    print("   └── Connect to your actual data sources")
    
    print("\n2. Configure API Connections:")
    print("   ├── Set SuperOps API credentials in environment")
    print("   ├── Set QuickBooks API credentials in environment")
    print("   └── Test API connections")
    
    print("\n3. Extract Real Data:")
    print("   ├── Run data extraction pipeline")
    print("   ├── Process data through preprocessing")
    print("   └── Create feature engineering")
    
    print("\n4. Train Models:")
    print("   ├── Split data into train/validation/test")
    print("   ├── Train models on your data")
    print("   └── Register models in MLflow")


def main():
    """Main function"""
    print("SuperHack AI/ML Data Setup Guide")
    print("=" * 35)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    load_sample_data()
    show_sample_data_structure()
    demonstrate_data_pipeline()
    next_steps()
    
    print("\n💡 TIP: You can start working with the sample data structure")
    print("   even before loading real data. The AI/ML pipeline is ready!")


if __name__ == "__main__":
    main()