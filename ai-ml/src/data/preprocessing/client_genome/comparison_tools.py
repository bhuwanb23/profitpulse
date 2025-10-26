"""
Genome Comparison Tools Module
Provides tools for comparing and analyzing client genome vectors
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple, Union
import logging
from datetime import datetime
from collections import defaultdict

from . import GENOME_STRUCTURE, GENOME_DIMENSIONS
from .similarity_calculator import SimilarityCalculator

logger = logging.getLogger(__name__)


class GenomeComparisonTools:
    """Tools for comparing and analyzing client genome vectors"""
    
    def __init__(self):
        """Initialize the Genome Comparison Tools"""
        self.similarity_calculator = SimilarityCalculator()
        self.comparison_history = []
    
    def compare_two_genomes(self, genome1: np.ndarray, genome2: np.ndarray,
                          client1_id: str = "Client1", client2_id: str = "Client2") -> Dict[str, Any]:
        """
        Compare two genome vectors and provide detailed analysis
        
        Args:
            genome1: First genome vector (50-dimensional)
            genome2: Second genome vector (50-dimensional)
            client1_id: Identifier for first client
            client2_id: Identifier for second client
            
        Returns:
            Dict[str, Any]: Detailed comparison results
        """
        try:
            # Calculate comprehensive similarities
            similarities = self.similarity_calculator.calculate_comprehensive_similarity(genome1, genome2)
            
            # Calculate dimensional differences
            differences = np.abs(genome1 - genome2)
            
            # Identify most and least similar dimensions
            most_similar_dim = np.argmin(differences)
            least_similar_dim = np.argmax(differences)
            
            # Calculate category-level differences
            category_differences = {}
            category_similarities = {}
            
            for category, info in GENOME_DIMENSIONS.items():
                dim_indices = info['dimensions']
                cat_diff = np.mean(np.abs(genome1[dim_indices] - genome2[dim_indices]))
                cat_sim = 1 - cat_diff  # Simple similarity from difference
                
                category_differences[category] = float(cat_diff)
                category_similarities[category] = float(cat_sim)
            
            # Create detailed comparison report
            comparison_result = {
                'clients': {
                    'client1': client1_id,
                    'client2': client2_id
                },
                'overall_similarities': similarities,
                'dimensional_analysis': {
                    'most_similar_dimension': {
                        'index': int(most_similar_dim),
                        'feature': GENOME_STRUCTURE[most_similar_dim]['feature'],
                        'category': GENOME_STRUCTURE[most_similar_dim]['category'],
                        'difference': float(differences[most_similar_dim])
                    },
                    'least_similar_dimension': {
                        'index': int(least_similar_dim),
                        'feature': GENOME_STRUCTURE[least_similar_dim]['feature'],
                        'category': GENOME_STRUCTURE[least_similar_dim]['category'],
                        'difference': float(differences[least_similar_dim])
                    },
                    'average_difference': float(np.mean(differences)),
                    'max_difference': float(np.max(differences)),
                    'min_difference': float(np.min(differences))
                },
                'category_analysis': {
                    'differences': category_differences,
                    'similarities': category_similarities,
                    'most_similar_category': max(category_similarities, key=lambda x: category_similarities[x]),
                    'least_similar_category': min(category_similarities, key=lambda x: category_similarities[x])
                },
                'timestamp': datetime.now().isoformat()
            }
            
            # Store in history
            self.comparison_history.append(comparison_result)
            
            logger.info(f"Genome comparison completed between {client1_id} and {client2_id}")
            return comparison_result
            
        except Exception as e:
            logger.error(f"Error comparing genomes: {e}")
            return {}
    
    def compare_genome_cluster(self, client_genomes: Dict[str, np.ndarray],
                             cluster_assignments: Dict[str, int]) -> Dict[int, Dict[str, Any]]:
        """
        Compare genomes within clusters and provide cluster-level analysis
        
        Args:
            client_genomes: Dictionary mapping client IDs to genome vectors
            cluster_assignments: Dictionary mapping client IDs to cluster labels
            
        Returns:
            Dict[int, Dict[str, Any]]: Analysis for each cluster
        """
        try:
            # Group clients by cluster
            clusters = defaultdict(list)
            for client_id, cluster_id in cluster_assignments.items():
                if client_id in client_genomes:
                    clusters[cluster_id].append(client_id)
            
            cluster_analysis = {}
            
            # Analyze each cluster
            for cluster_id, client_ids in clusters.items():
                if len(client_ids) < 2:
                    # Skip clusters with fewer than 2 clients
                    cluster_analysis[cluster_id] = {
                        'n_clients': len(client_ids),
                        'analysis': 'Insufficient clients for comparison'
                    }
                    continue
                
                # Get genome vectors for this cluster
                cluster_genomes = [client_genomes[client_id] for client_id in client_ids]
                
                # Calculate centroid
                centroid = np.mean(cluster_genomes, axis=0)
                
                # Calculate intra-cluster similarities
                intra_similarities = []
                for i in range(len(cluster_genomes)):
                    for j in range(i + 1, len(cluster_genomes)):
                        similarity = self.similarity_calculator.calculate_cosine_similarity(
                            cluster_genomes[i], cluster_genomes[j]
                        )
                        intra_similarities.append(similarity)
                
                # Calculate distances to centroid
                distances_to_centroid = [
                    np.linalg.norm(genome - centroid) for genome in cluster_genomes
                ]
                
                # Identify most and least representative clients
                min_distance_idx = np.argmin(distances_to_centroid)
                max_distance_idx = np.argmax(distances_to_centroid)
                
                cluster_analysis[cluster_id] = {
                    'n_clients': len(client_ids),
                    'centroid': centroid.tolist(),
                    'intra_cluster_analysis': {
                        'average_similarity': float(np.mean(intra_similarities)),
                        'min_similarity': float(np.min(intra_similarities)),
                        'max_similarity': float(np.max(intra_similarities)),
                        'std_similarity': float(np.std(intra_similarities))
                    },
                    'centroid_analysis': {
                        'average_distance_to_centroid': float(np.mean(distances_to_centroid)),
                        'min_distance_to_centroid': float(np.min(distances_to_centroid)),
                        'max_distance_to_centroid': float(np.max(distances_to_centroid)),
                        'most_representative_client': client_ids[min_distance_idx],
                        'least_representative_client': client_ids[max_distance_idx]
                    }
                }
            
            logger.info(f"Cluster comparison completed for {len(clusters)} clusters")
            return cluster_analysis
            
        except Exception as e:
            logger.error(f"Error comparing genome cluster: {e}")
            return {}
    
    def track_genome_evolution(self, client_id: str,
                             genome_history: List[Tuple[datetime, np.ndarray]]) -> Dict[str, Any]:
        """
        Track genome evolution over time for a specific client
        
        Args:
            client_id: Client identifier
            genome_history: List of (timestamp, genome_vector) tuples
            
        Returns:
            Dict[str, Any]: Evolution analysis results
        """
        try:
            if len(genome_history) < 2:
                return {
                    'client_id': client_id,
                    'analysis': 'Insufficient history for evolution analysis'
                }
            
            # Sort by timestamp
            genome_history.sort(key=lambda x: x[0])
            
            # Calculate changes over time
            initial_genome = genome_history[0][1]
            final_genome = genome_history[-1][1]
            total_change = np.abs(final_genome - initial_genome)
            
            # Calculate changes between consecutive points
            consecutive_changes = []
            for i in range(1, len(genome_history)):
                prev_genome = genome_history[i-1][1]
                curr_genome = genome_history[i][1]
                change = np.abs(curr_genome - prev_genome)
                consecutive_changes.append(np.mean(change))
            
            # Identify most and least changed dimensions
            most_changed_dim = np.argmax(total_change)
            least_changed_dim = np.argmin(total_change)
            
            # Calculate category-level changes
            category_changes = {}
            for category, info in GENOME_DIMENSIONS.items():
                dim_indices = info['dimensions']
                cat_change = np.mean(total_change[dim_indices])
                category_changes[category] = float(cat_change)
            
            evolution_analysis = {
                'client_id': client_id,
                'n_observations': len(genome_history),
                'time_span': {
                    'start': genome_history[0][0].isoformat(),
                    'end': genome_history[-1][0].isoformat(),
                    'duration_days': (genome_history[-1][0] - genome_history[0][0]).days
                },
                'overall_changes': {
                    'total_change_magnitude': float(np.sum(total_change)),
                    'average_change_per_dimension': float(np.mean(total_change)),
                    'max_change_dimension': {
                        'index': int(most_changed_dim),
                        'feature': GENOME_STRUCTURE[most_changed_dim]['feature'],
                        'category': GENOME_STRUCTURE[most_changed_dim]['category'],
                        'change': float(total_change[most_changed_dim])
                    },
                    'min_change_dimension': {
                        'index': int(least_changed_dim),
                        'feature': GENOME_STRUCTURE[least_changed_dim]['feature'],
                        'category': GENOME_STRUCTURE[least_changed_dim]['category'],
                        'change': float(total_change[least_changed_dim])
                    }
                },
                'category_analysis': {
                    'changes': category_changes,
                    'most_changed_category': max(category_changes, key=lambda x: category_changes[x]),
                    'least_changed_category': min(category_changes, key=lambda x: category_changes[x])
                },
                'temporal_analysis': {
                    'average_consecutive_change': float(np.mean(consecutive_changes)),
                    'max_consecutive_change': float(np.max(consecutive_changes)),
                    'min_consecutive_change': float(np.min(consecutive_changes)),
                    'trend': 'increasing' if consecutive_changes[-1] > consecutive_changes[0] else 'decreasing'
                }
            }
            
            logger.info(f"Genome evolution tracking completed for client {client_id}")
            return evolution_analysis
            
        except Exception as e:
            logger.error(f"Error tracking genome evolution for client {client_id}: {e}")
            return {}
    
    def identify_genome_anomalies(self, client_genomes: Dict[str, np.ndarray],
                                threshold: float = 2.0) -> Dict[str, List[str]]:
        """
        Identify anomalous genomes based on statistical analysis
        
        Args:
            client_genomes: Dictionary mapping client IDs to genome vectors
            threshold: Z-score threshold for anomaly detection
            
        Returns:
            Dict[str, List[str]]: Anomalies by category
        """
        try:
            if len(client_genomes) < 3:
                return {'analysis': ['Insufficient clients for anomaly detection']}
            
            # Convert to arrays
            client_ids = list(client_genomes.keys())
            genome_matrix = np.array(list(client_genomes.values()))
            
            # Calculate mean and std for each dimension
            dimension_means = np.mean(genome_matrix, axis=0)
            dimension_stds = np.std(genome_matrix, axis=0)
            
            # Avoid division by zero
            dimension_stds = np.where(dimension_stds == 0, 1, dimension_stds)
            
            # Calculate z-scores for each client
            z_scores = np.abs((genome_matrix - dimension_means) / dimension_stds)
            
            # Identify anomalies
            anomalies_by_dimension = {}
            for dim_idx in range(50):
                dim_anomalies = []
                for client_idx, client_id in enumerate(client_ids):
                    if z_scores[client_idx, dim_idx] > threshold:
                        dim_anomalies.append(client_id)
                
                if dim_anomalies:
                    feature_name = GENOME_STRUCTURE[dim_idx]['feature']
                    anomalies_by_dimension[feature_name] = dim_anomalies
            
            # Group anomalies by client
            client_anomalies = defaultdict(list)
            for feature_name, anomalous_clients in anomalies_by_dimension.items():
                for client_id in anomalous_clients:
                    client_anomalies[client_id].append(feature_name)
            
            # Identify overall anomalous clients (those with many anomalies)
            anomaly_counts = {client_id: len(features) for client_id, features in client_anomalies.items()}
            avg_anomalies = np.mean(list(anomaly_counts.values()))
            
            highly_anomalous_clients = [
                client_id for client_id, count in anomaly_counts.items() 
                if count > avg_anomalies
            ]
            
            anomaly_report = {
                'anomalies_by_dimension': anomalies_by_dimension,
                'anomalies_by_client': dict(client_anomalies),
                'highly_anomalous_clients': highly_anomalous_clients,
                'statistics': {
                    'total_anomalous_clients': len(client_anomalies),
                    'average_anomalies_per_client': float(avg_anomalies),
                    'max_anomalies_for_single_client': max(anomaly_counts.values()) if anomaly_counts else 0
                }
            }
            
            logger.info(f"Genome anomaly detection completed, found {len(client_anomalies)} anomalous clients")
            return anomaly_report
            
        except Exception as e:
            logger.error(f"Error identifying genome anomalies: {e}")
            return {}
    
    def generate_comparison_report(self, comparison_results: Dict[str, Any]) -> str:
        """
        Generate a human-readable comparison report
        
        Args:
            comparison_results: Results from compare_two_genomes
            
        Returns:
            str: Formatted comparison report
        """
        try:
            if not comparison_results:
                return "No comparison results available"
            
            clients = comparison_results['clients']
            similarities = comparison_results['overall_similarities']
            dim_analysis = comparison_results['dimensional_analysis']
            cat_analysis = comparison_results['category_analysis']
            
            report = f"""
