"""
Genome Creator Module
Creates 50-dimensional client profitability genome vectors from feature engineering outputs
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
import logging
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from datetime import datetime

from . import GENOME_STRUCTURE

logger = logging.getLogger(__name__)


class GenomeCreator:
    """Creates and manages 50-dimensional client profitability genome vectors"""
    
    def __init__(self):
        """Initialize the Genome Creator"""
        self.scaler = StandardScaler()
        self.minmax_scaler = MinMaxScaler()
        self.genome_history = {}
        
    def create_genome_vector(self, client_features: Dict[str, Any]) -> np.ndarray:
        """
        Create a 50-dimensional genome vector for a client based on their features
        
        Args:
            client_features: Dictionary containing all client features from feature engineering
            
        Returns:
            np.ndarray: 50-dimensional genome vector (normalized to 0-1 range)
        """
        genome_vector = np.zeros(50)
        
        try:
            # Financial Health Dimensions (0-9)
            genome_vector[0] = self._calculate_revenue_stability(client_features)
            genome_vector[1] = self._calculate_profit_margin_trend(client_features)
            genome_vector[2] = self._calculate_billing_efficiency(client_features)
            genome_vector[3] = self._calculate_payment_behavior(client_features)
            genome_vector[4] = self._calculate_cost_optimization(client_features)
            genome_vector[5] = self._calculate_financial_growth(client_features)
            genome_vector[6] = self._calculate_contract_value_stability(client_features)
            genome_vector[7] = self._calculate_revenue_diversification(client_features)
            genome_vector[8] = self._calculate_financial_predictability(client_features)
            genome_vector[9] = self._calculate_cash_flow_health(client_features)
            
            # Operational Efficiency Dimensions (10-19)
            genome_vector[10] = self._calculate_sla_compliance(client_features)
            genome_vector[11] = self._calculate_resolution_time(client_features)
            genome_vector[12] = self._calculate_technician_productivity(client_features)
            genome_vector[13] = self._calculate_service_quality(client_features)
            genome_vector[14] = self._calculate_resource_utilization(client_features)
            genome_vector[15] = self._calculate_operational_cost_efficiency(client_features)
            genome_vector[16] = self._calculate_service_consistency(client_features)
            genome_vector[17] = self._calculate_automation_adoption(client_features)
            genome_vector[18] = self._calculate_process_optimization(client_features)
            genome_vector[19] = self._calculate_operational_scalability(client_features)
            
            # Engagement Level Dimensions (20-29)
            genome_vector[20] = self._calculate_login_frequency(client_features)
            genome_vector[21] = self._calculate_feature_usage_depth(client_features)
            genome_vector[22] = self._calculate_support_interaction(client_features)
            genome_vector[23] = self._calculate_communication_responsiveness(client_features)
            genome_vector[24] = self._calculate_feedback_participation(client_features)
            genome_vector[25] = self._calculate_training_adoption(client_features)
            genome_vector[26] = self._calculate_portal_engagement(client_features)
            genome_vector[27] = self._calculate_community_participation(client_features)
            genome_vector[28] = self._calculate_advocacy_indicators(client_features)
            genome_vector[29] = self._calculate_relationship_strength(client_features)
            
            # Growth Potential Dimensions (30-39)
            genome_vector[30] = self._calculate_expansion_opportunity(client_features)
            genome_vector[31] = self._calculate_upsell_readiness(client_features)
            genome_vector[32] = self._calculate_market_position(client_features)
            genome_vector[33] = self._calculate_innovation_adoption(client_features)
            genome_vector[34] = self._calculate_partnership_potential(client_features)
            genome_vector[35] = self._calculate_cross_selling_opportunities(client_features)
            genome_vector[36] = self._calculate_revenue_growth_trajectory(client_features)
            genome_vector[37] = self._calculate_service_utilization_trends(client_features)
            genome_vector[38] = self._calculate_market_expansion(client_features)
            genome_vector[39] = self._calculate_strategic_alignment(client_features)
            
            # Risk Factors Dimensions (40-49)
            genome_vector[40] = self._calculate_churn_probability(client_features)
            genome_vector[41] = self._calculate_payment_delinquency_risk(client_features)
            genome_vector[42] = self._calculate_contract_expiration_risk(client_features)
            genome_vector[43] = self._calculate_service_quality_risk(client_features)
            genome_vector[44] = self._calculate_competitive_threat(client_features)
            genome_vector[45] = self._calculate_market_volatility_exposure(client_features)
            genome_vector[46] = self._calculate_dependency_risk(client_features)
            genome_vector[47] = self._calculate_compliance_risk(client_features)
            genome_vector[48] = self._calculate_operational_risk(client_features)
            genome_vector[49] = self._calculate_financial_stability_risk(client_features)
            
            # Normalize the genome vector to 0-1 range
            genome_vector = self._normalize_genome_vector(genome_vector)
            
            logger.info("Successfully created 50-dimensional genome vector")
            return genome_vector
            
        except Exception as e:
            logger.error(f"Error creating genome vector: {e}")
            # Return a zero vector if there's an error
            return np.zeros(50)
    
    def create_genomes_for_clients(self, clients_data: pd.DataFrame) -> Dict[str, np.ndarray]:
        """
        Create genome vectors for multiple clients
        
        Args:
            clients_data: DataFrame containing client data with all features
            
        Returns:
            Dict[str, np.ndarray]: Dictionary mapping client IDs to genome vectors
        """
        client_genomes = {}
        
        # Group data by client
        grouped_data = clients_data.groupby('client_id') if 'client_id' in clients_data.columns else clients_data.groupby(clients_data.index)
        
        for client_id, client_group in grouped_data:
            # Convert group to feature dictionary
            client_features = client_group.to_dict('records')[0] if len(client_group) > 0 else {}
            
            # Create genome vector
            genome_vector = self.create_genome_vector(client_features)
            client_genomes[client_id] = genome_vector
            
            # Store in history
            self.genome_history[client_id] = {
                'genome': genome_vector,
                'timestamp': datetime.now(),
                'features': client_features
            }
        
        logger.info(f"Created genome vectors for {len(client_genomes)} clients")
        return client_genomes
    
    def get_genome_history(self, client_id: str) -> Optional[Dict]:
        """
        Get historical genome data for a client
        
        Args:
            client_id: Client identifier
            
        Returns:
            Dict: Historical genome data or None if not found
        """
        return self.genome_history.get(client_id)
    
    def _normalize_genome_vector(self, vector: np.ndarray) -> np.ndarray:
        """
        Normalize genome vector to 0-1 range
        
        Args:
            vector: Raw genome vector
            
        Returns:
            np.ndarray: Normalized genome vector
        """
        # Clip values to reasonable range to prevent outliers
        vector = np.clip(vector, -10, 10)
        
        # Min-max normalization to 0-1 range
        if np.max(vector) != np.min(vector):
            normalized = (vector - np.min(vector)) / (np.max(vector) - np.min(vector))
        else:
            normalized = np.zeros_like(vector)
            
        return normalized
    
    # Financial Health Calculations (Dimensions 0-9)
    def _calculate_revenue_stability(self, features: Dict) -> float:
        """Calculate revenue stability score"""
        # Use standard deviation of revenue as inverse measure of stability
        revenue_std = features.get('revenue_std', 0)
        revenue_mean = features.get('revenue_mean', 1)
        
        if revenue_mean > 0:
            stability_ratio = revenue_std / revenue_mean
            return max(0, 1 - stability_ratio)  # Higher stability = lower ratio
        return 0.5
    
    def _calculate_profit_margin_trend(self, features: Dict) -> float:
        """Calculate profit margin trend score"""
        margin_trend = features.get('profit_margin_trend', 0)
        # Normalize trend to 0-1 range (assuming trend is between -1 and 1)
        return np.clip((margin_trend + 1) / 2, 0, 1)
    
    def _calculate_billing_efficiency(self, features: Dict) -> float:
        """Calculate billing efficiency score"""
        billing_accuracy = features.get('billing_accuracy', 0.8)
        return np.clip(billing_accuracy, 0, 1)
    
    def _calculate_payment_behavior(self, features: Dict) -> float:
        """Calculate payment behavior score"""
        late_payment_rate = features.get('late_payment_rate', 0)
        return max(0, 1 - late_payment_rate)  # Lower late payment rate = better score
    
    def _calculate_cost_optimization(self, features: Dict) -> float:
        """Calculate cost optimization score"""
        cost_efficiency = features.get('cost_efficiency', 0.7)
        return np.clip(cost_efficiency, 0, 1)
    
    def _calculate_financial_growth(self, features: Dict) -> float:
        """Calculate financial growth score"""
        growth_rate = features.get('revenue_growth_rate', 0)
        # Normalize growth rate (assuming reasonable range of -0.5 to 0.5)
        return np.clip((growth_rate + 0.5) / 1.0, 0, 1)
    
    def _calculate_contract_value_stability(self, features: Dict) -> float:
        """Calculate contract value stability score"""
        contract_stability = features.get('contract_stability', 0.8)
        return np.clip(contract_stability, 0, 1)
    
    def _calculate_revenue_diversification(self, features: Dict) -> float:
        """Calculate revenue diversification score"""
        diversification_score = features.get('revenue_diversification', 0.6)
        return np.clip(diversification_score, 0, 1)
    
    def _calculate_financial_predictability(self, features: Dict) -> float:
        """Calculate financial predictability score"""
        forecast_accuracy = features.get('forecast_accuracy', 0.7)
        return np.clip(forecast_accuracy, 0, 1)
    
    def _calculate_cash_flow_health(self, features: Dict) -> float:
        """Calculate cash flow health score"""
        cash_flow_ratio = features.get('cash_flow_ratio', 0.8)
        return np.clip(cash_flow_ratio, 0, 1)
    
    # Operational Efficiency Calculations (Dimensions 10-19)
    def _calculate_sla_compliance(self, features: Dict) -> float:
        """Calculate SLA compliance score"""
        sla_compliance_rate = features.get('sla_compliance_rate', 0.9)
        return np.clip(sla_compliance_rate, 0, 1)
    
    def _calculate_resolution_time(self, features: Dict) -> float:
        """Calculate resolution time score"""
        avg_resolution_time = features.get('avg_resolution_time', 24)  # hours
        target_time = features.get('target_resolution_time', 48)  # hours
        
        if target_time > 0:
            time_ratio = avg_resolution_time / target_time
            return max(0, 1 - time_ratio)
        return 0.5
    
    def _calculate_technician_productivity(self, features: Dict) -> float:
        """Calculate technician productivity score"""
        productivity_score = features.get('technician_productivity', 0.75)
        return np.clip(productivity_score, 0, 1)
    
    def _calculate_service_quality(self, features: Dict) -> float:
        """Calculate service quality score"""
        quality_score = features.get('avg_quality_score', 4.0)  # 1-5 scale
        return np.clip(quality_score / 5.0, 0, 1)
    
    def _calculate_resource_utilization(self, features: Dict) -> float:
        """Calculate resource utilization score"""
        utilization_rate = features.get('resource_utilization_rate', 0.7)
        # Optimal utilization is around 80%, so score based on proximity to 0.8
        optimal = 0.8
        deviation = abs(utilization_rate - optimal)
        return max(0, 1 - (deviation / optimal))
    
    def _calculate_operational_cost_efficiency(self, features: Dict) -> float:
        """Calculate operational cost efficiency score"""
        cost_efficiency = features.get('operational_cost_efficiency', 0.7)
        return np.clip(cost_efficiency, 0, 1)
    
    def _calculate_service_consistency(self, features: Dict) -> float:
        """Calculate service consistency score"""
        consistency_score = features.get('service_consistency', 0.85)
        return np.clip(consistency_score, 0, 1)
    
    def _calculate_automation_adoption(self, features: Dict) -> float:
        """Calculate automation adoption score"""
        automation_rate = features.get('automation_adoption_rate', 0.4)
        return np.clip(automation_rate, 0, 1)
    
    def _calculate_process_optimization(self, features: Dict) -> float:
        """Calculate process optimization score"""
        optimization_score = features.get('process_optimization_score', 0.6)
        return np.clip(optimization_score, 0, 1)
    
    def _calculate_operational_scalability(self, features: Dict) -> float:
        """Calculate operational scalability score"""
        scalability_score = features.get('scalability_score', 0.7)
        return np.clip(scalability_score, 0, 1)
    
    # Engagement Level Calculations (Dimensions 20-29)
    def _calculate_login_frequency(self, features: Dict) -> float:
        """Calculate login frequency score"""
        login_frequency = features.get('login_frequency', 10)  # logins per month
        # Normalize based on expected range (0-50 logins)
        return np.clip(login_frequency / 50.0, 0, 1)
    
    def _calculate_feature_usage_depth(self, features: Dict) -> float:
        """Calculate feature usage depth score"""
        usage_depth = features.get('feature_usage_depth', 0.6)
        return np.clip(usage_depth, 0, 1)
    
    def _calculate_support_interaction(self, features: Dict) -> float:
        """Calculate support interaction score"""
        support_requests = features.get('support_requests_per_month', 2)
        # Fewer support requests might indicate better self-service or disengagement
        # We'll assume optimal is around 1-3 requests per month
        optimal = 2
        if support_requests <= optimal:
            return 1.0 - (support_requests / (optimal * 2))
        else:
            return max(0, 1.0 - ((support_requests - optimal) / 10))
    
    def _calculate_communication_responsiveness(self, features: Dict) -> float:
        """Calculate communication responsiveness score"""
        response_rate = features.get('communication_response_rate', 0.8)
        return np.clip(response_rate, 0, 1)
    
    def _calculate_feedback_participation(self, features: Dict) -> float:
        """Calculate feedback participation score"""
        feedback_rate = features.get('feedback_participation_rate', 0.3)
        return np.clip(feedback_rate, 0, 1)
    
    def _calculate_training_adoption(self, features: Dict) -> float:
        """Calculate training adoption score"""
        training_completion = features.get('training_completion_rate', 0.5)
        return np.clip(training_completion, 0, 1)
    
    def _calculate_portal_engagement(self, features: Dict) -> float:
        """Calculate portal engagement score"""
        engagement_score = features.get('portal_engagement_score', 0.6)
        return np.clip(engagement_score, 0, 1)
    
    def _calculate_community_participation(self, features: Dict) -> float:
        """Calculate community participation score"""
        community_score = features.get('community_participation', 0.2)
        return np.clip(community_score, 0, 1)
    
    def _calculate_advocacy_indicators(self, features: Dict) -> float:
        """Calculate advocacy indicators score"""
        advocacy_score = features.get('advocacy_score', 0.3)
        return np.clip(advocacy_score, 0, 1)
    
    def _calculate_relationship_strength(self, features: Dict) -> float:
        """Calculate relationship strength score"""
        relationship_score = features.get('relationship_strength', 0.7)
        return np.clip(relationship_score, 0, 1)
    
    # Growth Potential Calculations (Dimensions 30-39)
    def _calculate_expansion_opportunity(self, features: Dict) -> float:
        """Calculate expansion opportunity score"""
        expansion_score = features.get('expansion_opportunity_score', 0.4)
        return np.clip(expansion_score, 0, 1)
    
    def _calculate_upsell_readiness(self, features: Dict) -> float:
        """Calculate upsell readiness score"""
        upsell_readiness = features.get('upsell_readiness', 0.5)
        return np.clip(upsell_readiness, 0, 1)
    
    def _calculate_market_position(self, features: Dict) -> float:
        """Calculate market position score"""
        market_position = features.get('market_position_strength', 0.6)
        return np.clip(market_position, 0, 1)
    
    def _calculate_innovation_adoption(self, features: Dict) -> float:
        """Calculate innovation adoption score"""
        innovation_adoption = features.get('innovation_adoption_rate', 0.4)
        return np.clip(innovation_adoption, 0, 1)
    
    def _calculate_partnership_potential(self, features: Dict) -> float:
        """Calculate partnership potential score"""
        partnership_score = features.get('partnership_potential', 0.3)
        return np.clip(partnership_score, 0, 1)
    
    def _calculate_cross_selling_opportunities(self, features: Dict) -> float:
        """Calculate cross-selling opportunities score"""
        cross_selling_score = features.get('cross_selling_opportunity', 0.5)
        return np.clip(cross_selling_score, 0, 1)
    
    def _calculate_revenue_growth_trajectory(self, features: Dict) -> float:
        """Calculate revenue growth trajectory score"""
        growth_trajectory = features.get('revenue_growth_trajectory', 0.3)
        # Normalize from -1 to 1 range to 0 to 1
        return np.clip((growth_trajectory + 1) / 2, 0, 1)
    
    def _calculate_service_utilization_trends(self, features: Dict) -> float:
        """Calculate service utilization trends score"""
        utilization_trend = features.get('service_utilization_trend', 0.2)
        # Normalize from -1 to 1 range to 0 to 1
        return np.clip((utilization_trend + 1) / 2, 0, 1)
    
    def _calculate_market_expansion(self, features: Dict) -> float:
        """Calculate market expansion score"""
        expansion_score = features.get('market_expansion_potential', 0.4)
        return np.clip(expansion_score, 0, 1)
    
    def _calculate_strategic_alignment(self, features: Dict) -> float:
        """Calculate strategic alignment score"""
        alignment_score = features.get('strategic_alignment', 0.6)
        return np.clip(alignment_score, 0, 1)
    
    # Risk Factors Calculations (Dimensions 40-49)
    def _calculate_churn_probability(self, features: Dict) -> float:
        """Calculate churn probability score (inverted)"""
        churn_prob = features.get('churn_probability', 0.2)
        return max(0, 1 - churn_prob)  # Lower churn risk = higher score
    
    def _calculate_payment_delinquency_risk(self, features: Dict) -> float:
        """Calculate payment delinquency risk score (inverted)"""
        delinquency_risk = features.get('payment_delinquency_risk', 0.1)
        return max(0, 1 - delinquency_risk)
    
    def _calculate_contract_expiration_risk(self, features: Dict) -> float:
        """Calculate contract expiration risk score (inverted)"""
        expiration_risk = features.get('contract_expiration_risk', 0.3)
        return max(0, 1 - expiration_risk)
    
    def _calculate_service_quality_risk(self, features: Dict) -> float:
        """Calculate service quality risk score (inverted)"""
        quality_risk = features.get('service_quality_risk', 0.2)
        return max(0, 1 - quality_risk)
    
    def _calculate_competitive_threat(self, features: Dict) -> float:
        """Calculate competitive threat score (inverted)"""
        competitive_threat = features.get('competitive_threat_level', 0.4)
        return max(0, 1 - competitive_threat)
    
    def _calculate_market_volatility_exposure(self, features: Dict) -> float:
        """Calculate market volatility exposure score (inverted)"""
        volatility_exposure = features.get('market_volatility_exposure', 0.3)
        return max(0, 1 - volatility_exposure)
    
    def _calculate_dependency_risk(self, features: Dict) -> float:
        """Calculate dependency risk score (inverted)"""
        dependency_risk = features.get('dependency_risk', 0.25)
        return max(0, 1 - dependency_risk)
    
    def _calculate_compliance_risk(self, features: Dict) -> float:
        """Calculate compliance risk score (inverted)"""
        compliance_risk = features.get('compliance_risk', 0.15)
        return max(0, 1 - compliance_risk)
    
    def _calculate_operational_risk(self, features: Dict) -> float:
        """Calculate operational risk score (inverted)"""
        operational_risk = features.get('operational_risk_score', 0.2)
        return max(0, 1 - operational_risk)
    
    def _calculate_financial_stability_risk(self, features: Dict) -> float:
        """Calculate financial stability risk score (inverted)"""
        financial_risk = features.get('financial_stability_risk', 0.1)
        return max(0, 1 - financial_risk)


def create_client_genome(client_features: Dict[str, Any]) -> np.ndarray:
    """
    Convenience function to create a client genome vector
    
    Args:
        client_features: Dictionary containing all client features
        
    Returns:
        np.ndarray: 50-dimensional genome vector
    """
    creator = GenomeCreator()
    return creator.create_genome_vector(client_features)


def create_client_genomes(clients_data: pd.DataFrame) -> Dict[str, np.ndarray]:
    """
    Convenience function to create genome vectors for multiple clients
    
    Args:
        clients_data: DataFrame containing client data with all features
        
    Returns:
        Dict[str, np.ndarray]: Dictionary mapping client IDs to genome vectors
    """
    creator = GenomeCreator()
    return creator.create_genomes_for_clients(clients_data)