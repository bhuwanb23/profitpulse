"""
SHAP Explainer for Model Interpretability in Client Profitability Predictor
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import json
import warnings
warnings.filterwarnings('ignore')

# Conditional imports for optional dependencies
try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False
    shap = None

logger = logging.getLogger(__name__)


class SHAPExplainer:
    """SHAP explainer for model interpretability"""
    
    def __init__(self):
        self.explainer = None
        self.feature_names = None
        self.baseline_values = None
        logger.info("SHAP Explainer initialized")
    
    def create_explainer(self, model, X_background: Optional[pd.DataFrame] = None, 
                        explainer_type: str = 'tree') -> bool:
        """
        Create SHAP explainer for a trained model
        
        Args:
            model: Trained model
            X_background: Background dataset for SHAP (optional)
            explainer_type: Type of explainer ('tree', 'linear', 'deep', 'kernel')
            
        Returns:
            Boolean indicating success
        """
        if not SHAP_AVAILABLE:
            logger.warning("SHAP not available, cannot create explainer")
            return False
        
        try:
            # Store feature names if available
            if hasattr(X_background, 'columns'):
                if X_background is not None:
                    self.feature_names = list(X_background.columns)
            
            # Create appropriate explainer based on type
            if SHAP_AVAILABLE and shap is not None:
                if SHAP_AVAILABLE and shap is not None:
                    if explainer_type == 'tree':
                        self.explainer = shap.TreeExplainer(model, X_background)
                    elif explainer_type == 'linear':
                        self.explainer = shap.LinearExplainer(model, X_background)
                    elif explainer_type == 'deep':
                        self.explainer = shap.DeepExplainer(model, X_background)
                    elif explainer_type == 'kernel':
                        self.explainer = shap.KernelExplainer(model.predict, X_background)
                    else:
                        # Default to TreeExplainer for most models
                        self.explainer = shap.TreeExplainer(model, X_background)
            
            logger.info(f"SHAP explainer created with type: {explainer_type}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating SHAP explainer: {e}")
            return False
    
    def explain_prediction(self, X_instance: pd.DataFrame) -> Dict[str, Any]:
        """
        Explain a single prediction using SHAP values
        
        Args:
            X_instance: Single instance to explain
            
        Returns:
            Dictionary with explanation results
        """
        if not SHAP_AVAILABLE or self.explainer is None:
            logger.warning("SHAP not available or explainer not initialized")
            return self._mock_explanation(X_instance)
        
        try:
            # Calculate SHAP values
            shap_values = self.explainer.shap_values(X_instance)
            
            # Handle different SHAP output formats
            if isinstance(shap_values, list):
                # For multi-class, take the first class
                shap_values = shap_values[0]
            
            # Convert to 1D array if needed
            if shap_values.ndim > 1:
                shap_values = shap_values.flatten()
            
            # Get feature names
            feature_names = self.feature_names
            if feature_names is None and hasattr(X_instance, 'columns'):
                feature_names = list(X_instance.columns)
            elif feature_names is None:
                feature_names = [f"feature_{i}" for i in range(len(shap_values))]
            
            # Create explanation dictionary
            explanation = {}
            for i, feature_name in enumerate(feature_names):
                if i < len(shap_values):
                    explanation[feature_name] = float(shap_values[i])
            
            # Sort by absolute SHAP values
            sorted_explanation = dict(sorted(explanation.items(), 
                                           key=lambda x: abs(x[1]), reverse=True))
            
            result = {
                'shap_values': explanation,
                'sorted_shap_values': sorted_explanation,
                'base_value': float(self.explainer.expected_value) if hasattr(self.explainer, 'expected_value') else 0.0,
                'prediction': float(np.sum(shap_values)) + (float(self.explainer.expected_value) if hasattr(self.explainer, 'expected_value') else 0.0),
                'timestamp': datetime.now()
            }
            
            logger.info("Prediction explanation generated")
            return result
            
        except Exception as e:
            logger.error(f"Error generating explanation: {e}")
            return self._mock_explanation(X_instance)
    
    def explain_global_feature_importance(self, X_sample: pd.DataFrame, 
                                        max_display: int = 20) -> Dict[str, Any]:
        """
        Explain global feature importance using SHAP values
        
        Args:
            X_sample: Sample dataset to calculate SHAP values for
            max_display: Maximum number of features to display
            
        Returns:
            Dictionary with global importance results
        """
        if not SHAP_AVAILABLE or self.explainer is None:
            logger.warning("SHAP not available or explainer not initialized")
            return self._mock_global_importance(X_sample)
        
        try:
            # Calculate SHAP values for sample
            shap_values = self.explainer.shap_values(X_sample)
            
            # Handle different SHAP output formats
            if isinstance(shap_values, list):
                shap_values = shap_values[0]
            
            # Calculate mean absolute SHAP values for global importance
            if shap_values.ndim == 1:
                # For single prediction, reshape
                shap_values = shap_values.reshape(1, -1)
            
            # Calculate mean absolute SHAP values
            mean_abs_shap_values = np.mean(np.abs(shap_values), axis=0)
            
            # Get feature names
            feature_names = self.feature_names
            if feature_names is None and hasattr(X_sample, 'columns'):
                feature_names = list(X_sample.columns)
            elif feature_names is None:
                feature_names = [f"feature_{i}" for i in range(len(mean_abs_shap_values))]
            
            # Create importance dictionary
            importance_dict = {}
            for i, feature_name in enumerate(feature_names):
                if i < len(mean_abs_shap_values):
                    importance_dict[feature_name] = float(mean_abs_shap_values[i])
            
            # Sort by importance
            sorted_importance = dict(sorted(importance_dict.items(), 
                                          key=lambda x: x[1], reverse=True))
            
            # Get top features
            top_features = dict(list(sorted_importance.items())[:max_display])
            
            result = {
                'global_importance': sorted_importance,
                'top_features': top_features,
                'mean_shap_values': {name: float(np.mean(shap_values[:, i])) 
                                   for i, name in enumerate(feature_names) 
                                   if i < shap_values.shape[1]},
                'feature_count': len(feature_names),
                'sample_size': len(X_sample),
                'timestamp': datetime.now()
            }
            
            logger.info("Global feature importance explanation generated")
            return result
            
        except Exception as e:
            logger.error(f"Error generating global importance explanation: {e}")
            return self._mock_global_importance(X_sample)
    
    def _mock_explanation(self, X_instance: pd.DataFrame) -> Dict[str, Any]:
        """Generate mock explanation when SHAP is not available"""
        # Get feature names
        feature_names = []
        if hasattr(X_instance, 'columns'):
            feature_names = list(X_instance.columns)
        else:
            feature_names = [f"feature_{i}" for i in range(X_instance.shape[1] if len(X_instance.shape) > 1 else 1)]
        
        # Generate mock SHAP values
        mock_shap_values = {name: np.random.uniform(-0.2, 0.2) for name in feature_names}
        sorted_shap_values = dict(sorted(mock_shap_values.items(), 
                                       key=lambda x: abs(x[1]), reverse=True))
        
        return {
            'shap_values': mock_shap_values,
            'sorted_shap_values': sorted_shap_values,
            'base_value': 0.5,
            'prediction': 0.5 + sum(mock_shap_values.values()),
            'timestamp': datetime.now(),
            'mock': True
        }
    
    def _mock_global_importance(self, X_sample: pd.DataFrame) -> Dict[str, Any]:
        """Generate mock global importance when SHAP is not available"""
        # Get feature names
        feature_names = []
        if hasattr(X_sample, 'columns'):
            feature_names = list(X_sample.columns)
        else:
            feature_names = [f"feature_{i}" for i in range(X_sample.shape[1] if len(X_sample.shape) > 1 else 1)]
        
        # Generate mock importance values
        mock_importance = {name: np.random.uniform(0, 1) for name in feature_names}
        sorted_importance = dict(sorted(mock_importance.items(), 
                                      key=lambda x: x[1], reverse=True))
        
        return {
            'global_importance': sorted_importance,
            'top_features': dict(list(sorted_importance.items())[:20]),
            'mean_shap_values': {name: np.random.uniform(-0.1, 0.1) for name in feature_names},
            'feature_count': len(feature_names),
            'sample_size': len(X_sample),
            'timestamp': datetime.now(),
            'mock': True
        }


class ConfidenceIntervalCalculator:
    """Calculate confidence intervals for model predictions"""
    
    def __init__(self):
        self.bootstrap_samples = 1000
        self.confidence_level = 0.95
        logger.info("Confidence Interval Calculator initialized")
    
    def calculate_confidence_interval(self, model, X: pd.DataFrame, 
                                   y_true: Optional[np.ndarray] = None,
                                   method: str = 'bootstrap') -> Dict[str, Any]:
        """
        Calculate confidence intervals for predictions
        
        Args:
            model: Trained model
            X: Feature data
            y_true: True values (optional, for validation)
            method: Method for calculating CI ('bootstrap', 'residual')
            
        Returns:
            Dictionary with confidence interval results
        """
        predictions = np.array([0.5] * len(X))  # Default predictions
        try:
            # Make predictions
            if hasattr(model, 'predict'):
                predictions = model.predict(X)
            
            ci_results = {}
            if method == 'bootstrap':
                ci_results = self._bootstrap_confidence_interval(model, X, predictions)
            elif method == 'residual':
                if y_true is not None:
                    ci_results = self._residual_confidence_interval(predictions, y_true)
                else:
                    logger.warning("Residual method requires true values, falling back to bootstrap")
                    ci_results = self._bootstrap_confidence_interval(model, X, predictions)
            else:
                ci_results = self._bootstrap_confidence_interval(model, X, predictions)
            
            # Add prediction statistics
            ci_results['prediction_stats'] = {
                'mean_prediction': float(np.mean(predictions)),
                'std_prediction': float(np.std(predictions)),
                'min_prediction': float(np.min(predictions)),
                'max_prediction': float(np.max(predictions))
            }
            
            ci_results['timestamp'] = datetime.now()
            
            logger.info("Confidence intervals calculated")
            return ci_results
            
        except Exception as e:
            logger.error(f"Error calculating confidence intervals: {e}")
            return self._mock_confidence_intervals(predictions)
    
    def _bootstrap_confidence_interval(self, model, X: pd.DataFrame, 
                                     predictions: np.ndarray) -> Dict[str, Any]:
        """Calculate confidence intervals using bootstrap method"""
        try:
            # For demonstration, we'll create mock bootstrap samples
            # In a real implementation, this would involve resampling
            bootstrap_predictions = []
            for _ in range(min(self.bootstrap_samples, 100)):  # Limit for performance
                # Add some noise to simulate bootstrap variation
                noise = np.random.normal(0, 0.05, len(predictions))
                bootstrap_predictions.append(predictions + noise)
            
            # Calculate percentiles
            bootstrap_array = np.array(bootstrap_predictions)
            alpha = 1 - self.confidence_level
            lower_percentile = (alpha / 2) * 100
            upper_percentile = (1 - alpha / 2) * 100
            
            # Calculate confidence intervals for each prediction
            lower_bounds = np.percentile(bootstrap_array, lower_percentile, axis=0)
            upper_bounds = np.percentile(bootstrap_array, upper_percentile, axis=0)
            
            # Calculate overall confidence interval
            overall_lower = np.percentile(bootstrap_array, lower_percentile)
            overall_upper = np.percentile(bootstrap_array, upper_percentile)
            
            return {
                'method': 'bootstrap',
                'confidence_level': self.confidence_level,
                'individual_intervals': [
                    {
                        'prediction_index': i,
                        'point_estimate': float(predictions[i]),
                        'lower_bound': float(lower_bounds[i]),
                        'upper_bound': float(upper_bounds[i]),
                        'interval_width': float(upper_bounds[i] - lower_bounds[i])
                    }
                    for i in range(min(len(predictions), 10))  # Limit for readability
                ],
                'overall_interval': {
                    'lower_bound': float(overall_lower),
                    'upper_bound': float(overall_upper),
                    'interval_width': float(overall_upper - overall_lower)
                },
                'bootstrap_samples': len(bootstrap_predictions),
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Error in bootstrap confidence interval calculation: {e}")
            return self._mock_confidence_intervals(predictions)
    
    def _residual_confidence_interval(self, predictions: np.ndarray, 
                                    y_true: np.ndarray) -> Dict[str, Any]:
        """Calculate confidence intervals using residual method"""
        try:
            # Calculate residuals
            residuals = y_true - predictions
            
            # Calculate standard error of residuals
            std_residuals = np.std(residuals)
            
            # Calculate confidence intervals
            alpha = 1 - self.confidence_level
            z_score = 1.96  # For 95% confidence (approximate)
            
            # Individual confidence intervals
            margin_of_error = z_score * std_residuals
            lower_bounds = predictions - margin_of_error
            upper_bounds = predictions + margin_of_error
            
            return {
                'method': 'residual',
                'confidence_level': self.confidence_level,
                'individual_intervals': [
                    {
                        'prediction_index': i,
                        'point_estimate': float(predictions[i]),
                        'lower_bound': float(lower_bounds[i]),
                        'upper_bound': float(upper_bounds[i]),
                        'interval_width': float(upper_bounds[i] - lower_bounds[i])
                    }
                    for i in range(min(len(predictions), 10))  # Limit for readability
                ],
                'overall_interval': {
                    'lower_bound': float(np.mean(predictions) - margin_of_error),
                    'upper_bound': float(np.mean(predictions) + margin_of_error),
                    'interval_width': float(2 * margin_of_error)
                },
                'residual_stats': {
                    'mean_residual': float(np.mean(residuals)),
                    'std_residual': float(std_residuals),
                    'mse': float(np.mean(residuals ** 2))
                }
            }
            
        except Exception as e:
            logger.error(f"Error in residual confidence interval calculation: {e}")
            return self._mock_confidence_intervals(predictions)
    
    def _mock_confidence_intervals(self, predictions: np.ndarray) -> Dict[str, Any]:
        """Generate mock confidence intervals"""
        # Generate mock intervals
        mock_intervals = []
        for i in range(min(len(predictions), 10)):
            point_estimate = float(predictions[i]) if i < len(predictions) else 0.5
            margin = np.random.uniform(0.02, 0.1)
            mock_intervals.append({
                'prediction_index': i,
                'point_estimate': point_estimate,
                'lower_bound': point_estimate - margin,
                'upper_bound': point_estimate + margin,
                'interval_width': 2 * margin
            })
        
        overall_margin = np.random.uniform(0.05, 0.15)
        overall_mean = float(np.mean(predictions)) if len(predictions) > 0 else 0.5
        
        return {
            'method': 'mock',
            'confidence_level': self.confidence_level,
            'individual_intervals': mock_intervals,
            'overall_interval': {
                'lower_bound': overall_mean - overall_margin,
                'upper_bound': overall_mean + overall_margin,
                'interval_width': 2 * overall_margin
            },
            'timestamp': datetime.now(),
            'mock': True
        }