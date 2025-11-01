"""
Main Anomaly Detector Orchestrator for Anomaly Detection System
Coordinates all components of the anomaly detection system
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import asyncio
import json
import warnings
warnings.filterwarnings('ignore')

from .anomaly_models import (
    get_one_class_svm_model, 
    get_dbscan_model, 
    get_statistical_detector, 
    get_ml_detector,
    get_ensemble_detector
)
from .data_processor import StreamDataProcessor, DataQualityMonitor, FeatureExtractor, DataProcessorConfig
from .streaming_service import AnomalyStreamingService, StreamingConfig
from .severity_classifier import (
    AnomalySeverity, 
    get_severity_classifier, 
    get_impact_assessor
)
from .alert_system import (
    get_alert_generator, 
    get_escalation_system,
    console_alert_handler,
    file_alert_handler
)

logger = logging.getLogger(__name__)


class AnomalyDetectorOrchestrator:
    """Main orchestrator for the anomaly detection system"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the anomaly detector orchestrator
        
        Args:
            config: Configuration dictionary with system parameters
        """
        self.config = config or {}
        self.is_running = False
        
        # Initialize components
        self._initialize_components()
        
        # Register alert handlers
        self.alert_generator.register_alert_handler(console_alert_handler)
        self.alert_generator.register_alert_handler(file_alert_handler)
        
        logger.info("Anomaly Detector Orchestrator initialized")
    
    def _initialize_components(self):
        """Initialize all system components"""
        try:
            # Initialize models
            self.one_class_svm = get_one_class_svm_model()
            self.dbscan = get_dbscan_model()
            self.statistical_detector = get_statistical_detector()
            self.ml_detector = get_ml_detector()
            self.ensemble_detector = get_ensemble_detector()
            
            # Initialize data processing components
            processor_config = DataProcessorConfig()
            self.data_processor = StreamDataProcessor(processor_config)
            self.quality_monitor = DataQualityMonitor(processor_config)
            self.feature_extractor = FeatureExtractor(processor_config)
            
            # Initialize streaming service
            streaming_config = StreamingConfig(
                websocket_port=self.config.get('streaming_port', 8766),
                update_interval=self.config.get('update_interval', 60),
                max_buffer_size=self.config.get('buffer_size', 1000)
            )
            self.streaming_service = AnomalyStreamingService(streaming_config)
            
            # Initialize classification components
            self.severity_classifier = get_severity_classifier()
            self.impact_assessor = get_impact_assessor()
            
            # Initialize alerting components
            self.alert_generator = get_alert_generator()
            self.escalation_system = get_escalation_system()
            
        except Exception as e:
            logger.error(f"Error initializing components: {e}")
            raise
    
    def train_models(self, training_data: pd.DataFrame) -> bool:
        """
        Train all anomaly detection models
        
        Args:
            training_data: DataFrame with training data
            
        Returns:
            Boolean indicating success
        """
        try:
            logger.info("Training anomaly detection models")
            
            # Train individual models
            svm_success = self.one_class_svm.train(training_data)
            dbscan_success = self.dbscan.train(training_data)
            statistical_success = self.statistical_detector.train(training_data)
            ml_success = self.ml_detector.train(training_data).get('success', False)
            
            # Train ensemble model
            ensemble_success = self.ensemble_detector.train(training_data)
            
            success = svm_success and dbscan_success and statistical_success and ml_success and ensemble_success
            
            if success:
                logger.info("All models trained successfully")
            else:
                logger.warning("Some models failed to train")
            
            return success
            
        except Exception as e:
            logger.error(f"Error training models: {e}")
            return False
    
    async def start_real_time_detection(self):
        """
        Start real-time anomaly detection
        """
        try:
            logger.info("Starting real-time anomaly detection")
            self.is_running = True
            
            # Start streaming service
            await self.streaming_service.start()
            
            # Process incoming data streams
            while self.is_running:
                # Get data from streams
                # Get data from all streams
                stream_data = []
                for stream_id in self.streaming_service.streams.keys():
                    stream_data.extend(self.streaming_service.get_stream_data(stream_id, 10))
                
                if stream_data:
                    # Process data
                    # Process data for each stream type
                    processed_data_list = []
                    for data in stream_data:
                        stream_type = data.get('type', 'generic')
                        processed_data = await self.data_processor.process_stream_data(data, stream_type)
                        processed_data_list.append(processed_data)
                    
                    # Combine processed data for anomaly detection
                    if processed_data_list:
                        # Extract features for anomaly detection
                        feature_data = []
                        for processed in processed_data_list:
                            features = processed.get('extracted_features', {})
                            if features:
                                feature_data.append(features)
                        
                        if feature_data:
                            # Convert to DataFrame for anomaly detection
                            feature_df = pd.DataFrame(feature_data)
                            
                            # Detect anomalies
                            anomalies = self.detect_anomalies(feature_df)
                            
                            # Generate alerts for detected anomalies
                            self._generate_anomaly_alerts(anomalies, feature_df)
                    else:
                        anomalies = {}
                        feature_df = pd.DataFrame()
                
                # Small delay to prevent busy waiting
                await asyncio.sleep(0.1)
                
        except Exception as e:
            logger.error(f"Error in real-time detection: {e}")
            self.is_running = False
        finally:
            await self.stop_real_time_detection()
    
    async def stop_real_time_detection(self):
        """
        Stop real-time anomaly detection
        """
        try:
            logger.info("Stopping real-time anomaly detection")
            self.is_running = False
            
            # Stop streaming service
            await self.streaming_service.stop()
            
        except Exception as e:
            logger.error(f"Error stopping real-time detection: {e}")
    
    def detect_anomalies(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Detect anomalies in the provided data using all models
        
        Args:
            data: DataFrame with data to analyze
            
        Returns:
            Dictionary with anomaly detection results
        """
        try:
            if data.empty:
                logger.warning("Empty data provided for anomaly detection")
                return {}
            
            # Get predictions from all models
            results = {}
            
            # One-Class SVM
            try:
                svm_predictions = self.one_class_svm.predict(data)
                svm_scores = self.one_class_svm.anomaly_scores(data)
                results['one_class_svm'] = {
                    'predictions': svm_predictions,
                    'scores': svm_scores
                }
            except Exception as e:
                logger.warning(f"Error in One-Class SVM detection: {e}")
                results['one_class_svm'] = {'predictions': np.ones(len(data)), 'scores': np.zeros(len(data))}
            
            # DBSCAN
            try:
                dbscan_predictions = self.dbscan.predict(data)
                dbscan_scores = self.dbscan.anomaly_scores(data)
                results['dbscan'] = {
                    'predictions': dbscan_predictions,
                    'scores': dbscan_scores
                }
            except Exception as e:
                logger.warning(f"Error in DBSCAN detection: {e}")
                results['dbscan'] = {'predictions': np.ones(len(data)), 'scores': np.zeros(len(data))}
            
            # Statistical detector
            try:
                statistical_predictions = self.statistical_detector.predict(data)
                statistical_scores = self.statistical_detector.anomaly_scores(data)
                results['statistical'] = {
                    'predictions': statistical_predictions,
                    'scores': statistical_scores
                }
            except Exception as e:
                logger.warning(f"Error in statistical detection: {e}")
                results['statistical'] = {'predictions': np.ones(len(data)), 'scores': np.zeros(len(data))}
            
            # ML detector
            try:
                ml_predictions = self.ml_detector.predict(data)
                ml_scores = self.ml_detector.anomaly_scores(data)
                results['ml'] = {
                    'predictions': ml_predictions,
                    'scores': ml_scores
                }
            except Exception as e:
                logger.warning(f"Error in ML detection: {e}")
                results['ml'] = {'predictions': np.ones(len(data)), 'scores': np.zeros(len(data))}
            
            # Ensemble detector
            try:
                ensemble_predictions = self.ensemble_detector.predict(data)
                results['ensemble'] = {
                    'predictions': ensemble_predictions
                }
                
                # Get model contributions (not stored in results due to type conflicts)
                contributions = self.ensemble_detector.get_model_contributions(data)
            except Exception as e:
                logger.warning(f"Error in ensemble detection: {e}")
                results['ensemble'] = {'predictions': np.ones(len(data)), 'contributions': {}}
            
            # Combine results
            combined_results = self._combine_detection_results(results, data)
            
            logger.info(f"Anomaly detection completed. Found {np.sum(combined_results['anomalies'] == -1)} anomalies")
            return combined_results
            
        except Exception as e:
            logger.error(f"Error detecting anomalies: {e}")
            return {}
    
    def _combine_detection_results(self, results: Dict[str, Any], data: pd.DataFrame) -> Dict[str, Any]:
        """
        Combine results from all detection models
        
        Args:
            results: Dictionary with results from all models
            data: Original data
            
        Returns:
            Combined results dictionary
        """
        try:
            # Extract ensemble predictions as primary results
            ensemble_predictions = results.get('ensemble', {}).get('predictions', np.ones(len(data)))
            
            # Create anomaly data for severity classification
            anomaly_indices = np.where(ensemble_predictions == -1)[0]
            
            # Create anomaly data DataFrame
            anomaly_data_list = []
            for idx in anomaly_indices:
                anomaly_row = data.iloc[idx].copy()
                anomaly_row['anomaly_index'] = idx
                anomaly_row['anomaly_score'] = np.mean([
                    results.get('one_class_svm', {}).get('scores', np.zeros(len(data)))[idx],
                    results.get('dbscan', {}).get('scores', np.zeros(len(data)))[idx],
                    results.get('statistical', {}).get('scores', np.zeros(len(data)))[idx],
                    results.get('ml', {}).get('scores', np.zeros(len(data)))[idx]
                ])
                anomaly_data_list.append(anomaly_row)
            
            anomaly_data = pd.DataFrame(anomaly_data_list) if anomaly_data_list else pd.DataFrame()
            
            # Classify severity for anomalies
            severities = self.severity_classifier.classify_severity(anomaly_data) if not anomaly_data.empty else []
            
            # Assess impact for anomalies
            impacts = self.impact_assessor.assess_impact(anomaly_data) if not anomaly_data.empty else np.array([])
            
            return {
                'anomalies': ensemble_predictions,
                'results': results,
                'anomaly_data': anomaly_data,
                'severities': severities,
                'impacts': impacts,
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Error combining detection results: {e}")
            return {
                'anomalies': np.ones(len(data)),
                'results': results,
                'anomaly_data': pd.DataFrame(),
                'severities': [],
                'impacts': np.array([]),
                'timestamp': datetime.now()
            }
    
    def _generate_anomaly_alerts(self, anomaly_results: Dict[str, Any], processed_data: pd.DataFrame):
        """
        Generate alerts for detected anomalies
        
        Args:
            anomaly_results: Results from anomaly detection
            processed_data: Processed data
        """
        try:
            anomalies = anomaly_results.get('anomalies', np.array([]))
            severities = anomaly_results.get('severities', [])
            anomaly_data = anomaly_results.get('anomaly_data', pd.DataFrame())
            
            if len(anomalies) == 0:
                return
            
            # Generate alerts for each anomaly
            anomaly_indices = np.where(anomalies == -1)[0]
            
            for i, idx in enumerate(anomaly_indices):
                if i < len(severities):
                    severity = severities[i]
                    
                    # Extract data for this anomaly
                    if idx < len(processed_data):
                        anomaly_row = processed_data.iloc[idx].to_dict()
                        anomaly_row['anomaly_index'] = idx
                    else:
                        anomaly_row = {'anomaly_index': idx}
                    
                    # Generate alert
                    self.alert_generator.generate_alert(
                        pd.DataFrame([anomaly_row]),
                        severity,
                        "Anomaly detected in system metrics with {severity} severity"
                    )
            
        except Exception as e:
            logger.error(f"Error generating anomaly alerts: {e}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get current status of the anomaly detection system
        
        Returns:
            Dictionary with system status information
        """
        try:
            return {
                'is_running': self.is_running,
                'models_trained': {
                    'one_class_svm': self.one_class_svm.is_trained,
                    'dbscan': self.dbscan.is_trained,
                    'statistical': self.statistical_detector.is_trained,
                    'ml': self.ml_detector.is_trained,
                    'ensemble': self.ensemble_detector.is_trained
                },
                'streaming_active': self.streaming_service.is_running,
                'processed_count': self.data_processor.processed_count,
                'error_count': self.data_processor.error_count,
                'alert_count': len(self.alert_generator.alert_history)
            }
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {}
    
    def load_sample_data(self, file_path: str) -> pd.DataFrame:
        """
        Load sample data for testing
        
        Args:
            file_path: Path to CSV file with sample data
            
        Returns:
            DataFrame with loaded data
        """
        try:
            data = pd.read_csv(file_path)
            logger.info(f"Loaded sample data from {file_path}, shape: {data.shape}")
            return data
        except Exception as e:
            logger.error(f"Error loading sample data: {e}")
            return pd.DataFrame()


# Global instance for easy access
anomaly_orchestrator_instance = None


def get_anomaly_orchestrator(config: Optional[Dict[str, Any]] = None) -> AnomalyDetectorOrchestrator:
    """Get singleton anomaly detector orchestrator instance"""
    global anomaly_orchestrator_instance
    if anomaly_orchestrator_instance is None:
        anomaly_orchestrator_instance = AnomalyDetectorOrchestrator(config)
    return anomaly_orchestrator_instance


# Example usage
async def main():
    """Example usage of the anomaly detector orchestrator"""
    # Initialize orchestrator
    orchestrator = get_anomaly_orchestrator({
        'streaming_host': 'localhost',
        'streaming_port': 8765
    })
    
    # Load sample data for training
    # In a real system, you would load your actual training data
    sample_data = pd.DataFrame({
        'feature1': np.random.normal(0, 1, 1000),
        'feature2': np.random.normal(0, 1, 1000),
        'feature3': np.random.normal(0, 1, 1000)
    })
    
    # Train models
    orchestrator.train_models(sample_data)
    
    # Start real-time detection (run for a short time for demo)
    print("Starting anomaly detection system...")
    detection_task = asyncio.create_task(orchestrator.start_real_time_detection())
    
    # Run for 10 seconds then stop
    await asyncio.sleep(10)
    orchestrator.is_running = False
    await detection_task
    
    # Print system status
    status = orchestrator.get_system_status()
    print(f"System status: {status}")


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Run example
    asyncio.run(main())