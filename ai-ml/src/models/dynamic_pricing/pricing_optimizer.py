"""
Pricing Optimization Engine for Dynamic Pricing
Handles price recommendations, ROI calculations, and market analysis
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


class PriceRecommendationEngine:
    """Engine for generating price recommendations"""
    
    def __init__(self):
        """Initialize price recommendation engine"""
        logger.info("Price Recommendation Engine initialized")
    
    def generate_price_recommendation(self, client_data: pd.DataFrame, 
                                   service_data: pd.DataFrame,
                                   market_data: pd.DataFrame,
                                   competitor_data: pd.DataFrame,
                                   client_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate price recommendations for clients or services
        
        Args:
            client_data: DataFrame with client value data
            service_data: DataFrame with service complexity data
            market_data: DataFrame with market rate data
            competitor_data: DataFrame with competitive pricing data
            client_id: Specific client ID to generate recommendation for (optional)
            
        Returns:
            Dictionary with price recommendations
        """
        try:
            recommendations = {}
            
            # If specific client requested, filter data
            if client_id:
                client_data_filtered = client_data[client_data['client_id'] == client_id]
                if isinstance(client_data_filtered, pd.DataFrame):
                    client_data = client_data_filtered
                else:
                    # If filtering returns a Series, convert back to DataFrame
                    client_data = pd.DataFrame([client_data_filtered]) if not client_data_filtered.empty else pd.DataFrame()
                if client_data.empty:
                    logger.warning(f"No data found for client {client_id}")
                    return {}
            
            # Generate recommendations for each client
            for _, client in client_data.iterrows():
                client_id_val = client['client_id']
                if isinstance(client_id_val, pd.Series):
                    client_id = client_id_val.iloc[0] if len(client_id_val) > 0 else "UNKNOWN"
                else:
                    client_id = str(client_id_val)
                
                # Calculate base price based on client value
                base_price = self._calculate_base_price(client, service_data, market_data)
                
                # Adjust for client-specific factors
                adjusted_price = self._adjust_for_client_factors(base_price, client, competitor_data)
                
                # Calculate confidence interval
                confidence_interval = self._calculate_confidence_interval(base_price, client)
                
                # Generate recommendation
                recommendations[client_id] = {
                    'base_price': base_price,
                    'recommended_price': adjusted_price,
                    'confidence_interval': confidence_interval,
                    'price_change_percentage': ((adjusted_price - base_price) / base_price) * 100,
                    'justification': self._generate_justification(client, base_price, adjusted_price)
                }
            
            logger.info(f"Generated price recommendations for {len(recommendations)} clients")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating price recommendations: {e}")
            return {}
    
    def _calculate_base_price(self, client: pd.Series, service_data: pd.DataFrame, 
                            market_data: pd.DataFrame) -> float:
        """
        Calculate base price for a client based on value and market data
        
        Args:
            client: Client data series
            service_data: DataFrame with service complexity data
            market_data: DataFrame with market rate data
            
        Returns:
            Base price
        """
        try:
            # Client value factors
            revenue_contribution = client.get('revenue_contribution', 10000)
            if revenue_contribution is None:
                revenue_contribution = 10000
            profit_margin = client.get('profit_margin', 0.3)
            if profit_margin is None:
                profit_margin = 0.3
            loyalty_score = client.get('loyalty_score', 50)
            if loyalty_score is None:
                loyalty_score = 50
            
            # Market factors
            avg_market_rate = market_data['market_rate'].mean() if not market_data.empty else 100
            
            # Service complexity factors (simplified)
            avg_complexity = service_data['technical_complexity'].mean() if not service_data.empty else 5
            
            # Base price calculation
            # Start with market rate
            base_price = avg_market_rate
            
            # Adjust for client value (higher value clients can pay more)
            value_multiplier = 1 + (revenue_contribution / 100000) * 0.2
            base_price *= value_multiplier
            
            # Adjust for service complexity
            complexity_multiplier = 1 + (avg_complexity / 10) * 0.3
            base_price *= complexity_multiplier
            
            # Adjust for profit margin target
            base_price = base_price / profit_margin
            
            # Ensure reasonable bounds
            base_price = max(50, min(500, base_price))
            
            return float(base_price)
            
        except Exception as e:
            logger.error(f"Error calculating base price: {e}")
            return 100.0
    
    def _adjust_for_client_factors(self, base_price: float, client: pd.Series, 
                                 competitor_data: pd.DataFrame) -> float:
        """
        Adjust price based on client-specific factors
        
        Args:
            base_price: Base price
            client: Client data series
            competitor_data: DataFrame with competitive pricing data
            
        Returns:
            Adjusted price
        """
        try:
            adjusted_price = base_price
            
            # Price sensitivity factor (lower sensitivity = can charge more)
            price_sensitivity = client.get('price_sensitivity', 50)
            if price_sensitivity is None:
                price_sensitivity = 50
            sensitivity_factor = 1 - (price_sensitivity - 50) / 100  # Normalize to 0.5-1.5 range
            adjusted_price *= sensitivity_factor
            
            # Loyalty factor (more loyal clients can pay more)
            loyalty_score = client.get('loyalty_score', 50)
            if loyalty_score is None:
                loyalty_score = 50
            loyalty_factor = 1 + (loyalty_score - 50) / 200  # Normalize to 0.75-1.25 range
            adjusted_price *= loyalty_factor
            
            # Satisfaction factor (happier clients can pay more)
            satisfaction_score = client.get('satisfaction_score', 5)
            if satisfaction_score is None:
                satisfaction_score = 5
            satisfaction_factor = 1 + (satisfaction_score - 5) / 20  # Normalize to 0.75-1.25 range
            adjusted_price *= satisfaction_factor
            
            # Competitive positioning
            if not competitor_data.empty:
                avg_competitor_price = competitor_data['avg_price'].mean()
                # If we're significantly below competitors, we can increase price
                if base_price < avg_competitor_price * 0.8:
                    adjusted_price *= 1.1  # 10% increase
                # If we're significantly above competitors, consider decreasing price
                elif base_price > avg_competitor_price * 1.2:
                    adjusted_price *= 0.95  # 5% decrease
            
            # Ensure reasonable bounds (within 30% of base price)
            min_price = base_price * 0.7
            max_price = base_price * 1.3
            adjusted_price = max(min_price, min(max_price, adjusted_price))
            
            return float(adjusted_price)
            
        except Exception as e:
            logger.error(f"Error adjusting for client factors: {e}")
            return base_price
    
    def _calculate_confidence_interval(self, base_price: float, client: pd.Series) -> Tuple[float, float]:
        """
        Calculate confidence interval for price recommendation
        
        Args:
            base_price: Base price
            client: Client data series
            
        Returns:
            Tuple of (lower_bound, upper_bound)
        """
        try:
            # Confidence based on data quality and client history
            satisfaction_score = client.get('satisfaction_score', 5)
            if satisfaction_score is None:
                satisfaction_score = 5
            loyalty_score = client.get('loyalty_score', 50)
            if loyalty_score is None:
                loyalty_score = 50
            service_usage = client.get('service_usage_frequency', 5)
            if service_usage is None:
                service_usage = 5
            
            # Calculate confidence score (0-1)
            confidence_score = (
                (satisfaction_score / 10) * 0.4 +  # 40% weight
                (loyalty_score / 100) * 0.3 +      # 30% weight
                min(service_usage / 10, 1) * 0.3    # 30% weight
            )
            
            # Confidence interval width (smaller for higher confidence)
            interval_width = 0.3 * (1 - confidence_score) + 0.1  # 10-40% range
            
            lower_bound = base_price * (1 - interval_width)
            upper_bound = base_price * (1 + interval_width)
            
            return (float(lower_bound), float(upper_bound))
            
        except Exception as e:
            logger.error(f"Error calculating confidence interval: {e}")
            return (base_price * 0.8, base_price * 1.2)
    
    def _generate_justification(self, client: pd.Series, base_price: float, 
                              adjusted_price: float) -> str:
        """
        Generate justification for price recommendation
        
        Args:
            client: Client data series
            base_price: Base price
            adjusted_price: Adjusted price
            
        Returns:
            Justification string
        """
        try:
            price_change = adjusted_price - base_price
            price_change_pct = (price_change / base_price) * 100
            
            if abs(price_change_pct) < 5:
                justification = "Price aligned with market rates and client value"
            elif price_change_pct > 0:
                justification = f"Price increased by {price_change_pct:.1f}% due to high client value and loyalty"
            else:
                justification = f"Price decreased by {abs(price_change_pct):.1f}% to improve competitiveness"
            
            return justification
            
        except Exception as e:
            logger.error(f"Error generating justification: {e}")
            return "Price recommendation based on market analysis"


