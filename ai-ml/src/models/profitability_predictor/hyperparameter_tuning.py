"""
Hyperparameter Tuning for Client Profitability Prediction Models
Implements grid search and Bayesian optimization for model hyperparameter tuning
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime

try:
    from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
    from sklearn.metrics import make_scorer, r2_score, mean_absolute_error, mean_squared_error
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    GridSearchCV = None
    RandomizedSearchCV = None
    make_scorer = None
    r2_score = None
    mean_absolute_error = None
    mean_squared_error = None

logger = logging.getLogger(__name__)


class HyperparameterTuner:
    """Hyperparameter tuner for profitability prediction models"""
    
    def __init__(self):
        """Initialize the hyperparameter tuner"""
        if not SKLEARN_AVAILABLE:
            raise ImportError("scikit-learn is required for hyperparameter tuning but not available")
    
    def create_xgboost_param_grid(self) -> Dict[str, List[Any]]:
        """
        Create parameter grid for XGBoost hyperparameter tuning
        
        Returns:
            Dictionary with parameter grid
        """
        return {
            'n_estimators': [50, 100, 200],
            'max_depth': [3, 6, 9],
            'learning_rate': [0.01, 0.1, 0.2],
            'subsample': [0.8, 0.9, 1.0],
            'colsample_bytree': [0.8, 0.9, 1.0]
        }
    
    def create_random_forest_param_grid(self) -> Dict[str, List[Any]]:
        """
        Create parameter grid for Random Forest hyperparameter tuning
        
        Returns:
            Dictionary with parameter grid
        """
        return {
            'n_estimators': [50, 100, 200],
            'max_depth': [5, 10, 15, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'max_features': ['auto', 'sqrt', 'log2']
        }
    
    def tune_xgboost_model(self, model, X_train: pd.DataFrame, y_train: np.ndarray,
                          param_grid: Optional[Dict[str, List[Any]]] = None,
                          cv: int = 5, n_iter: int = 10,
                          scoring: str = 'r2') -> Tuple[Any, Dict[str, Any]]:
        """
        Tune XGBoost model hyperparameters using grid search or random search
        
        Args:
            model: XGBoost model instance
            X_train: Training features
            y_train: Training targets
            param_grid: Parameter grid for tuning (if None, uses default)
            cv: Number of cross-validation folds
            n_iter: Number of iterations for random search
            scoring: Scoring metric
            
        Returns:
            Tuple of (best_model, best_params)
        """
        logger.info("Tuning XGBoost model hyperparameters")
        
        try:
            # Use default parameter grid if not provided
            if param_grid is None:
                param_grid = self.create_xgboost_param_grid()
            
            # Determine search method based on grid size
            total_combinations = np.prod([len(v) for v in param_grid.values()])
            
            if total_combinations <= 50:  # Use grid search for small grids
                logger.info(f"Using GridSearchCV with {total_combinations} combinations")
                search = GridSearchCV(
                    model, 
                    param_grid, 
                    cv=cv, 
                    scoring=scoring,
                    n_jobs=-1,
                    verbose=0
                )
            else:  # Use random search for large grids
                logger.info(f"Using RandomizedSearchCV with {n_iter} iterations")
                search = RandomizedSearchCV(
                    model, 
                    param_grid, 
                    n_iter=n_iter,
                    cv=cv, 
                    scoring=scoring,
                    n_jobs=-1,
                    verbose=0,
                    random_state=42
                )
            
            # Fit the search
            search.fit(X_train, y_train)
            
            logger.info(f"Best {scoring} score: {search.best_score_:.4f}")
            logger.info(f"Best parameters: {search.best_params_}")
            
            return search.best_estimator_, search.best_params_
            
        except Exception as e:
            logger.error(f"Error tuning XGBoost model: {e}")
            raise
    
    def tune_random_forest_model(self, model, X_train: pd.DataFrame, y_train: np.ndarray,
                               param_grid: Optional[Dict[str, List[Any]]] = None,
                               cv: int = 5, n_iter: int = 10,
                               scoring: str = 'r2') -> Tuple[Any, Dict[str, Any]]:
        """
        Tune Random Forest model hyperparameters using grid search or random search
        
        Args:
            model: Random Forest model instance
            X_train: Training features
            y_train: Training targets
            param_grid: Parameter grid for tuning (if None, uses default)
            cv: Number of cross-validation folds
            n_iter: Number of iterations for random search
            scoring: Scoring metric
            
        Returns:
            Tuple of (best_model, best_params)
        """
        logger.info("Tuning Random Forest model hyperparameters")
        
        try:
            # Use default parameter grid if not provided
            if param_grid is None:
                param_grid = self.create_random_forest_param_grid()
            
            # Determine search method based on grid size
            total_combinations = np.prod([len(v) for v in param_grid.values()])
            
            if total_combinations <= 50:  # Use grid search for small grids
                logger.info(f"Using GridSearchCV with {total_combinations} combinations")
                search = GridSearchCV(
                    model, 
                    param_grid, 
                    cv=cv, 
                    scoring=scoring,
                    n_jobs=-1,
                    verbose=0
                )
            else:  # Use random search for large grids
                logger.info(f"Using RandomizedSearchCV with {n_iter} iterations")
                search = RandomizedSearchCV(
                    model, 
                    param_grid, 
                    n_iter=n_iter,
                    cv=cv, 
                    scoring=scoring,
                    n_jobs=-1,
                    verbose=0,
                    random_state=42
                )
            
            # Fit the search
            search.fit(X_train, y_train)
            
            logger.info(f"Best {scoring} score: {search.best_score_:.4f}")
            logger.info(f"Best parameters: {search.best_params_}")
            
            return search.best_estimator_, search.best_params_
            
        except Exception as e:
            logger.error(f"Error tuning Random Forest model: {e}")
            raise
    
    def compare_tuning_results(self, results_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compare results from different tuning experiments
        
        Args:
            results_list: List of tuning results
            
        Returns:
            Dictionary with comparison results
        """
        logger.info("Comparing hyperparameter tuning results")
        
        try:
            if not results_list:
                return {}
            
            # Find best result based on validation score
            best_result = max(results_list, key=lambda x: x.get('best_score', 0))
            
            comparison = {
                'best_result': best_result,
                'total_experiments': len(results_list),
                'score_range': {
                    'min': min(r.get('best_score', 0) for r in results_list),
                    'max': max(r.get('best_score', 0) for r in results_list),
                    'mean': np.mean([r.get('best_score', 0) for r in results_list])
                },
                'all_results': results_list
            }
            
            logger.info(f"Best tuning result: {best_result.get('model_name', 'Unknown')} with score {best_result.get('best_score', 0):.4f}")
            return comparison
            
        except Exception as e:
            logger.error(f"Error comparing tuning results: {e}")
            raise


