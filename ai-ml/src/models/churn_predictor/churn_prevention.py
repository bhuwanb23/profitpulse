"""
Churn Prevention System for Client Churn Prediction
Handles risk scoring, recommendations, and early warning systems
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


class ChurnRiskScorer:
    """Calculates churn risk scores for clients"""
    
    def __init__(self):
        """Initialize churn risk scorer"""
        logger.info("Churn Risk Scorer initialized")
    
    def calculate_risk_score(self, client_features: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate churn risk score for clients
        
        Args:
            client_features: DataFrame with client features
            
        Returns:
            DataFrame with risk scores added
        """
        try:
            client_features = client_features.copy()
            
            # Initialize risk score
            client_features['churn_risk_score'] = 0.0
            
            # Risk factors (weights can be adjusted based on domain knowledge)
            risk_factors = {
                'late_payment_ratio': 0.2,
                'sla_breach_ratio': 0.15,
                'days_until_contract_end': 0.1,
                'avg_satisfaction_score': -0.1,  # Negative because lower satisfaction increases risk
                'support_tickets': 0.1,
                'interactions_per_month': -0.05,  # Negative because fewer interactions increases risk
                'contract_duration_days': -0.1,  # Negative because shorter contracts increase risk
                'payment_to_contract_ratio': -0.1  # Negative because lower payment ratio increases risk
            }
            
            # Calculate weighted risk score
            for factor, weight in risk_factors.items():
                if factor in client_features.columns:
                    # Normalize the factor (0-1 range)
                    factor_values = client_features[factor]
                    if factor_values.max() != factor_values.min():
                        normalized_values = (factor_values - factor_values.min()) / (factor_values.max() - factor_values.min())
                    else:
                        normalized_values = np.zeros(len(factor_values))
                    
                    # Apply weight and add to risk score
                    if 'avg_satisfaction_score' in factor or 'interactions_per_month' in factor or 'contract_duration_days' in factor or 'payment_to_contract_ratio' in factor:
                        # For inverse factors, we subtract from 1
                        client_features['churn_risk_score'] += weight * (1 - normalized_values)
                    else:
                        client_features['churn_risk_score'] += weight * normalized_values
            
            # Ensure risk score is between 0 and 1
            client_features['churn_risk_score'] = np.clip(client_features['churn_risk_score'], 0, 1)
            
            # Create risk categories
            client_features['risk_category'] = pd.cut(
                client_features['churn_risk_score'],
                bins=[0, 0.3, 0.6, 1.0],
                labels=['Low', 'Medium', 'High'],
                include_lowest=True
            )
            
            logger.info(f"Calculated risk scores for {len(client_features)} clients")
            return client_features
            
        except Exception as e:
            logger.error(f"Error calculating risk scores: {e}")
            return client_features


class ChurnRecommendationEngine:
    """Generates retention recommendations for clients at risk of churning"""
    
    def __init__(self):
        """Initialize recommendation engine"""
        logger.info("Churn Recommendation Engine initialized")
    
    def generate_recommendations(self, client_features: pd.DataFrame) -> pd.DataFrame:
        """
        Generate retention recommendations for clients
        
        Args:
            client_features: DataFrame with client features and risk scores
            
        Returns:
            DataFrame with recommendations added
        """
        try:
            client_features = client_features.copy()
            
            # Initialize recommendations column
            client_features['recommendations'] = ""
            
            # Generate recommendations based on risk factors
            for idx, client in client_features.iterrows():
                recommendations = []
                
                # Payment-related recommendations
                late_payment_ratio = client.get('late_payment_ratio', 0)
                if late_payment_ratio is not None and late_payment_ratio > 0.2:
                    recommendations.append("Offer flexible payment plans to improve payment behavior")
                
                payment_to_contract_ratio = client.get('payment_to_contract_ratio', 0)
                if payment_to_contract_ratio is not None and payment_to_contract_ratio < 0.8:
                    recommendations.append("Review contract terms and consider value-added services")
                
                # Service-related recommendations
                sla_breach_ratio = client.get('sla_breach_ratio', 0)
                if sla_breach_ratio is not None and sla_breach_ratio > 0.1:
                    recommendations.append("Assign dedicated support team to improve service quality")
                
                support_tickets = client.get('support_tickets', 0)
                if support_tickets is not None and support_tickets > 5:
                    recommendations.append("Schedule proactive check-ins to address issues early")
                
                # Engagement-related recommendations
                interactions_per_month = client.get('interactions_per_month', 0)
                if interactions_per_month is not None and interactions_per_month < 1:
                    recommendations.append("Increase engagement through regular communication and updates")
                
                avg_satisfaction_score = client.get('avg_satisfaction_score', 10)
                if avg_satisfaction_score is not None and avg_satisfaction_score < 7:
                    recommendations.append("Conduct satisfaction survey to identify specific pain points")
                
                # Contract-related recommendations
                days_until_contract_end = client.get('days_until_contract_end', 365)
                if days_until_contract_end is not None and days_until_contract_end < 60:
                    recommendations.append("Initiate contract renewal discussions early")
                
                contract_duration_days = client.get('contract_duration_days', 365)
                if contract_duration_days is not None and contract_duration_days < 180:
                    recommendations.append("Offer long-term contract discounts for increased commitment")
                
                # High-risk clients
                churn_risk_score = client.get('churn_risk_score', 0)
                if churn_risk_score is not None and churn_risk_score > 0.7:
                    recommendations.append("Escalate to account management team for immediate intervention")
                    recommendations.append("Prepare retention offer with significant value proposition")
                
                # Medium-risk clients
                elif churn_risk_score is not None and churn_risk_score > 0.4:
                    recommendations.append("Schedule account review meeting to discuss improvements")
                    recommendations.append("Offer loyalty incentives to strengthen relationship")
                
                # Low-risk clients
                else:
                    recommendations.append("Maintain regular communication to ensure continued satisfaction")
                    recommendations.append("Consider upselling opportunities for additional services")
                
                # Join recommendations
                client_features.loc[idx, 'recommendations'] = "; ".join(recommendations)
            
            logger.info(f"Generated recommendations for {len(client_features)} clients")
            return client_features
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return client_features


