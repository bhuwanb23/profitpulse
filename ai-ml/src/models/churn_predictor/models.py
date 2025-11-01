"""
Churn Prediction Models
Implements various machine learning models for client churn prediction
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Conditional imports for machine learning libraries
try:
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.neural_network import MLPClassifier
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
    SKLEARN_AVAILABLE = True
except ImportError:
    LogisticRegression = None
    RandomForestClassifier = None
    MLPClassifier = None
    StandardScaler = None
    SKLEARN_AVAILABLE = False

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

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    xgb = None
    XGBOOST_AVAILABLE = False

logger = logging.getLogger(__name__)


class ChurnLogisticRegression:
    """Logistic Regression model for churn prediction"""
    
    def __init__(self, **kwargs):
        """
        Initialize Logistic Regression model
        
        Args:
            **kwargs: Additional arguments for LogisticRegression
        """
        self.model = None
        self.scaler = StandardScaler() if StandardScaler else None
        self.feature_names = None
        self.is_trained = False
        self.kwargs = kwargs
        logger.info("Churn Logistic Regression Model initialized")
    
    def train(self, X: pd.DataFrame, y: pd.Series) -> bool:
        """
        Train the Logistic Regression model
        
        Args:
            X: Training features
            y: Training labels
            
        Returns:
            Boolean indicating success
        """
        try:
            if not SKLEARN_AVAILABLE:
                logger.warning("scikit-learn not available, cannot train Logistic Regression")
                return False
            
            # Store feature names
            self.feature_names = list(X.columns) if hasattr(X, 'columns') else [f"feature_{i}" for i in range(X.shape[1])]
            
            # Scale features
            if self.scaler is not None:
                X_scaled = self.scaler.fit_transform(X)
            else:
                X_scaled = X.values if hasattr(X, 'values') else X
            
            # Train model
            if LogisticRegression is not None:
                self.model = LogisticRegression(**self.kwargs)
                self.model.fit(X_scaled, y)
                self.is_trained = True
            else:
                logger.warning("LogisticRegression not available")
                return False
            
            logger.info("Logistic Regression model trained successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error training Logistic Regression model: {e}")
            return False
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict churn using the trained model
        
        Args:
            X: Data to predict churn for
            
        Returns:
            Array of churn predictions (0 for not churn, 1 for churn)
        """
        try:
            if not self.is_trained or self.model is None:
                logger.warning("Model not trained, returning mock predictions")
                return np.zeros(len(X))
            
            # Scale features
            if self.scaler is not None:
                X_scaled = self.scaler.transform(X)
            else:
                X_scaled = X.values if hasattr(X, 'values') else X
            
            # Predict
            predictions = self.model.predict(X_scaled)
            return predictions
            
        except Exception as e:
            logger.error(f"Error predicting with Logistic Regression model: {e}")
            return np.zeros(len(X))
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Get prediction probabilities using the trained model
        
        Args:
            X: Data to predict churn probabilities for
            
        Returns:
            Array of churn probabilities
        """
        try:
            if not self.is_trained or self.model is None:
                logger.warning("Model not trained, returning mock probabilities")
                return np.zeros(len(X))
            
            # Scale features
            if self.scaler is not None:
                X_scaled = self.scaler.transform(X)
            else:
                X_scaled = X.values if hasattr(X, 'values') else X
            
            # Get probabilities
            probabilities = self.model.predict_proba(X_scaled)
            return probabilities[:, 1]  # Return probability of churn (class 1)
            
        except Exception as e:
            logger.error(f"Error getting probabilities from Logistic Regression model: {e}")
            return np.zeros(len(X))


class ChurnNeuralNetwork:
    """Neural Network model for churn prediction"""
    
    def __init__(self, hidden_layers: Tuple[int, ...] = (64, 32), 
                 epochs: int = 100, batch_size: int = 32, **kwargs):
        """
        Initialize Neural Network model
        
        Args:
            hidden_layers: Tuple of hidden layer sizes
            epochs: Number of training epochs
            batch_size: Batch size for training
            **kwargs: Additional arguments for neural network
        """
        self.hidden_layers = hidden_layers
        self.epochs = epochs
        self.batch_size = batch_size
        self.model = None
        self.scaler = StandardScaler() if StandardScaler else None
        self.feature_names = None
        self.is_trained = False
        self.kwargs = kwargs
        logger.info("Churn Neural Network Model initialized")
    
    def train(self, X: pd.DataFrame, y: pd.Series) -> bool:
        """
        Train the Neural Network model
        
        Args:
            X: Training features
            y: Training labels
            
        Returns:
            Boolean indicating success
        """
        try:
            if not TENSORFLOW_AVAILABLE:
                logger.warning("TensorFlow not available, cannot train Neural Network")
                return False
            
            # Store feature names and dimensions
            self.feature_names = list(X.columns) if hasattr(X, 'columns') else [f"feature_{i}" for i in range(X.shape[1])]
            input_dim = X.shape[1]
            
            # Scale features
            if self.scaler is not None:
                X_scaled = self.scaler.fit_transform(X)
            else:
                X_scaled = X.values if hasattr(X, 'values') else X
            
            # Build model
            self._build_model(input_dim)
            
            if self.model is not None:
                # Train model
                self.model.fit(
                    X_scaled, y,
                    epochs=self.epochs,
                    batch_size=self.batch_size,
                    validation_split=0.2,
                    verbose=0,
                    **self.kwargs
                )
                self.is_trained = True
            else:
                logger.warning("Neural Network model not built successfully")
                return False
            
            logger.info("Neural Network model trained successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error training Neural Network model: {e}")
            return False
    
    def _build_model(self, input_dim: int):
        """Build the neural network architecture"""
        try:
            if keras is not None and layers is not None:
                model = keras.Sequential()
                model.add(layers.Dense(self.hidden_layers[0], activation='relu', input_shape=(input_dim,)))
                
                # Add hidden layers
                for units in self.hidden_layers[1:]:
                    model.add(layers.Dense(units, activation='relu'))
                    model.add(layers.Dropout(0.2))
                
                # Output layer
                model.add(layers.Dense(1, activation='sigmoid'))
                
                # Compile model
                model.compile(
                    optimizer='adam',
                    loss='binary_crossentropy',
                    metrics=['accuracy']
                )
                
                self.model = model
            else:
                logger.warning("Keras or layers not available for neural network building")
                self.model = None
        except Exception as e:
            logger.error(f"Error building neural network: {e}")
            self.model = None
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict churn using the trained model
        
        Args:
            X: Data to predict churn for
            
        Returns:
            Array of churn predictions (0 for not churn, 1 for churn)
        """
        try:
            if not self.is_trained or self.model is None:
                logger.warning("Model not trained, returning mock predictions")
                return np.zeros(len(X))
            
            # Scale features
            if self.scaler is not None:
                X_scaled = self.scaler.transform(X)
            else:
                X_scaled = X.values if hasattr(X, 'values') else X
            
            # Predict
            probabilities = self.model.predict(X_scaled, verbose=0)
            predictions = (probabilities > 0.5).astype(int).flatten()
            return predictions
            
        except Exception as e:
            logger.error(f"Error predicting with Neural Network model: {e}")
            return np.zeros(len(X))
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Get prediction probabilities using the trained model
        
        Args:
            X: Data to predict churn probabilities for
            
        Returns:
            Array of churn probabilities
        """
        try:
            if not self.is_trained or self.model is None:
                logger.warning("Model not trained, returning mock probabilities")
                return np.zeros(len(X))
            
            # Scale features
            if self.scaler is not None:
                X_scaled = self.scaler.transform(X)
            else:
                X_scaled = X.values if hasattr(X, 'values') else X
            
            # Get probabilities
            probabilities = self.model.predict(X_scaled, verbose=0).flatten()
            return probabilities
            
        except Exception as e:
            logger.error(f"Error getting probabilities from Neural Network model: {e}")
            return np.zeros(len(X))


class ChurnGradientBoosting:
    """Gradient Boosting model for churn prediction"""
    
    def __init__(self, model_type: str = 'xgboost', **kwargs):
        """
        Initialize Gradient Boosting model
        
        Args:
            model_type: Type of gradient boosting ('xgboost', 'random_forest')
            **kwargs: Additional arguments for the model
        """
        self.model_type = model_type
        self.model = None
        self.feature_names = None
        self.is_trained = False
        self.kwargs = kwargs
        logger.info(f"Churn Gradient Boosting Model ({model_type}) initialized")
    
    def train(self, X: pd.DataFrame, y: pd.Series) -> bool:
        """
        Train the Gradient Boosting model
        
        Args:
            X: Training features
            y: Training labels
            
        Returns:
            Boolean indicating success
        """
        try:
            # Store feature names
            self.feature_names = list(X.columns) if hasattr(X, 'columns') else [f"feature_{i}" for i in range(X.shape[1])]
            
            if self.model_type == 'xgboost':
                if not XGBOOST_AVAILABLE:
                    logger.warning("XGBoost not available, cannot train XGBoost model")
                    return False
                
                # Train XGBoost model
                if xgb is not None:
                    self.model = xgb.XGBClassifier(**self.kwargs)
                    self.model.fit(X, y)
                    self.is_trained = True
                else:
                    logger.warning("XGBClassifier not available")
                    return False
                    
            elif self.model_type == 'random_forest':
                if not SKLEARN_AVAILABLE:
                    logger.warning("scikit-learn not available, cannot train Random Forest")
                    return False
                
                # Train Random Forest model
                if RandomForestClassifier is not None:
                    self.model = RandomForestClassifier(**self.kwargs)
                    self.model.fit(X, y)
                    self.is_trained = True
                else:
                    logger.warning("RandomForestClassifier not available")
                    return False
            else:
                logger.warning(f"Unknown model type: {self.model_type}")
                return False
            
            logger.info(f"{self.model_type.capitalize()} model trained successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error training {self.model_type} model: {e}")
            return False
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict churn using the trained model
        
        Args:
            X: Data to predict churn for
            
        Returns:
            Array of churn predictions (0 for not churn, 1 for churn)
        """
        try:
            if not self.is_trained or self.model is None:
                logger.warning("Model not trained, returning mock predictions")
                return np.zeros(len(X))
            
            # Predict
            predictions = self.model.predict(X)
            return predictions
            
        except Exception as e:
            logger.error(f"Error predicting with {self.model_type} model: {e}")
            return np.zeros(len(X))
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Get prediction probabilities using the trained model
        
        Args:
            X: Data to predict churn probabilities for
            
        Returns:
            Array of churn probabilities
        """
        try:
            if not self.is_trained or self.model is None:
                logger.warning("Model not trained, returning mock probabilities")
                return np.zeros(len(X))
            
            # Get probabilities
            probabilities = self.model.predict_proba(X)
            return probabilities[:, 1]  # Return probability of churn (class 1)
            
        except Exception as e:
            logger.error(f"Error getting probabilities from {self.model_type} model: {e}")
            return np.zeros(len(X))


class ChurnEnsembleModel:
    """Ensemble of churn prediction models"""
    
    def __init__(self, voting_method: str = 'average'):
        """
        Initialize Ensemble Model
        
        Args:
            voting_method: Voting method ('average', 'majority')
        """
        self.voting_method = voting_method
        self.models = {
            'logistic_regression': ChurnLogisticRegression(),
            'neural_network': ChurnNeuralNetwork(),
            'xgboost': ChurnGradientBoosting(model_type='xgboost'),
            'random_forest': ChurnGradientBoosting(model_type='random_forest')
        }
        self.is_trained = False
        self.feature_names = None
        logger.info("Churn Ensemble Model initialized")
    
    def train(self, X: pd.DataFrame, y: pd.Series) -> bool:
        """
        Train all models in the ensemble
        
        Args:
            X: Training features
            y: Training labels
            
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
                result = model.train(X, y)
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
        Predict churn using ensemble of models
        
        Args:
            X: Data to predict churn for
            
        Returns:
            Array of churn predictions (0 for not churn, 1 for churn)
        """
        try:
            if not self.is_trained:
                logger.warning("Ensemble not trained, returning mock predictions")
                return np.zeros(len(X))
            
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
            else:
                return self._average_voting(predictions)
            
        except Exception as e:
            logger.error(f"Error predicting with ensemble models: {e}")
            return np.zeros(len(X))
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Get prediction probabilities using ensemble of models
        
        Args:
            X: Data to predict churn probabilities for
            
        Returns:
            Array of churn probabilities
        """
        try:
            if not self.is_trained:
                logger.warning("Ensemble not trained, returning mock probabilities")
                return np.zeros(len(X))
            
            # Get probabilities from all models
            probabilities = {}
            for model_name, model in self.models.items():
                prob = model.predict_proba(X)
                probabilities[model_name] = prob
            
            # Combine probabilities based on voting method
            if self.voting_method == 'majority':
                return self._average_probabilities(probabilities)
            elif self.voting_method == 'average':
                return self._average_probabilities(probabilities)
            else:
                return self._average_probabilities(probabilities)
            
        except Exception as e:
            logger.error(f"Error getting ensemble probabilities: {e}")
            return np.zeros(len(X))
    
    def _majority_voting(self, predictions: Dict[str, np.ndarray]) -> np.ndarray:
        """Combine predictions using majority voting"""
        # Sum predictions across models
        total_votes = np.zeros(len(list(predictions.values())[0]))
        for pred in predictions.values():
            total_votes += pred
        
        # Majority vote (more than half of models vote churn)
        threshold = len(predictions) / 2
        ensemble_predictions = (total_votes > threshold).astype(int)
        return ensemble_predictions
    
    def _average_voting(self, predictions: Dict[str, np.ndarray]) -> np.ndarray:
        """Combine predictions by averaging"""
        # Average predictions
        avg_predictions = np.zeros(len(list(predictions.values())[0]))
        for pred in predictions.values():
            avg_predictions += pred
        
        avg_predictions /= len(predictions)
        
        # Convert to binary predictions
        ensemble_predictions = (avg_predictions > 0.5).astype(int)
        return ensemble_predictions
    
    def _average_probabilities(self, probabilities: Dict[str, np.ndarray]) -> np.ndarray:
        """Average probabilities from all models"""
        avg_probabilities = np.zeros(len(list(probabilities.values())[0]))
        for prob in probabilities.values():
            avg_probabilities += prob
        
        return avg_probabilities / len(probabilities)


