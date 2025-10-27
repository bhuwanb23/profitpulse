"""
Model Evaluation Metrics for Client Profitability Prediction
Implements comprehensive evaluation metrics for regression models
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple, Optional, Any

try:
    from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    r2_score = None
    mean_absolute_error = None
    mean_squared_error = None
    mean_absolute_percentage_error = None

logger = logging.getLogger(__name__)


class ProfitabilityModelEvaluator:
    """Evaluator for profitability prediction models"""
    
    def __init__(self):
        """Initialize the model evaluator"""
        if not SKLEARN_AVAILABLE:
            raise ImportError("scikit-learn is required for model evaluation but not available")
    
    def calculate_r2_score(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Calculate R² (Coefficient of Determination) score
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            R² score
        """
        if r2_score is not None:
            return r2_score(y_true, y_pred)
        return 0.0
    
    def calculate_mae(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Calculate Mean Absolute Error (MAE)
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            MAE score
        """
        if mean_absolute_error is not None:
            return mean_absolute_error(y_true, y_pred)
        return 0.0
    
    def calculate_rmse(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Calculate Root Mean Square Error (RMSE)
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            RMSE score
        """
        if mean_squared_error is not None:
            return np.sqrt(mean_squared_error(y_true, y_pred))
        return 0.0
    
    def calculate_mape(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Calculate Mean Absolute Percentage Error (MAPE)
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            MAPE score
        """
        if mean_absolute_percentage_error is not None:
            return mean_absolute_percentage_error(y_true, y_pred)
        return 0.0
    
    def calculate_all_metrics(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """
        Calculate all evaluation metrics
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            Dictionary with all metrics
        """
        logger.info("Calculating all evaluation metrics")
        
        try:
            metrics = {
                'r2': self.calculate_r2_score(y_true, y_pred),
                'mae': self.calculate_mae(y_true, y_pred),
                'rmse': self.calculate_rmse(y_true, y_pred),
                'mape': self.calculate_mape(y_true, y_pred)
            }
            
            logger.info(f"Metrics calculated - R²: {metrics['r2']:.4f}, MAE: {metrics['mae']:.4f}")
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating metrics: {e}")
            raise
    
    def evaluate_model_performance(self, y_true: np.ndarray, y_pred: np.ndarray, 
                                 model_name: str = "Model") -> Dict[str, Any]:
        """
        Evaluate overall model performance with detailed metrics
        
        Args:
            y_true: True values
            y_pred: Predicted values
            model_name: Name of the model for reporting
            
        Returns:
            Dictionary with performance evaluation
        """
        logger.info(f"Evaluating {model_name} performance")
        
        try:
            # Calculate metrics
            metrics = self.calculate_all_metrics(y_true, y_pred)
            
            # Calculate additional statistics
            residuals = y_true - y_pred
            residual_stats = {
                'mean_residual': np.mean(residuals),
                'std_residual': np.std(residuals),
                'min_residual': np.min(residuals),
                'max_residual': np.max(residuals)
            }
            
            # Performance classification
            r2_score = metrics['r2']
            if r2_score >= 0.9:
                performance_level = "Excellent"
            elif r2_score >= 0.8:
                performance_level = "Good"
            elif r2_score >= 0.7:
                performance_level = "Fair"
            else:
                performance_level = "Poor"
            
            evaluation = {
                'model_name': model_name,
                'metrics': metrics,
                'residual_statistics': residual_stats,
                'performance_level': performance_level,
                'sample_size': len(y_true)
            }
            
            logger.info(f"{model_name} evaluation completed - Performance: {performance_level}")
            return evaluation
            
        except Exception as e:
            logger.error(f"Error evaluating model performance: {e}")
            raise


# Convenience functions for easy usage
def calculate_profitability_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """
    Calculate profitability prediction metrics
    
    Args:
        y_true: True values
        y_pred: Predicted values
        
    Returns:
        Dictionary with metrics
    """
    evaluator = ProfitabilityModelEvaluator()
    return evaluator.calculate_all_metrics(y_true, y_pred)


def evaluate_profitability_model(y_true: np.ndarray, y_pred: np.ndarray, 
                               model_name: str = "Model") -> Dict[str, Any]:
    """
    Evaluate profitability prediction model performance
    
    Args:
        y_true: True values
        y_pred: Predicted values
        model_name: Name of the model for reporting
        
    Returns:
        Dictionary with performance evaluation
    """
    evaluator = ProfitabilityModelEvaluator()
    return evaluator.evaluate_model_performance(y_true, y_pred, model_name)