class ChurnEarlyWarningSystem:
    """Early warning system for identifying clients at risk of churning"""
    
    def __init__(self, risk_threshold: float = 0.5):
        """
        Initialize early warning system
        
        Args:
            risk_threshold: Threshold for identifying high-risk clients
        """
        self.risk_threshold = risk_threshold
        logger.info("Churn Early Warning System initialized")
    
    def identify_high_risk_clients(self, client_features: pd.DataFrame) -> pd.DataFrame:
        """
        Identify clients at high risk of churning
        
        Args:
            client_features: DataFrame with client features and risk scores
            
        Returns:
            DataFrame with high-risk clients
        """
        try:
            # Filter high-risk clients
            high_risk_clients = client_features[
                client_features['churn_risk_score'] >= self.risk_threshold
            ].copy()
            
            # Sort by risk score (highest first)
            high_risk_clients = high_risk_clients.iloc[high_risk_clients['churn_risk_score'].argsort()[::-1]]
            
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
            alerts = []
            
            for _, client in high_risk_clients.iterrows():
                # Determine alert severity
                if client['churn_risk_score'] >= 0.8:
                    severity = 'critical'
                elif client['churn_risk_score'] >= 0.6:
                    severity = 'high'
                else:
                    severity = 'medium'
                
                # Create alert
                alert = {
                    'alert_id': f"CHURN-{client['client_id']}-{datetime.now().strftime('%Y%m%d')}",
                    'client_id': client['client_id'],
                    'client_name': client.get('client_name', 'Unknown'),
                    'risk_score': float(client['churn_risk_score']),
                    'risk_category': str(client['risk_category']),
                    'severity': severity,
                    'timestamp': datetime.now(),
                    'recommendations': client.get('recommendations', ''),
                    'trigger_factors': self._identify_trigger_factors(client)
                }
                
                alerts.append(alert)
            
            logger.info(f"Generated {len(alerts)} churn alerts")
            return alerts
            
        except Exception as e:
            logger.error(f"Error generating alerts: {e}")
            return []
    
    def _identify_trigger_factors(self, client: pd.Series) -> List[str]:
        """
        Identify factors that triggered the churn risk alert
        
        Args:
            client: Series with client data
            
        Returns:
            List of trigger factors
        """
        try:
            factors = []
            
            # Payment issues
            late_payment_ratio = client.get('late_payment_ratio', 0)
            if late_payment_ratio is not None and late_payment_ratio > 0.3:
                factors.append("High late payment ratio")
            
            payment_to_contract_ratio = client.get('payment_to_contract_ratio', 0)
            if payment_to_contract_ratio is not None and payment_to_contract_ratio < 0.7:
                factors.append("Low payment to contract ratio")
            
            # Service issues
            sla_breach_ratio = client.get('sla_breach_ratio', 0)
            if sla_breach_ratio is not None and sla_breach_ratio > 0.15:
                factors.append("Frequent SLA breaches")
            
            support_tickets = client.get('support_tickets', 0)
            if support_tickets is not None and support_tickets > 10:
                factors.append("High support ticket volume")
            
            # Engagement issues
            interactions_per_month = client.get('interactions_per_month', 0)
            if interactions_per_month is not None and interactions_per_month < 0.5:
                factors.append("Low engagement frequency")
            
            avg_satisfaction_score = client.get('avg_satisfaction_score', 10)
            if avg_satisfaction_score is not None and avg_satisfaction_score < 6:
                factors.append("Low satisfaction score")
            
            # Contract issues
            days_until_contract_end = client.get('days_until_contract_end', 365)
            if days_until_contract_end is not None and days_until_contract_end < 30:
                factors.append("Contract expiring soon")
            
            return factors
            
        except Exception as e:
            logger.error(f"Error identifying trigger factors: {e}")
            return []