# Model evaluation utilities
def evaluate_churn_model(y_true: np.ndarray, y_pred: np.ndarray, 
                        y_proba: Optional[np.ndarray] = None) -> Dict[str, float]:
    """
    Evaluate churn model performance
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        y_proba: Predicted probabilities (optional)
        
    Returns:
        Dictionary with evaluation metrics
    """
    try:
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, zero_division=0),
            'recall': recall_score(y_true, y_pred, zero_division=0),
            'f1_score': f1_score(y_true, y_pred, zero_division=0)
        }
        
        # Add AUC if probabilities are provided
        if y_proba is not None:
            try:
                metrics['auc'] = roc_auc_score(y_true, y_proba)
            except Exception:
                metrics['auc'] = 0.0
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error evaluating model: {e}")
        return {
            'accuracy': 0.0,
            'precision': 0.0,
            'recall': 0.0,
            'f1_score': 0.0,
            'auc': 0.0
        }


# Global instances for easy access
logistic_regression_instance = None
neural_network_instance = None
xgboost_instance = None
random_forest_instance = None
ensemble_instance = None


def get_logistic_regression_model() -> ChurnLogisticRegression:
    """Get singleton Logistic Regression model instance"""
    global logistic_regression_instance
    if logistic_regression_instance is None:
        logistic_regression_instance = ChurnLogisticRegression()
    return logistic_regression_instance


def get_neural_network_model() -> ChurnNeuralNetwork:
    """Get singleton Neural Network model instance"""
    global neural_network_instance
    if neural_network_instance is None:
        neural_network_instance = ChurnNeuralNetwork()
    return neural_network_instance


def get_xgboost_model() -> ChurnGradientBoosting:
    """Get singleton XGBoost model instance"""
    global xgboost_instance
    if xgboost_instance is None:
        xgboost_instance = ChurnGradientBoosting(model_type='xgboost')
    return xgboost_instance


def get_random_forest_model() -> ChurnGradientBoosting:
    """Get singleton Random Forest model instance"""
    global random_forest_instance
    if random_forest_instance is None:
        random_forest_instance = ChurnGradientBoosting(model_type='random_forest')
    return random_forest_instance


def get_ensemble_model() -> ChurnEnsembleModel:
    """Get singleton Ensemble model instance"""
    global ensemble_instance
    if ensemble_instance is None:
        ensemble_instance = ChurnEnsembleModel()
    return ensemble_instance