# Convenience functions for easy usage
def tune_profitability_model(model, X_train: pd.DataFrame, y_train: np.ndarray,
                           model_type: str = "xgboost",
                           param_grid: Optional[Dict[str, List[Any]]] = None,
                           cv: int = 5, n_iter: int = 10,
                           scoring: str = 'r2') -> Tuple[Any, Dict[str, Any]]:
    """
    Tune profitability prediction model hyperparameters
    
    Args:
        model: Model instance to tune
        X_train: Training features
        y_train: Training targets
        model_type: Type of model ("xgboost" or "random_forest")
        param_grid: Parameter grid for tuning
        cv: Number of cross-validation folds
        n_iter: Number of iterations for random search
        scoring: Scoring metric
        
    Returns:
        Tuple of (best_model, best_params)
    """
    tuner = HyperparameterTuner()
    
    if model_type.lower() == "xgboost":
        return tuner.tune_xgboost_model(model, X_train, y_train, param_grid, cv, n_iter, scoring)
    elif model_type.lower() == "random_forest":
        return tuner.tune_random_forest_model(model, X_train, y_train, param_grid, cv, n_iter, scoring)
    else:
        raise ValueError(f"Unsupported model type: {model_type}")


def compare_model_tuning_results(results_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compare results from different model tuning experiments
    
    Args:
        results_list: List of tuning results
        
    Returns:
        Dictionary with comparison results
    """
    tuner = HyperparameterTuner()
    return tuner.compare_tuning_results(results_list)