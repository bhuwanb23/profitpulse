"""
XGBoost Regression Model for Client Profitability Prediction
Implements gradient boosting for high-performance profitability prediction
"""

import pandas as pd
import numpy as np
import logging
import pickle
import os
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    xgb = None

try:
    from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
    from sklearn.model_selection import cross_val_score, GridSearchCV
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

logger = logging.getLogger(__name__)


class XGBoostProfitabilityModel:
    """XGBoost regression model for client profitability prediction"""
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the XGBoost model
        
        Args:
            model_path: Path to load a pre-trained model
        """
        if not XGBOOST_AVAILABLE:
            raise ImportError("XGBoost is required for this model but not available")
            
        if not SKLEARN_AVAILABLE:
            raise ImportError("scikit-learn is required for this model but not available")
        
        self.model = None
        self.feature_names = None
        self.is_trained = False
        self.training_timestamp = None
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
    
    def prepare_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare features for model training/prediction
        
        Args:
            data: DataFrame with features
            
        Returns:
            DataFrame with prepared features
        """
        logger.info("Preparing features for XGBoost model")
        
        try:
            # Create a copy to avoid modifying original data
            features_df = data.copy()
            
            # Remove non-feature columns
            non_feature_columns = ['id', 'name', 'start_date', 'end_date']
            feature_columns = [col for col in features_df.columns if col not in non_feature_columns]
            
            # Select only feature columns
            features_df = features_df[feature_columns].copy()
            
            # Handle categorical variables (one-hot encoding)
            categorical_columns = features_df.select_dtypes(include=['object']).columns
            if len(categorical_columns) > 0:
                features_df = pd.get_dummies(features_df, columns=categorical_columns, dummy_na=True)
            
            # Handle missing values
            features_df = features_df.fillna(0)
            
            logger.info(f"Prepared {len(features_df.columns)} features for model")
            return features_df
            
        except Exception as e:
            logger.error(f"Error preparing features: {e}")
            raise
    
    def train(self, train_data: pd.DataFrame, target_column: str = 'profit_margin',
              validation_data: Optional[pd.DataFrame] = None, 
              params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Train the XGBoost model
        
        Args:
            train_data: Training data DataFrame
            target_column: Column name for target variable
            validation_data: Optional validation data
            params: XGBoost parameters
            
        Returns:
            Dictionary with training results
        """
        logger.info("Training XGBoost profitability model")
        
        try:
            # Prepare features
            X_train = self.prepare_features(train_data)
            y_train = train_data[target_column].values
            
            # Store feature names
            self.feature_names = X_train.columns.tolist()
            
            # Default parameters
            if params is None:
                params = {
                    'objective': 'reg:squarederror',
                    'eval_metric': 'rmse',
                    'max_depth': 6,
                    'learning_rate': 0.1,
                    'n_estimators': 100,
                    'subsample': 0.8,
                    'colsample_bytree': 0.8,
                    'random_state': 42
                }
            
            # Create and train model
            self.model = xgb.XGBRegressor(**params)
            self.model.fit(X_train, y_train, verbose=False)
            
            # Evaluate on training data
            train_predictions = self.model.predict(X_train)
            train_r2 = r2_score(y_train, train_predictions)
            train_mae = mean_absolute_error(y_train, train_predictions)
            train_rmse = np.sqrt(mean_squared_error(y_train, train_predictions))
            
            # Evaluate on validation data if provided
            validation_metrics = {}
            if validation_data is not None:
                X_val = self.prepare_features(validation_data)
                y_val = validation_data[target_column].values
                val_predictions = self.model.predict(X_val)
                validation_metrics = {
                    'r2': r2_score(y_val, val_predictions),
                    'mae': mean_absolute_error(y_val, val_predictions),
                    'rmse': np.sqrt(mean_squared_error(y_val, val_predictions))
                }
            
            self.is_trained = True
            self.training_timestamp = datetime.now()
            
            results = {
                'training_metrics': {
                    'r2': train_r2,
                    'mae': train_mae,
                    'rmse': train_rmse
                },
                'validation_metrics': validation_metrics,
                'feature_importance': self.get_feature_importance(),
                'training_timestamp': self.training_timestamp.isoformat()
            }
            
            logger.info(f"Model training completed - Train R²: {train_r2:.4f}")
            return results
            
        except Exception as e:
            logger.error(f"Error training model: {e}")
            raise
    
    def predict(self, data: pd.DataFrame) -> np.ndarray:
        """
        Make predictions using the trained model
        
        Args:
            data: DataFrame with features
            
        Returns:
            Array of predictions
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
            
        logger.info("Making predictions with XGBoost model")
        
        try:
            # Prepare features
            X = self.prepare_features(data)
            
            # Ensure feature columns match training
            if self.feature_names:
                # Add missing columns with zeros
                for col in self.feature_names:
                    if col not in X.columns:
                        X[col] = 0
                
                # Remove extra columns
                X = X[self.feature_names]
            
            # Make predictions
            predictions = self.model.predict(X)
            
            logger.info(f"Generated {len(predictions)} predictions")
            return predictions
            
        except Exception as e:
            logger.error(f"Error making predictions: {e}")
            raise
    
    def get_feature_importance(self) -> Dict[str, float]:
        """
        Get feature importance from the trained model
        
        Returns:
            Dictionary with feature importance scores
        """
        if not self.is_trained or self.model is None:
            return {}
            
        try:
            if self.feature_names and hasattr(self.model, 'feature_importances_'):
                importance_scores = self.model.feature_importances_
                return dict(zip(self.feature_names, importance_scores))
            return {}
            
        except Exception as e:
            logger.error(f"Error getting feature importance: {e}")
            return {}
    
    def save_model(self, filepath: str) -> None:
        """
        Save the trained model to disk
        
        Args:
            filepath: Path to save the model
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")
            
        logger.info(f"Saving model to {filepath}")
        
        try:
            model_data = {
                'model': self.model,
                'feature_names': self.feature_names,
                'is_trained': self.is_trained,
                'training_timestamp': self.training_timestamp
            }
            
            with open(filepath, 'wb') as f:
                pickle.dump(model_data, f)
                
            logger.info("Model saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            raise
    
    def load_model(self, filepath: str) -> None:
        """
        Load a trained model from disk
        
        Args:
            filepath: Path to load the model from
        """
        logger.info(f"Loading model from {filepath}")
        
        try:
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            
            self.model = model_data['model']
            self.feature_names = model_data['feature_names']
            self.is_trained = model_data['is_trained']
            self.training_timestamp = model_data['training_timestamp']
            
            logger.info("Model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise


# Convenience function for easy usage
def train_xgboost_profitability_model(train_data: pd.DataFrame, 
                                    target_column: str = 'profit_margin',
                                    validation_data: Optional[pd.DataFrame] = None,
                                    params: Optional[Dict[str, Any]] = None,
                                    model_path: Optional[str] = None) -> Tuple[XGBoostProfitabilityModel, Dict[str, Any]]:
    """
    Train an XGBoost model for client profitability prediction
    
    Args:
        train_data: Training data DataFrame
        target_column: Column name for target variable
        validation_data: Optional validation data
        params: XGBoost parameters
        model_path: Path to save the trained model
        
    Returns:
        Tuple of (trained_model, training_results)
    """
    model = XGBoostProfitabilityModel()
    results = model.train(train_data, target_column, validation_data, params)
    
    if model_path:
        model.save_model(model_path)
    
    return model, results


def predict_with_xgboost_model(model_path: str, data: pd.DataFrame) -> np.ndarray:
    """
    Make predictions using a saved XGBoost model
    
    Args:
        model_path: Path to the saved model
        data: DataFrame with features
        
    Returns:
        Array of predictions
    """
    model = XGBoostProfitabilityModel(model_path)
    return model.predict(data)