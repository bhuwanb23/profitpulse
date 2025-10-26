"""
Example demonstrating integration between feature engineering and genome system
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
import numpy as np
from datetime import datetime

# Import the integrated feature engineering system
from src.data.preprocessing.feature_engineering import engineer_features


def create_sample_data():
    """Create sample data for demonstration"""
    np.random.seed(42)
    
    # Create sample client data
    client_data = []
    for i in range(10):
        client_id = f"client_{i+1}"
        
        # Create realistic client data
        record = {
            'client_id': client_id,
            'revenue': np.random.uniform(10000, 100000),
            'cost': np.random.uniform(5000, 50000),
            'tickets_resolved': np.random.randint(10, 100),
            'total_tickets': np.random.randint(20, 150),
            'sla_met_count': np.random.randint(15, 120),
            'total_sla_tickets': np.random.randint(20, 150),
            'technician_hours': np.random.uniform(100, 500),
            'service_requests': np.random.randint(5, 50),
            'client_satisfaction': np.random.uniform(3.0, 5.0),
            'support_requests': np.random.randint(0, 20),
            'contract_value': np.random.uniform(5000, 50000),
            'contract_duration': np.random.randint(12, 60),
            'payments_made': np.random.randint(6, 30),
            'total_payments': np.random.randint(8, 36),
            'service_utilization': np.random.uniform(0.5, 1.0),
            'login_frequency': np.random.randint(10, 100),
            'feature_usage': np.random.uniform(0.3, 1.0),
            'feedback_score': np.random.uniform(3.0, 5.0),
            'engagement_score': np.random.uniform(0.4, 0.9),
            'expansion_opportunities': np.random.randint(0, 5),
            'upsell_readiness': np.random.uniform(0.3, 0.8),
            'churn_risk_score': np.random.uniform(0.1, 0.5),
            'market_position': np.random.uniform(0.4, 0.9),
            'innovation_adoption': np.random.uniform(0.3, 0.8),
            'partnership_potential': np.random.uniform(0.2, 0.7),
            'cross_selling_opportunities': np.random.uniform(0.3, 0.7),
            'revenue_growth': np.random.uniform(-0.1, 0.3),
            'service_utilization_trend': np.random.uniform(-0.05, 0.2),
            'market_expansion': np.random.uniform(0.2, 0.6),
            'strategic_alignment': np.random.uniform(0.5, 0.8),
            'payment_delinquency': np.random.uniform(0.02, 0.2),
            'contract_expiration_risk': np.random.uniform(0.1, 0.4),
            'service_quality_risk': np.random.uniform(0.05, 0.3),
            'competitive_threat': np.random.uniform(0.2, 0.5),
            'market_volatility': np.random.uniform(0.1, 0.4),
            'dependency_risk': np.random.uniform(0.1, 0.3),
            'compliance_risk': np.random.uniform(0.05, 0.25),
            'operational_risk': np.random.uniform(0.08, 0.3),
            'financial_stability_risk': np.random.uniform(0.05, 0.2),
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        client_data.append(record)
    
    return pd.DataFrame(client_data)


def demonstrate_integration():
    """Demonstrate integration between feature engineering and genome system"""
    print("Feature Engineering and Genome System Integration Demo")
    print("=" * 55)
    
    # Create sample data
    df = create_sample_data()
    print(f"Created sample data for {len(df)} clients")
    print(f"Columns: {list(df.columns)[:10]}...")  # Show first 10 columns
    
    # Configure feature engineering with genome vector creation
    feature_config = {
        'use_modular_system': True,
        'financial_features': True,
        'operational_features': True,
        'behavioral_features': True,
        'create_genome_vectors': True  # Enable genome vector creation
    }
    
    # Apply feature engineering with genome vector creation
    print("\nApplying feature engineering with genome vector creation...")
    df_engineered = engineer_features(df, feature_config)
    
    print(f"Engineered data shape: {df_engineered.shape}")
    print(f"New columns include genome dimensions: {[col for col in df_engineered.columns if 'genome_dimension' in col][:5]}...")
    
    # Show some genome vector values
    if 'genome_dimension_0' in df_engineered.columns:
        print("\nSample genome vector values (first 5 dimensions):")
        for i in range(min(5, len(df_engineered))):
            genome_values = [df_engineered.iloc[i][f'genome_dimension_{j}'] for j in range(5)]
            print(f"  Client {df_engineered.iloc[i]['client_id']}: {genome_values}")
    
    print("\nIntegration demonstration completed successfully!")


if __name__ == "__main__":
    demonstrate_integration()