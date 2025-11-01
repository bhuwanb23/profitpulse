"""
Real-time Alert Generation System for Anomaly Detection
Implements real-time alert generation, escalation, and false positive reduction
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple, Callable
from datetime import datetime, timedelta
import asyncio
import json
import warnings
warnings.filterwarnings('ignore')

from .severity_classifier import AnomalySeverity, get_severity_classifier

logger = logging.getLogger(__name__)


class Alert:
    """Alert data structure"""
    
    def __init__(self, 
                 alert_id: str,
                 anomaly_id: str,
                 timestamp: datetime,
                 severity: AnomalySeverity,
                 message: str,
                 data: Dict[str, Any],
                 source: str = "anomaly_detector"):
        self.alert_id = alert_id
        self.anomaly_id = anomaly_id
        self.timestamp = timestamp
        self.severity = severity
        self.message = message
        self.data = data
        self.source = source
        self.escalation_level = 0
        self.handled = False
        self.handled_timestamp = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert alert to dictionary"""
        return {
            'alert_id': self.alert_id,
            'anomaly_id': self.anomaly_id,
            'timestamp': self.timestamp.isoformat(),
            'severity': self.severity.name,
            'message': self.message,
            'data': self.data,
            'source': self.source,
            'escalation_level': self.escalation_level,
            'handled': self.handled
        }


class AlertGenerator:
    """Real-time alert generation system"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize alert generator
        
        Args:
            config: Configuration dictionary with alert generation parameters
        """
        self.config = config or {}
        self.alert_handlers: List[Callable] = []
        self.severity_classifier = get_severity_classifier()
        self.alert_history = []
        self.alert_counter = 0
        self.false_positive_detector = FalsePositiveDetector()
        logger.info("Alert Generator initialized")
    
    def register_alert_handler(self, handler: Callable[[Alert], None]):
        """
        Register an alert handler function
        
        Args:
            handler: Function to call when an alert is generated
        """
        self.alert_handlers.append(handler)
        logger.info(f"Registered alert handler. Total handlers: {len(self.alert_handlers)}")
    
    def generate_alert(self, 
                      anomaly_data: pd.DataFrame,
                      severity: AnomalySeverity,
                      message_template: str = "Anomaly detected with {severity} severity") -> Optional[Alert]:
        """
        Generate an alert for detected anomalies
        
        Args:
            anomaly_data: DataFrame with anomaly information
            severity: Severity level of the anomaly
            message_template: Template for alert message
            
        Returns:
            Generated Alert object or None if filtered as false positive
        """
        try:
            # Check for false positives
            if self.false_positive_detector.is_false_positive(anomaly_data):
                logger.info("Anomaly filtered as false positive")
                return None
            
            # Generate alert ID
            self.alert_counter += 1
            alert_id = f"ALERT_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self.alert_counter}"
            anomaly_id = str(anomaly_data.get('anomaly_id', f"ANOMALY_{self.alert_counter}") if isinstance(anomaly_data, dict) else f"ANOMALY_{self.alert_counter}")
            
            # Create alert message
            severity_desc = self.severity_classifier.get_severity_description(severity)
            message = message_template.format(severity=severity_desc.lower())
            
            # Convert DataFrame to dict for alert data
            if isinstance(anomaly_data, pd.DataFrame):
                alert_data = anomaly_data.to_dict('records')[0] if len(anomaly_data) > 0 else {}
            else:
                alert_data = anomaly_data if isinstance(anomaly_data, dict) else {}
            
            # Create alert
            alert = Alert(
                alert_id=alert_id,
                anomaly_id=anomaly_id,
                timestamp=datetime.now(),
                severity=severity,
                message=message,
                data=alert_data
            )
            
            # Add to history
            self.alert_history.append(alert)
            
            # Trigger handlers
            for handler in self.alert_handlers:
                try:
                    handler(alert)
                except Exception as e:
                    logger.error(f"Error in alert handler: {e}")
            
            logger.info(f"Generated alert {alert_id} with severity {severity.name}")
            return alert
            
        except Exception as e:
            logger.error(f"Error generating alert: {e}")
            return None
    
    def generate_batch_alerts(self, 
                             anomaly_data_list: List[pd.DataFrame],
                             severities: List[AnomalySeverity]) -> List[Optional[Alert]]:
        """
        Generate alerts for a batch of anomalies
        
        Args:
            anomaly_data_list: List of DataFrames with anomaly information
            severities: List of severity levels for each anomaly
            
        Returns:
            List of generated Alert objects (None for filtered anomalies)
        """
        alerts = []
        for anomaly_data, severity in zip(anomaly_data_list, severities):
            alert = self.generate_alert(anomaly_data, severity)
            alerts.append(alert)
        return alerts
    
    def get_alert_history(self, 
                         hours_back: int = 24,
                         severity_filter: Optional[AnomalySeverity] = None) -> List[Alert]:
        """
        Get alert history
        
        Args:
            hours_back: Number of hours back to retrieve alerts
            severity_filter: Optional severity level to filter by
            
        Returns:
            List of Alert objects
        """
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours_back)
            filtered_alerts = [
                alert for alert in self.alert_history 
                if alert.timestamp >= cutoff_time
            ]
            
            if severity_filter:
                filtered_alerts = [
                    alert for alert in filtered_alerts
                    if alert.severity == severity_filter
                ]
            
            return filtered_alerts
        except Exception as e:
            logger.error(f"Error retrieving alert history: {e}")
            return []


