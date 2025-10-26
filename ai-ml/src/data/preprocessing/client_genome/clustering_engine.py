"""
Client Clustering Engine Module
Implements various clustering algorithms for client genome vectors
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple, Union
import logging
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, calinski_harabasz_score
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


class ClientClusteringEngine:
    """Implements clustering algorithms for client genome vectors"""
    
    def __init__(self):
        """Initialize the Client Clustering Engine"""
        self.scaler = StandardScaler()
        self.clustering_models = {}
        self.cluster_results = {}
        
    def perform_kmeans_clustering(self, client_genomes: Dict[str, np.ndarray], 
                                n_clusters: int = 5,
                                random_state: int = 42) -> Dict[str, int]:
        """
        Perform K-means clustering on client genome vectors
        
        Args:
            client_genomes: Dictionary mapping client IDs to genome vectors
            n_clusters: Number of clusters to create
            random_state: Random state for reproducibility
            
        Returns:
            Dict[str, int]: Dictionary mapping client IDs to cluster labels
        """
        try:
            # Convert to arrays
            client_ids = list(client_genomes.keys())
            genome_vectors = np.array(list(client_genomes.values()))
            
            # Standardize the data
            genome_vectors_scaled = self.scaler.fit_transform(genome_vectors)
            
            # Perform K-means clustering
            kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
            cluster_labels = kmeans.fit_predict(genome_vectors_scaled)
            
            # Store model and results
            self.clustering_models['kmeans'] = kmeans
            self.cluster_results['kmeans'] = {
                'client_ids': client_ids,
                'cluster_labels': cluster_labels,
                'centroids': kmeans.cluster_centers_,
                'inertia': kmeans.inertia_
            }
            
            # Create client-to-cluster mapping
            client_clusters = dict(zip(client_ids, cluster_labels))
            
            logger.info(f"K-means clustering completed with {n_clusters} clusters")
            return client_clusters
            
        except Exception as e:
            logger.error(f"Error performing K-means clustering: {e}")
            return {}
    
    def perform_dbscan_clustering(self, client_genomes: Dict[str, np.ndarray],
                                eps: float = 0.5,
                                min_samples: int = 5) -> Dict[str, int]:
        """
        Perform DBSCAN clustering on client genome vectors
        
        Args:
            client_genomes: Dictionary mapping client IDs to genome vectors
            eps: Maximum distance between two samples for them to be considered neighbors
            min_samples: Number of samples in a neighborhood for a point to be considered a core point
            
        Returns:
            Dict[str, int]: Dictionary mapping client IDs to cluster labels (-1 for noise)
        """
        try:
            # Convert to arrays
            client_ids = list(client_genomes.keys())
            genome_vectors = np.array(list(client_genomes.values()))
            
            # Standardize the data
            genome_vectors_scaled = self.scaler.fit_transform(genome_vectors)
            
            # Perform DBSCAN clustering
            dbscan = DBSCAN(eps=eps, min_samples=min_samples)
            cluster_labels = dbscan.fit_predict(genome_vectors_scaled)
            
            # Store model and results
            self.clustering_models['dbscan'] = dbscan
            self.cluster_results['dbscan'] = {
                'client_ids': client_ids,
                'cluster_labels': cluster_labels,
                'n_clusters': len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0),
                'n_noise_points': list(cluster_labels).count(-1)
            }
            
            # Create client-to-cluster mapping
            client_clusters = dict(zip(client_ids, cluster_labels))
            
            logger.info(f"DBSCAN clustering completed with {len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)} clusters")
            return client_clusters
            
        except Exception as e:
            logger.error(f"Error performing DBSCAN clustering: {e}")
            return {}
    
    def perform_hierarchical_clustering(self, client_genomes: Dict[str, np.ndarray],
                                      n_clusters: int = 5,
                                      linkage: str = 'ward') -> Dict[str, int]:
        """
        Perform hierarchical clustering on client genome vectors
        
        Args:
            client_genomes: Dictionary mapping client IDs to genome vectors
            n_clusters: Number of clusters to create
            linkage: Linkage criterion ('ward', 'complete', 'average', 'single')
            
        Returns:
            Dict[str, int]: Dictionary mapping client IDs to cluster labels
        """
        try:
            # Convert to arrays
            client_ids = list(client_genomes.keys())
            genome_vectors = np.array(list(client_genomes.values()))
            
            # Standardize the data
            genome_vectors_scaled = self.scaler.fit_transform(genome_vectors)
            
            # Perform hierarchical clustering
            hierarchical = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage)
            cluster_labels = hierarchical.fit_predict(genome_vectors_scaled)
            
            # Store results
            self.cluster_results['hierarchical'] = {
                'client_ids': client_ids,
                'cluster_labels': cluster_labels
            }
            
            # Create client-to-cluster mapping
            client_clusters = dict(zip(client_ids, cluster_labels))
            
            logger.info(f"Hierarchical clustering completed with {n_clusters} clusters")
            return client_clusters
            
        except Exception as e:
            logger.error(f"Error performing hierarchical clustering: {e}")
            return {}
    
    def perform_gaussian_mixture_clustering(self, client_genomes: Dict[str, np.ndarray],
                                          n_components: int = 5,
                                          random_state: int = 42) -> Dict[str, int]:
        """
        Perform Gaussian Mixture Model clustering on client genome vectors
        
        Args:
            client_genomes: Dictionary mapping client IDs to genome vectors
            n_components: Number of mixture components
            random_state: Random state for reproducibility
            
        Returns:
            Dict[str, int]: Dictionary mapping client IDs to cluster labels
        """
        try:
            # Convert to arrays
            client_ids = list(client_genomes.keys())
            genome_vectors = np.array(list(client_genomes.values()))
            
            # Standardize the data
            genome_vectors_scaled = self.scaler.fit_transform(genome_vectors)
            
            # Perform Gaussian Mixture clustering
            gmm = GaussianMixture(n_components=n_components, random_state=random_state)
            cluster_labels = gmm.fit_predict(genome_vectors_scaled)
            
            # Store model and results
            self.clustering_models['gmm'] = gmm
            self.cluster_results['gmm'] = {
                'client_ids': client_ids,
                'cluster_labels': cluster_labels,
                'aic': gmm.aic(genome_vectors_scaled),
                'bic': gmm.bic(genome_vectors_scaled)
            }
            
            # Create client-to-cluster mapping
            client_clusters = dict(zip(client_ids, cluster_labels))
            
            logger.info(f"Gaussian Mixture clustering completed with {n_components} components")
            return client_clusters
            
        except Exception as e:
            logger.error(f"Error performing Gaussian Mixture clustering: {e}")
            return {}
    
    def evaluate_clustering_quality(self, client_genomes: Dict[str, np.ndarray],
                                  cluster_labels: List[int]) -> Dict[str, float]:
        """
        Evaluate the quality of clustering results
        
        Args:
            client_genomes: Dictionary mapping client IDs to genome vectors
            cluster_labels: List of cluster labels for each client
            
        Returns:
            Dict[str, float]: Dictionary with clustering quality metrics
        """
        try:
            # Convert to arrays
            genome_vectors = np.array(list(client_genomes.values()))
            
            # Standardize the data
            genome_vectors_scaled = self.scaler.fit_transform(genome_vectors)
            
            # Calculate silhouette score
            silhouette_avg = silhouette_score(genome_vectors_scaled, cluster_labels)
            
            # Calculate Calinski-Harabasz score
            ch_score = calinski_harabasz_score(genome_vectors_scaled, cluster_labels)
            
            # Count number of clusters and noise points
            unique_labels = set(cluster_labels)
            n_clusters = len(unique_labels) - (1 if -1 in unique_labels else 0)
            n_noise = list(cluster_labels).count(-1) if -1 in unique_labels else 0
            
            quality_metrics = {
                'silhouette_score': silhouette_avg,
                'calinski_harabasz_score': ch_score,
                'n_clusters': n_clusters,
                'n_noise_points': n_noise
            }
            
            logger.info("Clustering quality evaluation completed")
            return quality_metrics
            
        except Exception as e:
            logger.error(f"Error evaluating clustering quality: {e}")
            return {}
    
    def get_cluster_statistics(self, clustering_method: str = 'kmeans') -> Dict[str, Any]:
        """
        Get statistics for a specific clustering method
        
        Args:
            clustering_method: Clustering method name ('kmeans', 'dbscan', 'hierarchical', 'gmm')
            
        Returns:
            Dict[str, Any]: Dictionary with cluster statistics
        """
        if clustering_method not in self.cluster_results:
            logger.warning(f"No results found for clustering method: {clustering_method}")
            return {}
        
        try:
            results = self.cluster_results[clustering_method]
            cluster_labels = results['cluster_labels']
            
            # Calculate cluster sizes
            unique_labels, counts = np.unique(cluster_labels, return_counts=True)
            cluster_sizes = dict(zip(unique_labels, counts))
            
            statistics = {
                'cluster_sizes': cluster_sizes,
                'total_clients': len(cluster_labels),
                'n_clusters': len(unique_labels)
            }
            
            # Add method-specific statistics
            if clustering_method == 'kmeans':
                statistics['inertia'] = results.get('inertia', 0)
            elif clustering_method == 'dbscan':
                statistics['n_noise_points'] = results.get('n_noise_points', 0)
            elif clustering_method == 'gmm':
                statistics['aic'] = results.get('aic', 0)
                statistics['bic'] = results.get('bic', 0)
            
            return statistics
            
        except Exception as e:
            logger.error(f"Error getting cluster statistics for {clustering_method}: {e}")
            return {}
    
    def get_clients_in_cluster(self, cluster_id: int, 
                             clustering_method: str = 'kmeans') -> List[str]:
        """
        Get list of client IDs in a specific cluster
        
        Args:
            cluster_id: Cluster ID to query
            clustering_method: Clustering method name
            
        Returns:
            List[str]: List of client IDs in the specified cluster
        """
        if clustering_method not in self.cluster_results:
            logger.warning(f"No results found for clustering method: {clustering_method}")
            return []
        
        try:
            results = self.cluster_results[clustering_method]
            client_ids = results['client_ids']
            cluster_labels = results['cluster_labels']
            
            # Find clients in the specified cluster
            clients_in_cluster = [
                client_id for client_id, label in zip(client_ids, cluster_labels) 
                if label == cluster_id
            ]
            
            return clients_in_cluster
            
        except Exception as e:
            logger.error(f"Error getting clients in cluster {cluster_id}: {e}")
            return []
    
    def perform_optimal_clustering(self, client_genomes: Dict[str, np.ndarray],
                                 max_clusters: int = 10,
                                 method: str = 'kmeans') -> Tuple[Dict[str, int], int]:
        """
        Perform clustering with optimal number of clusters based on silhouette score
        
        Args:
            client_genomes: Dictionary mapping client IDs to genome vectors
            max_clusters: Maximum number of clusters to try
            method: Clustering method to use
            
        Returns:
            Tuple[Dict[str, int], int]: (client_clusters mapping, optimal_n_clusters)
        """
        try:
            # Convert to arrays
            client_ids = list(client_genomes.keys())
            genome_vectors = np.array(list(client_genomes.values()))
            
            # Standardize the data
            genome_vectors_scaled = self.scaler.fit_transform(genome_vectors)
            
            best_score = -1
            best_n_clusters = 2
            best_labels = None
            
            # Try different numbers of clusters
            for n_clusters in range(2, min(max_clusters + 1, len(client_ids))):
                try:
                    if method == 'kmeans':
                        model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
                    elif method == 'gmm':
                        model = GaussianMixture(n_components=n_clusters, random_state=42)
                    else:
                        continue
                    
                    labels = model.fit_predict(genome_vectors_scaled)
                    
                    # Calculate silhouette score
                    score = silhouette_score(genome_vectors_scaled, labels)
                    
                    if score > best_score:
                        best_score = score
                        best_n_clusters = n_clusters
                        best_labels = labels
                        
                except Exception as e:
                    logger.warning(f"Error with {n_clusters} clusters: {e}")
                    continue
            
            # Perform final clustering with optimal number of clusters
            if method == 'kmeans':
                final_model = KMeans(n_clusters=best_n_clusters, random_state=42, n_init=10)
                final_labels = final_model.fit_predict(genome_vectors_scaled)
                self.clustering_models['optimal_kmeans'] = final_model
            else:  # gmm
                final_model = GaussianMixture(n_components=best_n_clusters, random_state=42)
                final_labels = final_model.fit_predict(genome_vectors_scaled)
                self.clustering_models['optimal_gmm'] = final_model
            
            # Store results
            self.cluster_results[f'optimal_{method}'] = {
                'client_ids': client_ids,
                'cluster_labels': final_labels,
                'optimal_n_clusters': best_n_clusters,
                'silhouette_score': best_score
            }
            
            # Create client-to-cluster mapping
            client_clusters = dict(zip(client_ids, final_labels))
            
            logger.info(f"Optimal clustering completed with {best_n_clusters} clusters (silhouette score: {best_score:.3f})")
            return client_clusters, best_n_clusters
            
        except Exception as e:
            logger.error(f"Error performing optimal clustering: {e}")
            return {}, 2


def perform_client_clustering(client_genomes: Dict[str, np.ndarray], 
                            method: str = 'kmeans',
                            **kwargs) -> Dict[str, int]:
    """
    Convenience function to perform client clustering
    
    Args:
        client_genomes: Dictionary mapping client IDs to genome vectors
        method: Clustering method ('kmeans', 'dbscan', 'hierarchical', 'gmm')
        **kwargs: Additional arguments for the clustering method
        
    Returns:
        Dict[str, int]: Dictionary mapping client IDs to cluster labels
    """
    engine = ClientClusteringEngine()
    
    if method == 'kmeans':
        return engine.perform_kmeans_clustering(client_genomes, **kwargs)
    elif method == 'dbscan':
        return engine.perform_dbscan_clustering(client_genomes, **kwargs)
    elif method == 'hierarchical':
        return engine.perform_hierarchical_clustering(client_genomes, **kwargs)
    elif method == 'gmm':
        return engine.perform_gaussian_mixture_clustering(client_genomes, **kwargs)
    else:
        # Default to K-means
        return engine.perform_kmeans_clustering(client_genomes, **kwargs)