"""
Test suite for Vector Similarity Calculator module
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch

from src.data.preprocessing.client_genome.similarity_calculator import (
    SimilarityCalculator, calculate_genome_similarity, find_similar_clients
)
from src.data.preprocessing.client_genome import GENOME_STRUCTURE


def test_similarity_calculator_initialization():
    """Test Similarity Calculator initialization"""
    calculator = SimilarityCalculator()
    assert calculator is not None


def test_cosine_similarity():
    """Test cosine similarity calculation"""
    calculator = SimilarityCalculator()
    
    # Create two identical vectors
    genome1 = np.random.rand(50)
    genome2 = genome1.copy()
    
    # Cosine similarity of identical vectors should be 1.0
    similarity = calculator.calculate_cosine_similarity(genome1, genome2)
    assert abs(similarity - 1.0) < 1e-6
    
    # Create two orthogonal vectors
    genome3 = np.array([1, 0] + [0] * 48)
    genome4 = np.array([0, 1] + [0] * 48)
    
    # Cosine similarity of orthogonal vectors should be 0.0
    similarity = calculator.calculate_cosine_similarity(genome3, genome4)
    assert abs(similarity - 0.0) < 1e-6


def test_euclidean_distance():
    """Test Euclidean distance calculation"""
    calculator = SimilarityCalculator()
    
    # Create two identical vectors
    genome1 = np.random.rand(50)
    genome2 = genome1.copy()
    
    # Euclidean distance of identical vectors should be 0.0
    distance = calculator.calculate_euclidean_distance(genome1, genome2)
    assert abs(distance - 0.0) < 1e-6
    
    # Create two simple vectors
    genome3 = np.array([0] * 50)
    genome4 = np.array([1] * 50)
    
    # Euclidean distance should be sqrt(50)
    distance = calculator.calculate_euclidean_distance(genome3, genome4)
    expected_distance = np.sqrt(50)
    assert abs(distance - expected_distance) < 1e-6


def test_euclidean_similarity():
    """Test Euclidean similarity calculation"""
    calculator = SimilarityCalculator()
    
    # Create two identical vectors
    genome1 = np.random.rand(50)
    genome2 = genome1.copy()
    
    # Euclidean similarity of identical vectors should be 1.0
    similarity = calculator.calculate_euclidean_similarity(genome1, genome2)
    assert abs(similarity - 1.0) < 1e-6


def test_manhattan_distance():
    """Test Manhattan distance calculation"""
    calculator = SimilarityCalculator()
    
    # Create two identical vectors
    genome1 = np.random.rand(50)
    genome2 = genome1.copy()
    
    # Manhattan distance of identical vectors should be 0.0
    distance = calculator.calculate_manhattan_distance(genome1, genome2)
    assert abs(distance - 0.0) < 1e-6
    
    # Create two simple vectors
    genome3 = np.array([0] * 50)
    genome4 = np.array([1] * 50)
    
    # Manhattan distance should be 50
    distance = calculator.calculate_manhattan_distance(genome3, genome4)
    assert abs(distance - 50.0) < 1e-6


def test_manhattan_similarity():
    """Test Manhattan similarity calculation"""
    calculator = SimilarityCalculator()
    
    # Create two identical vectors
    genome1 = np.random.rand(50)
    genome2 = genome1.copy()
    
    # Manhattan similarity of identical vectors should be 1.0
    similarity = calculator.calculate_manhattan_similarity(genome1, genome2)
    assert abs(similarity - 1.0) < 1e-6


def test_jaccard_similarity():
    """Test Jaccard similarity calculation"""
    calculator = SimilarityCalculator()
    
    # Create two identical vectors
    genome1 = np.array([1] * 25 + [0] * 25)
    genome2 = genome1.copy()
    
    # Jaccard similarity of identical vectors should be 1.0
    similarity = calculator.calculate_jaccard_similarity(genome1, genome2)
    assert abs(similarity - 1.0) < 1e-6
    
    # Create two disjoint vectors
    genome3 = np.array([1] * 25 + [0] * 25)
    genome4 = np.array([0] * 25 + [1] * 25)
    
    # Jaccard similarity of disjoint vectors should be 0.0
    similarity = calculator.calculate_jaccard_similarity(genome3, genome4)
    assert abs(similarity - 0.0) < 1e-6


def test_category_similarity():
    """Test category similarity calculation"""
    calculator = SimilarityCalculator()
    
    # Create two identical vectors
    genome1 = np.random.rand(50)
    genome2 = genome1.copy()
    
    # Test financial health category
    similarities = calculator.calculate_category_similarity(genome1, genome2, 'FinancialHealth')
    assert 'FinancialHealth_cosine_similarity' in similarities
    assert abs(similarities['FinancialHealth_cosine_similarity'] - 1.0) < 1e-6
    
    # Test unknown category
    similarities = calculator.calculate_category_similarity(genome1, genome2, 'UnknownCategory')
    assert len(similarities) == 0


def test_comprehensive_similarity():
    """Test comprehensive similarity calculation"""
    calculator = SimilarityCalculator()
    
    # Create two identical vectors
    genome1 = np.random.rand(50)
    genome2 = genome1.copy()
    
    # Calculate comprehensive similarities
    similarities = calculator.calculate_comprehensive_similarity(genome1, genome2)
    
    # Check that we have all expected metrics
    expected_metrics = [
        'cosine_similarity', 'euclidean_distance', 'euclidean_similarity',
        'manhattan_distance', 'manhattan_similarity', 'jaccard_similarity'
    ]
    
    for metric in expected_metrics:
        assert metric in similarities
    
    # Check that cosine similarity is 1.0 for identical vectors
    assert abs(similarities['cosine_similarity'] - 1.0) < 1e-6


def test_find_most_similar_clients():
    """Test finding most similar clients"""
    calculator = SimilarityCalculator()
    
    # Create test data
    target_genome = np.array([1] * 25 + [0] * 25)
    client_genomes = {
        'client_1': np.array([1] * 25 + [0] * 25),  # Identical to target
        'client_2': np.array([0] * 25 + [1] * 25),  # Orthogonal to target
        'client_3': np.array([0.5] * 50)            # Somewhere in between
    }
    
    # Find most similar clients using cosine similarity
    similar_clients = calculator.find_most_similar_clients(
        target_genome, client_genomes, top_k=3, metric='cosine'
    )
    
    # Check results
    assert len(similar_clients) == 3
    assert similar_clients[0][0] == 'client_1'  # client_1 should be most similar
    assert similar_clients[0][1] == 1.0         # cosine similarity should be 1.0


def test_convenience_functions():
    """Test convenience functions"""
    # Test calculate_genome_similarity
    genome1 = np.random.rand(50)
    genome2 = genome1.copy()
    
    similarities = calculate_genome_similarity(genome1, genome2)
    assert 'cosine_similarity' in similarities
    assert abs(similarities['cosine_similarity'] - 1.0) < 1e-6
    
    # Test find_similar_clients
    target_genome = np.array([1] * 25 + [0] * 25)
    client_genomes = {
        'client_1': np.array([1] * 25 + [0] * 25),
        'client_2': np.array([0] * 25 + [1] * 25)
    }
    
    similar_clients = find_similar_clients(target_genome, client_genomes, top_k=2)
    assert len(similar_clients) == 2
    assert similar_clients[0][0] == 'client_1'


if __name__ == '__main__':
    pytest.main([__file__])