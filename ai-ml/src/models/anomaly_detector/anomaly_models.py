"""
Anomaly Detection Models for Anomaly Detection System
Implements various anomaly detection algorithms including One-Class SVM, DBSCAN, and statistical methods
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Conditional imports for ML libraries
try:
    from sklearn.svm import OneClassSVM
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import accuracy_score
    SKLEARN_AVAILABLE = True
except ImportError:
    OneClassSVM = None
    StandardScaler = None
    accuracy_score = None
    SKLEARN_AVAILABLE = False

try:
    from sklearn.cluster import DBSCAN
    SKLEARN_CLUSTER_AVAILABLE = True
except ImportError:
    DBSCAN = None
    SKLEARN_CLUSTER_AVAILABLE = False

try:
    from sklearn.ensemble import IsolationForest
    SKLEARN_ENSEMBLE_AVAILABLE = True
except ImportError:
    IsolationForest = None
    SKLEARN_ENSEMBLE_AVAILABLE = False

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
        self.available = SKLEARN_AVAILABLE and OneClassSVM is not None
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
            if not self.available:
                logger.warning("Scikit-learn not available for One-Class SVM")
                return False
            
            if X.empty:
                logger.warning("Empty training data provided")
                return False
            
            # Store feature names
            self.feature_names = list(X.columns) if hasattr(X, 'columns') else None
            
            # Scale features
            if self.scaler is not None:
                X_scaled = self.scaler.fit_transform(X)
            else:
                X_scaled = X.values if hasattr(X, 'values') else X
            
            # Initialize and train model
            self.model = OneClassSVM(kernel=self.kernel, nu=self.nu, gamma=self.gamma)
            self.model.fit(X_scaled)
            
            self.is_trained = True
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
                return np.ones(len(X)) if len(X) > 0 else np.array([])
            
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
            return np.ones(len(X)) if len(X) > 0 else np.array([])
    
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
                return np.zeros(len(X)) if len(X) > 0 else np.array([])
            
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
            return np.zeros(len(X)) if len(X) > 0 else np.array([])


class DBSCANModel:
    """DBSCAN clustering for anomaly detection"""
    
    def __init__(self, eps: float = 0.5, min_samples: int = 5):
        """
        Initialize DBSCAN model
        
        Args:
            eps: The maximum distance between two samples for one to be considered as in the neighborhood of the other
            min_samples: The number of samples in a neighborhood for a point to be considered as a core point
        """
        self.eps = eps
        self.min_samples = min_samples
        self.model = None
        self.scaler = StandardScaler() if StandardScaler else None
        self.feature_names = None
        self.is_trained = False
        self.available = SKLEARN_CLUSTER_AVAILABLE and DBSCAN is not None
        logger.info("DBSCAN Model initialized")
    
    def train(self, X: pd.DataFrame) -> bool:
        """
        Train the DBSCAN model
        
        Args:
            X: Training data
            
        Returns:
            Boolean indicating success
        """
        try:
            if not self.available:
                logger.warning("Scikit-learn clustering not available for DBSCAN")
                return False
            
            if X.empty:
                logger.warning("Empty training data provided")
                return False
            
            # Store feature names
            self.feature_names = list(X.columns) if hasattr(X, 'columns') else None
            
            # Scale features
            if self.scaler is not None:
                X_scaled = self.scaler.fit_transform(X)
            else:
                X_scaled = X.values if hasattr(X, 'values') else X
            
            # Initialize and train model
            self.model = DBSCAN(eps=self.eps, min_samples=self.min_samples)
            cluster_labels = self.model.fit_predict(X_scaled)
            
            self.is_trained = True
            logger.info(f"DBSCAN model trained successfully with {len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)} clusters")
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
                return np.ones(len(X)) if len(X) > 0 else np.array([])
            
            # Scale features
            if self.scaler is not None:
                X_scaled = self.scaler.transform(X)
            else:
                X_scaled = X.values if hasattr(X, 'values') else X
            
            # Predict cluster labels
            cluster_labels = self.model.fit_predict(X_scaled)
            
            # Anomalies are points labeled as noise (-1)
            predictions = np.where(cluster_labels == -1, -1, 1)
            return predictions
            
        except Exception as e:
            logger.error(f"Error predicting with DBSCAN model: {e}")
            return np.ones(len(X)) if len(X) > 0 else np.array([])
    
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
                return np.zeros(len(X)) if len(X) > 0 else np.array([])
            
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
            return np.zeros(len(X)) if len(X) > 0 else np.array([])


class StatisticalAnomalyDetector:
    """Statistical methods for anomaly detection"""
    
    def __init__(self, method: str = 'zscore', threshold: float = 3.0):
        """
        Initialize statistical anomaly detector
        
        Args:
            method: Statistical method ('zscore', 'iqr', 'percentile')
            threshold: Threshold for anomaly detection
        """
        self.method = method
        self.threshold = threshold
        self.stats = {}
        self.feature_names = None
        self.is_trained = False
        logger.info("Statistical Anomaly Detector initialized")
    
    def train(self, X: pd.DataFrame) -> bool:
        """
        Train the statistical model by calculating statistics
        
        Args:
            X: Training data
            
        Returns:
            Boolean indicating success
        """
        try:
            if X.empty:
                logger.warning("Empty training data provided")
                return False
            
            # Store feature names
            self.feature_names = list(X.columns) if hasattr(X, 'columns') else None
            
            # Calculate statistics for each feature
            self.stats = {}
            for column in X.columns:
                values = X[column].dropna()
                if len(values) > 0:
                    self.stats[column] = {
                        'mean': np.mean(values),
                        'std': np.std(values),
                        'min': np.min(values),
                        'max': np.max(values),
                        'q25': np.percentile(values, 25),
                        'q75': np.percentile(values, 75),
                        'median': np.median(values)
                    }
            
            self.is_trained = True
            logger.info("Statistical model trained successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error training statistical model: {e}")
            return False
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict anomalies using statistical methods
        
        Args:
            X: Data to predict anomalies for
            
        Returns:
            Array of anomaly predictions (-1 for anomaly, 1 for normal)
        """
        try:
            if not self.is_trained:
                logger.warning("Model not trained, returning mock predictions")
                return np.ones(len(X)) if len(X) > 0 else np.array([])
            
            predictions = np.ones(len(X))
            
            # Apply statistical method
            if self.method == 'zscore':
                predictions = self._zscore_detection(X)
            elif self.method == 'iqr':
                predictions = self._iqr_detection(X)
            elif self.method == 'percentile':
                predictions = self._percentile_detection(X)
            
            return predictions
            
        except Exception as e:
            logger.error(f"Error predicting with statistical model: {e}")
            return np.ones(len(X)) if len(X) > 0 else np.array([])
    
    def _zscore_detection(self, X: pd.DataFrame) -> np.ndarray:
        """Detect anomalies using Z-score method"""
        try:
            predictions = np.ones(len(X))
            
            for column in X.columns:
                if column in self.stats:
                    values = X[column].fillna(self.stats[column]['mean'])
                    z_scores = np.abs((values - self.stats[column]['mean']) / (self.stats[column]['std'] + 1e-8))
                    predictions = np.where((z_scores > self.threshold) & (predictions == 1), -1, predictions)
            
            return predictions
        except Exception as e:
            logger.error(f"Error in Z-score detection: {e}")
            return np.ones(len(X))
    
    def _iqr_detection(self, X: pd.DataFrame) -> np.ndarray:
        """Detect anomalies using IQR method"""
        try:
            predictions = np.ones(len(X))
            
            for column in X.columns:
                if column in self.stats:
                    q25 = self.stats[column]['q25']
                    q75 = self.stats[column]['q75']
                    iqr = q75 - q25
                    lower_bound = q25 - 1.5 * iqr
                    upper_bound = q75 + 1.5 * iqr
                    values = X[column].fillna(self.stats[column]['median'])
                    predictions = np.where(((values < lower_bound) | (values > upper_bound)) & (predictions == 1), -1, predictions)
            
            return predictions
        except Exception as e:
            logger.error(f"Error in IQR detection: {e}")
            return np.ones(len(X))
    
    def _percentile_detection(self, X: pd.DataFrame) -> np.ndarray:
        """Detect anomalies using percentile method"""
        try:
            predictions = np.ones(len(X))
            
            lower_percentile = np.percentile(range(100), self.threshold if self.threshold < 50 else 100 - self.threshold)
            upper_percentile = 100 - lower_percentile
            
            for column in X.columns:
                if column in self.stats:
                    lower_bound = np.percentile([self.stats[column]['min'], self.stats[column]['max']], lower_percentile)
                    upper_bound = np.percentile([self.stats[column]['min'], self.stats[column]['max']], upper_percentile)
                    values = X[column].fillna(self.stats[column]['median'])
                    predictions = np.where(((values < lower_bound) | (values > upper_bound)) & (predictions == 1), -1, predictions)
            
            return predictions
        except Exception as e:
            logger.error(f"Error in percentile detection: {e}")
            return np.ones(len(X))
    
    def anomaly_scores(self, X: pd.DataFrame) -> np.ndarray:
        """
        Get anomaly scores using statistical methods
        
        Args:
            X: Data to score
            
        Returns:
            Array of anomaly scores
        """
        try:
            if not self.is_trained:
                logger.warning("Model not trained, returning mock scores")
                return np.zeros(len(X)) if len(X) > 0 else np.array([])
            
            scores = np.zeros(len(X))
            
            # Calculate scores based on method
            if self.method == 'zscore':
                scores = self._zscore_scores(X)
            elif self.method == 'iqr':
                scores = self._iqr_scores(X)
            elif self.method == 'percentile':
                scores = self._percentile_scores(X)
            
            return scores
            
        except Exception as e:
            logger.error(f"Error getting statistical anomaly scores: {e}")
            return np.zeros(len(X)) if len(X) > 0 else np.array([])
    
    def _zscore_scores(self, X: pd.DataFrame) -> np.ndarray:
        """Calculate Z-score based anomaly scores"""
        try:
            scores = np.zeros(len(X))
            
            for column in X.columns:
                if column in self.stats:
                    values = X[column].fillna(self.stats[column]['mean'])
                    z_scores = np.abs((values - self.stats[column]['mean']) / (self.stats[column]['std'] + 1e-8))
                    scores += z_scores
            
            return scores / len(X.columns) if len(X.columns) > 0 else scores
        except Exception as e:
            logger.error(f"Error calculating Z-score scores: {e}")
            return np.zeros(len(X))
    
    def _iqr_scores(self, X: pd.DataFrame) -> np.ndarray:
        """Calculate IQR based anomaly scores"""
        try:
            scores = np.zeros(len(X))
            
            for column in X.columns:
                if column in self.stats:
                    q25 = self.stats[column]['q25']
                    q75 = self.stats[column]['q75']
                    iqr = q75 - q25
                    values = X[column].fillna(self.stats[column]['median'])
                    # Normalize scores to be between 0 and 1
                    normalized_scores = np.abs(values - self.stats[column]['median']) / (iqr + 1e-8)
                    scores += normalized_scores
            
            return scores / len(X.columns) if len(X.columns) > 0 else scores
        except Exception as e:
            logger.error(f"Error calculating IQR scores: {e}")
            return np.zeros(len(X))
    
    def _percentile_scores(self, X: pd.DataFrame) -> np.ndarray:
        """Calculate percentile based anomaly scores"""
        try:
            scores = np.zeros(len(X))
            
            for column in X.columns:
                if column in self.stats:
                    median_val = self.stats[column]['median']
                    values = X[column].fillna(median_val)
                    # Simple distance from median as score
                    distances = np.abs(values - median_val)
                    max_distance = np.max(distances) if np.max(distances) > 0 else 1
                    normalized_scores = distances / max_distance
                    scores += normalized_scores
            
            return scores / len(X.columns) if len(X.columns) > 0 else scores
        except Exception as e:
            logger.error(f"Error calculating percentile scores: {e}")
            return np.zeros(len(X))


