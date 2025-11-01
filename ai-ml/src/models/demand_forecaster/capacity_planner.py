"""
Capacity Planning Module for Service Demand Forecaster
Handles forecast accuracy monitoring and performance metrics tracking
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


class ForecastMonitor:
    """Forecast accuracy monitoring system"""
    
    def __init__(self):
        """Initialize forecast monitor"""
        logger.info("Forecast Monitor initialized")
    
    def calculate_accuracy_metrics(self, actual_values: List[float], 
                                predicted_values: List[float]) -> Dict[str, Any]:
        """
        Calculate forecast accuracy metrics
        
        Args:
            actual_values: Actual observed values
            predicted_values: Predicted values
            
        Returns:
            Dictionary with accuracy metrics
        """
        try:
            if not actual_values or not predicted_values:
                return {
                    'success': False,
                    'message': 'Insufficient data for accuracy calculation',
                    'metrics': {}
                }
            
            # Ensure arrays are same length
            min_length = min(len(actual_values), len(predicted_values))
            actual = np.array(actual_values[:min_length])
            predicted = np.array(predicted_values[:min_length])
            
            # Calculate metrics
            mae = np.mean(np.abs(actual - predicted))
            mse = np.mean((actual - predicted) ** 2)
            rmse = np.sqrt(mse)
            
            # Mean Absolute Percentage Error (MAPE)
            non_zero_actual = actual[actual != 0]
            non_zero_predicted = predicted[actual != 0]
            if len(non_zero_actual) > 0:
                mape = np.mean(np.abs((non_zero_actual - non_zero_predicted) / non_zero_actual)) * 100
            else:
                mape = 0
            
            # Mean Absolute Scaled Error (MASE)
            if len(actual) > 1:
                naive_forecast = actual[:-1]  # Naive forecast (previous value)
                actual_comparison = actual[1:]  # Actual values for comparison
                predicted_comparison = predicted[1:]
                
                mae_naive = np.mean(np.abs(actual_comparison - naive_forecast))
                mae_forecast = np.mean(np.abs(actual_comparison - predicted_comparison))
                
                mase = mae_forecast / mae_naive if mae_naive > 0 else 0
            else:
                mase = 0
            
            metrics = {
                'mae': mae,
                'mse': mse,
                'rmse': rmse,
                'mape': mape,
                'mase': mase,
                'forecast_length': min_length
            }
            
            logger.info("Forecast accuracy metrics calculated")
            return {
                'success': True,
                'message': 'Accuracy metrics calculated',
                'metrics': metrics
            }
            
        except Exception as e:
            logger.error(f"Error calculating accuracy metrics: {e}")
            return {
                'success': False,
                'message': f'Accuracy calculation error: {str(e)}',
                'metrics': {}
            }
    
    def track_model_performance(self, model_name: str, actual_values: List[float],
                             predicted_values: List[float], timestamp: datetime) -> Dict[str, Any]:
        """
        Track model performance over time
        
        Args:
            model_name: Name of the model
            actual_values: Actual observed values
            predicted_values: Predicted values
            timestamp: Timestamp of the evaluation
            
        Returns:
            Dictionary with performance tracking results
        """
        try:
            # Calculate accuracy metrics
            accuracy_result = self.calculate_accuracy_metrics(actual_values, predicted_values)
            
            if not accuracy_result.get('success', False):
                return accuracy_result
            
            metrics = accuracy_result.get('metrics', {})
            
            # Create performance record
            performance_record = {
                'model_name': model_name,
                'timestamp': timestamp.isoformat(),
                'evaluation_metrics': metrics,
                'performance_score': self._calculate_performance_score(metrics)
            }
            
            logger.info(f"Model performance tracked for {model_name}")
            return {
                'success': True,
                'message': 'Model performance tracked',
                'performance_record': performance_record
            }
            
        except Exception as e:
            logger.error(f"Error tracking model performance: {e}")
            return {
                'success': False,
                'message': f'Performance tracking error: {str(e)}',
                'performance_record': {}
            }
    
    def _calculate_performance_score(self, metrics: Dict[str, float]) -> float:
        """Calculate overall performance score"""
        # Simple weighted score based on key metrics
        # Lower values are better for error metrics
        mae = metrics.get('mae', 0)
        rmse = metrics.get('rmse', 0)
        mape = metrics.get('mape', 0)
        
        # Normalize scores (assuming reasonable ranges)
        mae_score = max(0, 100 - mae * 2)  # Scale MAE
        rmse_score = max(0, 100 - rmse * 1.5)  # Scale RMSE
        mape_score = max(0, 100 - mape)  # MAPE is already percentage
        
        # Weighted average
        performance_score = (mae_score * 0.4 + rmse_score * 0.4 + mape_score * 0.2)
        
        return min(100, max(0, performance_score))  # Clamp between 0-100


class ModelDriftDetector:
    """Model drift detection system"""
    
    def __init__(self, threshold: float = 0.1):
        """
        Initialize model drift detector
        
        Args:
            threshold: Threshold for detecting significant drift
        """
        self.threshold = threshold
        self.historical_performance = {}
        logger.info("Model Drift Detector initialized")
    
    def detect_drift(self, model_name: str, current_metrics: Dict[str, float],
                  historical_metrics: Dict[str, float]) -> Dict[str, Any]:
        """
        Detect model drift by comparing current and historical performance
        
        Args:
            model_name: Name of the model
            current_metrics: Current performance metrics
            historical_metrics: Historical performance metrics
            
        Returns:
            Dictionary with drift detection results
        """
        try:
            drift_indicators = {}
            drift_detected = False
            
            # Compare key metrics
            for metric_name in ['mae', 'rmse', 'mape']:
                current_value = current_metrics.get(metric_name, 0)
                historical_value = historical_metrics.get(metric_name, 0)
                
                if historical_value > 0:
                    change_ratio = abs(current_value - historical_value) / historical_value
                    drift_indicators[metric_name] = {
                        'current': current_value,
                        'historical': historical_value,
                        'change_ratio': change_ratio,
                        'drift_detected': change_ratio > self.threshold
                    }
                    
                    if change_ratio > self.threshold:
                        drift_detected = True
            
            result = {
                'model_name': model_name,
                'drift_detected': drift_detected,
                'drift_indicators': drift_indicators,
                'threshold': self.threshold,
                'recommendation': self._generate_drift_recommendation(drift_detected, drift_indicators)
            }
            
            if drift_detected:
                logger.warning(f"Model drift detected for {model_name}")
            else:
                logger.info(f"No significant model drift for {model_name}")
            
            return {
                'success': True,
                'message': 'Drift detection completed',
                'drift_result': result
            }
            
        except Exception as e:
            logger.error(f"Error detecting model drift: {e}")
            return {
                'success': False,
                'message': f'Drift detection error: {str(e)}',
                'drift_result': {}
            }
    
    def _generate_drift_recommendation(self, drift_detected: bool, 
                                    drift_indicators: Dict[str, Dict]) -> str:
        """Generate recommendation based on drift detection"""
        if not drift_detected:
            return "Model performance stable, no action required"
        
        # Identify which metrics show drift
        drifted_metrics = [
            name for name, indicator in drift_indicators.items() 
            if indicator.get('drift_detected', False)
        ]
        
        if drifted_metrics:
            return f"Significant drift detected in {', '.join(drifted_metrics)}. Consider model retraining."
        else:
            return "Minor performance variations detected, monitor closely"


class AlertSystem:
    """Alerting system for significant forecast deviations"""
    
    def __init__(self, deviation_threshold: float = 0.2):
        """
        Initialize alert system
        
        Args:
            deviation_threshold: Threshold for triggering alerts (20% deviation)
        """
        self.deviation_threshold = deviation_threshold
        logger.info("Alert System initialized")
    
    def check_forecast_deviations(self, actual_values: List[float],
                               forecasted_values: List[float],
                               model_name: str) -> Dict[str, Any]:
        """
        Check for significant deviations between actual and forecasted values
        
        Args:
            actual_values: Actual observed values
            forecasted_values: Forecasted values
            model_name: Name of the model
            
        Returns:
            Dictionary with alert results
        """
        try:
            if not actual_values or not forecasted_values:
                return {
                    'success': False,
                    'message': 'Insufficient data for deviation check',
                    'alerts': []
                }
            
            alerts = []
            
            # Compare values
            min_length = min(len(actual_values), len(forecasted_values))
            for i in range(min_length):
                actual = actual_values[i]
                forecasted = forecasted_values[i]
                
                if forecasted > 0:
                    deviation = abs(actual - forecasted) / forecasted
                    if deviation > self.deviation_threshold:
                        alert = {
                            'timestamp': datetime.now().isoformat(),
                            'model_name': model_name,
                            'time_index': i,
                            'actual_value': actual,
                            'forecasted_value': forecasted,
                            'deviation': deviation,
                            'deviation_percentage': deviation * 100,
                            'severity': 'high' if deviation > self.deviation_threshold * 2 else 'medium'
                        }
                        alerts.append(alert)
            
            if alerts:
                logger.warning(f"{len(alerts)} significant deviations detected for {model_name}")
            else:
                logger.info(f"No significant deviations for {model_name}")
            
            return {
                'success': True,
                'message': 'Deviation check completed',
                'alerts': alerts,
                'alert_count': len(alerts)
            }
            
        except Exception as e:
            logger.error(f"Error checking forecast deviations: {e}")
            return {
                'success': False,
                'message': f'Deviation check error: {str(e)}',
                'alerts': []
            }


# Global instances for easy access
forecast_monitor_instance = None
model_drift_detector_instance = None
alert_system_instance = None


def get_forecast_monitor() -> ForecastMonitor:
    """Get singleton forecast monitor instance"""
    global forecast_monitor_instance
    if forecast_monitor_instance is None:
        forecast_monitor_instance = ForecastMonitor()
    return forecast_monitor_instance


def get_model_drift_detector(threshold: float = 0.1) -> ModelDriftDetector:
    """Get singleton model drift detector instance"""
    global model_drift_detector_instance
    if model_drift_detector_instance is None:
        model_drift_detector_instance = ModelDriftDetector(threshold)
    return model_drift_detector_instance


def get_alert_system(deviation_threshold: float = 0.2) -> AlertSystem:
    """Get singleton alert system instance"""
    global alert_system_instance
    if alert_system_instance is None:
        alert_system_instance = AlertSystem(deviation_threshold)
    return alert_system_instance