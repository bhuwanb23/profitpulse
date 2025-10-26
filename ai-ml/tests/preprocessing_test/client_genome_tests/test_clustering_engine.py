"""
Test suite for Client Clustering Engine module
"""

import pytest
import numpy as np
import pandas as pd
from unittest.mock import Mock, patch

from src.data.preprocessing.client_genome.clustering_engine import (
    ClientClusteringEngine, perform_client_clustering
)


def test_clustering_engine_initialization():
    """Test Client Clustering Engine initialization"""
    engine = ClientClusteringEngine()
    assert engine is not None
    assert hasattr(engine, 'scaler')
    assert hasattr(engine, 'clustering_models')
    assert hasattr(engine, 'cluster_results')


def test_kmeans_clustering():
    """Test K-means clustering"""
    engine = ClientClusteringEngine()
    
    # Create test data
    client_genomes = {
        'client_1': np.array([1] * 25 + [0] * 25),
        'client_2': np.array([1] * 25 + [0] * 25),
        'client_3': np.array([0] * 25 + [1] * 25),
        'client_4': np.array([0] * 25 + [1] * 25)
    }
    
    # Perform K-means clustering
    cluster_assignments = engine.perform_kmeans_clustering(
        client_genomes, n_clusters=2
    )
    
    # Check results
    assert len(cluster_assignments) == 4
    assert all(client_id in cluster_assignments for client_id in client_genomes.keys())
    
    # Similar clients should be in the same cluster
    cluster_1 = cluster_assignments['client_1']
    cluster_2 = cluster_assignments['client_2']
    cluster_3 = cluster_assignments['client_3']
    cluster_4 = cluster_assignments['client_4']
    
    assert cluster_1 == cluster_2  # client_1 and client_2 should be in same cluster
    assert cluster_3 == cluster_4  # client_3 and client_4 should be in same cluster


def test_dbscan_clustering():
    """Test DBSCAN clustering"""
    engine = ClientClusteringEngine()
    
    # Create test data with clear clusters
    client_genomes = {
        'client_1': np.array([1, 1, 1] + [0] * 47),
        'client_2': np.array([1, 1, 0.9] + [0] * 47),
        'client_3': np.array([0, 0, 0] + [1] * 47),
        'client_4': np.array([0, 0.1, 0] + [1] * 47)
    }
    
    # Perform DBSCAN clustering
    cluster_assignments = engine.perform_dbscan_clustering(
        client_genomes, eps=0.5, min_samples=2
    )
    
    # Check results
    assert len(cluster_assignments) == 4
    assert all(client_id in cluster_assignments for client_id in client_genomes.keys())


def test_hierarchical_clustering():
    """Test hierarchical clustering"""
    engine = ClientClusteringEngine()
    
    # Create test data
    client_genomes = {
        'client_1': np.array([1] * 25 + [0] * 25),
        'client_2': np.array([1] * 25 + [0] * 25),
        'client_3': np.array([0] * 25 + [1] * 25),
        'client_4': np.array([0] * 25 + [1] * 25)
    }
    
    # Perform hierarchical clustering
    cluster_assignments = engine.perform_hierarchical_clustering(
        client_genomes, n_clusters=2
    )
    
    # Check results
    assert len(cluster_assignments) == 4
    assert all(client_id in cluster_assignments for client_id in client_genomes.keys())


def test_gaussian_mixture_clustering():
    """Test Gaussian Mixture Model clustering"""
    engine = ClientClusteringEngine()
    
    # Create test data
    client_genomes = {
        'client_1': np.array([1] * 25 + [0] * 25),
        'client_2': np.array([1] * 25 + [0] * 25),
        'client_3': np.array([0] * 25 + [1] * 25),
        'client_4': np.array([0] * 25 + [1] * 25)
    }
    
    # Perform Gaussian Mixture clustering
    cluster_assignments = engine.perform_gaussian_mixture_clustering(
        client_genomes, n_components=2
    )
    
    # Check results
    assert len(cluster_assignments) == 4
    assert all(client_id in cluster_assignments for client_id in client_genomes.keys())


