"""
Training Pipeline for Client Churn Prediction
Handles model training, validation, and optimization
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.utils.class_weight import compute_class_weight
import warnings
warnings.filterwarnings('ignore')

# Conditional imports for data processing
try:
    from sklearn.model_selection import GridSearchCV
    from imblearn.over_sampling import SMOTE
    from imblearn.under_sampling import RandomUnderSampler
    IMBLEARN_AVAILABLE = True
except ImportError:
    GridSearchCV = None
    SMOTE = None
    RandomUnderSampler = None
    IMBLEARN_AVAILABLE = False

logger = logging.getLogger(__name__)


class ChurnTrainingPipeline:
    """Training pipeline for churn prediction models"""
    
    def __init__(self, test_size: float = 0.2, random_state: int = 42):
        """
        Initialize training pipeline
        
        Args:
            test_size: Proportion of data to use for testing
            random_state: Random state for reproducibility
        """
        self.test_size = test_size
        self.random_state = random_state
        logger.info("Churn Training Pipeline initialized")
    
    def handle_class_imbalance(self, X: pd.DataFrame, y: pd.Series, 
                              method: str = 'smote') -> Tuple[pd.DataFrame, pd.Series]:
        """
        Handle class imbalance in training data
        
        Args:
            X: Feature data
            y: Target labels
            method: Method to handle imbalance ('smote', 'undersample', 'class_weight')
            
        Returns:
            Tuple of balanced X and y
        """
        try:
            if not IMBLEARN_AVAILABLE:
                logger.warning("imbalanced-learn not available, returning original data")
                return X, y
            
            if method == 'smote' and SMOTE is not None:
                # Apply SMOTE oversampling
                smote = SMOTE(random_state=self.random_state)
                X_balanced, y_balanced = smote.fit_resample(X, y)
                logger.info(f"Applied SMOTE: {len(X)} -> {len(X_balanced)} samples")
                return X_balanced, y_balanced
                
            elif method == 'undersample' and RandomUnderSampler is not None:
                # Apply random undersampling
                undersampler = RandomUnderSampler(random_state=self.random_state)
                X_balanced, y_balanced = undersampler.fit_resample(X, y)
                logger.info(f"Applied undersampling: {len(X)} -> {len(X_balanced)} samples")
                return X_balanced, y_balanced
                
            else:
                logger.warning(f"Unknown method or unavailable sampler: {method}")
                return X, y
                
        except Exception as e:
            logger.error(f"Error handling class imbalance: {e}")
            return X, y
    
    def create_train_test_split(self, features: pd.DataFrame, 
                              target: pd.Series) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """
        Create train-test split for model training
        
        Args:
            features: DataFrame with features
            target: Series with target labels
            
        Returns:
            Tuple of (X_train, X_test, y_train, y_test)
        """
        try:
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                features, target, 
                test_size=self.test_size, 
                random_state=self.random_state,
                stratify=target  # Ensure balanced split
            )
            
            logger.info(f"Created train-test split: {len(X_train)} train, {len(X_test)} test samples")
            return X_train, X_test, y_train, y_test
            
        except Exception as e:
            logger.error(f"Error creating train-test split: {e}")
            # Fallback to simple split without stratification
            X_train, X_test, y_train, y_test = train_test_split(
                features, target, 
                test_size=self.test_size, 
                random_state=self.random_state
            )
            return X_train, X_test, y_train, y_test
    
    def compute_class_weights(self, y: pd.Series) -> Dict[int, float]:
        """
        Compute class weights for handling imbalanced data
        
        Args:
            y: Target labels
            
        Returns:
            Dictionary with class weights
        """
        try:
            classes = np.unique(y)
            weights = compute_class_weight('balanced', classes=classes, y=y)
            class_weights = dict(zip(classes, weights))
            logger.info(f"Computed class weights: {class_weights}")
            return class_weights
            
        except Exception as e:
            logger.error(f"Error computing class weights: {e}")
            return {0: 1.0, 1: 1.0}
    
    def cross_validate_model(self, model: Any, X: pd.DataFrame, y: pd.Series, 
                           cv_folds: int = 5) -> Dict[str, float]:
        """
        Perform cross-validation on a model
        
        Args:
            model: Model to validate
            X: Feature data
            y: Target labels
            cv_folds: Number of cross-validation folds
            
        Returns:
            Dictionary with validation metrics
        """
        try:
            # Create stratified k-fold
            skf = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=self.random_state)
            
            # Perform cross-validation
            cv_scores = cross_val_score(model, X, y, cv=skf, scoring='roc_auc')
            
            metrics = {
                'cv_mean_auc': float(cv_scores.mean()),
                'cv_std_auc': float(cv_scores.std()),
                'cv_scores': []  # Initialize as empty list
            }
            
            logger.info(f"Cross-validation results: {metrics['cv_mean_auc']:.4f} ± {metrics['cv_std_auc']:.4f}")
            return metrics
            
        except Exception as e:
            logger.error(f"Error performing cross-validation: {e}")
            return {
                'cv_mean_auc': 0.0,
                'cv_std_auc': 0.0,
                'cv_scores': []
            }


class ChurnModelOptimizer:
    """Optimizer for churn prediction models"""
    
    def __init__(self, random_state: int = 42):
        """
        Initialize model optimizer
        
        Args:
            random_state: Random state for reproducibility
        """
        self.random_state = random_state
        logger.info("Churn Model Optimizer initialized")
    
    def optimize_hyperparameters(self, model: Any, param_grid: Dict[str, List[Any]], 
                               X: pd.DataFrame, y: pd.Series, 
                               cv_folds: int = 3) -> Dict[str, Any]:
        """
        Optimize model hyperparameters using grid search
        
        Args:
            model: Model to optimize
            param_grid: Parameter grid for search
            X: Feature data
            y: Target labels
            cv_folds: Number of cross-validation folds
            
        Returns:
            Dictionary with best parameters and score
        """
        try:
            if GridSearchCV is None:
                logger.warning("GridSearchCV not available, returning default parameters")
                return {
                    'best_params': {},
                    'best_score': 0.0,
                    'best_estimator': model
                }
            
            # Perform grid search
            grid_search = GridSearchCV(
                model, param_grid, 
                cv=cv_folds, 
                scoring='roc_auc',
                n_jobs=-1,
                verbose=0
            )
            
            grid_search.fit(X, y)
            
            results = {
                'best_params': grid_search.best_params_,
                'best_score': grid_search.best_score_,
                'best_estimator': grid_search.best_estimator_
            }
            
            logger.info(f"Best parameters: {results['best_params']}")
            logger.info(f"Best CV score: {results['best_score']:.4f}")
            return results
            
        except Exception as e:
            logger.error(f"Error optimizing hyperparameters: {e}")
            return {
                'best_params': {},
                'best_score': 0.0,
                'best_estimator': model
            }
    
    def select_features(self, X: pd.DataFrame, y: pd.Series, 
                       method: str = 'correlation', 
                       threshold: float = 0.01) -> List[str]:
        """
        Select important features for churn prediction
        
        Args:
            X: Feature data
            y: Target labels
            method: Feature selection method ('correlation', 'variance')
            threshold: Threshold for feature selection
            
        Returns:
            List of selected feature names
        """
        try:
            if method == 'correlation':
                # Select features based on correlation with target
                correlations = X.corrwith(y).abs()
                # Get feature names where correlation is above threshold
                selected_features = []
                for col in X.columns:
                    if col in correlations and correlations[col] > threshold:
                        selected_features.append(str(col))
                logger.info(f"Selected {len(selected_features)} features based on correlation")
                return selected_features
                
            elif method == 'variance':
                # Select features based on variance
                variances = X.var()
                # Get feature names where variance is above threshold
                selected_features = []
                for col in X.columns:
                    try:
                        variance_value = variances[col]
                        if variance_value > threshold:
                            selected_features.append(str(col))
                    except (KeyError, TypeError):
                        # Skip if there's an issue accessing the variance
                        continue
                logger.info(f"Selected {len(selected_features)} features based on variance")
                return selected_features
                
            else:
                logger.warning(f"Unknown feature selection method: {method}")
                return [str(col) for col in X.columns]
                
        except Exception as e:
            logger.error(f"Error selecting features: {e}")
            return [str(col) for col in X.columns]


# Model evaluation utilities
def evaluate_churn_predictions(y_true: np.ndarray, y_pred: np.ndarray, 
                             y_proba: Optional[np.ndarray] = None) -> Dict[str, float]:
    """
    Evaluate churn prediction performance
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        y_proba: Predicted probabilities (optional)
        
    Returns:
        Dictionary with evaluation metrics
    """
    try:
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
        
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
        logger.error(f"Error evaluating predictions: {e}")
        return {
            'accuracy': 0.0,
            'precision': 0.0,
            'recall': 0.0,
            'f1_score': 0.0,
            'auc': 0.0
        }


# Global instances for easy access
training_pipeline_instance = None
model_optimizer_instance = None


def get_training_pipeline() -> ChurnTrainingPipeline:
    """Get singleton training pipeline instance"""
    global training_pipeline_instance
    if training_pipeline_instance is None:
        training_pipeline_instance = ChurnTrainingPipeline()
    return training_pipeline_instance


def get_model_optimizer() -> ChurnModelOptimizer:
    """Get singleton model optimizer instance"""
    global model_optimizer_instance
    if model_optimizer_instance is None:
        model_optimizer_instance = ChurnModelOptimizer()
    return model_optimizer_instance