=== Client Genome Comparison Report ===
Clients: {clients['client1']} vs {clients['client2']}
Generated: {comparison_results['timestamp']}

OVERALL SIMILARITY SCORES:
- Cosine Similarity: {similarities['cosine_similarity']:.3f}
- Euclidean Similarity: {similarities['euclidean_similarity']:.3f}
- Manhattan Similarity: {similarities['manhattan_similarity']:.3f}
- Jaccard Similarity: {similarities['jaccard_similarity']:.3f}

DIMENSIONAL ANALYSIS:
- Most Similar Dimension: {dim_analysis['most_similar_dimension']['feature']} 
  (Category: {dim_analysis['most_similar_dimension']['category']}, Difference: {dim_analysis['most_similar_dimension']['difference']:.3f})
- Least Similar Dimension: {dim_analysis['least_similar_dimension']['feature']}
  (Category: {dim_analysis['least_similar_dimension']['category']}, Difference: {dim_analysis['least_similar_dimension']['difference']:.3f})
- Average Difference: {dim_analysis['average_difference']:.3f}

CATEGORY ANALYSIS:
- Most Similar Category: {cat_analysis['most_similar_category']} ({cat_analysis['similarities'][cat_analysis['most_similar_category']]:.3f})
- Least Similar Category: {cat_analysis['least_similar_category']} ({cat_analysis['similarities'][cat_analysis['least_similar_category']]:.3f})