def test_clustering_quality_evaluation():
    """Test clustering quality evaluation"""
    engine = ClientClusteringEngine()
    
    # Create test data
    client_genomes = {
        'client_1': np.array([1] * 25 + [0] * 25),
        'client_2': np.array([1] * 25 + [0] * 25),
        'client_3': np.array([0] * 25 + [1] * 25),
        'client_4': np.array([0] * 25 + [1] * 25)
    }
    
    cluster_labels = [0, 0, 1, 1]
    
    # Evaluate clustering quality
    quality_metrics = engine.evaluate_clustering_quality(
        client_genomes, cluster_labels
    )
    
    # Check results
    assert 'silhouette_score' in quality_metrics
    assert 'calinski_harabasz_score' in quality_metrics
    assert 'n_clusters' in quality_metrics
    assert quality_metrics['n_clusters'] == 2


def test_cluster_statistics():
    """Test cluster statistics"""
    engine = ClientClusteringEngine()
    
    # Create test data and perform clustering
    client_genomes = {
        'client_1': np.array([1] * 25 + [0] * 25),
        'client_2': np.array([1] * 25 + [0] * 25),
        'client_3': np.array([0] * 25 + [1] * 25),
        'client_4': np.array([0] * 25 + [1] * 25)
    }
    
    engine.perform_kmeans_clustering(client_genomes, n_clusters=2)
    
    # Get cluster statistics
    stats = engine.get_cluster_statistics('kmeans')
    
    # Check results
    assert 'cluster_sizes' in stats
    assert 'total_clients' in stats
    assert 'n_clusters' in stats
    assert stats['total_clients'] == 4


def test_clients_in_cluster():
    """Test getting clients in a specific cluster"""
    engine = ClientClusteringEngine()
    
    # Create test data and perform clustering
    client_genomes = {
        'client_1': np.array([1] * 25 + [0] * 25),
        'client_2': np.array([1] * 25 + [0] * 25),
        'client_3': np.array([0] * 25 + [1] * 25),
        'client_4': np.array([0] * 25 + [1] * 25)
    }
    
    engine.perform_kmeans_clustering(client_genomes, n_clusters=2)
    
    # Get clients in cluster 0
    clients_in_cluster = engine.get_clients_in_cluster(0, 'kmeans')
    
    # Check results
    assert isinstance(clients_in_cluster, list)
    # Should have at least one client
    assert len(clients_in_cluster) >= 1


def test_optimal_clustering():
    """Test optimal clustering"""
    engine = ClientClusteringEngine()
    
    # Create test data with clear clusters
    client_genomes = {
        'client_1': np.array([1] * 25 + [0] * 25),
        'client_2': np.array([1] * 25 + [0] * 25),
        'client_3': np.array([0] * 25 + [1] * 25),
        'client_4': np.array([0] * 25 + [1] * 25)
    }
    
    # Perform optimal clustering
    cluster_assignments, optimal_n_clusters = engine.perform_optimal_clustering(
        client_genomes, max_clusters=5, method='kmeans'
    )
    
    # Check results
    assert len(cluster_assignments) == 4
    assert isinstance(optimal_n_clusters, int)
    assert optimal_n_clusters >= 1


def test_convenience_function():
    """Test convenience function for client clustering"""
    # Create test data
    client_genomes = {
        'client_1': np.array([1] * 25 + [0] * 25),
        'client_2': np.array([1] * 25 + [0] * 25),
        'client_3': np.array([0] * 25 + [1] * 25),
        'client_4': np.array([0] * 25 + [1] * 25)
    }
    
    # Test K-means clustering
    cluster_assignments = perform_client_clustering(
        client_genomes, method='kmeans', n_clusters=2
    )
    
    # Check results
    assert len(cluster_assignments) == 4
    assert all(client_id in cluster_assignments for client_id in client_genomes.keys())
    
    # Test DBSCAN clustering
    cluster_assignments = perform_client_clustering(
        client_genomes, method='dbscan', eps=0.5, min_samples=2
    )
    
    # Check results
    assert len(cluster_assignments) == 4
    assert all(client_id in cluster_assignments for client_id in client_genomes.keys())


if __name__ == '__main__':
    pytest.main([__file__])