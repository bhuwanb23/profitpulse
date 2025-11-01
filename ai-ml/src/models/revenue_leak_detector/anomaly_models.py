"""
Anomaly Detection Models for Revenue Leak Detection
Implements various anomaly detection algorithms for identifying revenue leaks
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Conditional imports for ML libraries
try:
    from sklearn.ensemble import IsolationForest
    SKLEARN_ENSEMBLE_AVAILABLE = True
except ImportError:
    IsolationForest = None
    SKLEARN_ENSEMBLE_AVAILABLE = False

try:
    from sklearn.svm import OneClassSVM
    SKLEARN_SVM_AVAILABLE = True
except ImportError:
    OneClassSVM = None
    SKLEARN_SVM_AVAILABLE = False

try:
    from sklearn.cluster import DBSCAN
    SKLEARN_CLUSTER_AVAILABLE = True
except ImportError:
    DBSCAN = None
    SKLEARN_CLUSTER_AVAILABLE = False

try:
    from sklearn.preprocessing import StandardScaler
    SKLEARN_PREPROCESSING_AVAILABLE = True
except ImportError:
    StandardScaler = None
    SKLEARN_PREPROCESSING_AVAILABLE = False

try:
    from sklearn.metrics import silhouette_score
    SKLEARN_METRICS_AVAILABLE = True
except ImportError:
    silhouette_score = None
    SKLEARN_METRICS_AVAILABLE = False

try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers
    TENSORFLOW_AVAILABLE = True
except ImportError:
    tf = None
    keras = None
    layers = None
    TENSORFLOW_AVAILABLE = False

logger = logging.getLogger(__name__)


class IsolationForestModel:
    """Isolation Forest implementation for anomaly detection"""
    
    def __init__(self, contamination: float = 0.1, random_state: int = 42):
        """
        Initialize Isolation Forest model
        
        Args:
            contamination: Expected proportion of outliers in the data
            random_state: Random state for reproducibility
        """
        self.contamination = contamination
        self.random_state = random_state
        self.model = None
        self.scaler = StandardScaler() if StandardScaler else None
        self.feature_names = None
        self.is_trained = False
        logger.info("Isolation Forest Model initialized")
    
    def train(self, X: pd.DataFrame) -> bool:
        """
        Train the Isolation Forest model
        
        Args:
            X: Training data
            
        Returns:
            Boolean indicating success
        """
        try:
            if not SKLEARN_ENSEMBLE_AVAILABLE:
                logger.warning("scikit-learn ensemble module not available, cannot train Isolation Forest")
                return False
            
            # Store feature names
            self.feature_names = list(X.columns) if hasattr(X, 'columns') else [f"feature_{i}" for i in range(X.shape[1])]
            
            # Scale features
            if self.scaler is not None:
                X_scaled = self.scaler.fit_transform(X)
            else:
                X_scaled = X.values if hasattr(X, 'values') else X
            
            # Train model
            if IsolationForest is not None:
                self.model = IsolationForest(
                    contamination=self.contamination,
                    random_state=self.random_state,
                    n_estimators=100
                )
                self.model.fit(X_scaled)
                self.is_trained = True
            else:
                logger.warning("IsolationForest not available")
                return False
            
            logger.info("Isolation Forest model trained successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error training Isolation Forest model: {e}")
            return False
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict anomalies using the trained model
        
        Args:
            X: Data to predict anomalies for
            
        Returns:
            Array of anomaly predictions (-1 for anomaly, 1 for normal)
        """
        try:
            if not self.is_trained or self.model is None:
                logger.warning("Model not trained, returning mock predictions")
                return np.ones(len(X))  # Return all normal
            
            # Scale features
            if self.scaler is not None:
                X_scaled = self.scaler.transform(X)
            else:
                X_scaled = X.values if hasattr(X, 'values') else X
            
            # Predict anomalies
            predictions = self.model.predict(X_scaled)
            return predictions
            
        except Exception as e:
            logger.error(f"Error predicting with Isolation Forest model: {e}")
            return np.ones(len(X))  # Return all normal
    
    def anomaly_scores(self, X: pd.DataFrame) -> np.ndarray:
        """
        Get anomaly scores for the data
        
        Args:
            X: Data to score
            
        Returns:
            Array of anomaly scores (lower scores indicate anomalies)
        """
        try:
            if not self.is_trained or self.model is None:
                logger.warning("Model not trained, returning mock scores")
                return np.zeros(len(X))
            
            # Scale features
            if self.scaler is not None:
                X_scaled = self.scaler.transform(X)
            else:
                X_scaled = X.values if hasattr(X, 'values') else X
            
            # Get anomaly scores
            scores = self.model.decision_function(X_scaled)
            return scores
            
        except Exception as e:
            logger.error(f"Error getting anomaly scores from Isolation Forest model: {e}")
            return np.zeros(len(X))