class FalsePositiveDetector:
    """Detect and filter false positive anomalies"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize false positive detector
        
        Args:
            config: Configuration dictionary with false positive detection parameters
        """
        self.config = config or {}
        self.false_positive_patterns = self.config.get('false_positive_patterns', [])
        self.similarity_threshold = self.config.get('similarity_threshold', 0.95)
        self.frequency_threshold = self.config.get('frequency_threshold', 10)
        self.pattern_history = {}
        logger.info("False Positive Detector initialized")
    
    def is_false_positive(self, anomaly_data: pd.DataFrame) -> bool:
        """
        Determine if an anomaly is a false positive
        
        Args:
            anomaly_data: DataFrame with anomaly information
            
        Returns:
            Boolean indicating if anomaly is a false positive
        """
        try:
            # Check against known false positive patterns
            if self._matches_false_positive_pattern(anomaly_data):
                return True
            
            # Check frequency-based false positives
            if self._is_high_frequency_pattern(anomaly_data):
                return True
            
            # Check similarity to previous false positives
            if self._is_similar_to_known_false_positive(anomaly_data):
                return True
            
            return False
        except Exception as e:
            logger.warning(f"Error in false positive detection: {e}")
            return False  # Don't filter as false positive on error
    
    def _matches_false_positive_pattern(self, anomaly_data: pd.DataFrame) -> bool:
        """Check if anomaly matches known false positive patterns"""
        try:
            # This is a simplified implementation
            # In a real system, this would check against a database of known false positive patterns
            return False
        except Exception as e:
            logger.warning(f"Error checking false positive patterns: {e}")
            return False
    
    def _is_high_frequency_pattern(self, anomaly_data: pd.DataFrame) -> bool:
        """Check if this is a high-frequency pattern that's likely a false positive"""
        try:
            # This is a simplified implementation
            # In a real system, this would track frequency of similar anomalies
            return False
        except Exception as e:
            logger.warning(f"Error checking high frequency patterns: {e}")
            return False
    
    def _is_similar_to_known_false_positive(self, anomaly_data: pd.DataFrame) -> bool:
        """Check if anomaly is similar to known false positives"""
        try:
            # This is a simplified implementation
            # In a real system, this would use similarity metrics to compare with known false positives
            return False
        except Exception as e:
            logger.warning(f"Error checking similarity to false positives: {e}")
            return False
    
    def add_false_positive_pattern(self, pattern: Dict[str, Any]):
        """
        Add a new false positive pattern
        
        Args:
            pattern: Dictionary describing the false positive pattern
        """
        try:
            self.false_positive_patterns.append(pattern)
            logger.info("Added new false positive pattern")
        except Exception as e:
            logger.error(f"Error adding false positive pattern: {e}")


