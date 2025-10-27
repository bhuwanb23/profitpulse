"""
Simple example showing where training and testing data is located in SuperHack AI/ML system
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
import numpy as np


def explain_data_locations():
    """Explain where training and testing data is located"""
    print("SuperHack AI/ML Data Locations and Flow")
    print("=" * 45)
    
    print("\n📂 DATA SOURCES:")
    print("1. Internal Database")
    print("   - Location: Database files in /database/")
    print("   - Content: Client profiles, service history, contracts")
    print("   - Access: src/data/ingestion/internal_db_connector.py")
    
    print("\n2. SuperOps API")
    print("   - Location: External API (SuperOps platform)")
    print("   - Content: Tickets, SLA metrics, technician data")
    print("   - Access: src/data/ingestion/superops_client.py")
    
    print("\n3. QuickBooks API")
    print("   - Location: External API (QuickBooks platform)")
    print("   - Content: Financial transactions, invoices, payments")
    print("   - Access: src/data/ingestion/quickbooks_client.py")
    
    print("\n🔄 DATA FLOW:")
    print("1. Extraction → src/data/ingestion/comprehensive_extractor.py")
    print("2. Preprocessing → src/data/preprocessing/")
    print("3. Feature Engineering → src/data/preprocessing/feature_engineering.py")
    print("4. Genome Creation → src/data/preprocessing/client_genome/")
    print("5. Model Training → src/models/ (various model files)")
    
    print("\n🧪 TRAINING/TEST DATA SPLIT:")
    print("Each ML model creates its own train/validation/test splits")
    print("Typical split: 70% training, 15% validation, 15% testing")
    print("Split strategy: Time-based or random, depending on model type")
    
    print("\n💾 MODEL STORAGE:")
    print("Models are stored in MLflow model registry")
    print("Location: Configurable via AI_MODEL_PATH environment variable")
    print("Default: ./ai-ml/models/")
    
    print("\n📊 SAMPLE DATA STRUCTURE:")
    sample_client_data = pd.DataFrame({
        'client_id': ['client_1', 'client_2', 'client_3'],
        'revenue': [50000, 75000, 30000],
        'cost': [30000, 45000, 20000],
        'profit_margin': [0.4, 0.4, 0.33],
        'tickets_resolved': [50, 75, 30],
        'sla_compliance': [0.95, 0.88, 0.92]
    })
    
    print("Sample client data structure:")
    print(sample_client_data.to_string(index=False))
    
    print("\n🧬 GENOME VECTOR EXAMPLE:")
    print("Each client gets a 50-dimensional genome vector:")
    genome_vector = np.random.rand(50)
    print(f"Genome dimensions 0-9: {genome_vector[:10]}")
    
    print("\n📈 MODEL TRAINING PROCESS:")
    print("1. Data is extracted from all sources")
    print("2. Features are engineered and genome vectors created")
    print("3. Data is split into train/validation/test sets")
    print("4. Models are trained on training data")
    print("5. Models are validated on validation data")
    print("6. Models are tested on test data")
    print("7. Best models are registered in MLflow")
    
    print("\n📋 TO ACCESS REAL DATA:")
    print("1. Set up API credentials in environment variables")
    print("2. Run data extraction pipeline")
    print("3. Process data through feature engineering")
    print("4. Use processed data for model training/testing")


if __name__ == "__main__":
    explain_data_locations()