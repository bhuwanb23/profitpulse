"""
Unit tests for severity classifier components
"""

import unittest
import numpy as np
import pandas as pd
from datetime import datetime

from src.models.anomaly_detector.severity_classifier import (
    AnomalySeverity,
    AnomalySeverityClassifier,
    AnomalyImpactAssessor,
    get_severity_classifier,
    get_impact_assessor
)


class TestAnomalySeverity(unittest.TestCase):
    """Test cases for AnomalySeverity enum"""
    
    def test_severity_values(self):
        """Test severity enum values"""
        self.assertEqual(AnomalySeverity.LOW.value, 1)
        self.assertEqual(AnomalySeverity.MEDIUM.value, 2)
        self.assertEqual(AnomalySeverity.HIGH.value, 3)
        self.assertEqual(AnomalySeverity.CRITICAL.value, 4)
    
    def test_severity_names(self):
        """Test severity enum names"""
        self.assertEqual(AnomalySeverity.LOW.name, 'LOW')
        self.assertEqual(AnomalySeverity.MEDIUM.name, 'MEDIUM')
        self.assertEqual(AnomalySeverity.HIGH.name, 'HIGH')
        self.assertEqual(AnomalySeverity.CRITICAL.name, 'CRITICAL')


class TestAnomalySeverityClassifier(unittest.TestCase):
    """Test cases for AnomalySeverityClassifier"""
    
    def setUp(self):
        """Set up test data"""
        self.classifier = AnomalySeverityClassifier()
        
        # Sample anomaly data
        self.sample_anomaly_data = pd.DataFrame([
            {
                'anomaly_score': 0.8,
                'frequency_factor': 0.6,
                'impact_factor': 0.7
            },
            {
                'anomaly_score': 0.3,
                'frequency_factor': 0.2,
                'impact_factor': 0.1
            }
        ])
    
    def test_initialization(self):
        """Test classifier initialization"""
        self.assertIsNotNone(self.classifier)
        self.assertIsInstance(self.classifier.severity_thresholds, dict)
        self.assertIsInstance(self.classifier.feature_weights, dict)
        
        # Check default thresholds
        self.assertIn('low', self.classifier.severity_thresholds)
        self.assertIn('medium', self.classifier.severity_thresholds)
        self.assertIn('high', self.classifier.severity_thresholds)
    
    def test_calculate_severity_score(self):
        """Test severity score calculation"""
        # Test with a single row
        sample_row = pd.Series({
            'anomaly_score': 0.8,
            'frequency_factor': 0.6,
            'impact_factor': 0.7
        })
        
        score = self.classifier._calculate_severity_score(sample_row)
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
    
    def test_score_to_severity(self):
        """Test score to severity conversion"""
        # Test low severity
        low_severity = self.classifier._score_to_severity(0.2)
        self.assertEqual(low_severity, AnomalySeverity.LOW)
        
        # Test medium severity
        medium_severity = self.classifier._score_to_severity(0.5)
        self.assertEqual(medium_severity, AnomalySeverity.MEDIUM)
        
        # Test high severity
        high_severity = self.classifier._score_to_severity(0.7)
        self.assertEqual(high_severity, AnomalySeverity.HIGH)
        
        # Test critical severity
        critical_severity = self.classifier._score_to_severity(0.9)
        self.assertEqual(critical_severity, AnomalySeverity.CRITICAL)
    
    def test_classify_severity(self):
        """Test severity classification"""
        severities = self.classifier.classify_severity(self.sample_anomaly_data)
        self.assertEqual(len(severities), len(self.sample_anomaly_data))
        
        # Check that all results are AnomalySeverity instances
        for severity in severities:
            self.assertIsInstance(severity, AnomalySeverity)
    
    def test_get_severity_description(self):
        """Test severity description retrieval"""
        # Test all severity levels
        low_desc = self.classifier.get_severity_description(AnomalySeverity.LOW)
        self.assertIn("Low priority", low_desc)
        
        medium_desc = self.classifier.get_severity_description(AnomalySeverity.MEDIUM)
        self.assertIn("Medium priority", medium_desc)
        
        high_desc = self.classifier.get_severity_description(AnomalySeverity.HIGH)
        self.assertIn("High priority", high_desc)
        
        critical_desc = self.classifier.get_severity_description(AnomalySeverity.CRITICAL)
        self.assertIn("Critical priority", critical_desc)
    
    def test_batch_classify(self):
        """Test batch severity classification"""
        # Create list of DataFrames
        batch_data = [self.sample_anomaly_data, self.sample_anomaly_data]
        batch_severities = self.classifier.batch_classify(batch_data)
        
        self.assertEqual(len(batch_severities), 2)
        for severities in batch_severities:
            self.assertEqual(len(severities), len(self.sample_anomaly_data))


class TestAnomalyImpactAssessor(unittest.TestCase):
    """Test cases for AnomalyImpactAssessor"""
    
    def setUp(self):
        """Set up test data"""
        self.assessor = AnomalyImpactAssessor()
        
        # Sample anomaly data with impact factors
        self.sample_anomaly_data = pd.DataFrame([
            {
                'financial_impact': 0.8,
                'operational_impact': 0.6,
                'reputational_impact': 0.7,
                'regulatory_impact': 0.5
            },
            {
                'financial_impact': 0.3,
                'operational_impact': 0.2,
                'reputational_impact': 0.1,
                'regulatory_impact': 0.1
            }
        ])
    
    def test_initialization(self):
        """Test assessor initialization"""
        self.assertIsNotNone(self.assessor)
        self.assertIsInstance(self.assessor.impact_factors, dict)
        
        # Check default impact factors
        self.assertIn('financial', self.assessor.impact_factors)
        self.assertIn('operational', self.assessor.impact_factors)
        self.assertIn('reputational', self.assessor.impact_factors)
        self.assertIn('regulatory', self.assessor.impact_factors)
    
    def test_assess_impact(self):
        """Test impact assessment"""
        impact_scores = self.assessor.assess_impact(self.sample_anomaly_data)
        
        self.assertIsInstance(impact_scores, np.ndarray)
        self.assertEqual(len(impact_scores), len(self.sample_anomaly_data))
        
        # Check that scores are between 0 and 1
        for score in impact_scores:
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 1.0)


class TestSingletonFunctions(unittest.TestCase):
    """Test cases for singleton functions"""
    
    def test_get_severity_classifier(self):
        """Test getting severity classifier singleton"""
        classifier1 = get_severity_classifier()
        classifier2 = get_severity_classifier()
        
        # Should return the same instance
        self.assertIs(classifier1, classifier2)
        
        # Should be an instance of AnomalySeverityClassifier
        self.assertIsInstance(classifier1, AnomalySeverityClassifier)
    
    def test_get_impact_assessor(self):
        """Test getting impact assessor singleton"""
        assessor1 = get_impact_assessor()
        assessor2 = get_impact_assessor()
        
        # Should return the same instance
        self.assertIs(assessor1, assessor2)
        
        # Should be an instance of AnomalyImpactAssessor
        self.assertIsInstance(assessor1, AnomalyImpactAssessor)


if __name__ == '__main__':
    unittest.main()