"""
Revenue Recovery System for Revenue Leak Detection
Handles leak classification, recovery amount estimation, and actionable recommendations
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Conditional imports for data processing
try:
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    SKLEARN_CLUSTER_AVAILABLE = True
except ImportError:
    KMeans = None
    StandardScaler = None
    SKLEARN_CLUSTER_AVAILABLE = False

logger = logging.getLogger(__name__)


class LeakClassifier:
    """Classify different types of revenue leaks"""
    
    def __init__(self):
        """Initialize leak classifier"""
        self.leak_types = [
            'unbilled_services',
            'underbilled_contracts',
            'overdue_invoices',
            'unpaid_invoices',
            'duplicate_billing',
            'pricing_errors',
            'time_tracking_issues',
            'service_delivery_gaps'
        ]
        self.scaler = StandardScaler() if StandardScaler else None
        logger.info("Leak Classifier initialized")
    
    def classify_leaks(self, anomalies: pd.DataFrame, 
                      client_data: pd.DataFrame) -> pd.DataFrame:
        """
        Classify revenue leaks based on anomaly characteristics
        
        Args:
            anomalies: DataFrame with detected anomalies
            client_data: DataFrame with client information
            
        Returns:
            DataFrame with classified leaks
        """
        try:
            if anomalies.empty:
                logger.warning("No anomalies to classify")
                return pd.DataFrame()
            
            classified_leaks = []
            
            for _, anomaly in anomalies.iterrows():
                leak_type = self._determine_leak_type(anomaly, client_data)
                classification = {
                    'leak_id': f"LEAK-{len(classified_leaks) + 1:04d}",
                    'client_id': anomaly.get('client_id', 'UNKNOWN'),
                    'leak_type': leak_type,
                    'confidence': self._calculate_confidence(anomaly, leak_type),
                    'severity': self._determine_severity(anomaly),
                    'potential_loss': anomaly.get('potential_loss', 0.0),
                    'description': anomaly.get('description', 'Unknown leak'),
                    'timestamp': datetime.now()
                }
                classified_leaks.append(classification)
            
            return pd.DataFrame(classified_leaks)
            
        except Exception as e:
            logger.error(f"Error classifying leaks: {e}")
            return pd.DataFrame()
    
    def _determine_leak_type(self, anomaly: pd.Series, 
                           client_data: pd.DataFrame) -> str:
        """Determine the type of revenue leak"""
        try:
            anomaly_type = str(anomaly.get('anomaly_type', '')).lower()
            
            # Map anomaly types to leak types
            if 'unbilled' in anomaly_type or 'unbilled' in str(anomaly.get('description', '')).lower():
                return 'unbilled_services'
            elif 'underbilled' in anomaly_type or 'underbilled' in str(anomaly.get('description', '')).lower():
                return 'underbilled_contracts'
            elif 'overdue' in anomaly_type or 'overdue' in str(anomaly.get('description', '')).lower():
                return 'overdue_invoices'
            elif 'unpaid' in anomaly_type or 'unpaid' in str(anomaly.get('description', '')).lower():
                return 'unpaid_invoices'
            elif 'duplicate' in anomaly_type or 'duplicate' in str(anomaly.get('description', '')).lower():
                return 'duplicate_billing'
            elif 'pricing' in anomaly_type or 'pricing' in str(anomaly.get('description', '')).lower():
                return 'pricing_errors'
            elif 'time' in anomaly_type or 'time' in str(anomaly.get('description', '')).lower():
                return 'time_tracking_issues'
            elif 'service' in anomaly_type or 'service' in str(anomaly.get('description', '')).lower():
                return 'service_delivery_gaps'
            else:
                # Use clustering for unknown types if possible
                return self._cluster_based_classification(anomaly, client_data)
                
        except Exception as e:
            logger.warning(f"Error determining leak type: {e}")
            return 'unclassified'
    
    def _cluster_based_classification(self, anomaly: pd.Series, 
                                    client_data: pd.DataFrame) -> str:
        """Use clustering to classify unknown leak types"""
        try:
            if not SKLEARN_CLUSTER_AVAILABLE or KMeans is None:
                return 'unclassified'
            
            # Extract features for clustering
            features = []
            feature_names = []
            
            # Numerical features
            for col in ['potential_loss', 'amount', 'hours_logged', 'hours_billed']:
                if col in anomaly:
                    features.append(float(anomaly[col]))
                    feature_names.append(col)
            
            # If we have features, try clustering
            if len(features) > 0 and self.scaler is not None:
                # In a real implementation, we would have trained clusters
                # For now, we'll randomly assign based on feature magnitude
                feature_sum = sum(features)
                cluster_idx = int(feature_sum) % len(self.leak_types)
                return self.leak_types[cluster_idx]
            else:
                return 'unclassified'
                
        except Exception as e:
            logger.warning(f"Error in cluster-based classification: {e}")
            return 'unclassified'
    
    def _calculate_confidence(self, anomaly: pd.Series, leak_type: str) -> float:
        """Calculate confidence score for leak classification"""
        try:
            # Base confidence on potential loss amount
            potential_loss = float(anomaly.get('potential_loss', 0) or 0)
            confidence = min(potential_loss / 1000.0, 1.0)  # Normalize by $1000
            
            # Adjust based on leak type specificity
            if leak_type != 'unclassified':
                confidence *= 1.2  # Boost confidence for known types
            
            # Cap at 1.0
            return min(confidence, 1.0)
            
        except Exception as e:
            logger.warning(f"Error calculating confidence: {e}")
            return 0.5
    
    def _determine_severity(self, anomaly: pd.Series) -> str:
        """Determine severity level of a leak"""
        try:
            potential_loss = float(anomaly.get('potential_loss', 0) or 0)
            severity = str(anomaly.get('severity', 'medium')).lower()
            
            # Override based on potential loss
            if potential_loss > 10000:
                return 'critical'
            elif potential_loss > 5000:
                return 'high'
            elif potential_loss > 1000:
                return 'medium'
            else:
                return severity if severity in ['low', 'medium', 'high', 'critical'] else 'low'
                
        except Exception as e:
            logger.warning(f"Error determining severity: {e}")
            return 'medium'


class RecoveryAmountEstimator:
    """Estimate recovery amounts for detected revenue leaks"""
    
    def __init__(self):
        """Initialize recovery amount estimator"""
        logger.info("Recovery Amount Estimator initialized")
    
    def estimate_recovery(self, classified_leaks: pd.DataFrame, 
                         client_data: pd.DataFrame) -> pd.DataFrame:
        """
        Estimate recovery amounts for classified leaks
        
        Args:
            classified_leaks: DataFrame with classified leaks
            client_data: DataFrame with client information
            
        Returns:
            DataFrame with recovery estimates
        """
        try:
            if classified_leaks.empty:
                logger.warning("No classified leaks to estimate recovery for")
                return pd.DataFrame()
            
            recovery_estimates = []
            
            for _, leak in classified_leaks.iterrows():
                estimate = self._calculate_recovery_estimate(leak, client_data)
                recovery_estimates.append(estimate)
            
            return pd.DataFrame(recovery_estimates)
            
        except Exception as e:
            logger.error(f"Error estimating recovery amounts: {e}")
            return pd.DataFrame()
    
    def _calculate_recovery_estimate(self, leak: pd.Series, 
                                   client_data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate recovery estimate for a single leak"""
        try:
            client_id = leak.get('client_id', 'UNKNOWN')
            leak_type = str(leak.get('leak_type', 'unclassified') or 'unclassified')
            potential_loss = float(leak.get('potential_loss', 0) or 0)
            
            # Get client information
            client_info = client_data[client_data['client_id'] == client_id].iloc[0] if not client_data.empty and client_id in client_data['client_id'].values else None
            
            # Base recovery estimate
            base_estimate = potential_loss
            
            # Adjust based on leak type
            adjustment_factor = self._get_adjustment_factor(leak_type, client_info)
            adjusted_estimate = base_estimate * adjustment_factor
            
            # Calculate confidence interval
            confidence_level = float(leak.get('confidence', 0.5) or 0.5)
            lower_bound = adjusted_estimate * (0.8 + 0.2 * confidence_level)
            upper_bound = adjusted_estimate * (1.2 - 0.2 * confidence_level)
            
            estimate = {
                'leak_id': leak.get('leak_id', ''),
                'client_id': client_id,
                'base_estimate': base_estimate,
                'adjusted_estimate': adjusted_estimate,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound,
                'confidence_level': confidence_level,
                'recovery_probability': self._calculate_recovery_probability(leak_type, client_info),
                'estimated_timeline': self._estimate_recovery_timeline(leak_type),
                'timestamp': datetime.now()
            }
            
            return estimate
            
        except Exception as e:
            logger.error(f"Error calculating recovery estimate: {e}")
            return {
                'leak_id': leak.get('leak_id', ''),
                'client_id': leak.get('client_id', 'UNKNOWN'),
                'base_estimate': 0.0,
                'adjusted_estimate': 0.0,
                'lower_bound': 0.0,
                'upper_bound': 0.0,
                'confidence_level': 0.0,
                'recovery_probability': 0.0,
                'estimated_timeline': 'Unknown',
                'timestamp': datetime.now(),
                'error': str(e)
            }
    
    def _get_adjustment_factor(self, leak_type: str, 
                             client_info: Optional[pd.Series]) -> float:
        """Get adjustment factor based on leak type and client information"""
        try:
            # Base factors by leak type
            factors = {
                'unbilled_services': 0.95,      # High recovery probability
                'underbilled_contracts': 0.90,  # High recovery probability
                'overdue_invoices': 0.85,       # Medium-high recovery probability
                'unpaid_invoices': 0.70,        # Medium recovery probability
                'duplicate_billing': 0.95,      # High recovery probability (refund)
                'pricing_errors': 0.80,         # Medium-high recovery probability
                'time_tracking_issues': 0.75,   # Medium recovery probability
                'service_delivery_gaps': 0.60,  # Lower recovery probability
                'unclassified': 0.50            # Low recovery probability
            }
            
            factor = factors.get(leak_type, 0.50)
            
            # Adjust based on client payment history if available
            if client_info is not None:
                payment_ratio = float(client_info.get('payment_ratio', 0.8) or 0.8)
                if payment_ratio > 0.9:
                    factor *= 1.1  # Good payment history
                elif payment_ratio < 0.5:
                    factor *= 0.8  # Poor payment history
            
            return min(factor, 1.0)  # Cap at 1.0
            
        except Exception as e:
            logger.warning(f"Error getting adjustment factor: {e}")
            return 0.75  # Default factor
    
    def _calculate_recovery_probability(self, leak_type: str, 
                                     client_info: Optional[pd.Series]) -> float:
        """Calculate probability of successful recovery"""
        try:
            # Base probabilities by leak type
            probabilities = {
                'unbilled_services': 0.90,
                'underbilled_contracts': 0.85,
                'overdue_invoices': 0.75,
                'unpaid_invoices': 0.60,
                'duplicate_billing': 0.95,
                'pricing_errors': 0.70,
                'time_tracking_issues': 0.65,
                'service_delivery_gaps': 0.50,
                'unclassified': 0.40
            }
            
            probability = probabilities.get(leak_type, 0.50)
            
            # Adjust based on client information
            if client_info is not None:
                # Adjust based on client relationship length
                client_age = int(client_info.get('client_age', 2) or 2)
                if client_age > 5:
                    probability *= 1.1  # Long-term clients more likely to resolve
                elif client_age < 1:
                    probability *= 0.9  # New clients less likely to resolve
                
                # Adjust based on satisfaction score
                satisfaction = float(client_info.get('satisfaction_score', 0.7) or 0.7)
                if satisfaction > 0.8:
                    probability *= 1.1
                elif satisfaction < 0.5:
                    probability *= 0.8
            
            return min(probability, 1.0)
            
        except Exception as e:
            logger.warning(f"Error calculating recovery probability: {e}")
            return 0.65  # Default probability
    
    def _estimate_recovery_timeline(self, leak_type: str) -> str:
        """Estimate timeline for recovery"""
        try:
            # Estimated timelines by leak type
            timelines = {
                'unbilled_services': '1-2 weeks',
                'underbilled_contracts': '2-4 weeks',
                'overdue_invoices': '1-4 weeks',
                'unpaid_invoices': '4-12 weeks',
                'duplicate_billing': '1-2 weeks',
                'pricing_errors': '2-6 weeks',
                'time_tracking_issues': '2-8 weeks',
                'service_delivery_gaps': '4-16 weeks',
                'unclassified': '4-12 weeks'
            }
            
            return timelines.get(leak_type, '4-12 weeks')
            
        except Exception as e:
            logger.warning(f"Error estimating recovery timeline: {e}")
            return '4-12 weeks'