class ChurnInterventionTracker:
    """Tracks intervention effectiveness and success metrics"""
    
    def __init__(self):
        """Initialize intervention tracker"""
        self.interventions = []
        logger.info("Churn Intervention Tracker initialized")
    
    def log_intervention(self, client_id: str, intervention_type: str, 
                        recommendations: str, predicted_risk: float) -> str:
        """
        Log a churn intervention
        
        Args:
            client_id: Client identifier
            intervention_type: Type of intervention
            recommendations: Recommendations provided
            predicted_risk: Predicted churn risk at time of intervention
            
        Returns:
            Intervention ID
        """
        try:
            intervention_id = f"INTERV-{client_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            intervention = {
                'intervention_id': intervention_id,
                'client_id': client_id,
                'intervention_type': intervention_type,
                'recommendations': recommendations,
                'predicted_risk': predicted_risk,
                'timestamp': datetime.now(),
                'status': 'pending',
                'outcome': None,
                'follow_up_date': datetime.now() + timedelta(days=30)
            }
            
            self.interventions.append(intervention)
            logger.info(f"Logged intervention {intervention_id} for client {client_id}")
            return intervention_id
            
        except Exception as e:
            logger.error(f"Error logging intervention: {e}")
            return ""
    
    def update_intervention_outcome(self, intervention_id: str, 
                                  outcome: str, actual_churn: Optional[bool] = None) -> bool:
        """
        Update the outcome of an intervention
        
        Args:
            intervention_id: Intervention identifier
            outcome: Outcome description
            actual_churn: Whether client actually churned (optional)
            
        Returns:
            Boolean indicating success
        """
        try:
            for intervention in self.interventions:
                if intervention['intervention_id'] == intervention_id:
                    intervention['outcome'] = outcome
                    intervention['status'] = 'completed'
                    if actual_churn is not None:
                        intervention['actual_churn'] = actual_churn
                    logger.info(f"Updated outcome for intervention {intervention_id}")
                    return True
            
            logger.warning(f"Intervention {intervention_id} not found")
            return False
            
        except Exception as e:
            logger.error(f"Error updating intervention outcome: {e}")
            return False
    
    def get_intervention_metrics(self) -> Dict[str, Any]:
        """
        Get intervention effectiveness metrics
        
        Returns:
            Dictionary with metrics
        """
        try:
            if not self.interventions:
                return {
                    'total_interventions': 0,
                    'completed_interventions': 0,
                    'success_rate': 0.0,
                    'avg_risk_score': 0.0
                }
            
            completed = [i for i in self.interventions if i['status'] == 'completed']
            successful = [i for i in completed if i.get('actual_churn') is False]
            
            metrics = {
                'total_interventions': len(self.interventions),
                'completed_interventions': len(completed),
                'success_rate': len(successful) / len(completed) if completed else 0.0,
                'avg_risk_score': np.mean([i['predicted_risk'] for i in self.interventions]) if self.interventions else 0.0
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating intervention metrics: {e}")
            return {
                'total_interventions': 0,
                'completed_interventions': 0,
                'success_rate': 0.0,
                'avg_risk_score': 0.0
            }


# Global instances for easy access
risk_scorer_instance = None
recommendation_engine_instance = None
early_warning_system_instance = None
intervention_tracker_instance = None


def get_risk_scorer() -> ChurnRiskScorer:
    """Get singleton risk scorer instance"""
    global risk_scorer_instance
    if risk_scorer_instance is None:
        risk_scorer_instance = ChurnRiskScorer()
    return risk_scorer_instance


def get_recommendation_engine() -> ChurnRecommendationEngine:
    """Get singleton recommendation engine instance"""
    global recommendation_engine_instance
    if recommendation_engine_instance is None:
        recommendation_engine_instance = ChurnRecommendationEngine()
    return recommendation_engine_instance


def get_early_warning_system(risk_threshold: float = 0.5) -> ChurnEarlyWarningSystem:
    """Get singleton early warning system instance"""
    global early_warning_system_instance
    if early_warning_system_instance is None:
        early_warning_system_instance = ChurnEarlyWarningSystem(risk_threshold)
    return early_warning_system_instance


def get_intervention_tracker() -> ChurnInterventionTracker:
    """Get singleton intervention tracker instance"""
    global intervention_tracker_instance
    if intervention_tracker_instance is None:
        intervention_tracker_instance = ChurnInterventionTracker()
    return intervention_tracker_instance