class AlertEscalationSystem:
    """Escalate alerts based on severity and handling status"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize alert escalation system
        
        Args:
            config: Configuration dictionary with escalation parameters
        """
        self.config = config or {}
        self.escalation_rules = self.config.get('escalation_rules', {
            AnomalySeverity.LOW: {'timeout_minutes': 60, 'escalate_to': AnomalySeverity.MEDIUM},
            AnomalySeverity.MEDIUM: {'timeout_minutes': 30, 'escalate_to': AnomalySeverity.HIGH},
            AnomalySeverity.HIGH: {'timeout_minutes': 15, 'escalate_to': AnomalySeverity.CRITICAL},
            AnomalySeverity.CRITICAL: {'timeout_minutes': 5, 'escalate_to': None}
        })
        self.escalation_handlers: List[Callable] = []
        logger.info("Alert Escalation System initialized")
    
    def register_escalation_handler(self, handler: Callable[[Alert], None]):
        """
        Register an escalation handler function
        
        Args:
            handler: Function to call when an alert is escalated
        """
        self.escalation_handlers.append(handler)
        logger.info(f"Registered escalation handler. Total handlers: {len(self.escalation_handlers)}")
    
    def check_escalation(self, alert: Alert) -> bool:
        """
        Check if an alert should be escalated
        
        Args:
            alert: Alert to check for escalation
            
        Returns:
            Boolean indicating if alert was escalated
        """
        try:
            # Skip if already handled
            if alert.handled:
                return False
            
            # Get escalation rule for current severity
            rule = self.escalation_rules.get(alert.severity)
            if not rule:
                return False
            
            # Check if timeout has passed
            if alert.timestamp + timedelta(minutes=rule['timeout_minutes']) < datetime.now():
                # Escalate if there's a higher level
                if rule['escalate_to']:
                    logger.info(f"Escalating alert {alert.alert_id} from {alert.severity.name} to {rule['escalate_to'].name}")
                    alert.severity = rule['escalate_to']
                    alert.escalation_level += 1
                    
                    # Trigger escalation handlers
                    for handler in self.escalation_handlers:
                        try:
                            handler(alert)
                        except Exception as e:
                            logger.error(f"Error in escalation handler: {e}")
                    
                    return True
            
            return False
        except Exception as e:
            logger.error(f"Error checking alert escalation: {e}")
            return False


# Global instances for easy access
alert_generator_instance = None
escalation_system_instance = None


def get_alert_generator(config: Optional[Dict[str, Any]] = None) -> AlertGenerator:
    """Get singleton alert generator instance"""
    global alert_generator_instance
    if alert_generator_instance is None:
        alert_generator_instance = AlertGenerator(config)
    return alert_generator_instance


def get_escalation_system(config: Optional[Dict[str, Any]] = None) -> AlertEscalationSystem:
    """Get singleton escalation system instance"""
    global escalation_system_instance
    if escalation_system_instance is None:
        escalation_system_instance = AlertEscalationSystem(config)
    return escalation_system_instance


# Example alert handler functions
def console_alert_handler(alert: Alert):
    """Simple console alert handler"""
    print(f"[{alert.timestamp}] {alert.severity.name} ALERT: {alert.message}")


def file_alert_handler(alert: Alert):
    """File-based alert handler"""
    try:
        with open("alerts.log", "a") as f:
            f.write(f"[{alert.timestamp}] {alert.severity.name} ALERT: {alert.message}\n")
    except Exception as e:
        logger.error(f"Error in file alert handler: {e}")