Detailed Category Similarities:
"""
            
            for category, similarity in cat_analysis['similarities'].items():
                report += f"- {category}: {similarity:.3f}\n"
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating comparison report: {e}")
            return "Error generating report"


def compare_client_genomes(genome1: np.ndarray, genome2: np.ndarray,
                         client1_id: str = "Client1", client2_id: str = "Client2") -> Dict[str, Any]:
    """
    Convenience function to compare two client genomes
    
    Args:
        genome1: First genome vector (50-dimensional)
        genome2: Second genome vector (50-dimensional)
        client1_id: Identifier for first client
        client2_id: Identifier for second client
        
    Returns:
        Dict[str, Any]: Detailed comparison results
    """
    tools = GenomeComparisonTools()
    return tools.compare_two_genomes(genome1, genome2, client1_id, client2_id)


def identify_genome_anomalies(client_genomes: Dict[str, np.ndarray],
                            threshold: float = 2.0) -> Dict[str, List[str]]:
    """
    Convenience function to identify genome anomalies
    
    Args:
        client_genomes: Dictionary mapping client IDs to genome vectors
        threshold: Z-score threshold for anomaly detection
        
    Returns:
        Dict[str, List[str]]: Anomalies by category
    """
    tools = GenomeComparisonTools()
    return tools.identify_genome_anomalies(client_genomes, threshold)