class RecommendationEngine:
    """Generate actionable recommendations for revenue leak recovery"""
    
    def __init__(self):
        """Initialize recommendation engine"""
        logger.info("Recommendation Engine initialized")
    
    def generate_recommendations(self, classified_leaks: pd.DataFrame, 
                               recovery_estimates: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Generate actionable recommendations for revenue leak recovery
        
        Args:
            classified_leaks: DataFrame with classified leaks
            recovery_estimates: DataFrame with recovery estimates
            
        Returns:
            List of recommendation dictionaries
        """
        try:
            if classified_leaks.empty:
                logger.warning("No classified leaks to generate recommendations for")
                return []
            
            recommendations = []
            
            for _, leak in classified_leaks.iterrows():
                recommendation = self._generate_leak_recommendation(leak, recovery_estimates)
                recommendations.append(recommendation)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return []
    
    def _generate_leak_recommendation(self, leak: pd.Series, 
                                    recovery_estimates: pd.DataFrame) -> Dict[str, Any]:
        """Generate recommendation for a single leak"""
        try:
            leak_id = leak.get('leak_id', '')
            client_id = leak.get('client_id', 'UNKNOWN')
            leak_type = leak.get('leak_type', 'unclassified')
            severity = leak.get('severity', 'medium')
            potential_loss = float(leak.get('potential_loss', 0) or 0)
            
            # Get recovery estimate for this leak
            estimate_row = recovery_estimates[recovery_estimates['leak_id'] == leak_id]
            if not estimate_row.empty and len(estimate_row) > 0:
                try:
                    # Try to get the first value safely
                    if hasattr(estimate_row['adjusted_estimate'], 'iloc'):
                        recovery_estimate = float(estimate_row['adjusted_estimate'].iloc[0])
                    elif hasattr(estimate_row['adjusted_estimate'], '__iter__'):
                        recovery_estimate = float(list(estimate_row['adjusted_estimate'])[0])
                    else:
                        recovery_estimate = float(estimate_row['adjusted_estimate'])
                except:
                    recovery_estimate = potential_loss
                try:
                    if hasattr(estimate_row['recovery_probability'], 'iloc'):
                      recovery_probability = float(estimate_row['recovery_probability'].iloc[0])
                    elif hasattr(estimate_row['recovery_probability'], '__iter__'):
                        recovery_probability = float(list(estimate_row['recovery_probability'])[0])
                    else:
                        recovery_probability = float(estimate_row['recovery_probability'])
                except:
                    recovery_probability = 0.65
            else:
                recovery_estimate = potential_loss
                recovery_probability = 0.65
            
            # Generate recommendation based on leak type
            recommendation_text = self._generate_recommendation_text(
                str(leak_type), str(client_id), recovery_estimate, str(severity)
            )
            
            # Determine priority
            priority = self._determine_priority(str(severity), recovery_estimate, recovery_probability)
            
            # Determine action owner
            action_owner = self._determine_action_owner(str(leak_type))
            
            # Determine follow-up timeline
            follow_up_timeline = self._determine_follow_up_timeline(priority)
            
            recommendation = {
                'recommendation_id': f"REC-{np.random.randint(1000, 9999)}",
                'leak_id': leak_id,
                'client_id': client_id,
                'leak_type': leak_type,
                'recommendation': recommendation_text,
                'priority': priority,
                'action_owner': action_owner,
                'estimated_value': recovery_estimate,
                'recovery_probability': recovery_probability,
                'follow_up_timeline': follow_up_timeline,
                'implementation_steps': self._generate_implementation_steps(str(leak_type)),
                'success_metrics': self._define_success_metrics(str(leak_type)),
                'timestamp': datetime.now()
            }
            
            return recommendation
            
        except Exception as e:
            logger.error(f"Error generating leak recommendation: {e}")
            return {
                'recommendation_id': f"REC-{np.random.randint(1000, 9999)}",
                'leak_id': leak.get('leak_id', ''),
                'client_id': leak.get('client_id', 'UNKNOWN'),
                'leak_type': leak.get('leak_type', 'unclassified'),
                'recommendation': 'Unable to generate specific recommendation due to system error',
                'priority': 'medium',
                'action_owner': 'Account Manager',
                'estimated_value': 0.0,
                'recovery_probability': 0.0,
                'follow_up_timeline': '2 weeks',
                'implementation_steps': ['Investigate system error', 'Contact client'],
                'success_metrics': ['Issue resolved'],
                'timestamp': datetime.now(),
                'error': str(e)
            }
    
    def _generate_recommendation_text(self, leak_type: str, client_id: str, 
                                    recovery_estimate: float, severity: str) -> str:
        """Generate recommendation text based on leak type"""
        try:
            base_texts = {
                'unbilled_services': f"Client {client_id} has unbilled services worth ${recovery_estimate:.2f}. Recommend reviewing time logs and generating invoices for unbilled work.",
                'underbilled_contracts': f"Client {client_id} has underbilled contracts. Recommend reviewing contract terms and adjusting billing to match actual service delivery.",
                'overdue_invoices': f"Client {client_id} has overdue invoices totaling ${recovery_estimate:.2f}. Recommend following up with payment reminders and establishing payment plans.",
                'unpaid_invoices': f"Client {client_id} has unpaid invoices worth ${recovery_estimate:.2f}. Recommend escalating to collections or legal team if necessary.",
                'duplicate_billing': f"Client {client_id} has been billed twice for services. Recommend issuing refunds or credits immediately.",
                'pricing_errors': f"Client {client_id} has pricing errors in billing. Recommend reviewing pricing structure and correcting invoices.",
                'time_tracking_issues': f"Client {client_id} has time tracking discrepancies. Recommend auditing time logs and reconciling with billing records.",
                'service_delivery_gaps': f"Client {client_id} has service delivery gaps. Recommend reviewing service level agreements and ensuring compliance.",
                'unclassified': f"Client {client_id} has an unclassified revenue leak worth ${recovery_estimate:.2f}. Recommend investigating further to determine root cause."
            }
            
            return base_texts.get(leak_type, f"Client {client_id} has a revenue leak of type '{leak_type}' worth ${recovery_estimate:.2f}. Recommend investigation and corrective action.")
            
        except Exception as e:
            logger.warning(f"Error generating recommendation text: {e}")
            return f"Client {client_id} has a revenue leak worth ${recovery_estimate:.2f}. Recommend investigation and corrective action."
    
    def _determine_priority(self, severity: str, recovery_estimate: float, 
                          recovery_probability: float) -> str:
        """Determine priority level for recommendation"""
        try:
            # Calculate priority score
            severity_score = {'low': 1, 'medium': 2, 'high': 3, 'critical': 4}.get(severity.lower(), 2)
            value_score = min(recovery_estimate / 1000, 5)  # Normalize by $1000
            probability_score = recovery_probability * 3
            
            total_score = severity_score + value_score + probability_score
            
            if total_score >= 10:
                return 'critical'
            elif total_score >= 7:
                return 'high'
            elif total_score >= 4:
                return 'medium'
            else:
                return 'low'
                
        except Exception as e:
            logger.warning(f"Error determining priority: {e}")
            return 'medium'
    
    def _determine_action_owner(self, leak_type: str) -> str:
        """Determine who should own the action"""
        try:
            owners = {
                'unbilled_services': 'Billing Specialist',
                'underbilled_contracts': 'Account Manager',
                'overdue_invoices': 'Collections Specialist',
                'unpaid_invoices': 'Collections Manager',
                'duplicate_billing': 'Billing Specialist',
                'pricing_errors': 'Account Manager',
                'time_tracking_issues': 'Operations Manager',
                'service_delivery_gaps': 'Service Delivery Manager',
                'unclassified': 'Account Manager'
            }
            
            return owners.get(leak_type, 'Account Manager')
            
        except Exception as e:
            logger.warning(f"Error determining action owner: {e}")
            return 'Account Manager'
    
    def _determine_follow_up_timeline(self, priority: str) -> str:
        """Determine follow-up timeline based on priority"""
        try:
            timelines = {
                'critical': '24-48 hours',
                'high': '1 week',
                'medium': '2 weeks',
                'low': '1 month'
            }
            
            return timelines.get(priority, '2 weeks')
            
        except Exception as e:
            logger.warning(f"Error determining follow-up timeline: {e}")
            return '2 weeks'
    
    def _generate_implementation_steps(self, leak_type: str) -> List[str]:
        """Generate implementation steps for a leak type"""
        try:
            step_templates = {
                'unbilled_services': [
                    'Review time logs for unbilled hours',
                    'Verify service delivery with client',
                    'Prepare and send invoice for unbilled services',
                    'Update billing system to prevent future occurrences'
                ],
                'underbilled_contracts': [
                    'Review contract terms and service delivery records',
                    'Calculate correct billing amount',
                    'Prepare adjustment invoice',
                    'Communicate changes to client'
                ],
                'overdue_invoices': [
                    'Send payment reminder notice',
                    'Establish payment plan with client',
                    'Escalate to collections if no response',
                    'Document all communication'
                ],
                'unpaid_invoices': [
                    'Send formal demand letter',
                    'Engage collections agency if necessary',
                    'Consider legal action for large amounts',
                    'Write off if recovery unlikely'
                ],
                'duplicate_billing': [
                    'Identify duplicate transactions',
                    'Issue refund or credit to client',
                    'Update accounting records',
                    'Implement controls to prevent recurrence'
                ],
                'pricing_errors': [
                    'Audit pricing structures',
                    'Identify affected clients',
                    'Calculate correct amounts',
                    'Issue corrected invoices'
                ],
                'time_tracking_issues': [
                    'Audit time tracking records',
                    'Reconcile with billing data',
                    'Train staff on proper procedures',
                    'Implement automated time tracking'
                ],
                'service_delivery_gaps': [
                    'Review service level agreements',
                    'Assess service delivery performance',
                    'Identify root causes of gaps',
                    'Implement corrective measures'
                ],
                'unclassified': [
                    'Investigate root cause of leak',
                    'Determine appropriate corrective action',
                    'Assign responsibility for resolution',
                    'Monitor for recurrence'
                ]
            }
            
            return step_templates.get(leak_type, [
                'Investigate the issue',
                'Determine root cause',
                'Develop corrective action plan',
                'Implement solution and monitor results'
            ])
            
        except Exception as e:
            logger.warning(f"Error generating implementation steps: {e}")
            return ['Investigate the issue', 'Determine root cause', 'Develop corrective action plan', 'Implement solution']
    
    def _define_success_metrics(self, leak_type: str) -> List[str]:
        """Define success metrics for a leak type"""
        try:
            metrics_templates = {
                'unbilled_services': [
                    'Amount recovered from unbilled services',
                    'Percentage of unbilled hours invoiced',
                    'Time to invoice unbilled services'
                ],
                'underbilled_contracts': [
                    'Additional revenue recovered',
                    'Client satisfaction with billing accuracy',
                    'Number of billing disputes resolved'
                ],
                'overdue_invoices': [
                    'Percentage of overdue invoices collected',
                    'Average collection time',
                    'Bad debt reduction'
                ],
                'unpaid_invoices': [
                    'Amount recovered from unpaid invoices',
                    'Collection agency success rate',
                    'Legal action recovery rate'
                ],
                'duplicate_billing': [
                    'Number of duplicate bills corrected',
                    'Amount refunded to clients',
                    'Prevention of future duplicates'
                ],
                'pricing_errors': [
                    'Number of pricing errors corrected',
                    'Revenue impact of corrections',
                    'Client billing accuracy improvement'
                ],
                'time_tracking_issues': [
                    'Time tracking accuracy improvement',
                    'Billing accuracy improvement',
                    'Staff compliance with tracking procedures'
                ],
                'service_delivery_gaps': [
                    'Service level agreement compliance',
                    'Client satisfaction improvement',
                    'Gap resolution rate'
                ],
                'unclassified': [
                    'Issue resolution time',
                    'Prevention of recurrence',
                    'Financial impact recovery'
                ]
            }
            
            return metrics_templates.get(leak_type, [
                'Issue resolution time',
                'Financial impact recovery',
                'Prevention of recurrence'
            ])
            
        except Exception as e:
            logger.warning(f"Error defining success metrics: {e}")
            return ['Issue resolution time', 'Financial impact recovery', 'Prevention of recurrence']


# Global instances for easy access
leak_classifier_instance = None
recovery_estimator_instance = None
recommendation_engine_instance = None


async def get_leak_classifier() -> LeakClassifier:
    """Get singleton leak classifier instance"""
    global leak_classifier_instance
    if leak_classifier_instance is None:
        leak_classifier_instance = LeakClassifier()
    return leak_classifier_instance


async def get_recovery_estimator() -> RecoveryAmountEstimator:
    """Get singleton recovery estimator instance"""
    global recovery_estimator_instance
    if recovery_estimator_instance is None:
        recovery_estimator_instance = RecoveryAmountEstimator()
    return recovery_estimator_instance


async def get_recommendation_engine() -> RecommendationEngine:
    """Get singleton recommendation engine instance"""
    global recommendation_engine_instance
    if recommendation_engine_instance is None:
        recommendation_engine_instance = RecommendationEngine()
    return recommendation_engine_instance