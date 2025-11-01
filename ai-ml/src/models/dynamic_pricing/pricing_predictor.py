"""
Pricing Predictor for Dynamic Pricing Engine
Handles client acceptance prediction and pricing strategy validation
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


class ClientAcceptancePredictor:
    """Predictor for client acceptance of pricing changes"""
    
    def __init__(self):
        """Initialize client acceptance predictor"""
        logger.info("Client Acceptance Predictor initialized")
    
    def predict_acceptance_probability(self, client_data: pd.DataFrame, 
                                   proposed_pricing: Dict[str, Any],
                                   historical_data: Optional[pd.DataFrame] = None) -> Dict[str, float]:
        """
        Predict probability of client acceptance for proposed pricing
        
        Args:
            client_data: DataFrame with client value data
            proposed_pricing: Dictionary with proposed pricing recommendations
            historical_data: DataFrame with historical pricing acceptance data (optional)
            
        Returns:
            Dictionary mapping client IDs to acceptance probabilities
        """
        try:
            acceptance_probabilities = {}
            
            # Generate predictions for each client
            for _, client in client_data.iterrows():
                client_id_val = client['client_id']
                if isinstance(client_id_val, pd.Series):
                    client_id_str = str(client_id_val.iloc[0]) if len(client_id_val) > 0 else "UNKNOWN"
                else:
                    client_id_str = str(client_id_val)
                    
                if client_id_str in proposed_pricing:
                    proposed_price = float(proposed_pricing[client_id_str]['recommended_price'])
                else:
                    # Use average proposed price if client not in recommendations
                    proposed_price = float(np.mean([rec['recommended_price'] for rec in proposed_pricing.values()])) if proposed_pricing else 100.0
                
                # Calculate acceptance probability
                acceptance_prob = self._calculate_acceptance_probability(client, proposed_price, historical_data)
                acceptance_probabilities[client_id_str] = float(acceptance_prob)
            
            logger.info(f"Predicted acceptance probabilities for {len(acceptance_probabilities)} clients")
            return acceptance_probabilities
            
        except Exception as e:
            logger.error(f"Error predicting acceptance probabilities: {e}")
            return {}
    
    def _calculate_acceptance_probability(self, client: pd.Series, 
                                       proposed_price: float,
                                       historical_data: Optional[pd.DataFrame] = None) -> float:
        """
        Calculate acceptance probability for a specific client and price
        
        Args:
            client: Client data series
            proposed_price: Proposed price
            historical_data: Historical pricing acceptance data
            
        Returns:
            Acceptance probability (0-1)
        """
        try:
            # Base probability factors
            base_prob = 0.7  # Start with 70% base probability
            
            # Price sensitivity factor
            price_sensitivity = client.get('price_sensitivity', 50)
            if price_sensitivity is None:
                price_sensitivity = 50
            
            # Normalize price sensitivity (0-100 to 0-1)
            normalized_sensitivity = price_sensitivity / 100
            
            # Current client price (if available)
            current_price = client.get('current_price', proposed_price)
            if current_price is None:
                current_price = proposed_price
            
            # Price change impact
            price_change_pct = ((proposed_price - current_price) / current_price) if current_price > 0 else 0
            
            # Adjust probability based on price change
            if price_change_pct > 0:
                # Price increase - reduce probability
                price_impact = -abs(price_change_pct) * (1 + normalized_sensitivity)
            else:
                # Price decrease or no change - increase probability
                price_impact = abs(price_change_pct) * (1 - normalized_sensitivity)
            
            # Loyalty factor
            loyalty_score = client.get('loyalty_score', 50)
            if loyalty_score is None:
                loyalty_score = 50
            loyalty_factor = (loyalty_score - 50) / 100  # Normalize to -0.5 to 0.5
            
            # Satisfaction factor
            satisfaction_score = client.get('satisfaction_score', 5)
            if satisfaction_score is None:
                satisfaction_score = 5
            satisfaction_factor = (satisfaction_score - 5) / 10  # Normalize to -0.5 to 0.5
            
            # Historical acceptance factor (if available)
            historical_factor = 0
            if historical_data is not None and not historical_data.empty:
                # Calculate average historical acceptance rate
                avg_acceptance = historical_data['client_acceptance_rate'].mean()
                historical_factor = (avg_acceptance - 0.7)  # Normalize around 0.7 base
            
            # Combine all factors
            total_adjustment = price_impact + loyalty_factor + satisfaction_factor + historical_factor
            acceptance_prob = base_prob + total_adjustment
            
            # Ensure probability is within valid range
            acceptance_prob = max(0.01, min(0.99, acceptance_prob))
            
            return float(acceptance_prob)
            
        except Exception as e:
            logger.error(f"Error calculating acceptance probability: {e}")
            return 0.5  # Return neutral probability on error


class PricingStrategyValidator:
    """Validator for pricing strategies and recommendations"""
    
    def __init__(self):
        """Initialize pricing strategy validator"""
        logger.info("Pricing Strategy Validator initialized")
    
    def validate_pricing_strategy(self, proposed_pricing: Dict[str, Any], 
                               client_data: pd.DataFrame,
                               market_data: pd.DataFrame,
                               competitor_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate proposed pricing strategy
        
        Args:
            proposed_pricing: Dictionary with proposed pricing recommendations
            client_data: DataFrame with client value data
            market_data: DataFrame with market rate data
            competitor_data: DataFrame with competitor pricing data
            
        Returns:
            Dictionary with validation results
        """
        try:
            # Calculate key metrics
            total_clients = len(proposed_pricing)
            avg_proposed_price = float(np.mean([rec['recommended_price'] for rec in proposed_pricing.values()])) if proposed_pricing else 0.0
            avg_current_price = float(client_data['revenue_contribution'].mean() / 12) if not client_data.empty else 0.0  # Simplified
            
            # Price change analysis
            price_changes = []
            for client_id, recommendation in proposed_pricing.items():
                proposed_price = recommendation['recommended_price']
                # Find client in client_data
                client_row = client_data[client_data['client_id'] == client_id]
                if not client_row.empty:
                    current_price = float(client_row.iloc[0]['revenue_contribution'] / 12)  # Simplified
                    price_change_pct = float(((proposed_price - current_price) / current_price) * 100) if current_price > 0 else 0.0
                    price_changes.append(price_change_pct)
            
            avg_price_change = float(np.mean(price_changes)) if price_changes else 0.0
            max_price_increase = float(max(price_changes)) if price_changes else 0.0
            max_price_decrease = float(min(price_changes)) if price_changes else 0.0
            
            # Market alignment check
            market_avg_price = float(market_data['market_rate'].mean()) if not market_data.empty else 100.0
            market_alignment = float(((avg_proposed_price - market_avg_price) / market_avg_price) * 100) if market_avg_price > 0 else 0.0
            
            # Competitive positioning
            competitor_avg_price = float(competitor_data['avg_price'].mean()) if not competitor_data.empty else 100.0
            competitive_positioning = float(((avg_proposed_price - competitor_avg_price) / competitor_avg_price) * 100) if competitor_avg_price > 0 else 0.0
            
            # Risk assessment
            high_risk_clients = sum(1 for rec in proposed_pricing.values() if rec.get('price_change_percentage', 0) > 20)
            low_risk_clients = sum(1 for rec in proposed_pricing.values() if abs(rec.get('price_change_percentage', 0)) <= 5)
            
            # Validation results
            validation_results = {
                'total_clients': total_clients,
                'average_proposed_price': float(avg_proposed_price),
                'average_current_price': float(avg_current_price),
                'average_price_change_percentage': float(avg_price_change),
                'maximum_price_increase_percentage': float(max_price_increase),
                'maximum_price_decrease_percentage': float(max_price_decrease),
                'market_alignment_percentage': float(market_alignment),
                'competitive_positioning_percentage': float(competitive_positioning),
                'high_risk_clients': high_risk_clients,
                'low_risk_clients': low_risk_clients,
                'risk_assessment': self._assess_risk(high_risk_clients, total_clients),
                'recommendations': self._generate_validation_recommendations(
                    avg_price_change, market_alignment, competitive_positioning, high_risk_clients
                )
            }
            
            logger.info("Pricing strategy validation completed")
            return validation_results
            
        except Exception as e:
            logger.error(f"Error validating pricing strategy: {e}")
            return {
                'validation_status': 'error',
                'error_message': str(e)
            }
    
    def _assess_risk(self, high_risk_clients: int, total_clients: int) -> str:
        """
        Assess overall risk level
        
        Args:
            high_risk_clients: Number of high-risk clients
            total_clients: Total number of clients
            
        Returns:
            Risk assessment string
        """
        if total_clients == 0:
            return 'unknown'
            
        risk_ratio = high_risk_clients / total_clients
        
        if risk_ratio > 0.3:
            return 'high'
        elif risk_ratio > 0.1:
            return 'medium'
        else:
            return 'low'
    
    def _generate_validation_recommendations(self, avg_price_change: float, 
                                          market_alignment: float,
                                          competitive_positioning: float,
                                          high_risk_clients: int) -> List[str]:
        """
        Generate recommendations based on validation results
        
        Args:
            avg_price_change: Average price change percentage
            market_alignment: Market alignment percentage
            competitive_positioning: Competitive positioning percentage
            high_risk_clients: Number of high-risk clients
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        # Price change recommendations
        if avg_price_change > 10:
            recommendations.append("Consider reducing average price increases to improve client retention")
        elif avg_price_change < -5:
            recommendations.append("Evaluate if price decreases are too aggressive")
        
        # Market alignment recommendations
        if abs(market_alignment) > 15:
            recommendations.append("Pricing significantly deviates from market rates - review strategy")
        
        # Competitive positioning recommendations
        if competitive_positioning > 20:
            recommendations.append("Prices are premium compared to competitors - ensure value proposition justifies pricing")
        elif competitive_positioning < -20:
            recommendations.append("Prices are significantly below competitors - consider increasing to improve margins")
        
        # Risk recommendations
        if high_risk_clients > 5:
            recommendations.append("High number of high-risk clients - consider phased implementation")
        
        # Default recommendation if no issues
        if not recommendations:
            recommendations.append("Pricing strategy appears balanced and market-aligned")
        
        return recommendations


class PricingPerformanceMonitor:
    """Monitor for tracking pricing performance and outcomes"""
    
    def __init__(self):
        """Initialize pricing performance monitor"""
        logger.info("Pricing Performance Monitor initialized")
    
    def monitor_pricing_performance(self, implemented_pricing: Dict[str, Any],
                                 actual_outcomes: pd.DataFrame,
                                 time_period_days: int = 30) -> Dict[str, Any]:
        """
        Monitor actual performance of implemented pricing
        
        Args:
            implemented_pricing: Dictionary with implemented pricing
            actual_outcomes: DataFrame with actual pricing outcomes
            time_period_days: Time period to analyze in days
            
        Returns:
            Dictionary with performance metrics
        """
        try:
            # Calculate key performance metrics
            total_revenue = actual_outcomes['revenue_generated'].sum() if not actual_outcomes.empty else 0
            total_units_sold = actual_outcomes['units_sold'].sum() if not actual_outcomes.empty else 0
            avg_acceptance_rate = actual_outcomes['client_acceptance_rate'].mean() if not actual_outcomes.empty else 0
            
            # Compare with expected outcomes
            expected_revenue = sum(rec['recommended_price'] for rec in implemented_pricing.values())
            revenue_variance = ((total_revenue - expected_revenue) / expected_revenue) * 100 if expected_revenue > 0 else 0
            
            # Client retention impact
            client_retention_rate = self._calculate_client_retention(actual_outcomes)
            
            # Profitability analysis
            avg_profit_margin = float(actual_outcomes['profit_margin'].mean()) if not actual_outcomes.empty else 0.0
            
            performance_metrics = {
                'total_revenue': float(total_revenue),
                'total_units_sold': int(total_units_sold),
                'average_acceptance_rate': float(avg_acceptance_rate),
                'expected_revenue': float(expected_revenue),
                'revenue_variance_percentage': float(revenue_variance),
                'client_retention_rate': float(client_retention_rate),
                'average_profit_margin': float(avg_profit_margin),
                'time_period_days': time_period_days,
                'performance_assessment': self._assess_performance(revenue_variance, client_retention_rate, avg_profit_margin)
            }
            
            logger.info("Pricing performance monitoring completed")
            return performance_metrics
            
        except Exception as e:
            logger.error(f"Error monitoring pricing performance: {e}")
            return {
                'monitoring_status': 'error',
                'error_message': str(e)
            }
    
    def _calculate_client_retention(self, outcomes_data: pd.DataFrame) -> float:
        """
        Calculate client retention rate from outcomes data
        
        Args:
            outcomes_data: DataFrame with pricing outcomes
            
        Returns:
            Client retention rate (0-1)
        """
        try:
            if outcomes_data.empty:
                return 0.0
            
            # Simplified retention calculation
            # In a real implementation, this would track actual client renewals/continuations
            total_clients = len(outcomes_data)
            
            # Count records with high acceptance rate as "retained"
            retained_count = len(outcomes_data[outcomes_data['client_acceptance_rate'] > 0.5])
            
            retention_rate = retained_count / total_clients if total_clients > 0 else 0
            return float(retention_rate)
            
        except Exception:
            return 0.0
    
    def _assess_performance(self, revenue_variance: float, 
                         retention_rate: float, 
                         profit_margin: float) -> str:
        """
        Assess overall pricing performance
        
        Args:
            revenue_variance: Revenue variance percentage
            retention_rate: Client retention rate
            profit_margin: Average profit margin
            
        Returns:
            Performance assessment string
        """
        # Simple scoring system
        score = 0
        
        # Revenue performance (positive variance is good)
        if revenue_variance > 5:
            score += 2
        elif revenue_variance > 0:
            score += 1
        elif revenue_variance < -10:
            score -= 2
        elif revenue_variance < 0:
            score -= 1
        
        # Retention performance (higher is better)
        if retention_rate > 0.9:
            score += 2
        elif retention_rate > 0.8:
            score += 1
        elif retention_rate < 0.6:
            score -= 2
        elif retention_rate < 0.7:
            score -= 1
        
        # Profit margin performance (higher is better)
        if profit_margin > 0.3:
            score += 2
        elif profit_margin > 0.2:
            score += 1
        elif profit_margin < 0.1:
            score -= 2
        elif profit_margin < 0.15:
            score -= 1
        
        if score >= 4:
            return 'excellent'
        elif score >= 2:
            return 'good'
        elif score >= 0:
            return 'acceptable'
        elif score >= -2:
            return 'concerning'
        else:
            return 'poor'


# Global instances for easy access
client_acceptance_predictor_instance = None
pricing_strategy_validator_instance = None
pricing_performance_monitor_instance = None


def get_client_acceptance_predictor() -> ClientAcceptancePredictor:
    """Get singleton client acceptance predictor instance"""
    global client_acceptance_predictor_instance
    if client_acceptance_predictor_instance is None:
        client_acceptance_predictor_instance = ClientAcceptancePredictor()
    return client_acceptance_predictor_instance


def get_pricing_strategy_validator() -> PricingStrategyValidator:
    """Get singleton pricing strategy validator instance"""
    global pricing_strategy_validator_instance
    if pricing_strategy_validator_instance is None:
        pricing_strategy_validator_instance = PricingStrategyValidator()
    return pricing_strategy_validator_instance


def get_pricing_performance_monitor() -> PricingPerformanceMonitor:
    """Get singleton pricing performance monitor instance"""
    global pricing_performance_monitor_instance
    if pricing_performance_monitor_instance is None:
        pricing_performance_monitor_instance = PricingPerformanceMonitor()
    return pricing_performance_monitor_instance