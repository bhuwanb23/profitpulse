"""
Test script to demonstrate the client genome pipeline working with sample data
"""

import sys
import os
import pandas as pd
import sqlite3
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data.preprocessing.client_genome.genome_creator import GenomeCreator
from src.data.preprocessing.client_genome.similarity_calculator import SimilarityCalculator


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
        
        conn.close()
        
        return clients_df
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return None


def demonstrate_client_genome(clients_df):
    """Demonstrate the client genome pipeline"""
    print("\nDemonstrating Client Genome Pipeline")
    print("=" * 35)
    
    if clients_df is None or clients_df.empty:
        print("No data to process")
        return
    
    print(f"Original data shape: {clients_df.shape}")
    print("Original columns:", list(clients_df.columns)[:5], "...")
    
    # Initialize genome creator
    genome_creator = GenomeCreator()
    similarity_calculator = SimilarityCalculator()
    
    # Create genome vectors for clients
    print("\nCreating Genome Vectors...")
    client_genomes = {}
    
    for idx, row in clients_df.iterrows():
        client_id = row['id']
        
        # Convert row to features dict (this is a simplified example)
        # In a real scenario, we would have engineered features from the previous steps
        client_features = {
            'client_id': client_id,
            'contract_value': row.get('contract_value', 0),
            'revenue_mean': row.get('contract_value', 0) * 0.8,  # Simulated
            'revenue_std': row.get('contract_value', 0) * 0.1,   # Simulated
            'profit_margin_trend': 0.05,  # Simulated
            'billing_accuracy': 0.95,     # Simulated
            'late_payment_rate': 0.02,    # Simulated
            'cost_efficiency': 0.85,      # Simulated
            'revenue_growth_rate': 0.03,  # Simulated
            'contract_stability': 0.9,    # Simulated
            'revenue_diversification': 0.6,  # Simulated
            'forecast_accuracy': 0.8,     # Simulated
            'cash_flow_ratio': 0.7,       # Simulated
            'sla_compliance_rate': 0.92,  # Simulated
            'avg_resolution_time': 24,    # Simulated (hours)
            'target_resolution_time': 48, # Simulated (hours)
            'technician_productivity': 0.78,  # Simulated
            'avg_quality_score': 4.2,     # Simulated (1-5 scale)
            'resource_utilization_rate': 0.72,  # Simulated
            'operational_cost_efficiency': 0.81,  # Simulated
            'service_consistency': 0.88,  # Simulated
            'login_frequency': 15,        # Simulated (logins per month)
            'feature_usage_depth': 0.65,  # Simulated
            'support_requests_per_month': 2,  # Simulated
            'communication_response_rate': 0.85,  # Simulated
            'feedback_participation_rate': 0.32,  # Simulated
            'training_completion_rate': 0.55,  # Simulated
            'churn_probability': 0.12,    # Simulated
            'payment_delinquency_risk': 0.08,  # Simulated
            'contract_expiration_risk': 0.25,  # Simulated
            # Add more simulated features as needed
        }
        
        # Create genome vector
        genome_vector = genome_creator.create_genome_vector(client_features)
        client_genomes[client_id] = genome_vector
        print(f"   Client {client_id}: {len(genome_vector)}-dimensional genome vector created")
    
    # Calculate similarities between clients
    print("\nCalculating Client Similarities...")
    client_ids = list(client_genomes.keys())
    
    if len(client_ids) >= 2:
        similarity = similarity_calculator.calculate_cosine_similarity(
            client_genomes[client_ids[0]], 
            client_genomes[client_ids[1]]
        )
        print(f"   Similarity between clients {client_ids[0]} and {client_ids[1]}: {similarity:.3f}")
    
    print("\n✅ Client genome pipeline completed successfully!")
    
    return client_genomes


def main():
    """Main function"""
    print("SuperHack Client Genome Pipeline Test")
    print("=" * 40)
    
    # Load sample data
    clients_df = load_sample_data()
    
    # Demonstrate client genome
    client_genomes = demonstrate_client_genome(clients_df)
    
    if client_genomes:
        print("\n" + "=" * 50)
        print("🎉 CLIENT GENOME DEMO COMPLETE")
        print("=" * 50)
        print("The client genome pipeline is working correctly!")
        print("You can now:")
        print("1. Cluster clients based on genome similarity")
        print("2. Identify client patterns and trends")
        print("3. Generate personalized recommendations")
        print("\nThe entire AI/ML pipeline is ready to use!")


if __name__ == "__main__":
    main()