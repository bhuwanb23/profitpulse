"""
Example script demonstrating the Client Profitability Genome system
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
import numpy as np
from datetime import datetime

# Import genome system components
from src.data.preprocessing.client_genome.genome_creator import GenomeCreator
from src.data.preprocessing.client_genome.similarity_calculator import SimilarityCalculator
from src.data.preprocessing.client_genome.clustering_engine import ClientClusteringEngine
from src.data.preprocessing.client_genome.comparison_tools import GenomeComparisonTools
from src.data.preprocessing.client_genome.genome_orchestrator import GenomeOrchestrator


def create_sample_client_data():
    """Create sample client data for demonstration"""
    # Create sample data for 10 clients with varying characteristics
    np.random.seed(42)  # For reproducible results
    
    client_data = []
    for i in range(10):
        client_id = f"client_{i+1}"
        
        # Create features with some realistic patterns
        # High-value clients (0-3)
        if i < 4:
            revenue_mean = np.random.uniform(50000, 100000)
            revenue_std = np.random.uniform(5000, 10000)
            profit_margin = np.random.uniform(0.2, 0.4)
            sla_compliance = np.random.uniform(0.9, 0.99)
            churn_risk = np.random.uniform(0.05, 0.15)
        # Medium-value clients (4-7)
        elif i < 8:
            revenue_mean = np.random.uniform(20000, 50000)
            revenue_std = np.random.uniform(3000, 8000)
            profit_margin = np.random.uniform(0.1, 0.25)
            sla_compliance = np.random.uniform(0.8, 0.95)
            churn_risk = np.random.uniform(0.1, 0.25)
        # Low-value clients (8-9)
        else:
            revenue_mean = np.random.uniform(5000, 20000)
            revenue_std = np.random.uniform(1000, 5000)
            profit_margin = np.random.uniform(0.05, 0.15)
            sla_compliance = np.random.uniform(0.7, 0.9)
            churn_risk = np.random.uniform(0.2, 0.4)
        
        client_record = {
            'client_id': client_id,
            'revenue_std': revenue_std,
            'revenue_mean': revenue_mean,
            'profit_margin_trend': profit_margin + np.random.uniform(-0.05, 0.05),
            'billing_accuracy': np.random.uniform(0.85, 0.99),
            'late_payment_rate': np.random.uniform(0.01, 0.15),
            'cost_efficiency': np.random.uniform(0.7, 0.95),
            'revenue_growth_rate': np.random.uniform(-0.05, 0.2),
            'contract_stability': np.random.uniform(0.8, 0.99),
            'revenue_diversification': np.random.uniform(0.5, 0.9),
            'forecast_accuracy': np.random.uniform(0.7, 0.95),
            'cash_flow_ratio': np.random.uniform(0.7, 0.95),
            'sla_compliance_rate': sla_compliance,
            'avg_resolution_time': np.random.uniform(12, 48),
            'target_resolution_time': 48,
            'technician_productivity': np.random.uniform(0.7, 0.95),
            'avg_quality_score': np.random.uniform(3.5, 5.0),
            'resource_utilization_rate': np.random.uniform(0.6, 0.9),
            'operational_cost_efficiency': np.random.uniform(0.6, 0.9),
            'service_consistency': np.random.uniform(0.7, 0.95),
            'automation_adoption_rate': np.random.uniform(0.3, 0.8),
            'process_optimization_score': np.random.uniform(0.5, 0.85),
            'scalability_score': np.random.uniform(0.6, 0.9),
            'login_frequency': np.random.randint(5, 30),
            'feature_usage_depth': np.random.uniform(0.4, 0.9),
            'support_requests_per_month': np.random.randint(0, 10),
            'communication_response_rate': np.random.uniform(0.6, 0.95),
            'feedback_participation_rate': np.random.uniform(0.1, 0.6),
            'training_completion_rate': np.random.uniform(0.3, 0.8),
            'portal_engagement_score': np.random.uniform(0.4, 0.9),
            'community_participation': np.random.uniform(0.05, 0.4),
            'advocacy_score': np.random.uniform(0.1, 0.5),
            'relationship_strength': np.random.uniform(0.6, 0.9),
            'expansion_opportunity_score': np.random.uniform(0.2, 0.8),
            'upsell_readiness': np.random.uniform(0.3, 0.7),
            'market_position_strength': np.random.uniform(0.4, 0.8),
            'innovation_adoption_rate': np.random.uniform(0.2, 0.7),
            'partnership_potential': np.random.uniform(0.1, 0.6),
            'cross_selling_opportunity': np.random.uniform(0.3, 0.7),
            'revenue_growth_trajectory': np.random.uniform(-0.1, 0.3),
            'service_utilization_trend': np.random.uniform(-0.05, 0.2),
            'market_expansion_potential': np.random.uniform(0.2, 0.6),
            'strategic_alignment': np.random.uniform(0.5, 0.8),
            'churn_probability': churn_risk,
            'payment_delinquency_risk': np.random.uniform(0.02, 0.2),
            'contract_expiration_risk': np.random.uniform(0.1, 0.4),
            'service_quality_risk': np.random.uniform(0.05, 0.3),
            'competitive_threat_level': np.random.uniform(0.2, 0.5),
            'market_volatility_exposure': np.random.uniform(0.1, 0.4),
            'dependency_risk': np.random.uniform(0.1, 0.3),
            'compliance_risk': np.random.uniform(0.05, 0.25),
            'operational_risk_score': np.random.uniform(0.08, 0.3),
            'financial_stability_risk': np.random.uniform(0.05, 0.2)
        }
        client_data.append(client_record)
    
    return pd.DataFrame(client_data)


def demonstrate_genome_creator():
    """Demonstrate the Genome Creator component"""
    print("=== Genome Creator Demonstration ===")
    
    # Create sample client data
    client_data = create_sample_client_data()
    print(f"Created sample data for {len(client_data)} clients")
    
    # Initialize genome creator
    creator = GenomeCreator()
    
    # Create genome vectors for all clients
    client_genomes = creator.create_genomes_for_clients(client_data)
    
    print(f"Created genome vectors for {len(client_genomes)} clients")
    for client_id, genome in list(client_genomes.items())[:3]:  # Show first 3
        print(f"  {client_id}: {genome.shape} vector, first 5 dimensions: {genome[:5]}")
    
    return client_genomes


def demonstrate_similarity_calculator(client_genomes):
    """Demonstrate the Similarity Calculator component"""
    print("\n=== Similarity Calculator Demonstration ===")
    
    # Initialize similarity calculator
    calculator = SimilarityCalculator()
    
    # Get two client genomes to compare
    client_ids = list(client_genomes.keys())
    genome1 = client_genomes[client_ids[0]]
    genome2 = client_genomes[client_ids[1]]
    
    # Calculate various similarities
    cosine_sim = calculator.calculate_cosine_similarity(genome1, genome2)
    euclidean_sim = calculator.calculate_euclidean_similarity(genome1, genome2)
    manhattan_sim = calculator.calculate_manhattan_similarity(genome1, genome2)
    jaccard_sim = calculator.calculate_jaccard_similarity(genome1, genome2)
    
    print(f"Similarity between {client_ids[0]} and {client_ids[1]}:")
    print(f"  Cosine similarity: {cosine_sim:.3f}")
    print(f"  Euclidean similarity: {euclidean_sim:.3f}")
    print(f"  Manhattan similarity: {manhattan_sim:.3f}")
    print(f"  Jaccard similarity: {jaccard_sim:.3f}")
    
    # Find most similar clients to the first client
    similar_clients = calculator.find_most_similar_clients(
        genome1, client_genomes, top_k=3
    )
    
    print(f"\nTop 3 clients most similar to {client_ids[0]}:")
    for client_id, similarity in similar_clients:
        print(f"  {client_id}: {similarity:.3f}")


def demonstrate_clustering_engine(client_genomes):
    """Demonstrate the Clustering Engine component"""
    print("\n=== Clustering Engine Demonstration ===")
    
    # Initialize clustering engine
    engine = ClientClusteringEngine()
    
    # Perform K-means clustering
    kmeans_clusters = engine.perform_kmeans_clustering(
        client_genomes, n_clusters=3
    )
    
    print("K-means clustering results:")
    cluster_counts = {}
    for client_id, cluster_id in kmeans_clusters.items():
        cluster_counts[cluster_id] = cluster_counts.get(cluster_id, 0) + 1
    for cluster_id, count in cluster_counts.items():
        print(f"  Cluster {cluster_id}: {count} clients")
    
    # Perform DBSCAN clustering
    dbscan_clusters = engine.perform_dbscan_clustering(
        client_genomes, eps=0.3, min_samples=2
    )
    
    print("\nDBSCAN clustering results:")
    cluster_counts = {}
    noise_points = 0
    for client_id, cluster_id in dbscan_clusters.items():
        if cluster_id == -1:
            noise_points += 1
        else:
            cluster_counts[cluster_id] = cluster_counts.get(cluster_id, 0) + 1
    
    for cluster_id, count in cluster_counts.items():
        print(f"  Cluster {cluster_id}: {count} clients")
    print(f"  Noise points: {noise_points} clients")


def demonstrate_comparison_tools(client_genomes):
    """Demonstrate the Comparison Tools component"""
    print("\n=== Comparison Tools Demonstration ===")
    
    # Initialize comparison tools
    tools = GenomeComparisonTools()
    
    # Compare two clients
    client_ids = list(client_genomes.keys())
    genome1 = client_genomes[client_ids[0]]
    genome2 = client_genomes[client_ids[1]]
    
    comparison_result = tools.compare_two_genomes(
        genome1, genome2, client_ids[0], client_ids[1]
    )
    
    print(f"Comparison between {client_ids[0]} and {client_ids[1]}:")
    print(f"  Overall cosine similarity: {comparison_result['overall_similarities']['cosine_similarity']:.3f}")
    print(f"  Average dimensional difference: {comparison_result['dimensional_analysis']['average_difference']:.3f}")
    print(f"  Most similar category: {comparison_result['category_analysis']['most_similar_category']}")
    print(f"  Least similar category: {comparison_result['category_analysis']['least_similar_category']}")
    
    # Identify anomalies
    anomalies = tools.identify_genome_anomalies(client_genomes, threshold=1.5)
    
    print(f"\nAnomaly detection results:")
    if isinstance(anomalies, dict) and 'anomalies_by_client' in anomalies:
        anomalous_clients = anomalies['anomalies_by_client']
        if isinstance(anomalous_clients, dict):
            print(f"  Found {len(anomalous_clients)} clients with anomalies")
            for i, (client_id, features) in enumerate(anomalous_clients.items()):
                if i >= 3:  # Show first 3
                    break
                print(f"    {client_id}: {len(features)} anomalous dimensions")
        else:
            print(f"  Anomalies by client is of type {type(anomalous_clients)}")
    else:
        print("  No anomalies detected")


def demonstrate_genome_orchestrator():
    """Demonstrate the Genome Orchestrator component"""
    print("\n=== Genome Orchestrator Demonstration ===")
    
    # Create sample client data
    client_data = create_sample_client_data()
    print(f"Created sample data for {len(client_data)} clients")
    
    # Initialize orchestrator
    orchestrator = GenomeOrchestrator()
    
    # Process client data through complete pipeline
    client_genomes = orchestrator.process_client_data(client_data)
    print(f"Processed {len(client_genomes)} client genomes")
    
    # Cluster clients
    cluster_assignments = orchestrator.cluster_clients(method="kmeans", n_clusters=3)
    print(f"Clustered clients into {len(set(cluster_assignments.values()))} clusters")
    
    # Find similar clients
    target_client = list(client_genomes.keys())[0]
    similar_clients = orchestrator.find_similar_clients(target_client, top_k=3)
    print(f"Top 3 clients similar to {target_client}:")
    for client_id, similarity in similar_clients:
        print(f"  {client_id}: {similarity:.3f}")
    
    # Generate client profile
    profile = orchestrator.generate_client_profile(target_client)
    print(f"\nProfile for {target_client}:")
    print(f"  Overall genome score: {profile['overall_assessment']['profitability_genome_score']:.3f}")
    print(f"  Strength level: {profile['overall_assessment']['overall_strength_level']}")
    
    # Show category scores
    print("  Category scores:")
    for category, data in profile['categories'].items():
        print(f"    {category}: {data['average_score']:.3f} ({data['strength_level']})")


def main():
    """Main demonstration function"""
    print("Client Profitability Genome System Demonstration")
    print("=" * 50)
    print(f"Timestamp: {datetime.now()}")
    print()
    
    # Demonstrate individual components
    client_genomes = demonstrate_genome_creator()
    demonstrate_similarity_calculator(client_genomes)
    demonstrate_clustering_engine(client_genomes)
    demonstrate_comparison_tools(client_genomes)
    
    # Demonstrate orchestrator
    demonstrate_genome_orchestrator()
    
    print("\n" + "=" * 50)
    print("Demonstration completed successfully!")


if __name__ == "__main__":
    main()