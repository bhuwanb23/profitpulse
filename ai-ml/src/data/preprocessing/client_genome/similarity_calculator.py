"""
Vector Similarity Calculator Module
Calculates similarity between client genome vectors using multiple distance metrics
"""

import numpy as np
from typing import Dict, List, Optional, Union, Tuple
import logging
from scipy.spatial.distance import cosine, euclidean, cityblock
from scipy.spatial import distance
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


class SimilarityCalculator:
    """Calculates similarity between client genome vectors"""
    
    def __init__(self):
        """Initialize the Similarity Calculator"""
        pass
    
    def calculate_cosine_similarity(self, genome1: np.ndarray, genome2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two genome vectors
        
        Args:
            genome1: First genome vector (50-dimensional)
            genome2: Second genome vector (50-dimensional)
            
        Returns:
            float: Cosine similarity score (0-1, where 1 is identical)
        """
        try:
            # Reshape vectors for sklearn cosine_similarity
            genome1_reshaped = genome1.reshape(1, -1)
            genome2_reshaped = genome2.reshape(1, -1)
            
            # Calculate cosine similarity
            similarity = cosine_similarity(genome1_reshaped, genome2_reshaped)[0][0]
            
            # Ensure the result is in 0-1 range
            return float(np.clip(similarity, 0, 1))
        except Exception as e:
            logger.error(f"Error calculating cosine similarity: {e}")
            return 0.0
    
    def calculate_euclidean_distance(self, genome1: np.ndarray, genome2: np.ndarray) -> float:
        """
        Calculate Euclidean distance between two genome vectors
        
        Args:
            genome1: First genome vector (50-dimensional)
            genome2: Second genome vector (50-dimensional)
            
        Returns:
            float: Euclidean distance (0-infinity, where 0 is identical)
        """
        try:
            distance = euclidean(genome1, genome2)
            return float(distance)
        except Exception as e:
            logger.error(f"Error calculating Euclidean distance: {e}")
            return float('inf')
    
    def calculate_euclidean_similarity(self, genome1: np.ndarray, genome2: np.ndarray) -> float:
        """
        Calculate Euclidean similarity (normalized to 0-1 range)
        
        Args:
            genome1: First genome vector (50-dimensional)
            genome2: Second genome vector (50-dimensional)
            
        Returns:
            float: Euclidean similarity score (0-1, where 1 is identical)
        """
        try:
            # Calculate Euclidean distance
            euclidean_dist = self.calculate_euclidean_distance(genome1, genome2)
            
            # Convert distance to similarity (0-1 range)
            # Using exponential decay: similarity = exp(-distance)
            similarity = np.exp(-euclidean_dist / 50)  # 50 is scaling factor for 50-dim space
            
            return float(np.clip(similarity, 0, 1))
        except Exception as e:
            logger.error(f"Error calculating Euclidean similarity: {e}")
            return 0.0
    
    def calculate_manhattan_distance(self, genome1: np.ndarray, genome2: np.ndarray) -> float:
        """
        Calculate Manhattan (L1) distance between two genome vectors
        
        Args:
            genome1: First genome vector (50-dimensional)
            genome2: Second genome vector (50-dimensional)
            
        Returns:
            float: Manhattan distance (0-infinity, where 0 is identical)
        """
        try:
            distance = cityblock(genome1, genome2)
            return float(distance)
        except Exception as e:
            logger.error(f"Error calculating Manhattan distance: {e}")
            return float('inf')
    
    def calculate_manhattan_similarity(self, genome1: np.ndarray, genome2: np.ndarray) -> float:
        """
        Calculate Manhattan similarity (normalized to 0-1 range)
        
        Args:
            genome1: First genome vector (50-dimensional)
            genome2: Second genome vector (50-dimensional)
            
        Returns:
            float: Manhattan similarity score (0-1, where 1 is identical)
        """
        try:
            # Calculate Manhattan distance
            manhattan_dist = self.calculate_manhattan_distance(genome1, genome2)
            
            # Convert distance to similarity (0-1 range)
            # Using exponential decay: similarity = exp(-distance)
            similarity = np.exp(-manhattan_dist / 50)  # 50 is scaling factor for 50-dim space
            
            return float(np.clip(similarity, 0, 1))
        except Exception as e:
            logger.error(f"Error calculating Manhattan similarity: {e}")
            return 0.0
    
    def calculate_jaccard_similarity(self, genome1: np.ndarray, genome2: np.ndarray, 
                                   threshold: float = 0.5) -> float:
        """
        Calculate Jaccard similarity between two genome vectors using thresholding
        
        Args:
            genome1: First genome vector (50-dimensional)
            genome2: Second genome vector (50-dimensional)
            threshold: Threshold for binarizing vectors (default: 0.5)
            
        Returns:
            float: Jaccard similarity score (0-1, where 1 is identical)
        """
        try:
            # Binarize vectors using threshold
            binary_genome1 = (genome1 >= threshold).astype(int)
            binary_genome2 = (genome2 >= threshold).astype(int)
            
            # Calculate intersection and union
            intersection = np.sum(np.logical_and(binary_genome1, binary_genome2))
            union = np.sum(np.logical_or(binary_genome1, binary_genome2))
            
            # Calculate Jaccard similarity
            if union == 0:
                return 1.0  # Both vectors are all zeros
            
            jaccard_similarity = intersection / union
            return float(jaccard_similarity)
        except Exception as e:
            logger.error(f"Error calculating Jaccard similarity: {e}")
            return 0.0
    
    def calculate_category_similarity(self, genome1: np.ndarray, genome2: np.ndarray,
                                    category: str) -> Dict[str, float]:
        """
        Calculate similarity for a specific category of dimensions
        
        Args:
            genome1: First genome vector (50-dimensional)
            genome2: Second genome vector (50-dimensional)
            category: Category name ('FinancialHealth', 'OperationalEfficiency', 
                     'EngagementLevel', 'GrowthPotential', 'RiskFactors')
            
        Returns:
            Dict[str, float]: Dictionary with similarity scores for the category
        """
        from . import GENOME_DIMENSIONS
        
        if category not in GENOME_DIMENSIONS:
            logger.warning(f"Unknown category: {category}")
            return {}
        
        try:
            # Get dimension indices for the category
            dim_indices = GENOME_DIMENSIONS[category]['dimensions']
            
            # Extract category-specific vectors
            cat_genome1 = genome1[dim_indices]
            cat_genome2 = genome2[dim_indices]
            
            # Calculate similarities for this category
            similarities = {
                f'{category}_cosine_similarity': self.calculate_cosine_similarity(cat_genome1, cat_genome2),
                f'{category}_euclidean_similarity': self.calculate_euclidean_similarity(cat_genome1, cat_genome2),
                f'{category}_manhattan_similarity': self.calculate_manhattan_similarity(cat_genome1, cat_genome2),
                f'{category}_jaccard_similarity': self.calculate_jaccard_similarity(cat_genome1, cat_genome2)
            }
            
            return similarities
        except Exception as e:
            logger.error(f"Error calculating category similarity for {category}: {e}")
            return {}
    
    def calculate_comprehensive_similarity(self, genome1: np.ndarray, genome2: np.ndarray) -> Dict[str, float]:
        """
        Calculate comprehensive similarity metrics between two genome vectors
        
        Args:
            genome1: First genome vector (50-dimensional)
            genome2: Second genome vector (50-dimensional)
            
        Returns:
            Dict[str, float]: Dictionary with all similarity metrics
        """
        try:
            # Overall similarities
            similarities = {
                'cosine_similarity': self.calculate_cosine_similarity(genome1, genome2),
                'euclidean_distance': self.calculate_euclidean_distance(genome1, genome2),
                'euclidean_similarity': self.calculate_euclidean_similarity(genome1, genome2),
                'manhattan_distance': self.calculate_manhattan_distance(genome1, genome2),
                'manhattan_similarity': self.calculate_manhattan_similarity(genome1, genome2),
                'jaccard_similarity': self.calculate_jaccard_similarity(genome1, genome2)
            }
            
            # Category-specific similarities
            from . import GENOME_DIMENSIONS
            for category in GENOME_DIMENSIONS.keys():
                category_similarities = self.calculate_category_similarity(genome1, genome2, category)
                similarities.update(category_similarities)
            
            logger.info("Successfully calculated comprehensive similarity metrics")
            return similarities
        except Exception as e:
            logger.error(f"Error calculating comprehensive similarity: {e}")
            return {}
    
    def find_most_similar_clients(self, target_genome: np.ndarray, 
                                client_genomes: Dict[str, np.ndarray],
                                top_k: int = 5,
                                metric: str = 'cosine') -> List[Tuple[str, float]]:
        """
        Find the most similar clients to a target genome
        
        Args:
            target_genome: Target genome vector (50-dimensional)
            client_genomes: Dictionary mapping client IDs to genome vectors
            top_k: Number of most similar clients to return
            metric: Similarity metric to use ('cosine', 'euclidean', 'manhattan')
            
        Returns:
            List[Tuple[str, float]]: List of (client_id, similarity_score) tuples, sorted by similarity
        """
        try:
            similarities = []
            
            for client_id, genome in client_genomes.items():
                if metric == 'cosine':
                    similarity = self.calculate_cosine_similarity(target_genome, genome)
                elif metric == 'euclidean':
                    similarity = self.calculate_euclidean_similarity(target_genome, genome)
                elif metric == 'manhattan':
                    similarity = self.calculate_manhattan_similarity(target_genome, genome)
                else:
                    # Default to cosine similarity
                    similarity = self.calculate_cosine_similarity(target_genome, genome)
                
                similarities.append((client_id, similarity))
            
            # Sort by similarity (descending order)
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            # Return top K results
            return similarities[:top_k]
        except Exception as e:
            logger.error(f"Error finding most similar clients: {e}")
            return []


def calculate_genome_similarity(genome1: np.ndarray, genome2: np.ndarray) -> Dict[str, float]:
    """
    Convenience function to calculate comprehensive similarity between two genome vectors
    
    Args:
        genome1: First genome vector (50-dimensional)
        genome2: Second genome vector (50-dimensional)
        
    Returns:
        Dict[str, float]: Dictionary with all similarity metrics
    """
    calculator = SimilarityCalculator()
    return calculator.calculate_comprehensive_similarity(genome1, genome2)


def find_similar_clients(target_genome: np.ndarray, 
                        client_genomes: Dict[str, np.ndarray],
                        top_k: int = 5) -> List[Tuple[str, float]]:
    """
    Convenience function to find most similar clients
    
    Args:
        target_genome: Target genome vector (50-dimensional)
        client_genomes: Dictionary mapping client IDs to genome vectors
        top_k: Number of most similar clients to return
        
    Returns:
        List[Tuple[str, float]]: List of (client_id, similarity_score) tuples, sorted by similarity
    """
    calculator = SimilarityCalculator()
    return calculator.find_most_similar_clients(target_genome, client_genomes, top_k)