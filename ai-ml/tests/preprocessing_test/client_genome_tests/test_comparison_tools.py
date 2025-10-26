"""
Test suite for Genome Comparison Tools module
"""

import pytest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from src.data.preprocessing.client_genome.comparison_tools import (
    GenomeComparisonTools, compare_client_genomes, identify_genome_anomalies
)
from src.data.preprocessing.client_genome import GENOME_STRUCTURE


def test_comparison_tools_initialization():
    """Test Genome Comparison Tools initialization"""
    tools = GenomeComparisonTools()
    assert tools is not None
    assert hasattr(tools, 'similarity_calculator')
    assert hasattr(tools, 'comparison_history')


def test_compare_two_genomes():
    """Test comparison of two genome vectors"""
    tools = GenomeComparisonTools()
    
    # Create two identical vectors
    genome1 = np.random.rand(50)
    genome2 = genome1.copy()
    
    # Compare genomes
    comparison_result = tools.compare_two_genomes(
        genome1, genome2, "Client1", "Client2"
    )
    
    # Check results
    assert 'clients' in comparison_result
    assert 'overall_similarities' in comparison_result
    assert 'dimensional_analysis' in comparison_result
    assert 'category_analysis' in comparison_result
    assert comparison_result['clients']['client1'] == "Client1"
    assert comparison_result['clients']['client2'] == "Client2"
    
    # For identical vectors, differences should be minimal
    dimensional_analysis = comparison_result['dimensional_analysis']
    assert abs(dimensional_analysis['average_difference']) < 1e-6


def test_compare_genome_cluster():
    """Test comparison of genome cluster"""
    tools = GenomeComparisonTools()
    
    # Create test data
    client_genomes = {
        'client_1': np.array([1] * 25 + [0] * 25),
        'client_2': np.array([1] * 25 + [0] * 25),
        'client_3': np.array([0] * 25 + [1] * 25),
        'client_4': np.array([0] * 25 + [1] * 25)
    }
    
    cluster_assignments = {
        'client_1': 0,
        'client_2': 0,
        'client_3': 1,
        'client_4': 1
    }
    
    # Compare cluster
    cluster_analysis = tools.compare_genome_cluster(
        client_genomes, cluster_assignments
    )
    
    # Check results
    assert len(cluster_analysis) == 2
    assert 0 in cluster_analysis
    assert 1 in cluster_analysis
    assert 'n_clients' in cluster_analysis[0]
    assert 'n_clients' in cluster_analysis[1]
    assert cluster_analysis[0]['n_clients'] == 2
    assert cluster_analysis[1]['n_clients'] == 2


def test_track_genome_evolution():
    """Test tracking genome evolution over time"""
    tools = GenomeComparisonTools()
    
    # Create genome history
    genome_history = [
        (datetime.now() - timedelta(days=30), np.random.rand(50)),
        (datetime.now() - timedelta(days=15), np.random.rand(50)),
        (datetime.now(), np.random.rand(50))
    ]
    
    # Track evolution
    evolution_analysis = tools.track_genome_evolution(
        "test_client", genome_history
    )
    
    # Check results
    assert 'client_id' in evolution_analysis
    assert 'n_observations' in evolution_analysis
    assert 'time_span' in evolution_analysis
    assert 'overall_changes' in evolution_analysis
    assert evolution_analysis['client_id'] == "test_client"
    assert evolution_analysis['n_observations'] == 3


def test_identify_genome_anomalies():
    """Test identifying genome anomalies"""
    tools = GenomeComparisonTools()
    
    # Create test data with clear outliers
    client_genomes = {
        'client_1': np.array([0.5] * 50),  # Normal client
        'client_2': np.array([0.5] * 50),  # Normal client
        'client_3': np.array([0.5] * 50),  # Normal client
        'client_4': np.array([0.5] * 49 + [0.99])  # Anomalous client
    }
    
    # Identify anomalies
    anomalies = tools.identify_genome_anomalies(
        client_genomes, threshold=2.0
    )
    
    # Check results
    assert isinstance(anomalies, dict)
    # Should have some anomalies detected
    assert len(anomalies) > 0


def test_generate_comparison_report():
    """Test generating comparison report"""
    tools = GenomeComparisonTools()
    
    # Create mock comparison results
    comparison_results = {
        'clients': {
            'client1': 'Client1',
            'client2': 'Client2'
        },
        'timestamp': datetime.now().isoformat(),
        'overall_similarities': {
            'cosine_similarity': 0.95,
            'euclidean_similarity': 0.85,
            'manhattan_similarity': 0.80,
            'jaccard_similarity': 0.75
        },
        'dimensional_analysis': {
            'most_similar_dimension': {
                'index': 0,
                'feature': 'RevenueStability',
                'category': 'FinancialHealth',
                'difference': 0.01
            },
            'least_similar_dimension': {
                'index': 1,
                'feature': 'ProfitMarginTrend',
                'category': 'FinancialHealth',
                'difference': 0.2
            },
            'average_difference': 0.1
        },
        'category_analysis': {
            'similarities': {
                'FinancialHealth': 0.9,
                'OperationalEfficiency': 0.85,
                'EngagementLevel': 0.8,
                'GrowthPotential': 0.75,
                'RiskFactors': 0.7
            },
            'differences': {
                'FinancialHealth': 0.1,
                'OperationalEfficiency': 0.15,
                'EngagementLevel': 0.2,
                'GrowthPotential': 0.25,
                'RiskFactors': 0.3
            },
            'most_similar_category': 'FinancialHealth',
            'least_similar_category': 'RiskFactors'
        }
    }
    
    # Generate report
    report = tools.generate_comparison_report(comparison_results)
    
    # Check results
    assert isinstance(report, str)
    assert len(report) > 0
    assert 'Client Genome Comparison Report' in report
    assert 'Client1 vs Client2' in report


def test_convenience_functions():
    """Test convenience functions"""
    # Test compare_client_genomes
    genome1 = np.random.rand(50)
    genome2 = genome1.copy()
    
    comparison_result = compare_client_genomes(
        genome1, genome2, "Client1", "Client2"
    )
    
    assert 'clients' in comparison_result
    assert 'overall_similarities' in comparison_result
    
    # Test identify_genome_anomalies
    client_genomes = {
        'client_1': np.array([0.5] * 50),
        'client_2': np.array([0.5] * 50),
        'client_3': np.array([0.5] * 49 + [0.99])
    }
    
    anomalies = identify_genome_anomalies(client_genomes, threshold=2.0)
    assert isinstance(anomalies, dict)


if __name__ == '__main__':
    pytest.main([__file__])