class AutoencoderModel:
    """Autoencoder implementation for anomaly detection"""
    
    def __init__(self, encoding_dim: int = 10, epochs: int = 100, batch_size: int = 32):
        """
        Initialize Autoencoder model
        
        Args:
            encoding_dim: Dimension of the encoded representation
            epochs: Number of training epochs
            batch_size: Batch size for training
        """
        self.encoding_dim = encoding_dim
        self.epochs = epochs
        self.batch_size = batch_size
        self.model = None
        self.encoder = None
        self.decoder = None
        self.scaler = StandardScaler() if StandardScaler else None
        self.feature_names = None
        self.is_trained = False
        self.input_dim = None
        logger.info("Autoencoder Model initialized")
    
    def train(self, X: pd.DataFrame) -> bool:
        """
        Train the Autoencoder model
        
        Args:
            X: Training data
            
        Returns:
            Boolean indicating success
        """
        try:
            if not TENSORFLOW_AVAILABLE:
                logger.warning("TensorFlow not available, cannot train Autoencoder")
                return False
            
            # Store feature names and dimensions
            self.feature_names = list(X.columns) if hasattr(X, 'columns') else [f"feature_{i}" for i in range(X.shape[1])]
            self.input_dim = X.shape[1]
            
            # Scale features
            if self.scaler is not None:
                X_scaled = self.scaler.fit_transform(X)
            else:
                X_scaled = X.values if hasattr(X, 'values') else X
            
            # Build autoencoder
            self._build_autoencoder()
            
            # Train model
            # Build autoencoder
            self._build_autoencoder()
            
            if self.model is not None:
                self.model.compile(optimizer='adam', loss='mse')
                self.model.fit(
                    X_scaled, X_scaled,
                    epochs=self.epochs,
                    batch_size=self.batch_size,
                    shuffle=True,
                    verbose=0
                )
                self.is_trained = True
            else:
                logger.warning("Autoencoder model not built successfully")
                return False
            
            logger.info("Autoencoder model trained successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error training Autoencoder model: {e}")
            return False
    
    def _build_autoencoder(self):
        """Build the autoencoder architecture"""
        try:
            if keras is not None and layers is not None:
                # Encoder
                input_layer = keras.Input(shape=(self.input_dim,))
                encoded = layers.Dense(self.encoding_dim, activation='relu')(input_layer)
                
                # Decoder
                decoded = layers.Dense(self.input_dim, activation='linear')(encoded)
                
                # Autoencoder
                self.model = keras.Model(input_layer, decoded)
                
                # Encoder only (for feature extraction)
                self.encoder = keras.Model(input_layer, encoded)
            else:
                logger.warning("Keras or layers not available for autoencoder building")
                self.model = None
                self.encoder = None
        except Exception as e:
            logger.error(f"Error building autoencoder: {e}")
            self.model = None
            self.encoder = None
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict anomalies using the trained model
        
        Args:
            X: Data to predict anomalies for
            
        Returns:
            Array of anomaly predictions (1 for normal, -1 for anomaly)
        """
        try:
            if not self.is_trained or self.model is None:
                logger.warning("Model not trained, returning mock predictions")
                return np.ones(len(X))  # Return all normal
            
            # Scale features
            if self.scaler is not None:
                X_scaled = self.scaler.transform(X)
            else:
                X_scaled = X.values if hasattr(X, 'values') else X
            
            # Reconstruct data
            reconstructed = self.model.predict(X_scaled, verbose=0)
            
            # Calculate reconstruction errors
            mse = np.mean(np.power(X_scaled - reconstructed, 2), axis=1)
            
            # Determine threshold (95th percentile of training errors)
            threshold = np.percentile(mse, 95)
            
            # Predict anomalies
            predictions = np.where(mse > threshold, -1, 1)
            return predictions
            
        except Exception as e:
            logger.error(f"Error predicting with Autoencoder model: {e}")
            return np.ones(len(X))  # Return all normal
    
    def anomaly_scores(self, X: pd.DataFrame) -> np.ndarray:
        """
        Get anomaly scores for the data
        
        Args:
            X: Data to score
            
        Returns:
            Array of anomaly scores (higher scores indicate anomalies)
        """
        try:
            if not self.is_trained or self.model is None:
                logger.warning("Model not trained, returning mock scores")
                return np.zeros(len(X))
            
            # Scale features
            if self.scaler is not None:
                X_scaled = self.scaler.transform(X)
            else:
                X_scaled = X.values if hasattr(X, 'values') else X
            
            # Reconstruct data
            reconstructed = self.model.predict(X_scaled, verbose=0)
            
            # Calculate reconstruction errors (MSE)
            mse = np.mean(np.power(X_scaled - reconstructed, 2), axis=1)
            return mse
            
        except Exception as e:
            logger.error(f"Error getting anomaly scores from Autoencoder model: {e}")
            return np.zeros(len(X))


class DBSCANModel:
    """DBSCAN clustering for anomaly detection"""
    
    def __init__(self, eps: float = 0.5, min_samples: int = 5):
        """
        Initialize DBSCAN model
        
        Args:
            eps: The maximum distance between two samples for them to be considered as in the same neighborhood
            min_samples: The number of samples in a neighborhood for a point to be considered as a core point
        """
        self.eps = eps
        self.min_samples = min_samples
        self.model = None
        self.scaler = StandardScaler() if StandardScaler else None
        self.feature_names = None
        self.is_trained = False
        logger.info("DBSCAN Model initialized")
    
    def train(self, X: pd.DataFrame) -> bool:
        """
        Train the DBSCAN model (fitting clustering)
        
        Args:
            X: Training data
            
        Returns:
            Boolean indicating success
        """
        try:
            if not SKLEARN_CLUSTER_AVAILABLE:
                logger.warning("scikit-learn cluster module not available, cannot train DBSCAN")
                return False
            
            # Store feature names
            self.feature_names = list(X.columns) if hasattr(X, 'columns') else [f"feature_{i}" for i in range(X.shape[1])]
            
            # Scale features
            if self.scaler is not None:
                X_scaled = self.scaler.fit_transform(X)
            else:
                X_scaled = X.values if hasattr(X, 'values') else X
            
            # Train model
            if DBSCAN is not None:
                self.model = DBSCAN(eps=self.eps, min_samples=self.min_samples)
                self.model.fit(X_scaled)
                self.is_trained = True
            else:
                logger.warning("DBSCAN not available")
                return False
            
            logger.info("DBSCAN model trained successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error training DBSCAN model: {e}")
            return False
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict anomalies using the trained model
        
        Args:
            X: Data to predict anomalies for
            
        Returns:
            Array of anomaly predictions (-1 for anomaly, 1 for normal)
        """
        try:
            if not self.is_trained or self.model is None:
                logger.warning("Model not trained, returning mock predictions")
                return np.ones(len(X))  # Return all normal
            
            # Scale features
            if self.scaler is not None:
                X_scaled = self.scaler.transform(X)
            else:
                X_scaled = X.values if hasattr(X, 'values') else X
            
            # Predict clusters
            cluster_labels = self.model.fit_predict(X_scaled)
            
            # Anomalies are points labeled as noise (-1)
            predictions = np.where(cluster_labels == -1, -1, 1)
            return predictions
            
        except Exception as e:
            logger.error(f"Error predicting with DBSCAN model: {e}")
            return np.ones(len(X))  # Return all normal
    
    def anomaly_scores(self, X: pd.DataFrame) -> np.ndarray:
        """
        Get anomaly scores for the data (based on distance to cluster centers)
        
        Args:
            X: Data to score
            
        Returns:
            Array of anomaly scores (higher scores indicate anomalies)
        """
        try:
            if not self.is_trained or self.model is None:
                logger.warning("Model not trained, returning mock scores")
                return np.zeros(len(X))
            
            # Scale features
            if self.scaler is not None:
                X_scaled = self.scaler.transform(X)
            else:
                X_scaled = X.values if hasattr(X, 'values') else X
            
            # For DBSCAN, we'll use the distance to the nearest core point as anomaly score
            # This is a simplified approach
            try:
                if hasattr(self.model, 'components_') and len(self.model.components_) > 0:
                    # Calculate distances to core points
                    from sklearn.metrics.pairwise import euclidean_distances
                    distances = euclidean_distances(X_scaled, self.model.components_)
                    min_distances = np.min(distances, axis=1)
                    return min_distances
                else:
                    return np.zeros(len(X))
            except Exception as e:
                logger.warning(f"Error calculating DBSCAN distances: {e}")
                return np.zeros(len(X))
            
        except Exception as e:
            logger.error(f"Error getting anomaly scores from DBSCAN model: {e}")
            return np.zeros(len(X))


