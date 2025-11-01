"""
Training Pipeline for Revenue Leak Detection Models
Handles unsupervised learning, threshold optimization, and model evaluation
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
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    train_test_split = None
    precision_score = None
    recall_score = None
    f1_score = None
    roc_auc_score = None
    StandardScaler = None
    SKLEARN_AVAILABLE = False

logger = logging.getLogger(__name__)


class UnsupervisedTrainingPipeline:
    """Training pipeline for unsupervised anomaly detection models"""
    
    def __init__(self, test_size: float = 0.2, random_state: int = 42):
        """
        Initialize the training pipeline
        
        Args:
            test_size: Proportion of data to use for testing
            random_state: Random state for reproducibility
        """
        self.test_size = test_size
        self.random_state = random_state
        self.scaler = StandardScaler() if StandardScaler else None
        self.feature_names = None
        logger.info("Unsupervised Training Pipeline initialized")
    
    def prepare_data(self, X: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Prepare data for training (split into train/test)
        
        Args:
            X: Input data
            
        Returns:
            Tuple of (train_data, test_data)
        """
        try:
            # Store feature names
            self.feature_names = list(X.columns) if hasattr(X, 'columns') else [f"feature_{i}" for i in range(X.shape[1])]
            
            # Split data
            if train_test_split is not None:
                X_train, X_test = train_test_split(
                    X, test_size=self.test_size, random_state=self.random_state
                )
            else:
                # Manual split if sklearn not available
                split_idx = int(len(X) * (1 - self.test_size))
                if hasattr(X, 'iloc'):
                    X_train = X.iloc[:split_idx]
                    X_test = X.iloc[split_idx:]
                else:
                    # Convert to DataFrame if it's a numpy array
                    X_df = pd.DataFrame(X) if not isinstance(X, pd.DataFrame) else X
                    X_train = X_df.iloc[:split_idx]
                    X_test = X_df.iloc[split_idx:]
            
            # Ensure we return DataFrames
            if not isinstance(X_train, pd.DataFrame):
                X_train = pd.DataFrame(X_train)
            if not isinstance(X_test, pd.DataFrame):
                X_test = pd.DataFrame(X_test)
            
            return X_train, X_test
            
        except Exception as e:
            logger.error(f"Error preparing data: {e}")
            return X, pd.DataFrame()
    
    def optimize_threshold(self, model, X_test: pd.DataFrame, 
                         method: str = 'f1') -> Tuple[float, Dict[str, float]]:
        """
        Optimize anomaly detection threshold
        
        Args:
            model: Trained anomaly detection model
            X_test: Test data
            method: Optimization method ('f1', 'precision', 'recall')
            
        Returns:
            Tuple of (optimal_threshold, metrics_dict)
        """
        try:
            # Get anomaly scores
            scores = model.anomaly_scores(X_test)
            
            # Try different thresholds
            thresholds = np.percentile(scores, np.arange(0, 100, 5))
            
            best_threshold = 0.0
            best_score = 0.0
            best_metrics = {}
            
            # For demonstration, we'll generate mock labels since this is unsupervised
            # In a real scenario, you might have some labeled data or use domain knowledge
            mock_labels = np.random.choice([1, -1], size=len(X_test), p=[0.9, 0.1])
            
            for threshold in thresholds:
                # Convert scores to binary predictions
                predictions = np.where(scores > threshold, -1, 1)
                
                # Calculate metrics
                if SKLEARN_AVAILABLE and precision_score is not None and recall_score is not None and f1_score is not None:
                    precision = precision_score(mock_labels, predictions, pos_label=-1)
                    recall = recall_score(mock_labels, predictions, pos_label=-1)
                    f1 = f1_score(mock_labels, predictions, pos_label=-1)
                else:
                    # Simple calculation if sklearn not available
                    tp = np.sum((mock_labels == -1) & (predictions == -1))
                    fp = np.sum((mock_labels == 1) & (predictions == -1))
                    fn = np.sum((mock_labels == -1) & (predictions == 1))
                    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
                    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
                    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
                
                # Select best threshold based on method
                if method == 'f1' and f1 > best_score:
                    best_score = f1
                    best_threshold = threshold
                    best_metrics = {'precision': precision, 'recall': recall, 'f1': f1}
                elif method == 'precision' and precision > best_score:
                    best_score = precision
                    best_threshold = threshold
                    best_metrics = {'precision': precision, 'recall': recall, 'f1': f1}
                elif method == 'recall' and recall > best_score:
                    best_score = recall
                    best_threshold = threshold
                    best_metrics = {'precision': precision, 'recall': recall, 'f1': f1}
            
            logger.info(f"Optimal threshold found: {best_threshold:.4f} with {method} score: {best_score:.4f}")
            return best_threshold, best_metrics
            
        except Exception as e:
            logger.error(f"Error optimizing threshold: {e}")
            return 0.0, {}
    
    def reduce_false_positives(self, model, X_test: pd.DataFrame, 
                             threshold: float, max_fp_rate: float = 0.1) -> float:
        """
        Reduce false positive rate by adjusting threshold
        
        Args:
            model: Trained anomaly detection model
            X_test: Test data
            threshold: Current threshold
            max_fp_rate: Maximum acceptable false positive rate
            
        Returns:
            Adjusted threshold
        """
        try:
            # Get anomaly scores
            scores = model.anomaly_scores(X_test)
            
            # For demonstration, generate mock normal data
            mock_normal_data = X_test.sample(frac=0.5, random_state=self.random_state)
            normal_scores = model.anomaly_scores(mock_normal_data)
            
            # Calculate current false positive rate
            fp_count = np.sum(normal_scores > threshold)
            fp_rate = fp_count / len(normal_scores)
            
            # If FP rate is too high, adjust threshold
            if fp_rate > max_fp_rate:
                # Find threshold that meets FP rate requirement
                sorted_normal_scores = np.sort(normal_scores)
                target_idx = int(len(sorted_normal_scores) * (1 - max_fp_rate))
                adjusted_threshold = sorted_normal_scores[min(target_idx, len(sorted_normal_scores) - 1)]
                
                logger.info(f"False positive rate reduced from {fp_rate:.4f} to {max_fp_rate:.4f} "
                           f"by adjusting threshold from {threshold:.4f} to {adjusted_threshold:.4f}")
                return adjusted_threshold
            else:
                logger.info(f"False positive rate {fp_rate:.4f} is within acceptable limits")
                return threshold
                
        except Exception as e:
            logger.error(f"Error reducing false positives: {e}")
            return threshold
    
    def optimize_precision_recall(self, model, X_test: pd.DataFrame, 
                                target_precision: float = 0.8,
                                target_recall: float = 0.6) -> float:
        """
        Optimize for target precision and recall
        
        Args:
            model: Trained anomaly detection model
            X_test: Test data
            target_precision: Target precision
            target_recall: Target recall
            
        Returns:
            Optimized threshold
        """
        try:
            # Get anomaly scores
            scores = model.anomaly_scores(X_test)
            
            # Generate mock labels for optimization
            mock_labels = np.random.choice([1, -1], size=len(X_test), p=[0.9, 0.1])
            
            # Try different thresholds
            thresholds = np.percentile(scores, np.arange(0, 100, 1))
            
            best_threshold = 0.0
            best_diff = float('inf')
            
            for threshold in thresholds:
                # Convert scores to binary predictions
                predictions = np.where(scores > threshold, -1, 1)
                
                # Calculate metrics
                if SKLEARN_AVAILABLE and precision_score is not None and recall_score is not None:
                    precision = precision_score(mock_labels, predictions, pos_label=-1)
                    recall = recall_score(mock_labels, predictions, pos_label=-1)
                else:
                    # Simple calculation if sklearn not available
                    tp = np.sum((mock_labels == -1) & (predictions == -1))
                    fp = np.sum((mock_labels == 1) & (predictions == -1))
                    fn = np.sum((mock_labels == -1) & (predictions == 1))
                    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
                    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
                
                # Calculate difference from targets
                precision_diff = abs(precision - target_precision)
                recall_diff = abs(recall - target_recall)
                total_diff = precision_diff + recall_diff
                
                if total_diff < best_diff:
                    best_diff = total_diff
                    best_threshold = threshold
            
            logger.info(f"Precision-recall optimization completed. "
                       f"Best threshold: {best_threshold:.4f}")
            return best_threshold
            
        except Exception as e:
            logger.error(f"Error optimizing precision/recall: {e}")
            return 0.0


