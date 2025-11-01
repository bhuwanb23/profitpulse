"""
Unit tests for alert system components
"""

import unittest
import numpy as np
import pandas as pd
from datetime import datetime

from src.models.anomaly_detector.alert_system import (
    Alert,
    AlertGenerator,
    FalsePositiveDetector,
    AlertEscalationSystem,
    AnomalySeverity,
    get_alert_generator,
    get_escalation_system
)


class TestAlert(unittest.TestCase):
    """Test cases for Alert class"""
    
    def setUp(self):
        """Set up test data"""
        self.alert_data = {
            'anomaly_score': 0.85,
            'feature1': 1.2,
            'feature2': 3.4
        }
        
        self.alert = Alert(
            alert_id="ALERT_001",
            anomaly_id="ANOMALY_001",
            timestamp=datetime.now(),
            severity=AnomalySeverity.HIGH,
            message="Test alert message",
            data=self.alert_data
        )
    
    def test_initialization(self):
        """Test alert initialization"""
        self.assertEqual(self.alert.alert_id, "ALERT_001")
        self.assertEqual(self.alert.anomaly_id, "ANOMALY_001")
        self.assertIsNotNone(self.alert.timestamp)
        self.assertEqual(self.alert.severity, AnomalySeverity.HIGH)
        self.assertEqual(self.alert.message, "Test alert message")
        self.assertEqual(self.alert.data, self.alert_data)
        self.assertEqual(self.alert.source, "anomaly_detector")
        self.assertEqual(self.alert.escalation_level, 0)
        self.assertFalse(self.alert.handled)
        self.assertIsNone(self.alert.handled_timestamp)
    
    def test_to_dict(self):
        """Test alert to dictionary conversion"""
        alert_dict = self.alert.to_dict()
        
        self.assertIsInstance(alert_dict, dict)
        self.assertIn('alert_id', alert_dict)
        self.assertIn('anomaly_id', alert_dict)
        self.assertIn('timestamp', alert_dict)
        self.assertIn('severity', alert_dict)
        self.assertIn('message', alert_dict)
        self.assertIn('data', alert_dict)
        self.assertIn('source', alert_dict)
        self.assertIn('escalation_level', alert_dict)
        self.assertIn('handled', alert_dict)
        
        # Check values
        self.assertEqual(alert_dict['alert_id'], "ALERT_001")
        self.assertEqual(alert_dict['anomaly_id'], "ANOMALY_001")
        self.assertEqual(alert_dict['severity'], "HIGH")
        self.assertEqual(alert_dict['message'], "Test alert message")
        self.assertEqual(alert_dict['data'], self.alert_data)
        self.assertEqual(alert_dict['source'], "anomaly_detector")
        self.assertEqual(alert_dict['escalation_level'], 0)
        self.assertFalse(alert_dict['handled'])


class TestAlertGenerator(unittest.TestCase):
    """Test cases for AlertGenerator"""
    
    def setUp(self):
        """Set up test data"""
        self.generator = AlertGenerator()
        
        # Sample anomaly data
        self.sample_anomaly_data = pd.DataFrame([{
            'anomaly_score': 0.85,
            'feature1': 1.2,
            'feature2': 3.4
        }])
    
    def test_initialization(self):
        """Test generator initialization"""
        self.assertIsNotNone(self.generator)
        self.assertEqual(len(self.generator.alert_handlers), 0)
        self.assertIsNotNone(self.generator.severity_classifier)
        self.assertEqual(len(self.generator.alert_history), 0)
        self.assertEqual(self.generator.alert_counter, 0)
    
    def test_register_alert_handler(self):
        """Test registering alert handlers"""
        def test_handler(alert):
            pass
        
        self.generator.register_alert_handler(test_handler)
        self.assertEqual(len(self.generator.alert_handlers), 1)
        
        # Register another handler
        self.generator.register_alert_handler(test_handler)
        self.assertEqual(len(self.generator.alert_handlers), 2)
    
    def test_generate_alert(self):
        """Test alert generation"""
        alert = self.generator.generate_alert(
            self.sample_anomaly_data,
            AnomalySeverity.HIGH,
            "Test alert with {severity} severity"
        )
        
        # The alert might be None if filtered as false positive, but in our test it should not be
        self.assertIsNotNone(alert)
        if alert is not None:
            self.assertIsInstance(alert, Alert)
            self.assertIn("ALERT_", alert.alert_id)
            self.assertIn("ANOMALY_", alert.anomaly_id)
            self.assertEqual(alert.severity, AnomalySeverity.HIGH)
            self.assertIn("high", alert.message)
            
            # Check that alert was added to history
            self.assertEqual(len(self.generator.alert_history), 1)
            self.assertIs(self.generator.alert_history[0], alert)
    
    def test_generate_batch_alerts(self):
        """Test batch alert generation"""
        # Create list of anomaly data and severities
        anomaly_data_list = [self.sample_anomaly_data, self.sample_anomaly_data]
        severities = [AnomalySeverity.HIGH, AnomalySeverity.MEDIUM]
        
        alerts = self.generator.generate_batch_alerts(anomaly_data_list, severities)
        
        self.assertEqual(len(alerts), 2)
        for alert in alerts:
            # Alert might be None if filtered as false positive
            if alert is not None:
                self.assertIsInstance(alert, Alert)
    
    def test_get_alert_history(self):
        """Test getting alert history"""
        # Generate some alerts
        self.generator.generate_alert(
            self.sample_anomaly_data,
            AnomalySeverity.HIGH
        )
        self.generator.generate_alert(
            self.sample_anomaly_data,
            AnomalySeverity.MEDIUM
        )
        
        # Get all alerts
        all_alerts = self.generator.get_alert_history()
        self.assertEqual(len(all_alerts), 2)
        
        # Get alerts from last hour
        recent_alerts = self.generator.get_alert_history(hours_back=1)
        self.assertEqual(len(recent_alerts), 2)
        
        # Get alerts with specific severity
        high_alerts = self.generator.get_alert_history(severity_filter=AnomalySeverity.HIGH)
        self.assertEqual(len(high_alerts), 1)