class ROICalculator:
    """Calculator for ROI impact of pricing decisions"""
    
    def __init__(self):
        """Initialize ROI calculator"""
        logger.info("ROI Calculator initialized")
    
    def calculate_pricing_roi(self, current_pricing: pd.DataFrame, 
                            proposed_pricing: Dict[str, Any],
                            time_horizon_months: int = 12) -> Dict[str, Any]:
        """
        Calculate ROI impact of proposed pricing changes
        
        Args:
            current_pricing: DataFrame with current pricing data
            proposed_pricing: Dictionary with proposed pricing recommendations
            time_horizon_months: Time horizon for ROI calculation in months
            
        Returns:
            Dictionary with ROI metrics
        """
        try:
            total_current_revenue = current_pricing['revenue_generated'].sum() if not current_pricing.empty else 0
            total_proposed_revenue = sum([rec['recommended_price'] for rec in proposed_pricing.values()])
            
            # Calculate revenue impact
            revenue_increase = total_proposed_revenue - total_current_revenue
            revenue_increase_pct = (revenue_increase / total_current_revenue * 100) if total_current_revenue > 0 else 0
            
            # Calculate cost impact (assume 10% of revenue as variable cost)
            current_variable_cost = total_current_revenue * 0.1
            proposed_variable_cost = total_proposed_revenue * 0.1
            cost_increase = proposed_variable_cost - current_variable_cost
            
            # Calculate profit impact
            current_profit = total_current_revenue - current_variable_cost
            proposed_profit = total_proposed_revenue - proposed_variable_cost
            profit_increase = proposed_profit - current_profit
            profit_increase_pct = (profit_increase / current_profit * 100) if current_profit > 0 else 0
            
            # Calculate ROI
            # For simplicity, assume fixed costs remain constant
            roi = (profit_increase / 1000) * 100 if 1000 > 0 else 0  # Assume $1000 implementation cost
            
            roi_metrics = {
                'current_revenue': float(total_current_revenue),
                'proposed_revenue': float(total_proposed_revenue),
                'revenue_increase': float(revenue_increase),
                'revenue_increase_percentage': float(revenue_increase_pct),
                'current_profit': float(current_profit),
                'proposed_profit': float(proposed_profit),
                'profit_increase': float(profit_increase),
                'profit_increase_percentage': float(profit_increase_pct),
                'roi_percentage': float(roi),
                'time_horizon_months': time_horizon_months
            }
            
            logger.info(f"Calculated pricing ROI: {roi_metrics['roi_percentage']:.2f}%")
            return roi_metrics
            
        except Exception as e:
            logger.error(f"Error calculating pricing ROI: {e}")
            return {
                'current_revenue': 0.0,
                'proposed_revenue': 0.0,
                'revenue_increase': 0.0,
                'revenue_increase_percentage': 0.0,
                'current_profit': 0.0,
                'proposed_profit': 0.0,
                'profit_increase': 0.0,
                'profit_increase_percentage': 0.0,
                'roi_percentage': 0.0,
                'time_horizon_months': time_horizon_months
            }


