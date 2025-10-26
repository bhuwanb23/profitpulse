"""
Test suite for Genome Creator module
"""

import pytest
import numpy as np
import pandas as pd
from unittest.mock import Mock, patch

from src.data.preprocessing.client_genome.genome_creator import (
    GenomeCreator, create_client_genome, create_client_genomes
)
from src.data.preprocessing.client_genome import GENOME_STRUCTURE


def test_genome_creator_initialization():
    """Test Genome Creator initialization"""
    creator = GenomeCreator()
    assert creator is not None
    assert hasattr(creator, 'genome_history')


def test_create_genome_vector():
    """Test creation of a single genome vector"""
    creator = GenomeCreator()
    
    # Create mock client features
    client_features = {
        'revenue_std': 1000,
        'revenue_mean': 10000,
        'profit_margin_trend': 0.05,
        'billing_accuracy': 0.95,
        'late_payment_rate': 0.02,
        'cost_efficiency': 0.85,
        'revenue_growth_rate': 0.1,
        'contract_stability': 0.9,
        'revenue_diversification': 0.7,
        'forecast_accuracy': 0.8,
        'cash_flow_ratio': 0.85,
        'sla_compliance_rate': 0.95,
        'avg_resolution_time': 24,
        'target_resolution_time': 48,
        'technician_productivity': 0.8,
        'avg_quality_score': 4.2,
        'resource_utilization_rate': 0.75,
        'operational_cost_efficiency': 0.8,
        'service_consistency': 0.9,
        'automation_adoption_rate': 0.5,
        'process_optimization_score': 0.7,
        'scalability_score': 0.8,
        'login_frequency': 15,
        'feature_usage_depth': 0.7,
        'support_requests_per_month': 2,
        'communication_response_rate': 0.85,
        'feedback_participation_rate': 0.4,
        'training_completion_rate': 0.6,
        'portal_engagement_score': 0.75,
        'community_participation': 0.3,
        'advocacy_score': 0.4,
        'relationship_strength': 0.8,
        'expansion_opportunity_score': 0.5,
        'upsell_readiness': 0.6,
        'market_position_strength': 0.7,
        'innovation_adoption_rate': 0.5,
        'partnership_potential': 0.4,
        'cross_selling_opportunity': 0.6,
        'revenue_growth_trajectory': 0.3,
        'service_utilization_trend': 0.2,
        'market_expansion_potential': 0.5,
        'strategic_alignment': 0.7,
        'churn_probability': 0.1,
        'payment_delinquency_risk': 0.05,
        'contract_expiration_risk': 0.2,
        'service_quality_risk': 0.1,
        'competitive_threat_level': 0.3,
        'market_volatility_exposure': 0.2,
        'dependency_risk': 0.15,
        'compliance_risk': 0.1,
        'operational_risk_score': 0.12,
        'financial_stability_risk': 0.08
    }
    
    # Create genome vector
    genome_vector = creator.create_genome_vector(client_features)
    
    # Check that we get a 50-dimensional vector
    assert len(genome_vector) == 50
    assert isinstance(genome_vector, np.ndarray)
    
    # Check that all values are in 0-1 range
    assert np.all(genome_vector >= 0)
    assert np.all(genome_vector <= 1)


