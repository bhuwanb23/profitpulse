"""
Example showing how to access training and testing data in SuperHack AI/ML system
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from src.data.ingestion.comprehensive_extractor import create_comprehensive_extractor
from src.data.preprocessing.feature_engineering import engineer_features


def demonstrate_data_access():
    """Demonstrate how to access training and testing data"""
    print("SuperHack AI/ML Data Access Example")
    print("=" * 40)
    
    # Option 1: Using the Comprehensive Data Extractor
    print("\n1. Extracting data from all sources:")
    try:
        # Create extractor for the last 30 days
        extractor = create_comprehensive_extractor(
            start_date=datetime.now() - timedelta(days=30),
            end_date=datetime.now()
        )
        
        print("   Comprehensive data extractor created successfully")
        print("   Note: In a real implementation, this would connect to SuperOps, QuickBooks, and internal database")
        
        # Create mock data for demonstration
        sample_data = pd.DataFrame({
            'client_id': [f'client_{i}' for i in range(1, 6)],
            'revenue': [50000, 75000, 30000, 100000, 45000],
            'cost': [30000, 45000, 20000, 60000, 25000],
            'tickets_resolved': [50, 75, 30, 120, 40],
            'sla_compliance': [0.95, 0.88, 0.92, 0.97, 0.85]
        })
        print(f"   Created mock data with {len(sample_data)} records")
        
    except Exception as e:
        print(f"   Error creating data extractor: {e}")
        # Fallback to mock data
        sample_data = pd.DataFrame({
            'client_id': [f'client_{i}' for i in range(1, 6)],
            'revenue': [50000, 75000, 30000, 100000, 45000],
            'cost': [30000, 45000, 20000, 60000, 25000],
            'tickets_resolved': [50, 75, 30, 120, 40],
            'sla_compliance': [0.95, 0.88, 0.92, 0.97, 0.85]
        })
        print(f"   Created mock data with {len(sample_data)} records")
    
    # Option 2: Feature Engineering Pipeline
    print("\n2. Applying feature engineering:")
    feature_config = {
        'use_modular_system': True,
        'financial_features': True,
        'operational_features': True,
        'behavioral_features': True
    }
    
    try:
        engineered_data = engineer_features(sample_data, feature_config)
        print(f"   Engineered data shape: {engineered_data.shape}")
        print(f"   New features created: {engineered_data.shape[1] - sample_data.shape[1]}")
    except Exception as e:
        print(f"   Feature engineering demonstration - {e}")
        engineered_data = sample_data
    
    # Option 3: Creating Genome Vectors
    print("\n3. Creating client genome vectors:")
    genome_config = {
        'use_modular_system': True,
        'financial_features': True,
        'operational_features': True,
        'behavioral_features': True,
        'create_genome_vectors': True
    }
    
    try:
        genome_data = engineer_features(engineered_data, genome_config)
        genome_columns = [col for col in genome_data.columns if 'genome_dimension_' in col]
        print(f"   Created {len(genome_columns)} genome dimensions")
        print(f"   Genome data shape: {genome_data.shape}")
    except Exception as e:
        print(f"   Genome creation demonstration - {e}")
    
    print("\n4. Data for Model Training:")
    print("   - Raw data comes from src/data/ingestion/")
    print("   - Processed features in src/data/preprocessing/")
    print("   - Genome vectors created by client_genome/ modules")
    print("   - Training/test splits created within each model")
    
    print("\n5. Model Storage:")
    print("   - Models are registered in MLflow")
    print("   - Model artifacts stored in ai-ml/models/")
    print("   - Performance metrics tracked in MLflow")


if __name__ == "__main__":
    demonstrate_data_access()