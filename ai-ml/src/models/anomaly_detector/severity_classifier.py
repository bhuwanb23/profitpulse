"""
Anomaly Severity Classification System for Anomaly Detection
Implements severity classification for detected anomalies based on multiple factors
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from enum import Enum
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


class AnomalySeverity(Enum):
    """Anomaly severity levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class AnomalySeverityClassifier:
    """Classify anomalies based on severity levels"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize severity classifier
        
        Args:
            config: Configuration dictionary with severity thresholds
        """
        self.config = config or {}
        self.severity_thresholds = self.config.get('severity_thresholds', {
            'low': 0.3,
            'medium': 0.6,
            'high': 0.8
        })
        self.feature_weights = self.config.get('feature_weights', {
            'score': 0.4,
            'frequency': 0.3,
            'impact': 0.3
        })
        logger.info("Anomaly Severity Classifier initialized")
    
    def classify_severity(self, anomaly_data: pd.DataFrame) -> List[AnomalySeverity]:
        """
        Classify severity of detected anomalies
        
        Args:
            anomaly_data: DataFrame with anomaly information including scores, features, etc.
            
        Returns:
            List of severity classifications for each anomaly
        """
        try:
            if anomaly_data.empty:
                logger.warning("Empty anomaly data provided")
                return []
            
            severities = []
            
            # Calculate severity scores for each anomaly
            for idx, row in anomaly_data.iterrows():
                severity_score = self._calculate_severity_score(row)
                severity = self._score_to_severity(severity_score)
                severities.append(severity)
            
            logger.info(f"Classified severity for {len(severities)} anomalies")
            return severities
            
        except Exception as e:
            logger.error(f"Error classifying anomaly severity: {e}")
            return [AnomalySeverity.LOW] * len(anomaly_data) if len(anomaly_data) > 0 else []
    
    def _calculate_severity_score(self, anomaly_row: pd.Series) -> float:
        """
        Calculate severity score for a single anomaly
        
        Args:
            anomaly_row: Series with anomaly data
            
        Returns:
            Severity score between 0 and 1
        """
        try:
            score = 0.0
            
            # Anomaly detection score (higher = more severe)
            detection_score = anomaly_row.get('anomaly_score', 0.5)
            score += detection_score * self.feature_weights['score']
            
            # Frequency factor (how often similar anomalies occur)
            frequency_factor = anomaly_row.get('frequency_factor', 0.5)
            score += frequency_factor * self.feature_weights['frequency']
            
            # Impact factor (business impact of anomaly)
            impact_factor = anomaly_row.get('impact_factor', 0.5)
            score += impact_factor * self.feature_weights['impact']
            
            # Ensure score is between 0 and 1
            score = max(0.0, min(1.0, score))
            return score
            
        except Exception as e:
            logger.warning(f"Error calculating severity score: {e}")
            return 0.5  # Default medium severity
    
    def _score_to_severity(self, score: float) -> AnomalySeverity:
        """
        Convert severity score to severity level
        
        Args:
            score: Severity score between 0 and 1
            
        Returns:
            AnomalySeverity level
        """
        try:
            if score >= self.severity_thresholds['high']:
                return AnomalySeverity.CRITICAL
            elif score >= self.severity_thresholds['medium']:
                return AnomalySeverity.HIGH
            elif score >= self.severity_thresholds['low']:
                return AnomalySeverity.MEDIUM
            else:
                return AnomalySeverity.LOW
        except Exception as e:
            logger.warning(f"Error converting score to severity: {e}")
            return AnomalySeverity.MEDIUM  # Default medium severity
    
    def get_severity_description(self, severity: AnomalySeverity) -> str:
        """
        Get human-readable description of severity level
        
        Args:
            severity: AnomalySeverity level
            
        Returns:
            Description of severity level
        """
        descriptions = {
            AnomalySeverity.LOW: "Low priority anomaly, minimal impact",
            AnomalySeverity.MEDIUM: "Medium priority anomaly, moderate impact",
            AnomalySeverity.HIGH: "High priority anomaly, significant impact",
            AnomalySeverity.CRITICAL: "Critical priority anomaly, immediate attention required"
        }
        return descriptions.get(severity, "Unknown severity level")
    
    def batch_classify(self, anomaly_data_list: List[pd.DataFrame]) -> List[List[AnomalySeverity]]:
        """
        Classify severity for multiple batches of anomaly data
        
        Args:
            anomaly_data_list: List of DataFrames with anomaly information
            
        Returns:
            List of severity classification lists for each batch
        """
        try:
            batch_severities = []
            for anomaly_data in anomaly_data_list:
                severities = self.classify_severity(anomaly_data)
                batch_severities.append(severities)
            return batch_severities
        except Exception as e:
            logger.error(f"Error in batch severity classification: {e}")
            return []


class AnomalyImpactAssessor:
    """Assess business impact of anomalies"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize impact assessor
        
        Args:
            config: Configuration dictionary with impact assessment parameters
        """
        self.config = config or {}
        self.impact_factors = self.config.get('impact_factors', {
            'financial': 0.4,
            'operational': 0.3,
            'reputational': 0.2,
            'regulatory': 0.1
        })
        logger.info("Anomaly Impact Assessor initialized")
    
    def assess_impact(self, anomaly_data: pd.DataFrame) -> np.ndarray:
        """
        Assess business impact of anomalies
        
        Args:
            anomaly_data: DataFrame with anomaly information
            
        Returns:
            Array of impact scores between 0 and 1
        """
        try:
            if anomaly_data.empty:
                logger.warning("Empty anomaly data provided for impact assessment")
                return np.array([])
            
            impact_scores = []
            
            for idx, row in anomaly_data.iterrows():
                financial_impact = row.get('financial_impact', 0.0)
                operational_impact = row.get('operational_impact', 0.0)
                reputational_impact = row.get('reputational_impact', 0.0)
                regulatory_impact = row.get('regulatory_impact', 0.0)
                
                # Weighted impact score
                impact_score = (
                    financial_impact * self.impact_factors['financial'] +
                    operational_impact * self.impact_factors['operational'] +
                    reputational_impact * self.impact_factors['reputational'] +
                    regulatory_impact * self.impact_factors['regulatory']
                )
                
                # Ensure score is between 0 and 1
                impact_score = max(0.0, min(1.0, impact_score))
                impact_scores.append(impact_score)
            
            logger.info(f"Assessed impact for {len(impact_scores)} anomalies")
            return np.array(impact_scores)
            
        except Exception as e:
            logger.error(f"Error assessing anomaly impact: {e}")
            return np.zeros(len(anomaly_data)) if len(anomaly_data) > 0 else np.array([])


# Global instances for easy access
severity_classifier_instance = None
impact_assessor_instance = None


def get_severity_classifier(config: Optional[Dict[str, Any]] = None) -> AnomalySeverityClassifier:
    """Get singleton severity classifier instance"""
    global severity_classifier_instance
    if severity_classifier_instance is None:
        severity_classifier_instance = AnomalySeverityClassifier(config)
    return severity_classifier_instance


def get_impact_assessor(config: Optional[Dict[str, Any]] = None) -> AnomalyImpactAssessor:
    """Get singleton impact assessor instance"""
    global impact_assessor_instance
    if impact_assessor_instance is None:
        impact_assessor_instance = AnomalyImpactAssessor(config)
    return impact_assessor_instance