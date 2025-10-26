"""
Genome Orchestrator Module
Coordinates all components of the Client Profitability Genome system
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
import logging
from datetime import datetime

from .genome_creator import GenomeCreator
from .similarity_calculator import SimilarityCalculator
from .clustering_engine import ClientClusteringEngine, perform_client_clustering
from .comparison_tools import GenomeComparisonTools

logger = logging.getLogger(__name__)


class GenomeOrchestrator:
    """Orchestrates all components of the Client Profitability Genome system"""
    
    def __init__(self):
        """Initialize the Genome Orchestrator"""
        self.genome_creator = GenomeCreator()
        self.similarity_calculator = SimilarityCalculator()
        self.clustering_engine = ClientClusteringEngine()
        self.comparison_tools = GenomeComparisonTools()
        self.genome_database = {}
        self.processing_history = []
        
    def process_client_data(self, clients_data: pd.DataFrame) -> Dict[str, np.ndarray]:
        """
        Process client data through the complete genome pipeline
        
        Args:
            clients_data: DataFrame containing client data with all features
            
        Returns:
            Dict[str, np.ndarray]: Dictionary mapping client IDs to genome vectors
        """
        try:
            start_time = datetime.now()
            logger.info(f"Starting genome processing for {len(clients_data)} clients")
            
            # Step 1: Create genome vectors
            client_genomes = self.genome_creator.create_genomes_for_clients(clients_data)
            
            # Store in database
            self.genome_database.update(client_genomes)
            
            # Record processing
            processing_record = {
                'timestamp': start_time,
                'n_clients': len(client_genomes),
                'duration_seconds': (datetime.now() - start_time).total_seconds(),
                'status': 'completed'
            }
            self.processing_history.append(processing_record)
            
            logger.info(f"Genome processing completed in {processing_record['duration_seconds']:.2f} seconds")
            return client_genomes
            
        except Exception as e:
            logger.error(f"Error processing client data: {e}")
            processing_record = {
                'timestamp': datetime.now(),
                'n_clients': len(clients_data) if clients_data is not None else 0,
                'duration_seconds': 0,
                'status': 'failed',
                'error': str(e)
            }
            self.processing_history.append(processing_record)
            return {}
    
    def analyze_client_similarity(self, client_id1: str, client_id2: str) -> Dict[str, Any]:
        """
        Analyze similarity between two clients
        
        Args:
            client_id1: First client identifier
            client_id2: Second client identifier
            
        Returns:
            Dict[str, Any]: Comprehensive similarity analysis
        """
        try:
            # Check if genomes exist
            if client_id1 not in self.genome_database or client_id2 not in self.genome_database:
                logger.warning(f"One or both clients not found in genome database")
                return {}
            
            # Get genome vectors
            genome1 = self.genome_database[client_id1]
            genome2 = self.genome_database[client_id2]
            
            # Perform comprehensive similarity analysis
            similarity_analysis = self.comparison_tools.compare_two_genomes(
                genome1, genome2, client_id1, client_id2
            )
            
            return similarity_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing client similarity: {e}")
            return {}
    
    def cluster_clients(self, method: str = 'kmeans', **kwargs) -> Dict[str, int]:
        """
        Cluster all clients using specified method
        
        Args:
            method: Clustering method ('kmeans', 'dbscan', 'hierarchical', 'gmm')
            **kwargs: Additional arguments for the clustering method
            
        Returns:
            Dict[str, int]: Dictionary mapping client IDs to cluster labels
        """
        try:
            if not self.genome_database:
                logger.warning("No genomes available for clustering")
                return {}
            
            # Perform clustering
            cluster_assignments = perform_client_clustering(
                self.genome_database, method, **kwargs
            )
            
            return cluster_assignments
            
        except Exception as e:
            logger.error(f"Error clustering clients: {e}")
            return {}
    
    def get_cluster_analysis(self, cluster_assignments: Dict[str, int]) -> Dict[int, Dict[str, Any]]:
        """
        Get detailed analysis of client clusters
        
        Args:
            cluster_assignments: Dictionary mapping client IDs to cluster labels
            
        Returns:
            Dict[int, Dict[str, Any]]: Analysis for each cluster
        """
        try:
            if not self.genome_database:
                logger.warning("No genomes available for cluster analysis")
                return {}
            
            # Perform cluster analysis
            cluster_analysis = self.comparison_tools.compare_genome_cluster(
                self.genome_database, cluster_assignments
            )
            
            return cluster_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing clusters: {e}")
            return {}
    
    def identify_anomalies(self, threshold: float = 2.0) -> Dict[str, List[str]]:
        """
        Identify anomalous clients based on genome analysis
        
        Args:
            threshold: Z-score threshold for anomaly detection
            
        Returns:
            Dict[str, List[str]]: Anomalies by category
        """
        try:
            if not self.genome_database:
                logger.warning("No genomes available for anomaly detection")
                return {}
            
            # Identify anomalies
            anomalies = self.comparison_tools.identify_genome_anomalies(
                self.genome_database, threshold
            )
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error identifying anomalies: {e}")
            return {}
    
    def find_similar_clients(self, target_client_id: str, 
                           top_k: int = 5,
                           metric: str = 'cosine') -> List[Tuple[str, float]]:
        """
        Find clients most similar to a target client
        
        Args:
            target_client_id: Target client identifier
            top_k: Number of similar clients to return
            metric: Similarity metric to use
            
        Returns:
            List[Tuple[str, float]]: List of (client_id, similarity_score) tuples
        """
        try:
            # Check if target client exists
            if target_client_id not in self.genome_database:
                logger.warning(f"Target client {target_client_id} not found in genome database")
                return []
            
            # Get target genome
            target_genome = self.genome_database[target_client_id]
            
            # Find similar clients
            similar_clients = self.similarity_calculator.find_most_similar_clients(
                target_genome, self.genome_database, top_k, metric
            )
            
            return similar_clients
            
        except Exception as e:
            logger.error(f"Error finding similar clients: {e}")
            return []
    
    def generate_client_profile(self, client_id: str) -> Dict[str, Any]:
        """
        Generate comprehensive profile for a client based on their genome
        
        Args:
            client_id: Client identifier
            
        Returns:
            Dict[str, Any]: Comprehensive client profile
        """
        try:
            # Check if client exists
            if client_id not in self.genome_database:
                logger.warning(f"Client {client_id} not found in genome database")
                return {}
            
            # Get genome vector
            genome = self.genome_database[client_id]
            
            # Generate profile based on genome dimensions
            profile = {
                'client_id': client_id,
                'genome_timestamp': datetime.now().isoformat(),
                'categories': {}
            }
            
            from . import GENOME_DIMENSIONS
            
            # Analyze each category
            for category, info in GENOME_DIMENSIONS.items():
                dim_indices = info['dimensions']
                category_values = genome[dim_indices]
                
                profile['categories'][category] = {
                    'average_score': float(np.mean(category_values)),
                    'max_score': float(np.max(category_values)),
                    'min_score': float(np.min(category_values)),
                    'std_deviation': float(np.std(category_values)),
                    'strength_level': self._categorize_strength(np.mean(category_values))
                }
            
            # Overall assessment
            overall_score = float(np.mean(genome))
            profile['overall_assessment'] = {
                'profitability_genome_score': overall_score,
                'overall_strength_level': self._categorize_strength(overall_score),
                'recommendation': self._generate_recommendation(profile['categories'])
            }
            
            return profile
            
        except Exception as e:
            logger.error(f"Error generating client profile: {e}")
            return {}
    
    def _categorize_strength(self, score: float) -> str:
        """
        Categorize strength level based on score
        
        Args:
            score: Score value (0-1)
            
        Returns:
            str: Strength category
        """
        if score >= 0.8:
            return "Very Strong"
        elif score >= 0.6:
            return "Strong"
        elif score >= 0.4:
            return "Moderate"
        elif score >= 0.2:
            return "Weak"
        else:
            return "Very Weak"
    
    def _generate_recommendation(self, categories: Dict[str, Any]) -> str:
        """
        Generate recommendation based on category analysis
        
        Args:
            categories: Category analysis results
            
        Returns:
            str: Recommendation text
        """
        # Find the weakest category
        weakest_category = min(categories.keys(), key=lambda x: categories[x]['average_score'])
        weakest_score = categories[weakest_category]['average_score']
        
        # Find the strongest category
        strongest_category = max(categories.keys(), key=lambda x: categories[x]['average_score'])
        
        if weakest_score < 0.3:
            return f"Focus on improving {weakest_category} as it's a critical weakness"
        elif categories['FinancialHealth']['average_score'] < 0.5:
            return "Prioritize financial health improvements for better profitability"
        elif categories['RiskFactors']['average_score'] > 0.7:
            return "Monitor risk factors closely to prevent potential issues"
        else:
            return f"Leverage strong {strongest_category} while maintaining overall balance"


def process_client_genomes(clients_data: pd.DataFrame) -> Dict[str, np.ndarray]:
    """
    Convenience function to process client data through the genome pipeline
    
    Args:
        clients_data: DataFrame containing client data with all features
        
    Returns:
        Dict[str, np.ndarray]: Dictionary mapping client IDs to genome vectors
    """
    orchestrator = GenomeOrchestrator()
    return orchestrator.process_client_data(clients_data)


def analyze_genome_system(clients_data: pd.DataFrame) -> Dict[str, Any]:
    """
    Convenience function to perform complete genome analysis
    
    Args:
        clients_data: DataFrame containing client data with all features
        
    Returns:
        Dict[str, Any]: Complete genome analysis results
    """
    orchestrator = GenomeOrchestrator()
    
    # Process client data
    client_genomes = orchestrator.process_client_data(clients_data)
    
    if not client_genomes:
        return {'error': 'Failed to process client data'}
    
    # Perform clustering
    cluster_assignments = orchestrator.cluster_clients(method='kmeans', n_clusters=5)
    
    # Analyze clusters
    cluster_analysis = orchestrator.get_cluster_analysis(cluster_assignments)
    
    # Identify anomalies
    anomalies = orchestrator.identify_anomalies()
    
    # Generate sample profiles
    sample_client_id = list(client_genomes.keys())[0] if client_genomes.keys() else None
    sample_profile = orchestrator.generate_client_profile(sample_client_id) if sample_client_id else {}
    
    return {
        'client_genomes': client_genomes,
        'cluster_assignments': cluster_assignments,
        'cluster_analysis': cluster_analysis,
        'anomalies': anomalies,
        'sample_profile': sample_profile
    }