class OneClassSVMModel:
    """One-Class SVM implementation for anomaly detection"""
    
    def __init__(self, kernel: str = 'rbf', nu: float = 0.1, gamma: str = 'scale'):
        """
        Initialize One-Class SVM model
        
        Args:
            kernel: Kernel type ('linear', 'poly', 'rbf', 'sigmoid')
            nu: An upper bound on the fraction of training errors and a lower bound of the fraction of support vectors
            gamma: Kernel coefficient for 'rbf', 'poly' and 'sigmoid'
        """
        self.kernel = kernel
        self.nu = nu
        self.gamma = gamma
        self.model = None
        self.scaler = StandardScaler() if StandardScaler else None
        self.feature_names = None
        self.is_trained = False
        logger.info("One-Class SVM Model initialized")
    
    def train(self, X: pd.DataFrame) -> bool:
        """
        Train the One-Class SVM model
        
        Args:
            X: Training data
            
        Returns:
            Boolean indicating success
        """
        try:
            if not SKLEARN_SVM_AVAILABLE:
                logger.warning("scikit-learn SVM module not available, cannot train One-Class SVM")
                return False
            
            # Store feature names
            self.feature_names = list(X.columns) if hasattr(X, 'columns') else [f"feature_{i}" for i in range(X.shape[1])]
            
            # Scale features
            if self.scaler is not None:
                X_scaled = self.scaler.fit_transform(X)
            else:
                X_scaled = X.values if hasattr(X, 'values') else X
            
            # Train model
            if OneClassSVM is not None:
                self.model = OneClassSVM(kernel=self.kernel, nu=self.nu, gamma=self.gamma)
                self.model.fit(X_scaled)
                self.is_trained = True
            else:
                logger.warning("OneClassSVM not available")
                return False
            
            logger.info("One-Class SVM model trained successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error training One-Class SVM model: {e}")
            return False
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict anomalies using the trained model
        
        Args:
            X: Data to predict anomalies for
            
        Returns:
            Array of anomaly predictions (-1 for anomaly, 1 for normal)
        """
        try:
            if not self.is_trained or self.model is None:
                logger.warning("Model not trained, returning mock predictions")
                return np.ones(len(X))  # Return all normal
            
            # Scale features
            if self.scaler is not None:
                X_scaled = self.scaler.transform(X)
            else:
                X_scaled = X.values if hasattr(X, 'values') else X
            
            # Predict anomalies
            predictions = self.model.predict(X_scaled)
            return predictions
            
        except Exception as e:
            logger.error(f"Error predicting with One-Class SVM model: {e}")
            return np.ones(len(X))  # Return all normal
    
    def anomaly_scores(self, X: pd.DataFrame) -> np.ndarray:
        """
        Get anomaly scores for the data
        
        Args:
            X: Data to score
            
        Returns:
            Array of anomaly scores (lower scores indicate anomalies)
        """
        try:
            if not self.is_trained or self.model is None:
                logger.warning("Model not trained, returning mock scores")
                return np.zeros(len(X))
            
            # Scale features
            if self.scaler is not None:
                X_scaled = self.scaler.transform(X)
            else:
                X_scaled = X.values if hasattr(X, 'values') else X
            
            # Get decision function scores
            scores = self.model.decision_function(X_scaled)
            return scores
            
        except Exception as e:
            logger.error(f"Error getting anomaly scores from One-Class SVM model: {e}")
            return np.zeros(len(X))


class EnsembleAnomalyDetector:
    """Ensemble of anomaly detection models"""
    
    def __init__(self, contamination: float = 0.1, voting_method: str = 'majority'):
        """
        Initialize Ensemble Anomaly Detector
        
        Args:
            contamination: Expected proportion of outliers in the data
            voting_method: Voting method ('majority', 'average', 'weighted')
        """
        self.contamination = contamination
        self.voting_method = voting_method
        self.models = {
            'isolation_forest': IsolationForestModel(contamination=contamination),
            'autoencoder': AutoencoderModel(encoding_dim=8, epochs=50),
            'dbscan': DBSCANModel(eps=0.5, min_samples=5),
            'one_class_svm': OneClassSVMModel(nu=contamination)
        }
        self.model_weights = {
            'isolation_forest': 0.25,
            'autoencoder': 0.25,
            'dbscan': 0.25,
            'one_class_svm': 0.25
        }
        self.is_trained = False
        self.feature_names = None
        logger.info("Ensemble Anomaly Detector initialized")
    
    def train(self, X: pd.DataFrame) -> bool:
        """
        Train all models in the ensemble
        
        Args:
            X: Training data
            
        Returns:
            Boolean indicating success
        """
        try:
            # Store feature names
            self.feature_names = list(X.columns) if hasattr(X, 'columns') else [f"feature_{i}" for i in range(X.shape[1])]
            
            # Train all models
            training_results = []
            for model_name, model in self.models.items():
                logger.info(f"Training {model_name}...")
                result = model.train(X)
                training_results.append(result)
                logger.info(f"{model_name} training {'successful' if result else 'failed'}")
            
            self.is_trained = all(training_results)
            
            if self.is_trained:
                logger.info("All ensemble models trained successfully")
            else:
                logger.warning("Some ensemble models failed to train")
            
            return self.is_trained
            
        except Exception as e:
            logger.error(f"Error training ensemble models: {e}")
            return False
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict anomalies using ensemble of models
        
        Args:
            X: Data to predict anomalies for
            
        Returns:
            Array of anomaly predictions (-1 for anomaly, 1 for normal)
        """
        try:
            if not self.is_trained:
                logger.warning("Ensemble not trained, returning mock predictions")
                return np.ones(len(X))  # Return all normal
            
            # Get predictions from all models
            predictions = {}
            for model_name, model in self.models.items():
                pred = model.predict(X)
                predictions[model_name] = pred
            
            # Combine predictions based on voting method
            if self.voting_method == 'majority':
                return self._majority_voting(predictions)
            elif self.voting_method == 'average':
                return self._average_voting(predictions)
            elif self.voting_method == 'weighted':
                return self._weighted_voting(predictions)
            else:
                return self._majority_voting(predictions)
            
        except Exception as e:
            logger.error(f"Error predicting with ensemble models: {e}")
            return np.ones(len(X))  # Return all normal
    
    def anomaly_scores(self, X: pd.DataFrame) -> np.ndarray:
        """
        Get anomaly scores using ensemble of models
        
        Args:
            X: Data to score
            
        Returns:
            Array of anomaly scores
        """
        try:
            if not self.is_trained:
                logger.warning("Ensemble not trained, returning mock scores")
                return np.zeros(len(X))
            
            # Get scores from all models
            scores = {}
            for model_name, model in self.models.items():
                score = model.anomaly_scores(X)
                scores[model_name] = score
            
            # Combine scores based on voting method
            if self.voting_method == 'majority':
                return self._average_scores(scores)
            elif self.voting_method == 'average':
                return self._average_scores(scores)
            elif self.voting_method == 'weighted':
                return self._weighted_scores(scores)
            else:
                return self._average_scores(scores)
            
        except Exception as e:
            logger.error(f"Error getting ensemble anomaly scores: {e}")
            return np.zeros(len(X))
    
    def _majority_voting(self, predictions: Dict[str, np.ndarray]) -> np.ndarray:
        """Combine predictions using majority voting"""
        # Convert predictions to binary (0 for normal, 1 for anomaly)
        binary_predictions = {}
        for model_name, pred in predictions.items():
            binary_predictions[model_name] = np.where(pred == -1, 1, 0)
        
        # Sum predictions across models
        total_votes = np.zeros(len(list(predictions.values())[0]))
        for pred in binary_predictions.values():
            total_votes += pred
        
        # Majority vote (more than half of models vote anomaly)
        threshold = len(predictions) / 2
        ensemble_predictions = np.where(total_votes > threshold, -1, 1)
        return ensemble_predictions
    
    def _average_voting(self, predictions: Dict[str, np.ndarray]) -> np.ndarray:
        """Combine predictions by averaging"""
        # Average predictions
        avg_predictions = np.zeros(len(list(predictions.values())[0]))
        for pred in predictions.values():
            avg_predictions += pred
        
        avg_predictions /= len(predictions)
        
        # Convert to binary predictions
        ensemble_predictions = np.where(avg_predictions < 0, -1, 1)
        return ensemble_predictions
    
    def _weighted_voting(self, predictions: Dict[str, np.ndarray]) -> np.ndarray:
        """Combine predictions using weighted voting"""
        weighted_predictions = np.zeros(len(list(predictions.values())[0]))
        total_weight = 0
        
        for model_name, pred in predictions.items():
            weight = self.model_weights.get(model_name, 1.0)
            weighted_predictions += pred * weight
            total_weight += weight
        
        weighted_predictions /= total_weight
        
        # Convert to binary predictions
        ensemble_predictions = np.where(weighted_predictions < 0, -1, 1)
        return ensemble_predictions
    
    def _average_scores(self, scores: Dict[str, np.ndarray]) -> np.ndarray:
        """Average anomaly scores from all models"""
        avg_scores = np.zeros(len(list(scores.values())[0]))
        for score in scores.values():
            avg_scores += score
        
        return avg_scores / len(scores)
    
    def _weighted_scores(self, scores: Dict[str, np.ndarray]) -> np.ndarray:
        """Weighted average of anomaly scores"""
        weighted_scores = np.zeros(len(list(scores.values())[0]))
        total_weight = 0
        
        for model_name, score in scores.items():
            weight = self.model_weights.get(model_name, 1.0)
            weighted_scores += score * weight
            total_weight += weight
        
        return weighted_scores / total_weight if total_weight > 0 else weighted_scores