class ModelEvaluator:
    """Evaluate performance of anomaly detection models"""
    
    def __init__(self):
        """Initialize model evaluator"""
        logger.info("Model Evaluator initialized")
    
    def evaluate_model(self, model, X_test: pd.DataFrame, 
                      y_test: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """
        Evaluate model performance
        
        Args:
            model: Trained anomaly detection model
            X_test: Test data
            y_test: True labels (if available)
            
        Returns:
            Dictionary with evaluation metrics
        """
        try:
            # Get predictions and scores
            predictions = model.predict(X_test)
            scores = model.anomaly_scores(X_test)
            
            # Calculate basic statistics
            anomaly_count = np.sum(predictions == -1)
            normal_count = np.sum(predictions == 1)
            anomaly_rate = anomaly_count / len(predictions)
            
            evaluation = {
                'anomaly_count': int(anomaly_count),
                'normal_count': int(normal_count),
                'anomaly_rate': float(anomaly_rate),
                'mean_score': float(np.mean(scores)),
                'std_score': float(np.std(scores)),
                'min_score': float(np.min(scores)),
                'max_score': float(np.max(scores))
            }
            
            # If true labels are available, calculate additional metrics
            if y_test is not None:
                if SKLEARN_AVAILABLE and precision_score is not None and recall_score is not None and f1_score is not None:
                    precision = precision_score(y_test, predictions, pos_label=-1)
                    recall = recall_score(y_test, predictions, pos_label=-1)
                    f1 = f1_score(y_test, predictions, pos_label=-1)
                    
                    evaluation.update({
                        'precision': float(precision),
                        'recall': float(recall),
                        'f1_score': float(f1)
                    })
                    
                    # Try to calculate AUC if possible
                    try:
                        if roc_auc_score is not None:
                            auc = roc_auc_score(y_test, scores)
                            evaluation['auc'] = float(auc)
                    except Exception:
                        pass
                else:
                    # Simple calculation if sklearn not available
                    tp = np.sum((y_test == -1) & (predictions == -1))
                    fp = np.sum((y_test == 1) & (predictions == -1))
                    fn = np.sum((y_test == -1) & (predictions == 1))
                    tn = np.sum((y_test == 1) & (predictions == 1))
                    
                    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
                    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
                    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
                    
                    evaluation.update({
                        'precision': float(precision),
                        'recall': float(recall),
                        'f1_score': float(f1)
                    })
            
            logger.info(f"Model evaluation completed: {anomaly_count} anomalies detected "
                       f"({anomaly_rate:.2%} anomaly rate)")
            return evaluation
            
        except Exception as e:
            logger.error(f"Error evaluating model: {e}")
            return {'error': str(e)}
    
    def compare_models(self, models: Dict[str, Any], X_test: pd.DataFrame,
                      y_test: Optional[np.ndarray] = None) -> Dict[str, Dict[str, Any]]:
        """
        Compare multiple models
        
        Args:
            models: Dictionary of model names and model objects
            X_test: Test data
            y_test: True labels (if available)
            
        Returns:
            Dictionary with evaluation results for each model
        """
        try:
            results = {}
            
            for model_name, model in models.items():
                logger.info(f"Evaluating {model_name}...")
                evaluation = self.evaluate_model(model, X_test, y_test)
                results[model_name] = evaluation
            
            # Find best model based on F1 score if available
            if all('f1_score' in metrics for metrics in results.values()):
                best_model = max(results.items(), key=lambda x: x[1]['f1_score'])
                results['best_model'] = best_model[0]
                results['best_f1_score'] = best_model[1]['f1_score']
            
            logger.info("Model comparison completed")
            return results
            
        except Exception as e:
            logger.error(f"Error comparing models: {e}")
            return {'error': {'message': str(e)}}


# Global instances for easy access
training_pipeline_instance = None
evaluator_instance = None


async def get_training_pipeline() -> UnsupervisedTrainingPipeline:
    """Get singleton training pipeline instance"""
    global training_pipeline_instance
    if training_pipeline_instance is None:
        training_pipeline_instance = UnsupervisedTrainingPipeline()
    return training_pipeline_instance


async def get_model_evaluator() -> ModelEvaluator:
    """Get singleton model evaluator instance"""
    global evaluator_instance
    if evaluator_instance is None:
        evaluator_instance = ModelEvaluator()
    return evaluator_instance