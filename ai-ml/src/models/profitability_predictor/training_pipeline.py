"""
Training Pipeline for Client Profitability Prediction Models
Implements end-to-end training pipeline for model development
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
import os

# Import our modules
from src.models.profitability_predictor.historical_data_collector import HistoricalDataCollector
from src.models.profitability_predictor.feature_engineering import ProfitabilityFeatureEngineer
from src.models.profitability_predictor.data_splitter import ProfitabilityDataSplitter
from src.models.profitability_predictor.data_quality import ProfitabilityDataQualityAssessor
from src.models.profitability_predictor.xgboost_model import XGBoostProfitabilityModel
from src.models.profitability_predictor.random_forest_model import RandomForestProfitabilityModel
from src.models.profitability_predictor.hyperparameter_tuning import HyperparameterTuner
from src.models.profitability_predictor.cross_validation import CrossValidator, perform_cross_validation
from src.models.profitability_predictor.model_evaluation import ProfitabilityModelEvaluator

logger = logging.getLogger(__name__)


class ProfitabilityTrainingPipeline:
    """End-to-end training pipeline for profitability prediction models"""
    
    def __init__(self, db_path: str = "../../database/superhack.db"):
        """
        Initialize the training pipeline
        
        Args:
            db_path: Path to the SQLite database
        """
        self.db_path = db_path
        self.data_collector = HistoricalDataCollector(db_path)
        self.feature_engineer = ProfitabilityFeatureEngineer(db_path)
        self.data_splitter = ProfitabilityDataSplitter()
        self.data_assessor = ProfitabilityDataQualityAssessor()
        self.xgboost_model = None
        self.random_forest_model = None
        self.hyperparameter_tuner = HyperparameterTuner()
        self.cross_validator = CrossValidator()
        self.model_evaluator = ProfitabilityModelEvaluator()
        
    def collect_and_prepare_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
        """
        Collect and prepare data for model training
        
        Returns:
            Tuple of (train_df, validation_df, test_df, data_quality_report)
        """
        logger.info("Collecting and preparing data for training")
        
        try:
            # 1. Collect historical financial data
            financial_data = self.data_collector.aggregate_financial_metrics()
            logger.info(f"Collected financial data for {len(financial_data)} clients")
            
            # 2. Engineer features
            features_df = self.feature_engineer.engineer_features(financial_data)
            logger.info(f"Engineered {len(features_df.columns)} features")
            
            # 3. Assess data quality
            quality_report = self.data_assessor.assess_data_quality(features_df)
            logger.info("Data quality assessment completed")
            
            # 4. Split dataset
            train_df, validation_df, test_df = self.data_splitter.split_dataset(
                features_df, 
                target_column='profit_margin',
                split_method='stratified',
                test_size=0.15, 
                validation_size=0.15,
                random_state=42
            )
            logger.info(f"Dataset split - Train: {len(train_df)}, Validation: {len(validation_df)}, Test: {len(test_df)}")
            
            return train_df, validation_df, test_df, quality_report
            
        except Exception as e:
            logger.error(f"Error in data collection and preparation: {e}")
            raise
    
    def train_models(self, train_df: pd.DataFrame, validation_df: pd.DataFrame,
                    target_column: str = 'profit_margin') -> Dict[str, Any]:
        """
        Train multiple models with hyperparameter tuning
        
        Args:
            train_df: Training data
            validation_df: Validation data
            target_column: Target variable column name
            
        Returns:
            Dictionary with trained models and results
        """
        logger.info("Training models with hyperparameter tuning")
        
        try:
            # Prepare features and targets
            X_train = train_df.drop(columns=[target_column, 'id', 'name'], errors='ignore')
            y_train = train_df[target_column].values
            X_val = validation_df.drop(columns=[target_column, 'id', 'name'], errors='ignore')
            y_val = validation_df[target_column].values
            
            # Convert to numpy arrays
            y_train = np.array(y_train)
            y_val = np.array(y_val)
            
            # Handle missing values
            X_train = X_train.fillna(0)
            X_val = X_val.fillna(0)
            
            results = {}
            
            # 1. Train XGBoost model
            logger.info("Training XGBoost model")
            xgb_model = XGBoostProfitabilityModel()
            
            # Tune hyperparameters
            tuned_xgb, best_xgb_params = self.hyperparameter_tuner.tune_xgboost_model(
                xgb_model.model, X_train, y_train
            )
            
            # Set the tuned model
            xgb_model.model = tuned_xgb
            xgb_model.is_trained = True
            xgb_model.feature_names = X_train.columns.tolist()
            xgb_model.training_timestamp = datetime.now()
            
            # Evaluate XGBoost model
            xgb_predictions = xgb_model.predict(validation_df)
            xgb_metrics = self.model_evaluator.calculate_all_metrics(y_val, xgb_predictions)
            
            results['xgboost'] = {
                'model': xgb_model,
                'best_params': best_xgb_params,
                'metrics': xgb_metrics,
                'predictions': xgb_predictions
            }
            
            # 2. Train Random Forest model
            logger.info("Training Random Forest model")
            rf_model = RandomForestProfitabilityModel()
            
            # Tune hyperparameters
            tuned_rf, best_rf_params = self.hyperparameter_tuner.tune_random_forest_model(
                rf_model.model, X_train, y_train
            )
            
            # Set the tuned model
            rf_model.model = tuned_rf
            rf_model.is_trained = True
            rf_model.feature_names = X_train.columns.tolist()
            rf_model.training_timestamp = datetime.now()
            
            # Evaluate Random Forest model
            rf_predictions = rf_model.predict(validation_df)
            rf_metrics = self.model_evaluator.calculate_all_metrics(y_val, rf_predictions)
            
            results['random_forest'] = {
                'model': rf_model,
                'best_params': best_rf_params,
                'metrics': rf_metrics,
                'predictions': rf_predictions
            }
            
            # 3. Select best model based on R² score
            best_model_name = 'xgboost' if xgb_metrics['r2'] > rf_metrics['r2'] else 'random_forest'
            results['best_model'] = best_model_name
            results['best_model_instance'] = results[best_model_name]['model']
            
            logger.info(f"Model training completed - Best model: {best_model_name}")
            return results
            
        except Exception as e:
            logger.error(f"Error in model training: {e}")
            raise
    
    def cross_validate_models(self, train_df: pd.DataFrame, 
                            target_column: str = 'profit_margin',
                            cv_method: str = 'k-fold', k: int = 5) -> Dict[str, Any]:
        """
        Perform cross-validation on trained models
        
        Args:
            train_df: Training data
            target_column: Target variable column name
            cv_method: Cross-validation method
            k: Number of folds
            
        Returns:
            Dictionary with cross-validation results
        """
        logger.info(f"Performing {cv_method} cross-validation")
        
        try:
            # Prepare features and targets
            X_train = train_df.drop(columns=[target_column, 'id', 'name'], errors='ignore')
            y_train = train_df[target_column].values
            
            # Convert to numpy arrays
            y_train = np.array(y_train)
            
            # Handle missing values
            X_train = X_train.fillna(0)
            
            cv_results = {}
            
            # Perform cross-validation for both models
            for model_name, model_class in [('xgboost', XGBoostProfitabilityModel), 
                                          ('random_forest', RandomForestProfitabilityModel)]:
                logger.info(f"Cross-validating {model_name} model")
                model = model_class()
                cv_result = perform_cross_validation(
                    model.model, X_train, y_train, cv_method, k
                )
                cv_results[model_name] = cv_result
            
            return cv_results
            
        except Exception as e:
            logger.error(f"Error in cross-validation: {e}")
            raise
    
    def evaluate_final_models(self, test_df: pd.DataFrame, trained_models: Dict[str, Any],
                            target_column: str = 'profit_margin') -> Dict[str, Any]:
        """
        Evaluate final trained models on test set
        
        Args:
            test_df: Test data
            trained_models: Dictionary with trained models
            target_column: Target variable column name
            
        Returns:
            Dictionary with final evaluation results
        """
        logger.info("Evaluating final models on test set")
        
        try:
            # Prepare test data
            X_test = test_df.drop(columns=[target_column, 'id', 'name'], errors='ignore')
            y_test = test_df[target_column].values
            
            # Convert to numpy arrays
            y_test = np.array(y_test)
            
            # Handle missing values
            X_test = X_test.fillna(0)
            
            final_results = {}
            
            # Evaluate each model
            for model_name in ['xgboost', 'random_forest']:
                if model_name in trained_models:
                    model = trained_models[model_name]['model']
                    predictions = model.predict(test_df)
                    metrics = self.model_evaluator.calculate_all_metrics(y_test, predictions)
                    evaluation = self.model_evaluator.evaluate_model_performance(
                        y_test, predictions, model_name.upper()
                    )
                    
                    final_results[model_name] = {
                        'metrics': metrics,
                        'evaluation': evaluation,
                        'predictions': predictions
                    }
            
            # Select overall best model
            if 'xgboost' in final_results and 'random_forest' in final_results:
                xgboost_r2 = final_results['xgboost']['metrics']['r2']
                rf_r2 = final_results['random_forest']['metrics']['r2']
                best_model = 'xgboost' if xgboost_r2 > rf_r2 else 'random_forest'
                final_results['best_model'] = best_model
            
            logger.info("Final model evaluation completed")
            return final_results
            
        except Exception as e:
            logger.error(f"Error in final model evaluation: {e}")
            raise
    
    def save_models(self, trained_models: Dict[str, Any], 
                   output_dir: str = "./trained_models") -> Dict[str, str]:
        """
        Save trained models to disk
        
        Args:
            trained_models: Dictionary with trained models
            output_dir: Directory to save models
            
        Returns:
            Dictionary with saved model paths
        """
        logger.info(f"Saving models to {output_dir}")
        
        try:
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            saved_paths = {}
            
            # Save each model
            for model_name in ['xgboost', 'random_forest']:
                if model_name in trained_models:
                    model = trained_models[model_name]['model']
                    filepath = os.path.join(output_dir, f"{model_name}_model.pkl")
                    model.save_model(filepath)
                    saved_paths[model_name] = filepath
                    logger.info(f"Saved {model_name} model to {filepath}")
            
            return saved_paths
            
        except Exception as e:
            logger.error(f"Error saving models: {e}")
            raise
    
    def run_complete_pipeline(self, save_models: bool = True,
                            output_dir: str = "./trained_models") -> Dict[str, Any]:
        """
        Run the complete training pipeline
        
        Args:
            save_models: Whether to save trained models
            output_dir: Directory to save models
            
        Returns:
            Dictionary with complete pipeline results
        """
        logger.info("Running complete profitability prediction training pipeline")
        
        try:
            # 1. Collect and prepare data
            train_df, validation_df, test_df, data_quality_report = self.collect_and_prepare_data()
            
            # 2. Train models
            trained_models = self.train_models(train_df, validation_df)
            
            # 3. Cross-validate models
            cv_results = self.cross_validate_models(train_df)
            
            # 4. Evaluate final models
            final_evaluation = self.evaluate_final_models(test_df, trained_models)
            
            # 5. Save models if requested
            saved_paths = {}
            if save_models:
                saved_paths = self.save_models(trained_models, output_dir)
            
            # 6. Compile complete results
            pipeline_results = {
                'data_preparation': {
                    'train_samples': len(train_df),
                    'validation_samples': len(validation_df),
                    'test_samples': len(test_df),
                    'data_quality_report': data_quality_report
                },
                'model_training': trained_models,
                'cross_validation': cv_results,
                'final_evaluation': final_evaluation,
                'saved_models': saved_paths,
                'pipeline_timestamp': datetime.now().isoformat()
            }
            
            logger.info("Complete training pipeline finished successfully")
            return pipeline_results
            
        except Exception as e:
            logger.error(f"Error in complete training pipeline: {e}")
            raise


# Convenience function for easy usage
def run_profitability_training_pipeline(db_path: str = "../../database/superhack.db",
                                      save_models: bool = True,
                                      output_dir: str = "./trained_models") -> Dict[str, Any]:
    """
    Run the complete profitability prediction training pipeline
    
    Args:
        db_path: Path to the SQLite database
        save_models: Whether to save trained models
        output_dir: Directory to save models
        
    Returns:
        Dictionary with complete pipeline results
    """
    pipeline = ProfitabilityTrainingPipeline(db_path)
    return pipeline.run_complete_pipeline(save_models, output_dir)