# Global instances for easy access
isolation_forest_instance = None
autoencoder_instance = None
dbscan_instance = None
one_class_svm_instance = None
ensemble_instance = None


async def get_isolation_forest_model() -> IsolationForestModel:
    """Get singleton Isolation Forest model instance"""
    global isolation_forest_instance
    if isolation_forest_instance is None:
        isolation_forest_instance = IsolationForestModel()
    return isolation_forest_instance


async def get_autoencoder_model() -> AutoencoderModel:
    """Get singleton Autoencoder model instance"""
    global autoencoder_instance
    if autoencoder_instance is None:
        autoencoder_instance = AutoencoderModel()
    return autoencoder_instance


async def get_dbscan_model() -> DBSCANModel:
    """Get singleton DBSCAN model instance"""
    global dbscan_instance
    if dbscan_instance is None:
        dbscan_instance = DBSCANModel()
    return dbscan_instance


async def get_one_class_svm_model() -> OneClassSVMModel:
    """Get singleton One-Class SVM model instance"""
    global one_class_svm_instance
    if one_class_svm_instance is None:
        one_class_svm_instance = OneClassSVMModel()
    return one_class_svm_instance


async def get_ensemble_model() -> EnsembleAnomalyDetector:
    """Get singleton Ensemble model instance"""
    global ensemble_instance
    if ensemble_instance is None:
        ensemble_instance = EnsembleAnomalyDetector()
    return ensemble_instance