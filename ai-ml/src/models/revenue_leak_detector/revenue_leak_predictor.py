"""
Main Revenue Leak Predictor
Orchestrates all components of the revenue leak detection system
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime, timedelta
import warnings
import asyncio
warnings.filterwarnings('ignore')

# Import all the components we've created
from .data_preparation import RevenueLeakDataPreparator, get_data_preparator
from .anomaly_models import (
    IsolationForestModel, AutoencoderModel, DBSCANModel, 
    OneClassSVMModel, EnsembleAnomalyDetector,
    get_isolation_forest_model, get_autoencoder_model,
    get_dbscan_model, get_one_class_svm_model, get_ensemble_model
)
from .training_pipeline import (
    UnsupervisedTrainingPipeline, ModelEvaluator,
    get_training_pipeline, get_model_evaluator
)
from .recovery_system import (
    LeakClassifier, RecoveryAmountEstimator, RecommendationEngine,
    get_leak_classifier, get_recovery_estimator, get_recommendation_engine
)
from .alert_system import (
    AlertGenerator, RecoveryTracker,
    get_alert_generator, get_recovery_tracker
)

logger = logging.getLogger(__name__)


class RevenueLeakPredictor:
    """Main orchestrator for revenue leak detection"""
    
    def __init__(self, db_path: str = "../../database/superhack.db"):
        """
        Initialize the revenue leak predictor
        
        Args:
            db_path: Path to database
        """
        self.db_path = db_path
        self.data_preparator = None
        self.anomaly_models = {}
        self.training_pipeline = None
        self.evaluator = None
        self.leak_classifier = None
        self.recovery_estimator = None
        self.recommendation_engine = None
        self.alert_generator = None
        self.recovery_tracker = None
        self.is_initialized = False
        logger.info("Revenue Leak Predictor initialized")
    
    async def initialize(self):
        """Initialize all components"""
        try:
            # Initialize data preparator
            self.data_preparator = await get_data_preparator()
            
            # Initialize anomaly detection models
            self.anomaly_models['isolation_forest'] = await get_isolation_forest_model()
            self.anomaly_models['autoencoder'] = await get_autoencoder_model()
            self.anomaly_models['dbscan'] = await get_dbscan_model()
            self.anomaly_models['one_class_svm'] = await get_one_class_svm_model()
            self.anomaly_models['ensemble'] = await get_ensemble_model()
            
            # Initialize training pipeline components
            self.training_pipeline = await get_training_pipeline()
            self.evaluator = await get_model_evaluator()
            
            # Initialize recovery system components
            self.leak_classifier = await get_leak_classifier()
            self.recovery_estimator = await get_recovery_estimator()
            self.recommendation_engine = await get_recommendation_engine()
            
            # Initialize alert system components
            self.alert_generator = await get_alert_generator()
            self.recovery_tracker = await get_recovery_tracker()
            
            self.is_initialized = True
            logger.info("Revenue Leak Predictor initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing Revenue Leak Predictor: {e}")
            raise
    
    async def detect_revenue_leaks(self, start_date: Optional[datetime] = None, 
                                 end_date: Optional[datetime] = None,
                                 client_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Detect revenue leaks in the specified time period
        
        Args:
            start_date: Start date for analysis
            end_date: End date for analysis
            client_ids: Specific client IDs to analyze (None for all clients)
            
        Returns:
            Dictionary with detection results
        """
        try:
            if not self.is_initialized:
                await self.initialize()
            
            if start_date is None:
                start_date = datetime.now() - timedelta(days=90)
            if end_date is None:
                end_date = datetime.now()
            
            # Step 1: Collect and prepare data
            logger.info("Collecting invoice data...")
            if self.data_preparator is not None:
                invoice_data = await self.data_preparator.collect_invoice_data(start_date, end_date)
                
                logger.info("Collecting time log data...")
                time_log_data = await self.data_preparator.collect_time_log_data(start_date, end_date)
                
                logger.info("Collecting service delivery data...")
                service_data = await self.data_preparator.collect_service_delivery_data(start_date, end_date)
            else:
                logger.error("Data preparator not initialized")
                return {
                    'status': 'error',
                    'message': 'Data preparator not initialized',
                    'timestamp': datetime.now()
                }
            
            # Step 2: Prepare features for anomaly detection
            logger.info("Preparing features for anomaly detection...")
            if self.data_preparator is not None:
                features = self.data_preparator.prepare_features(invoice_data, time_log_data, service_data)
            else:
                features = pd.DataFrame()
            
            if client_ids:
                features = features[features['client_id'].isin(client_ids)]
            
            if features.empty:
                logger.warning("No data available for analysis")
                return {
                    'status': 'no_data',
                    'message': 'No data available for the specified period',
                    'timestamp': datetime.now()
                }
            
            # Step 3: Train anomaly detection models
            logger.info("Training anomaly detection models...")
            if self.training_pipeline is not None and not features.empty:
                if isinstance(features, pd.DataFrame):
                    X_train, X_test = self.training_pipeline.prepare_data(features)
                else:
                    X_train, X_test = pd.DataFrame(), pd.DataFrame()
            else:
                X_train, X_test = pd.DataFrame(), pd.DataFrame()
            
            # Train ensemble model (which trains all individual models)
            ensemble_model = None
            if 'ensemble' in self.anomaly_models and not X_train.empty:
                ensemble_model = self.anomaly_models['ensemble']
                training_success = ensemble_model.train(X_train)
            else:
                training_success = False
            
            if not training_success:
                logger.warning("Failed to train ensemble model")
                return {
                    'status': 'training_failed',
                    'message': 'Failed to train anomaly detection models',
                    'timestamp': datetime.now()
                }
            
            # Step 4: Detect anomalies
            logger.info("Detecting anomalies...")
            predictions = ensemble_model.predict(X_test) if ensemble_model is not None else np.ones(len(X_test))
            anomaly_scores = ensemble_model.anomaly_scores(X_test) if ensemble_model is not None else np.zeros(len(X_test))
            
            # Add predictions and scores to features
            X_test_with_predictions = X_test.copy()
            X_test_with_predictions['anomaly_prediction'] = predictions
            X_test_with_predictions['anomaly_score'] = anomaly_scores
            
            # Filter to only anomalies (predictions == -1)
            anomalies = X_test_with_predictions[X_test_with_predictions['anomaly_prediction'] == -1] if not X_test_with_predictions.empty else pd.DataFrame()
            
            # Step 5: Classify leaks
            logger.info("Classifying detected leaks...")
            if self.leak_classifier is not None and not anomalies.empty:
                if isinstance(anomalies, pd.DataFrame) and isinstance(features, pd.DataFrame):
                    classified_leaks = self.leak_classifier.classify_leaks(anomalies, features)
                else:
                    classified_leaks = pd.DataFrame()
            else:
                classified_leaks = pd.DataFrame()
            
            # Step 6: Estimate recovery amounts
            logger.info("Estimating recovery amounts...")
            if self.recovery_estimator is not None and not classified_leaks.empty:
                if isinstance(classified_leaks, pd.DataFrame) and isinstance(features, pd.DataFrame):
                    recovery_estimates = self.recovery_estimator.estimate_recovery(classified_leaks, features)
                else:
                    recovery_estimates = pd.DataFrame()
            else:
                recovery_estimates = pd.DataFrame()
            
            # Step 7: Generate recommendations
            logger.info("Generating recommendations...")
            if self.recommendation_engine is not None and not classified_leaks.empty:
                if isinstance(classified_leaks, pd.DataFrame) and isinstance(recovery_estimates, pd.DataFrame):
                    recommendations = self.recommendation_engine.generate_recommendations(
                        classified_leaks, recovery_estimates
                    )
                else:
                    recommendations = []
            else:
                recommendations = []
            
            # Step 8: Generate alerts
            logger.info("Generating alerts...")
            if self.alert_generator is not None and not classified_leaks.empty:
                if isinstance(classified_leaks, pd.DataFrame) and isinstance(recovery_estimates, pd.DataFrame):
                    alerts = self.alert_generator.generate_alerts(classified_leaks, recovery_estimates)
                else:
                    alerts = []
            else:
                alerts = []
            
            # Step 9: Compile results
            results = {
                'status': 'success',
                'total_records_analyzed': len(X_test),
                'anomalies_detected': len(anomalies),
                'leaks_classified': len(classified_leaks),
                'alerts_generated': len(alerts),
                'total_potential_loss': float(anomalies['revenue_leak_score'].sum()) if 'revenue_leak_score' in anomalies.columns else 0.0,
                'anomalies': anomalies.to_dict('records') if isinstance(anomalies, pd.DataFrame) and not anomalies.empty else [],
                'classified_leaks': classified_leaks.to_dict('records') if isinstance(classified_leaks, pd.DataFrame) and not classified_leaks.empty else [],
                'recovery_estimates': recovery_estimates.to_dict('records') if isinstance(recovery_estimates, pd.DataFrame) and not recovery_estimates.empty else [],
                'recommendations': recommendations,
                'alerts': alerts,
                'model_performance': self.evaluator.evaluate_model(ensemble_model, X_test) if self.evaluator is not None and ensemble_model is not None else {},
                'timestamp': datetime.now()
            }
            
            logger.info(f"Revenue leak detection completed: {len(anomalies)} anomalies detected")
            return results
            
        except Exception as e:
            logger.error(f"Error detecting revenue leaks: {e}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now()
            }
    
    async def get_client_leak_summary(self, client_id: str) -> Dict[str, Any]:
        """
        Get revenue leak summary for a specific client
        
        Args:
            client_id: Client ID to analyze
            
        Returns:
            Dictionary with client leak summary
        """
        try:
            if not self.is_initialized:
                await self.initialize()
            
            # Get alerts for this client
            if self.alert_generator is not None:
                client_alerts = self.alert_generator.get_alerts_by_client(client_id)
            else:
                client_alerts = []
            
            # Get recovery records for this client
            if self.recovery_tracker is not None:
                recovery_summary = self.recovery_tracker.get_recovery_summary(client_id)
            else:
                recovery_summary = {}
            
            # Get recommendations for this client
            client_recommendations = []
            for alert in client_alerts:
                leak_id = alert.get('leak_id', '')
                # In a real implementation, we would link alerts to recommendations
                # For now, we'll just note that recommendations exist
            
            summary = {
                'client_id': client_id,
                'total_alerts': len(client_alerts),
                'critical_alerts': len([a for a in client_alerts if a.get('alert_level') == 'critical']),
                'high_alerts': len([a for a in client_alerts if a.get('alert_level') == 'high']),
                'total_recovery_actions': recovery_summary.get('total_actions', 0),
                'total_amount_recovered': recovery_summary.get('total_amount_recovered', 0.0),
                'average_recovery_per_action': recovery_summary.get('average_recovery_per_action', 0.0),
                'alerts': client_alerts,
                'recovery_summary': recovery_summary,
                'timestamp': datetime.now()
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting client leak summary for {client_id}: {e}")
            return {
                'client_id': client_id,
                'error': str(e),
                'timestamp': datetime.now()
            }
    
    async def record_recovery_action(self, leak_id: str, client_id: str, 
                                   action_taken: str, amount_recovered: float = 0.0,
                                   action_owner: str = "Unknown") -> Dict[str, Any]:
        """
        Record a recovery action taken for a leak
        
        Args:
            leak_id: ID of the leak
            client_id: ID of the client
            action_taken: Description of action taken
            amount_recovered: Amount recovered (if any)
            action_owner: Who took the action
            
        Returns:
            Dictionary with recording result
        """
        try:
            if not self.is_initialized:
                await self.initialize()
            
            record_id = ""
            if self.recovery_tracker is not None:
                record_id = self.recovery_tracker.record_recovery_action(
                    leak_id, client_id, action_taken, amount_recovered, action_owner
                )
            
            if record_id:
                # Update alert status if it exists
                if self.alert_generator is not None:
                    self.alert_generator.update_alert_status(leak_id, 'resolved', action_owner)
                
                return {
                    'status': 'success',
                    'record_id': record_id,
                    'message': f"Recovery action recorded successfully for leak {leak_id}",
                    'timestamp': datetime.now()
                }
            else:
                return {
                    'status': 'error',
                    'message': "Failed to record recovery action",
                    'timestamp': datetime.now()
                }
                
        except Exception as e:
            logger.error(f"Error recording recovery action: {e}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now()
            }
    
    async def generate_periodic_report(self, period_days: int = 30) -> Dict[str, Any]:
        """
        Generate a periodic revenue leak detection report
        
        Args:
            period_days: Number of days to include in report
            
        Returns:
            Dictionary with report data
        """
        try:
            if not self.is_initialized:
                await self.initialize()
            
            # Detect revenue leaks for the period
            end_date = datetime.now()
            start_date = end_date - timedelta(days=period_days)
            
            detection_results = await self.detect_revenue_leaks(start_date, end_date)
            
            # Get recovery report
            if self.recovery_tracker is not None:
                recovery_report = self.recovery_tracker.generate_recovery_report(period_days)
            else:
                recovery_report = {}
            
            # Compile comprehensive report
            report = {
                'report_period_days': period_days,
                'period_start': start_date,
                'period_end': end_date,
                'detection_results': detection_results,
                'recovery_report': recovery_report,
                'generated_at': datetime.now()
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating periodic report: {e}")
            return {
                'status': 'error',
                'message': str(e),
                'generated_at': datetime.now()
            }


# Global instance for easy access
predictor_instance = None


async def get_revenue_leak_predictor() -> RevenueLeakPredictor:
    """Get singleton revenue leak predictor instance"""
    global predictor_instance
    if predictor_instance is None:
        predictor_instance = RevenueLeakPredictor()
        await predictor_instance.initialize()
    return predictor_instance


# Convenience functions for common operations
async def detect_revenue_leaks(start_date: Optional[datetime] = None, 
                             end_date: Optional[datetime] = None,
                             client_ids: Optional[List[str]] = None) -> Dict[str, Any]:
    """Convenience function to detect revenue leaks"""
    predictor = await get_revenue_leak_predictor()
    return await predictor.detect_revenue_leaks(start_date, end_date, client_ids)


async def get_client_leak_summary(client_id: str) -> Dict[str, Any]:
    """Convenience function to get client leak summary"""
    predictor = await get_revenue_leak_predictor()
    return await predictor.get_client_leak_summary(client_id)


async def record_recovery_action(leak_id: str, client_id: str, 
                               action_taken: str, amount_recovered: float = 0.0,
                               action_owner: str = "Unknown") -> Dict[str, Any]:
    """Convenience function to record recovery action"""
    predictor = await get_revenue_leak_predictor()
    return await predictor.record_recovery_action(
        leak_id, client_id, action_taken, amount_recovered, action_owner
    )


async def generate_periodic_report(period_days: int = 30) -> Dict[str, Any]:
    """Convenience function to generate periodic report"""
    predictor = await get_revenue_leak_predictor()
    return await predictor.generate_periodic_report(period_days)