class MachineLearningAnomalyDetector:
    """Machine learning based anomaly detection"""
    
    def __init__(self, model_type: str = 'isolation_forest'):
        """
        Initialize machine learning anomaly detector
        
        Args:
            model_type: Type of model ('isolation_forest', 'autoencoder')
        """
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler() if StandardScaler else None
        self.feature_names = None
        self.is_trained = False
        self.available = True
        
        # Check specific model availability
        if model_type == 'isolation_forest' and not SKLEARN_ENSEMBLE_AVAILABLE:
            self.available = False
        elif model_type == 'autoencoder' and not TENSORFLOW_AVAILABLE:
            self.available = False
            
        logger.info(f"Machine Learning Anomaly Detector ({model_type}) initialized")
    
    def train(self, X: pd.DataFrame) -> Dict[str, Any]:
        """
        Train the machine learning model
        
        Args:
            X: Training data
            
        Returns:
            Dictionary with training results
        """
        try:
            if not self.available:
                logger.warning(f"Required libraries not available for {self.model_type}")
                return {
                    'success': False,
                    'message': f'Required libraries not available for {self.model_type}',
                    'model': None
                }
            
            if X.empty:
                logger.warning("Empty training data provided")
                return {
                    'success': False,
                    'message': 'Empty training data provided',
                    'model': None
                }
            
            # Store feature names
            self.feature_names = list(X.columns) if hasattr(X, 'columns') else None
            
            # Train based on model type
            if self.model_type == 'isolation_forest':
                result = self._train_isolation_forest(X)
            elif self.model_type == 'autoencoder':
                result = self._train_autoencoder(X)
            else:
                result = {
                    'success': False,
                    'message': f'Unknown model type: {self.model_type}',
                    'model': None
                }
            
            if result.get('success', False):
                self.is_trained = True
                logger.info(f"{self.model_type} model trained successfully")
            
            return result
            
        except Exception as e:
            logger.error(f"Error training {self.model_type} model: {e}")
            return {
                'success': False,
                'message': f'Training error: {str(e)}',
                'model': None
            }
    
    def _train_isolation_forest(self, X: pd.DataFrame) -> Dict[str, Any]:
        """Train Isolation Forest model"""
        try:
            if not SKLEARN_ENSEMBLE_AVAILABLE or IsolationForest is None:
                return {
                    'success': False,
                    'message': 'Scikit-learn ensemble not available',
                    'model': None
                }
            
            # Scale features
            if self.scaler is not None:
                X_scaled = self.scaler.fit_transform(X)
            else:
                X_scaled = X.values if hasattr(X, 'values') else X
            
            # Initialize and train model
            self.model = IsolationForest(contamination=0.1, random_state=42)
            self.model.fit(X_scaled)
            
            return {
                'success': True,
                'message': 'Isolation Forest trained successfully',
                'model': self.model
            }
            
        except Exception as e:
            logger.error(f"Error training Isolation Forest: {e}")
            return {
                'success': False,
                'message': f'Isolation Forest training error: {str(e)}',
                'model': None
            }
    
    def _train_autoencoder(self, X: pd.DataFrame) -> Dict[str, Any]:
        """Train Autoencoder model"""
        try:
            if not TENSORFLOW_AVAILABLE or tf is None:
                return {
                    'success': False,
                    'message': 'TensorFlow not available',
                    'model': None
                }
            
            # Scale features
            if self.scaler is not None:
                X_scaled = self.scaler.fit_transform(X)
            else:
                X_scaled = X.values if hasattr(X, 'values') else X
            
            input_dim = X_scaled.shape[1]
            encoding_dim = max(1, input_dim // 2)
            
            # Create autoencoder
            input_layer = keras.layers.Input(shape=(input_dim,))
            encoder = keras.layers.Dense(encoding_dim, activation='relu')(input_layer)
            decoder = keras.layers.Dense(input_dim, activation='linear')(encoder)
            
            self.model = keras.models.Model(inputs=input_layer, outputs=decoder)
            self.model.compile(optimizer='adam', loss='mse')
            
            # Train model
            self.model.fit(
                X_scaled, X_scaled,
                epochs=50,
                batch_size=32,
                shuffle=True,
                verbose=0
            )
            
            return {
                'success': True,
                'message': 'Autoencoder trained successfully',
                'model': self.model
            }
            
        except Exception as e:
            logger.error(f"Error training Autoencoder: {e}")
            return {
                'success': False,
                'message': f'Autoencoder training error: {str(e)}',
                'model': None
            }
    
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
                return np.ones(len(X)) if len(X) > 0 else np.array([])
            
            # Apply based on model type
            if self.model_type == 'isolation_forest':
                return self._predict_isolation_forest(X)
            elif self.model_type == 'autoencoder':
                return self._predict_autoencoder(X)
            else:
                return np.ones(len(X)) if len(X) > 0 else np.array([])
            
        except Exception as e:
            logger.error(f"Error predicting with {self.model_type} model: {e}")
            return np.ones(len(X)) if len(X) > 0 else np.array([])
    
    def _predict_isolation_forest(self, X: pd.DataFrame) -> np.ndarray:
        """Predict using Isolation Forest"""
        try:
            # Scale features
            if self.scaler is not None:
                X_scaled = self.scaler.transform(X)
            else:
                X_scaled = X.values if hasattr(X, 'values') else X
            
            # Predict anomalies
            predictions = self.model.predict(X_scaled)
            return predictions
            
        except Exception as e:
            logger.error(f"Error predicting with Isolation Forest: {e}")
            return np.ones(len(X))
    
    def _predict_autoencoder(self, X: pd.DataFrame) -> np.ndarray:
        """Predict using Autoencoder"""
        try:
            # Scale features
            if self.scaler is not None:
                X_scaled = self.scaler.transform(X)
            else:
                X_scaled = X.values if hasattr(X, 'values') else X
            
            # Reconstruct data
            reconstructed = self.model.predict(X_scaled, verbose=0)
            
            # Calculate reconstruction error
            mse = np.mean(np.power(X_scaled - reconstructed, 2), axis=1)
            
            # Use threshold to classify anomalies (simplified approach)
            threshold = np.percentile(mse, 90)  # Top 10% as anomalies
            predictions = np.where(mse > threshold, -1, 1)
            
            return predictions
            
        except Exception as e:
            logger.error(f"Error predicting with Autoencoder: {e}")
            return np.ones(len(X))
    
    def anomaly_scores(self, X: pd.DataFrame) -> np.ndarray:
        """
        Get anomaly scores for the data
        
        Args:
            X: Data to score
            
        Returns:
            Array of anomaly scores
        """
        try:
            if not self.is_trained or self.model is None:
                logger.warning("Model not trained, returning mock scores")
                return np.zeros(len(X)) if len(X) > 0 else np.array([])
            
            # Apply based on model type
            if self.model_type == 'isolation_forest':
                return self._scores_isolation_forest(X)
            elif self.model_type == 'autoencoder':
                return self._scores_autoencoder(X)
            else:
                return np.zeros(len(X)) if len(X) > 0 else np.array([])
            
        except Exception as e:
            logger.error(f"Error getting anomaly scores from {self.model_type} model: {e}")
            return np.zeros(len(X)) if len(X) > 0 else np.array([])
    
    def _scores_isolation_forest(self, X: pd.DataFrame) -> np.ndarray:
        """Get scores from Isolation Forest"""
        try:
            # Scale features
            if self.scaler is not None:
                X_scaled = self.scaler.transform(X)
            else:
                X_scaled = X.values if hasattr(X, 'values') else X
            
            # Get decision function scores
            scores = self.model.decision_function(X_scaled)
            return scores
            
        except Exception as e:
            logger.error(f"Error getting Isolation Forest scores: {e}")
            return np.zeros(len(X))
    
    def _scores_autoencoder(self, X: pd.DataFrame) -> np.ndarray:
        """Get scores from Autoencoder"""
        try:
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
            logger.error(f"Error getting Autoencoder scores: {e}")
            return np.zeros(len(X))


class EnsembleAnomalyDetector:
    """Ensemble anomaly detection combining multiple models"""
    
    def __init__(self, voting_method: str = 'majority', weights: Optional[List[float]] = None):
        """
        Initialize ensemble anomaly detector
        
        Args:
            voting_method: Voting method ('majority', 'weighted', 'average')
            weights: Weights for each model (if voting_method is 'weighted')
        """
        self.voting_method = voting_method
        self.weights = weights or [1.0, 1.0, 1.0, 1.0]  # Default weights for 4 models
        self.models = {
            'one_class_svm': get_one_class_svm_model(),
            'dbscan': get_dbscan_model(),
            'statistical': get_statistical_detector(),
            'ml': get_ml_detector()
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
            if X.empty:
                logger.warning("Empty training data provided")
                return False
            
            # Store feature names
            self.feature_names = list(X.columns) if hasattr(X, 'columns') else None
            
            # Train all models
            svm_success = self.models['one_class_svm'].train(X)
            dbscan_success = self.models['dbscan'].train(X)
            statistical_success = self.models['statistical'].train(X)
            ml_result = self.models['ml'].train(X)
            ml_success = ml_result.get('success', False) if isinstance(ml_result, dict) else False
            
            self.is_trained = svm_success and dbscan_success and statistical_success and ml_success
            logger.info(f"Ensemble model training completed. Success: {self.is_trained}")
            return self.is_trained
            
        except Exception as e:
            logger.error(f"Error training ensemble model: {e}")
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
                logger.warning("Ensemble model not trained, returning mock predictions")
                return np.ones(len(X)) if len(X) > 0 else np.array([])
            
            # Get predictions from all models
            predictions = {}
            
            # One-Class SVM predictions
            try:
                predictions['one_class_svm'] = self.models['one_class_svm'].predict(X)
            except Exception as e:
                logger.warning(f"Error getting One-Class SVM predictions: {e}")
                predictions['one_class_svm'] = np.ones(len(X)) if len(X) > 0 else np.array([])
            
            # DBSCAN predictions
            try:
                predictions['dbscan'] = self.models['dbscan'].predict(X)
            except Exception as e:
                logger.warning(f"Error getting DBSCAN predictions: {e}")
                predictions['dbscan'] = np.ones(len(X)) if len(X) > 0 else np.array([])
            
            # Statistical detector predictions
            try:
                predictions['statistical'] = self.models['statistical'].predict(X)
            except Exception as e:
                logger.warning(f"Error getting statistical predictions: {e}")
                predictions['statistical'] = np.ones(len(X)) if len(X) > 0 else np.array([])
            
            # ML detector predictions
            try:
                predictions['ml'] = self.models['ml'].predict(X)
            except Exception as e:
                logger.warning(f"Error getting ML predictions: {e}")
                predictions['ml'] = np.ones(len(X)) if len(X) > 0 else np.array([])
            
            # Combine predictions based on voting method
            if self.voting_method == 'majority':
                return self._majority_voting(predictions)
            elif self.voting_method == 'weighted':
                return self._weighted_voting(predictions)
            elif self.voting_method == 'average':
                return self._average_scores(predictions)
            else:
                # Default to majority voting
                return self._majority_voting(predictions)
                
        except Exception as e:
            logger.error(f"Error predicting with ensemble model: {e}")
            return np.ones(len(X)) if len(X) > 0 else np.array([])
    
    def _majority_voting(self, predictions: Dict[str, np.ndarray]) -> np.ndarray:
        """Combine predictions using majority voting"""
        try:
            # Convert predictions to a matrix
            pred_matrix = np.array([predictions[key] for key in predictions.keys()])
            
            # Count votes for each sample
            # Anomalies are -1, normal are 1
            anomaly_votes = np.sum(pred_matrix == -1, axis=0)
            normal_votes = np.sum(pred_matrix == 1, axis=0)
            
            # Majority vote
            ensemble_predictions = np.where(anomaly_votes > normal_votes, -1, 1)
            return ensemble_predictions
        except Exception as e:
            logger.error(f"Error in majority voting: {e}")
            return np.ones(len(predictions[list(predictions.keys())[0]])) if predictions else np.array([])
    
    def _weighted_voting(self, predictions: Dict[str, np.ndarray]) -> np.ndarray:
        """Combine predictions using weighted voting"""
        try:
            # Convert predictions to a matrix
            pred_matrix = np.array([predictions[key] for key in predictions.keys()])
            
            # Apply weights
            weighted_anomaly_scores = np.zeros(pred_matrix.shape[1])
            total_weight = sum(self.weights[:len(predictions)])
            
            for i, key in enumerate(predictions.keys()):
                if i < len(self.weights):
                    # Convert predictions to scores (anomaly=-1 -> score=1, normal=1 -> score=0)
                    scores = np.where(pred_matrix[i] == -1, 1, 0)
                    weighted_anomaly_scores += scores * self.weights[i]
            
            # Normalize by total weight
            normalized_scores = weighted_anomaly_scores / total_weight
            
            # Threshold at 0.5 for anomaly classification
            ensemble_predictions = np.where(normalized_scores > 0.5, -1, 1)
            return ensemble_predictions
        except Exception as e:
            logger.error(f"Error in weighted voting: {e}")
            return np.ones(len(predictions[list(predictions.keys())[0]])) if predictions else np.array([])
    
    def _average_scores(self, predictions: Dict[str, np.ndarray]) -> np.ndarray:
        """Combine predictions by averaging anomaly scores"""
        try:
            # Get scores from all models
            scores = {}
            
            # One-Class SVM scores
            try:
                svm_scores = self.models['one_class_svm'].anomaly_scores(predictions[list(predictions.keys())[0]])
                # Normalize SVM scores to [0,1] where higher means more anomalous
                scores['one_class_svm'] = (svm_scores - np.min(svm_scores)) / (np.max(svm_scores) - np.min(svm_scores) + 1e-8)
            except Exception as e:
                logger.warning(f"Error getting One-Class SVM scores: {e}")
                scores['one_class_svm'] = np.zeros(len(predictions[list(predictions.keys())[0]])) if predictions else np.array([])
            
            # DBSCAN scores
            try:
                dbscan_scores = self.models['dbscan'].anomaly_scores(predictions[list(predictions.keys())[0]])
                # DBSCAN scores are already distances (higher means more anomalous)
                scores['dbscan'] = dbscan_scores
                # Normalize if not all zeros
                if len(dbscan_scores) > 0 and np.max(dbscan_scores) > 0:
                    scores['dbscan'] = dbscan_scores / np.max(dbscan_scores)
            except Exception as e:
                logger.warning(f"Error getting DBSCAN scores: {e}")
                scores['dbscan'] = np.zeros(len(predictions[list(predictions.keys())[0]])) if predictions else np.array([])
            
            # Statistical scores
            try:
                statistical_scores = self.models['statistical'].anomaly_scores(predictions[list(predictions.keys())[0]])
                # Statistical scores are already normalized
                scores['statistical'] = statistical_scores
            except Exception as e:
                logger.warning(f"Error getting statistical scores: {e}")
                scores['statistical'] = np.zeros(len(predictions[list(predictions.keys())[0]])) if predictions else np.array([])
            
            # ML scores
            try:
                ml_scores = self.models['ml'].anomaly_scores(predictions[list(predictions.keys())[0]])
                # Normalize ML scores to [0,1]
                if len(ml_scores) > 0 and np.max(ml_scores) > np.min(ml_scores):
                    scores['ml'] = (ml_scores - np.min(ml_scores)) / (np.max(ml_scores) - np.min(ml_scores) + 1e-8)
                else:
                    scores['ml'] = np.zeros(len(ml_scores))
            except Exception as e:
                logger.warning(f"Error getting ML scores: {e}")
                scores['ml'] = np.zeros(len(predictions[list(predictions.keys())[0]])) if predictions else np.array([])
            
            # Average scores
            score_matrix = np.array([scores[key] for key in scores.keys()])
            average_scores = np.mean(score_matrix, axis=0)
            
            # Threshold at 0.5 for anomaly classification
            ensemble_predictions = np.where(average_scores > 0.5, -1, 1)
            return ensemble_predictions
        except Exception as e:
            logger.error(f"Error in average scores: {e}")
            return np.ones(len(predictions[list(predictions.keys())[0]])) if predictions else np.array([])
    
    def get_model_contributions(self, X: pd.DataFrame) -> Dict[str, float]:
        """
        Get the contribution of each model to the ensemble decision
        
        Args:
            X: Data to analyze
            
        Returns:
            Dictionary with model names and their contribution percentages
        """
        try:
            if not self.is_trained:
                return {}
            
            # Get predictions from all models
            predictions = {}
            predictions['one_class_svm'] = self.models['one_class_svm'].predict(X)
            predictions['dbscan'] = self.models['dbscan'].predict(X)
            predictions['statistical'] = self.models['statistical'].predict(X)
            predictions['ml'] = self.models['ml'].predict(X)
            
            # Count anomalies detected by each model
            contributions = {}
            total_anomalies = 0
            
            for model_name, preds in predictions.items():
                anomaly_count = np.sum(preds == -1)
                contributions[model_name] = int(anomaly_count)
                total_anomalies += anomaly_count
            
            # Convert to percentages
            if total_anomalies > 0:
                for model_name in contributions:
                    contributions[model_name] = round((contributions[model_name] / total_anomalies) * 100, 2)
            
            return contributions
            
        except Exception as e:
            logger.error(f"Error getting model contributions: {e}")
            return {}


# Global instances for easy access
one_class_svm_instance = None
dbscan_instance = None
statistical_detector_instance = None
ml_detector_instance = None
ensemble_detector_instance = None


def get_one_class_svm_model(kernel: str = 'rbf', nu: float = 0.1, gamma: str = 'scale') -> OneClassSVMModel:
    """Get singleton One-Class SVM model instance"""
    global one_class_svm_instance
    if one_class_svm_instance is None:
        one_class_svm_instance = OneClassSVMModel(kernel, nu, gamma)
    return one_class_svm_instance


def get_dbscan_model(eps: float = 0.5, min_samples: int = 5) -> DBSCANModel:
    """Get singleton DBSCAN model instance"""
    global dbscan_instance
    if dbscan_instance is None:
        dbscan_instance = DBSCANModel(eps, min_samples)
    return dbscan_instance


def get_statistical_detector(method: str = 'zscore', threshold: float = 3.0) -> StatisticalAnomalyDetector:
    """Get singleton statistical detector instance"""
    global statistical_detector_instance
    if statistical_detector_instance is None:
        statistical_detector_instance = StatisticalAnomalyDetector(method, threshold)
    return statistical_detector_instance


def get_ml_detector(model_type: str = 'isolation_forest') -> MachineLearningAnomalyDetector:
    """Get singleton machine learning detector instance"""
    global ml_detector_instance
    if ml_detector_instance is None:
        ml_detector_instance = MachineLearningAnomalyDetector(model_type)
    return ml_detector_instance


def get_ensemble_detector(voting_method: str = 'majority', weights: Optional[List[float]] = None) -> EnsembleAnomalyDetector:
    """Get singleton ensemble detector instance"""
    global ensemble_detector_instance
    if ensemble_detector_instance is None:
        ensemble_detector_instance = EnsembleAnomalyDetector(voting_method, weights)
    return ensemble_detector_instance