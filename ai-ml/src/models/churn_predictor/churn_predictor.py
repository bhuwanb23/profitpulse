"""
Main Orchestrator for Client Churn Prediction
Coordinates all components of the churn prediction system
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import asyncio
import warnings
warnings.filterwarnings('ignore')

# Import all components
from .data_preparation import ChurnDataPreparator, get_churn_data_preparator
from .feature_engineering import ChurnFeatureEngineer, get_churn_feature_engineer
from .models import (
    ChurnLogisticRegression, ChurnNeuralNetwork, 
    ChurnGradientBoosting, ChurnEnsembleModel,
    get_logistic_regression_model, get_neural_network_model,
    get_xgboost_model, get_random_forest_model, get_ensemble_model
)
from .training_pipeline import (
    ChurnTrainingPipeline, ChurnModelOptimizer,
    get_training_pipeline, get_model_optimizer,
    evaluate_churn_predictions
)
from .churn_prevention import (
    ChurnRiskScorer, ChurnRecommendationEngine, 
    ChurnEarlyWarningSystem, ChurnInterventionTracker,
    get_risk_scorer, get_recommendation_engine,
    get_early_warning_system, get_intervention_tracker
)

logger = logging.getLogger(__name__)


class ChurnPredictor:
    """Main orchestrator for client churn prediction system"""
    
    def __init__(self, db_path: str = "../../database/superhack.db"):
        """
        Initialize churn predictor
        
        Args:
            db_path: Path to database
        """
        self.db_path = db_path
        self.is_trained = False
        self.models = {}
        self.feature_columns = []
        
        # Initialize all components
        self.data_preparator = get_churn_data_preparator()
        self.feature_engineer = get_churn_feature_engineer()
        self.training_pipeline = get_training_pipeline()
        self.model_optimizer = get_model_optimizer()
        self.risk_scorer = get_risk_scorer()
        self.recommendation_engine = get_recommendation_engine()
        self.early_warning_system = get_early_warning_system()
        self.intervention_tracker = get_intervention_tracker()
        
        logger.info("Churn Predictor initialized")
    
    async def prepare_data(self, start_date: Optional[datetime] = None, 
                          end_date: Optional[datetime] = None) -> Dict[str, pd.DataFrame]:
        """
        Prepare all data for churn prediction
        
        Args:
            start_date: Start date for data collection
            end_date: End date for data collection
            
        Returns:
            Dictionary with all data components
        """
        try:
            logger.info("Preparing data for churn prediction...")
            
            # Collect all data
            data_preparator_instance = await self.data_preparator
            client_history = await data_preparator_instance.collect_client_history_data(start_date, end_date)
            interactions = await data_preparator_instance.collect_client_interactions(start_date, end_date)
            financial_data = await data_preparator_instance.collect_financial_metrics(start_date, end_date)
            service_data = await data_preparator_instance.collect_service_usage(start_date, end_date)
            
            # Create churn labels
            client_history = data_preparator_instance.create_churn_labels(client_history)
            
            data = {
                'client_history': client_history,
                'interactions': interactions,
                'financial_data': financial_data,
                'service_data': service_data
            }
            
            logger.info(f"Data preparation completed: {len(client_history)} clients")
            return data
            
        except Exception as e:
            logger.error(f"Error preparing data: {e}")
            return {}
    
    def engineer_features(self, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Engineer features for churn prediction
        
        Args:
            data: Dictionary with all data components
            
        Returns:
            DataFrame with engineered features
        """
        try:
            logger.info("Engineering features for churn prediction...")
            
            # Prepare features
            features = self.feature_engineer.prepare_features(
                data['client_history'],
                data['interactions'],
                data['financial_data'],
                data['service_data']
            )
            
            # Select important features
            target_series = features['churn'] if 'churn' in features.columns else pd.Series([0]*len(features))
            if isinstance(target_series, pd.DataFrame):
                target_series = target_series.iloc[:, 0]  # Convert DataFrame to Series
            selected_features = self.model_optimizer.select_features(
                features.drop(['client_id', 'churn'], axis=1, errors='ignore'),
                target_series
            )
            
            # Keep only selected features plus client_id and churn
            feature_columns = ['client_id', 'churn'] + selected_features
            features = features[feature_columns] if all(col in features.columns for col in feature_columns) else features
            
            self.feature_columns = list(features.columns)
            logger.info(f"Feature engineering completed: {len(features.columns)} features")
            # Ensure we return a DataFrame
            if not isinstance(features, pd.DataFrame):
                features = pd.DataFrame(features)
            return features
            
        except Exception as e:
            logger.error(f"Error engineering features: {e}")
            return pd.DataFrame()
    
    def train_models(self, features: pd.DataFrame) -> bool:
        """
        Train all churn prediction models
        
        Args:
            features: DataFrame with features
            
        Returns:
            Boolean indicating success
        """
        try:
            logger.info("Training churn prediction models...")
            
            if features.empty or 'churn' not in features.columns:
                logger.error("Invalid features data for training")
                return False
            
            # Prepare training data
            X = features.drop(['client_id', 'churn'], axis=1, errors='ignore')
            y = features['churn']
            
            # Handle class imbalance
            # Ensure y is a Series
            if isinstance(y, pd.DataFrame):
                y_series = y.iloc[:, 0]
            else:
                y_series = y
            X_balanced, y_balanced = self.training_pipeline.handle_class_imbalance(X, y_series, method='smote')
            
            # Create train-test split
            X_train, X_test, y_train, y_test = self.training_pipeline.create_train_test_split(
                X_balanced, y_balanced
            )
            
            # Initialize models
            models = {
                'logistic_regression': get_logistic_regression_model(),
                'neural_network': get_neural_network_model(),
                'xgboost': get_xgboost_model(),
                'random_forest': get_random_forest_model(),
                'ensemble': get_ensemble_model()
            }
            
            # Train all models
            training_results = {}
            for name, model in models.items():
                logger.info(f"Training {name}...")
                result = model.train(X_train, y_train)
                training_results[name] = result
                
                if result:
                    # Evaluate model
                    y_pred = model.predict(X_test)
                    y_proba = model.predict_proba(X_test)
                    # Convert to numpy arrays for evaluation
                    y_test_array = np.array(y_test)
                    y_pred_array = np.array(y_pred)
                    y_proba_array = np.array(y_proba)
                    metrics = evaluate_churn_predictions(y_test_array, y_pred_array, y_proba_array)
                    logger.info(f"{name} evaluation: {metrics}")
            
            self.models = models
            self.is_trained = any(training_results.values())
            
            if self.is_trained:
                logger.info("Model training completed successfully")
            else:
                logger.warning("Model training failed for all models")
            
            return self.is_trained
            
        except Exception as e:
            logger.error(f"Error training models: {e}")
            return False
    
    def predict_churn(self, features: pd.DataFrame) -> pd.DataFrame:
        """
        Predict churn for clients
        
        Args:
            features: DataFrame with features
            
        Returns:
            DataFrame with predictions
        """
        try:
            if not self.is_trained or not self.models:
                logger.warning("Models not trained, returning empty predictions")
                return pd.DataFrame()
            
            logger.info("Predicting churn for clients...")
            
            # Prepare data for prediction
            X = features.drop(['client_id', 'churn'], axis=1, errors='ignore')
            
            # Use ensemble model for predictions (or any trained model)
            ensemble_model = self.models.get('ensemble')
            if ensemble_model and ensemble_model.is_trained:
                predictions = ensemble_model.predict(X)
                probabilities = ensemble_model.predict_proba(X)
            else:
                # Fallback to first available trained model
                for model in self.models.values():
                    if hasattr(model, 'is_trained') and model.is_trained:
                        predictions = model.predict(X)
                        probabilities = model.predict_proba(X) if hasattr(model, 'predict_proba') else np.zeros(len(X))
                        break
                else:
                    logger.warning("No trained models available for prediction")
                    return pd.DataFrame()
            
            # Add predictions to features
            results = features.copy()
            results['churn_prediction'] = predictions
            results['churn_probability'] = probabilities
            
            logger.info(f"Churn prediction completed for {len(results)} clients")
            return results
            
        except Exception as e:
            logger.error(f"Error predicting churn: {e}")
            return pd.DataFrame()
    
    def generate_risk_scores(self, predictions: pd.DataFrame) -> pd.DataFrame:
        """
        Generate risk scores for clients
        
        Args:
            predictions: DataFrame with predictions
            
        Returns:
            DataFrame with risk scores
        """
        try:
            logger.info("Generating risk scores...")
            
            # Calculate risk scores
            risk_scores = self.risk_scorer.calculate_risk_score(predictions)
            
            logger.info("Risk scoring completed")
            return risk_scores
            
        except Exception as e:
            logger.error(f"Error generating risk scores: {e}")
            return predictions
    
    def generate_recommendations(self, risk_scores: pd.DataFrame) -> pd.DataFrame:
        """
        Generate retention recommendations for clients
        
        Args:
            risk_scores: DataFrame with risk scores
            
        Returns:
            DataFrame with recommendations
        """
        try:
            logger.info("Generating retention recommendations...")
            
            # Generate recommendations
            recommendations = self.recommendation_engine.generate_recommendations(risk_scores)
            
            logger.info("Recommendation generation completed")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return risk_scores
    
    def identify_high_risk_clients(self, recommendations: pd.DataFrame) -> pd.DataFrame:
        """
        Identify high-risk clients who need immediate attention
        
        Args:
            recommendations: DataFrame with recommendations
            
        Returns:
            DataFrame with high-risk clients
        """
        try:
            logger.info("Identifying high-risk clients...")
            
            # Identify high-risk clients
            high_risk_clients = self.early_warning_system.identify_high_risk_clients(recommendations)
            
            logger.info(f"Identified {len(high_risk_clients)} high-risk clients")
            return high_risk_clients
            
        except Exception as e:
            logger.error(f"Error identifying high-risk clients: {e}")
            return pd.DataFrame()
    
    def generate_alerts(self, high_risk_clients: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Generate alerts for high-risk clients
        
        Args:
            high_risk_clients: DataFrame with high-risk clients
            
        Returns:
            List of alert dictionaries
        """
        try:
            logger.info("Generating alerts for high-risk clients...")
            
            # Generate alerts
            alerts = self.early_warning_system.generate_alerts(high_risk_clients)
            
            # Log interventions
            for alert in alerts:
                self.intervention_tracker.log_intervention(
                    client_id=alert['client_id'],
                    intervention_type='churn_prevention',
                    recommendations=alert['recommendations'],
                    predicted_risk=alert['risk_score']
                )
            
            logger.info(f"Generated {len(alerts)} alerts")
            return alerts
            
        except Exception as e:
            logger.error(f"Error generating alerts: {e}")
            return []
    
    async def run_full_pipeline(self, start_date: Optional[datetime] = None, 
                               end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Run the complete churn prediction pipeline
        
        Args:
            start_date: Start date for data collection
            end_date: End date for data collection
            
        Returns:
            Dictionary with all results
        """
        try:
            logger.info("Running full churn prediction pipeline...")
            
            # Step 1: Prepare data
            data = await self.prepare_data(start_date, end_date)
            if not data:
                logger.error("Failed to prepare data")
                return {}
            
            # Step 2: Engineer features
            features = self.engineer_features(data)
            if features.empty:
                logger.error("Failed to engineer features")
                return {}
            
            # Step 3: Train models (if not already trained)
            if not self.is_trained:
                training_success = self.train_models(features)
                if not training_success:
                    logger.warning("Model training failed, continuing with prediction using default models")
            
            # Step 4: Predict churn
            predictions = self.predict_churn(features)
            if predictions.empty:
                logger.error("Failed to predict churn")
                return {}
            
            # Step 5: Generate risk scores
            risk_scores = self.generate_risk_scores(predictions)
            
            # Step 6: Generate recommendations
            recommendations = self.generate_recommendations(risk_scores)
            
            # Step 7: Identify high-risk clients
            high_risk_clients = self.identify_high_risk_clients(recommendations)
            
            # Step 8: Generate alerts
            alerts = self.generate_alerts(high_risk_clients)
            
            results = {
                'data': data,
                'features': features,
                'predictions': predictions,
                'risk_scores': risk_scores,
                'recommendations': recommendations,
                'high_risk_clients': high_risk_clients,
                'alerts': alerts
            }
            
            logger.info("Full pipeline completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"Error running full pipeline: {e}")
            return {}


# Global instance for easy access
churn_predictor_instance = None


async def get_churn_predictor() -> ChurnPredictor:
    """Get singleton churn predictor instance"""
    global churn_predictor_instance
    if churn_predictor_instance is None:
        churn_predictor_instance = ChurnPredictor()
    return churn_predictor_instance


# Example usage function
async def run_churn_prediction_example():
    """Example of how to use the churn predictor"""
    try:
        # Get predictor instance
        predictor = await get_churn_predictor()
        
        # Run full pipeline
        results = await predictor.run_full_pipeline()
        
        if results:
            print("Churn prediction completed successfully!")
            print(f"Processed {len(results.get('predictions', []))} clients")
            print(f"Identified {len(results.get('high_risk_clients', []))} high-risk clients")
            print(f"Generated {len(results.get('alerts', []))} alerts")
            
            # Show sample results
            if 'high_risk_clients' in results and not results['high_risk_clients'].empty:
                print("\nSample High-Risk Clients:")
                print(results['high_risk_clients'][['client_id', 'client_name', 'churn_risk_score', 'risk_category']].head())
                
            if 'alerts' in results and results['alerts']:
                print("\nSample Alerts:")
                for alert in results['alerts'][:3]:
                    print(f"Client: {alert['client_name']} (Risk: {alert['risk_score']:.2f})")
                    print(f"Recommendations: {alert['recommendations'][:100]}...")
                    print("---")
        else:
            print("Churn prediction failed!")
            
    except Exception as e:
        logger.error(f"Error in example: {e}")


if __name__ == "__main__":
    # Run example if script is executed directly
    asyncio.run(run_churn_prediction_example())