class MarketSensitivityAnalyzer:
    """Analyzer for market sensitivity and competitive positioning"""
    
    def __init__(self):
        """Initialize market sensitivity analyzer"""
        logger.info("Market Sensitivity Analyzer initialized")
    
    def analyze_price_elasticity(self, pricing_history: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze price elasticity based on historical data
        
        Args:
            pricing_history: DataFrame with historical pricing and sales data
            
        Returns:
            Dictionary with elasticity metrics
        """
        try:
            if pricing_history.empty or len(pricing_history) < 10:
                logger.warning("Insufficient data for price elasticity analysis")
                return {
                    'elasticity_coefficient': -1.0,  # Default elastic demand
                    'price_sensitivity_score': 75,   # Medium-high sensitivity
                    'confidence_score': 0.5
                }
            
            # Calculate price elasticity using historical data
            # Price elasticity = (% change in quantity) / (% change in price)
            pricing_history = pricing_history.sort_values('date')
            
            # Calculate percentage changes
            pricing_history['price_pct_change'] = pricing_history['final_price'].pct_change()
            pricing_history['quantity_pct_change'] = pricing_history['units_sold'].pct_change()
            
            # Remove NaN values
            valid_data = pricing_history.dropna(subset=['price_pct_change', 'quantity_pct_change'])
            
            if len(valid_data) < 5:
                logger.warning("Insufficient valid data for elasticity calculation")
                return {
                    'elasticity_coefficient': -1.0,
                    'price_sensitivity_score': 75,
                    'confidence_score': 0.3
                }
            
            # Calculate elasticity coefficient
            # Avoid division by zero
            valid_data = valid_data[valid_data['price_pct_change'] != 0]
            
            if valid_data.empty:
                elasticity = -1.0
            else:
                elasticity_values = valid_data['quantity_pct_change'] / valid_data['price_pct_change']
                elasticity = np.median(elasticity_values)  # Use median to reduce outliers
            
            # Convert to price sensitivity score (0-100, higher = more sensitive)
            # Elasticity typically negative, so we invert and scale
            sensitivity_score = max(0, min(100, 50 - (elasticity * 10)))
            
            # Confidence based on data quality
            confidence_score = min(1.0, len(valid_data) / 50)  # Max confidence at 50 data points
            
            elasticity_metrics = {
                'elasticity_coefficient': float(elasticity),
                'price_sensitivity_score': float(sensitivity_score),
                'confidence_score': float(confidence_score),
                'data_points': len(valid_data)
            }
            
            logger.info(f"Analyzed price elasticity: coefficient={elasticity:.2f}, sensitivity={sensitivity_score:.1f}")
            return elasticity_metrics
            
        except Exception as e:
            logger.error(f"Error analyzing price elasticity: {e}")
            return {
                'elasticity_coefficient': -1.0,
                'price_sensitivity_score': 75,
                'confidence_score': 0.2
            }
    
    def analyze_competitive_positioning(self, competitor_data: pd.DataFrame, 
                                     our_pricing: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze competitive positioning
        
        Args:
            competitor_data: DataFrame with competitor pricing data
            our_pricing: Dictionary with our pricing recommendations
            
        Returns:
            Dictionary with competitive positioning metrics
        """
        try:
            if competitor_data.empty:
                logger.warning("No competitor data available")
                return {
                    'competitive_position': 'unknown',
                    'price_ranking': 0,
                    'market_share_impact': 0.0
                }
            
            # Calculate our average price
            our_avg_price = np.mean([rec['recommended_price'] for rec in our_pricing.values()]) if our_pricing else 100
            
            # Calculate competitor average price
            competitor_avg_price = competitor_data['avg_price'].mean()
            
            # Calculate price difference
            price_difference = our_avg_price - competitor_avg_price
            price_difference_pct = (price_difference / competitor_avg_price) * 100
            
            # Determine competitive position
            if price_difference_pct < -10:
                position = 'underpriced'
            elif price_difference_pct > 10:
                position = 'overpriced'
            else:
                position = 'competitive'
            
            # Estimate price ranking (1 = cheapest, 5 = most expensive)
            all_prices = list(competitor_data['avg_price']) + [our_avg_price]
            all_prices.sort()
            our_rank = all_prices.index(our_avg_price) + 1
            price_ranking = (our_rank / len(all_prices)) * 5  # Scale to 1-5
            
            # Estimate market share impact (simplified)
            if position == 'underpriced':
                market_share_impact = 0.05  # 5% positive impact
            elif position == 'overpriced':
                market_share_impact = -0.03  # 3% negative impact
            else:
                market_share_impact = 0.0  # Neutral impact
            
            competitive_metrics = {
                'competitive_position': position,
                'price_ranking': float(price_ranking),
                'price_difference_percentage': float(price_difference_pct),
                'market_share_impact': float(market_share_impact),
                'our_average_price': float(our_avg_price),
                'competitor_average_price': float(competitor_avg_price)
            }
            
            logger.info(f"Analyzed competitive positioning: {position}, ranking={price_ranking:.1f}")
            return competitive_metrics
            
        except Exception as e:
            logger.error(f"Error analyzing competitive positioning: {e}")
            return {
                'competitive_position': 'unknown',
                'price_ranking': 0,
                'price_difference_percentage': 0.0,
                'market_share_impact': 0.0,
                'our_average_price': 100.0,
                'competitor_average_price': 100.0
            }


# Global instances for easy access
price_recommendation_engine_instance = None
roi_calculator_instance = None
market_sensitivity_analyzer_instance = None


def get_price_recommendation_engine() -> PriceRecommendationEngine:
    """Get singleton price recommendation engine instance"""
    global price_recommendation_engine_instance
    if price_recommendation_engine_instance is None:
        price_recommendation_engine_instance = PriceRecommendationEngine()
    return price_recommendation_engine_instance


def get_roi_calculator() -> ROICalculator:
    """Get singleton ROI calculator instance"""
    global roi_calculator_instance
    if roi_calculator_instance is None:
        roi_calculator_instance = ROICalculator()
    return roi_calculator_instance


def get_market_sensitivity_analyzer() -> MarketSensitivityAnalyzer:
    """Get singleton market sensitivity analyzer instance"""
    global market_sensitivity_analyzer_instance
    if market_sensitivity_analyzer_instance is None:
        market_sensitivity_analyzer_instance = MarketSensitivityAnalyzer()
    return market_sensitivity_analyzer_instance