"""
Cross-Validation for Client Profitability Prediction Models
Implements k-fold and time series cross-validation for model evaluation
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime

try:
    from sklearn.model_selection import KFold, StratifiedKFold, TimeSeriesSplit, cross_val_score
    from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    KFold = None
    StratifiedKFold = None
    TimeSeriesSplit = None
    cross_val_score = None
    r2_score = None
    mean_absolute_error = None
    mean_squared_error = None

logger = logging.getLogger(__name__)


class CrossValidator:
    """Cross-validator for profitability prediction models"""
    
    def __init__(self):
        """Initialize the cross-validator"""
        if not SKLEARN_AVAILABLE:
            raise ImportError("scikit-learn is required for cross-validation but not available")
    
    def k_fold_cv(self, model, X: pd.DataFrame, y: np.ndarray, 
                  k: int = 5, scoring: str = 'r2') -> Dict[str, Any]:
        """
        Perform k-fold cross-validation
        
        Args:
            model: Model to evaluate
            X: Features
            y: Targets
            k: Number of folds
            scoring: Scoring metric
            
        Returns:
            Dictionary with CV results
        """
        logger.info(f"Performing {k}-fold cross-validation")
        
        try:
            # Create k-fold cross-validator
            kf = KFold(n_splits=k, shuffle=True, random_state=42)
            
            # Perform cross-validation
            cv_scores = cross_val_score(model, X, y, cv=kf, scoring=scoring)
            
            results = {
                'cv_method': 'k-fold',
                'n_folds': k,
                'scores': cv_scores.tolist(),
                'mean_score': np.mean(cv_scores),
                'std_score': np.std(cv_scores),
                'min_score': np.min(cv_scores),
                'max_score': np.max(cv_scores),
                'scoring_metric': scoring
            }
            
            logger.info(f"CV Results - Mean {scoring}: {results['mean_score']:.4f} (+/- {results['std_score']:.4f})")
            return results
            
        except Exception as e:
            logger.error(f"Error in k-fold cross-validation: {e}")
            raise
    
    def stratified_cv(self, model, X: pd.DataFrame, y: np.ndarray,
                     k: int = 5, scoring: str = 'r2') -> Dict[str, Any]:
        """
        Perform stratified cross-validation
        
        Args:
            model: Model to evaluate
            X: Features
            y: Targets (will be discretized for stratification)
            k: Number of folds
            scoring: Scoring metric
            
        Returns:
            Dictionary with CV results
        """
        logger.info(f"Performing stratified {k}-fold cross-validation")
        
        try:
            # Discretize target variable for stratification
            y_discrete = pd.qcut(y, q=min(10, len(y)//2), labels=False, duplicates='drop')
            
            # Create stratified k-fold cross-validator
            skf = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)
            
            # Perform cross-validation
            cv_scores = cross_val_score(model, X, y, cv=skf, scoring=scoring)
            
            results = {
                'cv_method': 'stratified',
                'n_folds': k,
                'scores': cv_scores.tolist(),
                'mean_score': np.mean(cv_scores),
                'std_score': np.std(cv_scores),
                'min_score': np.min(cv_scores),
                'max_score': np.max(cv_scores),
                'scoring_metric': scoring
            }
            
            logger.info(f"CV Results - Mean {scoring}: {results['mean_score']:.4f} (+/- {results['std_score']:.4f})")
            return results
            
        except Exception as e:
            logger.error(f"Error in stratified cross-validation: {e}")
            raise
    
    def time_series_cv(self, model, X: pd.DataFrame, y: np.ndarray,
                      k: int = 5, scoring: str = 'r2') -> Dict[str, Any]:
        """
        Perform time series cross-validation
        
        Args:
            model: Model to evaluate
            X: Features (assumed to be ordered by time)
            y: Targets
            k: Number of folds
            scoring: Scoring metric
            
        Returns:
            Dictionary with CV results
        """
        logger.info(f"Performing time series {k}-fold cross-validation")
        
        try:
            # Create time series cross-validator
            tscv = TimeSeriesSplit(n_splits=k)
            
            # Perform cross-validation
            cv_scores = cross_val_score(model, X, y, cv=tscv, scoring=scoring)
            
            results = {
                'cv_method': 'time_series',
                'n_folds': k,
                'scores': cv_scores.tolist(),
                'mean_score': np.mean(cv_scores),
                'std_score': np.std(cv_scores),
                'min_score': np.min(cv_scores),
                'max_score': np.max(cv_scores),
                'scoring_metric': scoring
            }
            
            logger.info(f"CV Results - Mean {scoring}: {results['mean_score']:.4f} (+/- {results['std_score']:.4f})")
            return results
            
        except Exception as e:
            logger.error(f"Error in time series cross-validation: {e}")
            raise
    
    def compare_cv_methods(self, cv_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compare results from different cross-validation methods
        
        Args:
            cv_results: List of CV results from different methods
            
        Returns:
            Dictionary with comparison results
        """
        logger.info("Comparing cross-validation methods")
        
        try:
            if not cv_results:
                return {}
            
            # Calculate overall statistics
            all_scores = []
            method_scores = {}
            
            for result in cv_results:
                method = result.get('cv_method', 'unknown')
                scores = result.get('scores', [])
                all_scores.extend(scores)
                method_scores[method] = scores
            
            comparison = {
                'best_method': max(cv_results, key=lambda x: x.get('mean_score', 0)),
                'all_methods': cv_results,
                'overall_statistics': {
                    'mean_score': np.mean(all_scores),
                    'std_score': np.std(all_scores),
                    'min_score': np.min(all_scores),
                    'max_score': np.max(all_scores)
                },
                'method_comparison': {}
            }
            
            # Calculate per-method statistics
            for method, scores in method_scores.items():
                comparison['method_comparison'][method] = {
                    'mean_score': np.mean(scores),
                    'std_score': np.std(scores),
                    'min_score': np.min(scores),
                    'max_score': np.max(scores)
                }
            
            best_method = comparison['best_method']['cv_method']
            best_score = comparison['best_method']['mean_score']
            logger.info(f"Best CV method: {best_method} with mean score {best_score:.4f}")
            return comparison
            
        except Exception as e:
            logger.error(f"Error comparing CV methods: {e}")
            raise


# Convenience functions for easy usage
def perform_cross_validation(model, X: pd.DataFrame, y: np.ndarray,
                           cv_method: str = 'k-fold', k: int = 5,
                           scoring: str = 'r2') -> Dict[str, Any]:
    """
    Perform cross-validation on a profitability prediction model
    
    Args:
        model: Model to evaluate
        X: Features
        y: Targets
        cv_method: Cross-validation method ('k-fold', 'stratified', 'time_series')
        k: Number of folds
        scoring: Scoring metric
        
    Returns:
        Dictionary with CV results
    """
    validator = CrossValidator()
    
    if cv_method == 'k-fold':
        return validator.k_fold_cv(model, X, y, k, scoring)
    elif cv_method == 'stratified':
        return validator.stratified_cv(model, X, y, k, scoring)
    elif cv_method == 'time_series':
        return validator.time_series_cv(model, X, y, k, scoring)
    else:
        raise ValueError(f"Unsupported CV method: {cv_method}")


def compare_cross_validation_methods(cv_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compare results from different cross-validation methods
    
    Args:
        cv_results: List of CV results from different methods
        
    Returns:
        Dictionary with comparison results
    """
    validator = CrossValidator()
    return validator.compare_cv_methods(cv_results)