def test_create_genomes_for_clients():
    """Test creation of genome vectors for multiple clients"""
    creator = GenomeCreator()
    
    # Create mock client data
    client_data = pd.DataFrame({
        'client_id': ['client_1', 'client_2'],
        'revenue_std': [1000, 1500],
        'revenue_mean': [10000, 12000],
        'profit_margin_trend': [0.05, 0.03],
        'billing_accuracy': [0.95, 0.92],
        # Add other required features...
        'late_payment_rate': [0.02, 0.05],
        'cost_efficiency': [0.85, 0.8],
        'revenue_growth_rate': [0.1, 0.08],
        'contract_stability': [0.9, 0.85],
        'revenue_diversification': [0.7, 0.6],
        'forecast_accuracy': [0.8, 0.75],
        'cash_flow_ratio': [0.85, 0.8],
        'sla_compliance_rate': [0.95, 0.9],
        'avg_resolution_time': [24, 30],
        'target_resolution_time': [48, 48],
        'technician_productivity': [0.8, 0.75],
        'avg_quality_score': [4.2, 4.0],
        'resource_utilization_rate': [0.75, 0.7],
        'operational_cost_efficiency': [0.8, 0.75],
        'service_consistency': [0.9, 0.85],
        'automation_adoption_rate': [0.5, 0.4],
        'process_optimization_score': [0.7, 0.65],
        'scalability_score': [0.8, 0.75],
        'login_frequency': [15, 10],
        'feature_usage_depth': [0.7, 0.6],
        'support_requests_per_month': [2, 3],
        'communication_response_rate': [0.85, 0.8],
        'feedback_participation_rate': [0.4, 0.3],
        'training_completion_rate': [0.6, 0.5],
        'portal_engagement_score': [0.75, 0.7],
        'community_participation': [0.3, 0.25],
        'advocacy_score': [0.4, 0.35],
        'relationship_strength': [0.8, 0.75],
        'expansion_opportunity_score': [0.5, 0.45],
        'upsell_readiness': [0.6, 0.55],
        'market_position_strength': [0.7, 0.65],
        'innovation_adoption_rate': [0.5, 0.45],
        'partnership_potential': [0.4, 0.35],
        'cross_selling_opportunity': [0.6, 0.55],
        'revenue_growth_trajectory': [0.3, 0.25],
        'service_utilization_trend': [0.2, 0.15],
        'market_expansion_potential': [0.5, 0.45],
        'strategic_alignment': [0.7, 0.65],
        'churn_probability': [0.1, 0.15],
        'payment_delinquency_risk': [0.05, 0.08],
        'contract_expiration_risk': [0.2, 0.25],
        'service_quality_risk': [0.1, 0.15],
        'competitive_threat_level': [0.3, 0.35],
        'market_volatility_exposure': [0.2, 0.25],
        'dependency_risk': [0.15, 0.2],
        'compliance_risk': [0.1, 0.15],
        'operational_risk_score': [0.12, 0.18],
        'financial_stability_risk': [0.08, 0.12]
    })
    
    # Create genome vectors
    client_genomes = creator.create_genomes_for_clients(client_data)
    
    # Check results
    assert len(client_genomes) == 2
    assert 'client_1' in client_genomes
    assert 'client_2' in client_genomes
    
    # Check that each genome is 50-dimensional
    for genome in client_genomes.values():
        assert len(genome) == 50
        assert isinstance(genome, np.ndarray)
        assert np.all(genome >= 0)
        assert np.all(genome <= 1)


def test_genome_history():
    """Test genome history tracking"""
    creator = GenomeCreator()
    
    # Create mock client features
    client_features = {
        'revenue_std': 1000,
        'revenue_mean': 10000,
        'profit_margin_trend': 0.05,
        'billing_accuracy': 0.95,
        'late_payment_rate': 0.02,
        # Add minimal set of features for testing
    }
    
    # Create genome vector
    genome_vector = creator.create_genome_vector(client_features)
    
    # Check history
    history = creator.get_genome_history('test_client')
    # History should be None for non-existent client
    assert history is None


def test_convenience_functions():
    """Test convenience functions"""
    # Test create_client_genome
    client_features = {
        'revenue_std': 1000,
        'revenue_mean': 10000,
        'profit_margin_trend': 0.05,
        'billing_accuracy': 0.95,
        'late_payment_rate': 0.02,
        # Add minimal set of features for testing
    }
    
    genome_vector = create_client_genome(client_features)
    assert len(genome_vector) == 50
    assert isinstance(genome_vector, np.ndarray)
    
    # Test create_client_genomes
    client_data = pd.DataFrame({
        'client_id': ['client_1'],
        'revenue_std': [1000],
        'revenue_mean': [10000],
        'profit_margin_trend': [0.05],
        'billing_accuracy': [0.95],
        'late_payment_rate': [0.02],
        # Add minimal set of features for testing
    })
    
    client_genomes = create_client_genomes(client_data)
    assert len(client_genomes) == 1
    assert 'client_1' in client_genomes
    assert len(client_genomes['client_1']) == 50


if __name__ == '__main__':
    pytest.main([__file__])