class TestFalsePositiveDetector(unittest.TestCase):
    """Test cases for FalsePositiveDetector"""
    
    def setUp(self):
        """Set up test data"""
        self.detector = FalsePositiveDetector()
        
        # Sample anomaly data
        self.sample_anomaly_data = pd.DataFrame([{
            'anomaly_score': 0.85,
            'feature1': 1.2,
            'feature2': 3.4
        }])
    
    def test_initialization(self):
        """Test detector initialization"""
        self.assertIsNotNone(self.detector)
        self.assertIsInstance(self.detector.false_positive_patterns, list)
        self.assertEqual(self.detector.similarity_threshold, 0.95)
        self.assertEqual(self.detector.frequency_threshold, 10)
        self.assertIsInstance(self.detector.pattern_history, dict)
    
    def test_is_false_positive(self):
        """Test false positive detection"""
        # This is a simplified implementation that always returns False
        # In a real system, this would have more complex logic
        result = self.detector.is_false_positive(self.sample_anomaly_data)
        self.assertIsInstance(result, bool)
    
    def test_add_false_positive_pattern(self):
        """Test adding false positive patterns"""
        pattern = {"pattern": "test_pattern"}
        initial_length = len(self.detector.false_positive_patterns)
        
        self.detector.add_false_positive_pattern(pattern)
        self.assertEqual(len(self.detector.false_positive_patterns), initial_length + 1)
        
        # Check that pattern was added
        self.assertIn(pattern, self.detector.false_positive_patterns)


class TestAlertEscalationSystem(unittest.TestCase):
    """Test cases for AlertEscalationSystem"""
    
    def setUp(self):
        """Set up test data"""
        self.escalation_system = AlertEscalationSystem()
        
        # Create a test alert
        self.alert_data = {
            'anomaly_score': 0.85,
            'feature1': 1.2,
            'feature2': 3.4
        }
        
        self.alert = Alert(
            alert_id="ALERT_001",
            anomaly_id="ANOMALY_001",
            timestamp=datetime.now(),
            severity=AnomalySeverity.MEDIUM,
            message="Test alert message",
            data=self.alert_data
        )
    
    def test_initialization(self):
        """Test escalation system initialization"""
        self.assertIsNotNone(self.escalation_system)
        self.assertIsInstance(self.escalation_system.escalation_rules, dict)
        self.assertEqual(len(self.escalation_system.escalation_handlers), 0)
        
        # Check that rules exist for all severity levels
        self.assertIn(AnomalySeverity.LOW, self.escalation_system.escalation_rules)
        self.assertIn(AnomalySeverity.MEDIUM, self.escalation_system.escalation_rules)
        self.assertIn(AnomalySeverity.HIGH, self.escalation_system.escalation_rules)
        self.assertIn(AnomalySeverity.CRITICAL, self.escalation_system.escalation_rules)
    
    def test_register_escalation_handler(self):
        """Test registering escalation handlers"""
        def test_handler(alert):
            pass
        
        self.escalation_system.register_escalation_handler(test_handler)
        self.assertEqual(len(self.escalation_system.escalation_handlers), 1)
        
        # Register another handler
        self.escalation_system.register_escalation_handler(test_handler)
        self.assertEqual(len(self.escalation_system.escalation_handlers), 2)
    
    def test_check_escalation(self):
        """Test alert escalation check"""
        # Test with an alert that should not be escalated (no timeout passed)
        result = self.escalation_system.check_escalation(self.alert)
        self.assertFalse(result)
        self.assertEqual(self.alert.escalation_level, 0)
        
        # Test with handled alert (should not be escalated)
        self.alert.handled = True
        result = self.escalation_system.check_escalation(self.alert)
        self.assertFalse(result)


class TestSingletonFunctions(unittest.TestCase):
    """Test cases for singleton functions"""
    
    def test_get_alert_generator(self):
        """Test getting alert generator singleton"""
        generator1 = get_alert_generator()
        generator2 = get_alert_generator()
        
        # Should return the same instance
        self.assertIs(generator1, generator2)
        
        # Should be an instance of AlertGenerator
        self.assertIsInstance(generator1, AlertGenerator)
    
    def test_get_escalation_system(self):
        """Test getting escalation system singleton"""
        escalation1 = get_escalation_system()
        escalation2 = get_escalation_system()
        
        # Should return the same instance
        self.assertIs(escalation1, escalation2)
        
        # Should be an instance of AlertEscalationSystem
        self.assertIsInstance(escalation1, AlertEscalationSystem)


if __name__ == '__main__':
    unittest.main()