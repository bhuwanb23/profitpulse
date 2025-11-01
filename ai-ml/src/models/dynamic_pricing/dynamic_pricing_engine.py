"""
Main Dynamic Pricing Engine Orchestrator
Coordinates all components of the dynamic pricing system
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import asyncio
import warnings
warnings.filterwarnings('ignore')

# Import all modules
from .data_preparation import get_pricing_data_preparator
from .reinforcement_learning import (
    get_q_learning_agent, 
    get_multi_armed_bandit_agent, 
    get_pricing_reward_function
)
from .pricing_optimizer import (
    get_price_recommendation_engine,
    get_roi_calculator,
    get_market_sensitivity_analyzer
)
from .market_analysis import (
    get_market_trend_analyzer,
    get_competitive_intelligence_analyzer,
    get_demand_forecast_analyzer
)
from .pricing_predictor import (
    get_client_acceptance_predictor,
    get_pricing_strategy_validator,
    get_pricing_performance_monitor
)

logger = logging.getLogger(__name__)


class DynamicPricingEngine:
    """Main orchestrator for the dynamic pricing engine"""
    
    def __init__(self):
        """Initialize the dynamic pricing engine"""
        logger.info("Dynamic Pricing Engine initialized")
        
        # Initialize all components
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize all engine components"""
        try:
            # Data preparation
            self.data_preparator = None
            
            # Reinforcement learning agents
            self.q_learning_agent = None
            self.multi_armed_bandit_agent = None
            self.reward_function = None
            
            # Pricing optimization
            self.price_recommendation_engine = None
            self.roi_calculator = None
            self.market_sensitivity_analyzer = None
            
            # Market analysis
            self.market_trend_analyzer = None
            self.competitive_intelligence_analyzer = None
            self.demand_forecast_analyzer = None
            
            # Pricing prediction and validation
            self.client_acceptance_predictor = None
            self.pricing_strategy_validator = None
            self.pricing_performance_monitor = None
            
            logger.info("Dynamic Pricing Engine components initialized")
            
        except Exception as e:
            logger.error(f"Error initializing engine components: {e}")
            raise
    
    async def initialize_data_preparator(self):
        """Initialize the data preparator"""
        if self.data_preparator is None:
            self.data_preparator = await get_pricing_data_preparator()
    
    async def initialize_reinforcement_learning_agents(self, price_points: List[float]):
        """Initialize reinforcement learning agents"""
        if self.q_learning_agent is None:
            self.q_learning_agent = get_q_learning_agent()
            # Define state and action spaces
            self.q_learning_agent.define_state_space([
                'client_value', 'market_trend', 'competition_level', 
                'seasonal_factor', 'demand_index'
            ])
            self.q_learning_agent.define_action_space(price_points)
        
        if self.multi_armed_bandit_agent is None:
            self.multi_armed_bandit_agent = get_multi_armed_bandit_agent(len(price_points))
        
        if self.reward_function is None:
            self.reward_function = get_pricing_reward_function()
    
    async def initialize_pricing_optimization_engines(self):
        """Initialize pricing optimization engines"""
        if self.price_recommendation_engine is None:
            self.price_recommendation_engine = get_price_recommendation_engine()
        
        if self.roi_calculator is None:
            self.roi_calculator = get_roi_calculator()
        
        if self.market_sensitivity_analyzer is None:
            self.market_sensitivity_analyzer = get_market_sensitivity_analyzer()
    
    async def initialize_market_analysis_engines(self):
        """Initialize market analysis engines"""
        if self.market_trend_analyzer is None:
            self.market_trend_analyzer = get_market_trend_analyzer()
        
        if self.competitive_intelligence_analyzer is None:
            self.competitive_intelligence_analyzer = get_competitive_intelligence_analyzer()
        
        if self.demand_forecast_analyzer is None:
            self.demand_forecast_analyzer = get_demand_forecast_analyzer()
    
    async def initialize_prediction_and_validation_engines(self):
        """Initialize prediction and validation engines"""
        if self.client_acceptance_predictor is None:
            self.client_acceptance_predictor = get_client_acceptance_predictor()
        
        if self.pricing_strategy_validator is None:
            self.pricing_strategy_validator = get_pricing_strategy_validator()
        
        if self.pricing_performance_monitor is None:
            self.pricing_performance_monitor = get_pricing_performance_monitor()
    
    async def prepare_data(self, start_date: Optional[datetime] = None, 
                        end_date: Optional[datetime] = None) -> Dict[str, pd.DataFrame]:
        """
        Prepare all required data for pricing analysis
        
        Args:
            start_date: Start date for data collection
            end_date: End date for data collection
            
        Returns:
            Dictionary with all prepared data
        """
        try:
            await self.initialize_data_preparator()
            
            # Collect all required data
            if self.data_preparator is not None:
                market_rate_data = await self.data_preparator.collect_market_rate_data(start_date, end_date)
                client_value_data = await self.data_preparator.collect_client_value_data(start_date, end_date)
                service_complexity_data = await self.data_preparator.collect_service_complexity_data(start_date, end_date)
                competitive_pricing_data = await self.data_preparator.collect_competitive_pricing_data(start_date, end_date)
                pricing_history_data = await self.data_preparator.collect_pricing_history_data(start_date, end_date)
            else:
                # Return empty DataFrames if preparator failed to initialize
                market_rate_data = pd.DataFrame()
                client_value_data = pd.DataFrame()
                service_complexity_data = pd.DataFrame()
                competitive_pricing_data = pd.DataFrame()
                pricing_history_data = pd.DataFrame()
            
            prepared_data = {
                'market_rates': market_rate_data,
                'client_values': client_value_data,
                'service_complexity': service_complexity_data,
                'competitive_pricing': competitive_pricing_data,
                'pricing_history': pricing_history_data
            }
            
            logger.info("Data preparation completed")
            return prepared_data
            
        except Exception as e:
            logger.error(f"Error preparing data: {e}")
            return {}
    
    async def analyze_market_conditions(self, market_data: pd.DataFrame, 
                                     competitor_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze current market conditions
        
        Args:
            market_data: Market rate data
            competitor_data: Competitor pricing data
            
        Returns:
            Dictionary with market analysis results
        """
        try:
            await self.initialize_market_analysis_engines()
            
            # Analyze market trends
            if self.market_trend_analyzer is not None:
                market_trends = self.market_trend_analyzer.analyze_market_trends(market_data)
                seasonality = self.market_trend_analyzer.detect_seasonality(market_data)
            else:
                market_trends = {}
                seasonality = {}
            
            # Analyze competitive landscape
            if self.competitive_intelligence_analyzer is not None:
                competitive_analysis = self.competitive_intelligence_analyzer.analyze_competitive_landscape(competitor_data)
            else:
                competitive_analysis = {}
            
            market_analysis = {
                'market_trends': market_trends,
                'competitive_analysis': competitive_analysis,
                'seasonality': seasonality
            }
            
            logger.info("Market condition analysis completed")
            return market_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing market conditions: {e}")
            return {}
    
    async def generate_price_recommendations(self, client_data: pd.DataFrame,
                                          service_data: pd.DataFrame,
                                          market_data: pd.DataFrame,
                                          competitor_data: pd.DataFrame,
                                          client_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate price recommendations for clients
        
        Args:
            client_data: Client value data
            service_data: Service complexity data
            market_data: Market rate data
            competitor_data: Competitor pricing data
            client_id: Specific client ID (optional)
            
        Returns:
            Dictionary with price recommendations
        """
        try:
            await self.initialize_pricing_optimization_engines()
            
            # Generate recommendations
            if self.price_recommendation_engine is not None:
                recommendations = self.price_recommendation_engine.generate_price_recommendation(
                    client_data, service_data, market_data, competitor_data, client_id
                )
            else:
                recommendations = {}
            
            logger.info(f"Generated price recommendations for {len(recommendations)} clients")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating price recommendations: {e}")
            return {}
    
    async def predict_client_acceptance(self, client_data: pd.DataFrame,
                                     proposed_pricing: Dict[str, Any],
                                     historical_data: Optional[pd.DataFrame] = None) -> Dict[str, float]:
        """
        Predict client acceptance of proposed pricing
        
        Args:
            client_data: Client value data
            proposed_pricing: Proposed pricing recommendations
            historical_data: Historical pricing data (optional)
            
        Returns:
            Dictionary with acceptance probabilities
        """
        try:
            await self.initialize_prediction_and_validation_engines()
            
            # Predict acceptance
            if self.client_acceptance_predictor is not None:
                acceptance_probabilities = self.client_acceptance_predictor.predict_acceptance_probability(
                    client_data, proposed_pricing, historical_data
                )
            else:
                acceptance_probabilities = {}
            
            logger.info(f"Predicted client acceptance for {len(acceptance_probabilities)} clients")
            return acceptance_probabilities
            
        except Exception as e:
            logger.error(f"Error predicting client acceptance: {e}")
            return {}
    
    async def calculate_pricing_roi(self, current_pricing: pd.DataFrame,
                                 proposed_pricing: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate ROI impact of proposed pricing changes
        
        Args:
            current_pricing: Current pricing data
            proposed_pricing: Proposed pricing recommendations
            
        Returns:
            Dictionary with ROI metrics
        """
        try:
            await self.initialize_pricing_optimization_engines()
            
            # Calculate ROI
            if self.roi_calculator is not None:
                roi_metrics = self.roi_calculator.calculate_pricing_roi(current_pricing, proposed_pricing)
            else:
                roi_metrics = {}
            
            logger.info("Calculated pricing ROI")
            return roi_metrics
            
        except Exception as e:
            logger.error(f"Error calculating pricing ROI: {e}")
            return {}
    
    async def validate_pricing_strategy(self, proposed_pricing: Dict[str, Any],
                                     client_data: pd.DataFrame,
                                     market_data: pd.DataFrame,
                                     competitor_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate proposed pricing strategy
        
        Args:
            proposed_pricing: Proposed pricing recommendations
            client_data: Client value data
            market_data: Market rate data
            competitor_data: Competitor pricing data
            
        Returns:
            Dictionary with validation results
        """
        try:
            await self.initialize_prediction_and_validation_engines()
            
            # Validate strategy
            if self.pricing_strategy_validator is not None:
                validation_results = self.pricing_strategy_validator.validate_pricing_strategy(
                    proposed_pricing, client_data, market_data, competitor_data
                )
            else:
                validation_results = {}
            
            logger.info("Validated pricing strategy")
            return validation_results
            
        except Exception as e:
            logger.error(f"Error validating pricing strategy: {e}")
            return {}
    
    async def optimize_pricing_with_rl(self, client_data: pd.DataFrame,
                                    market_data: pd.DataFrame,
                                    competitor_data: pd.DataFrame,
                                    episodes: int = 100) -> Dict[str, Any]:
        """
        Optimize pricing using reinforcement learning
        
        Args:
            client_data: Client value data
            market_data: Market rate data
            competitor_data: Competitor pricing data
            episodes: Number of training episodes
            
        Returns:
            Dictionary with RL optimization results
        """
        try:
            # Define price points for action space
            base_prices: List[float] = [80.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0, 150.0]
            await self.initialize_reinforcement_learning_agents(base_prices)
            
            # Check if all RL components are initialized
            if (self.q_learning_agent is None or 
                self.reward_function is None):
                logger.warning("RL components not properly initialized")
                return {}
            
            # Training loop
            total_rewards = []
            
            for episode in range(episodes):
                episode_reward = 0
                
                # Process each client
                for _, client in client_data.iterrows():
                    client_id = client['client_id']
                    
                    # Get current state
                    client_value_raw = client.get('revenue_contribution', 10000)
                    client_value = float(client_value_raw) if client_value_raw is not None else 10000.0
                    
                    market_trend_raw = market_data['market_rate'].pct_change().mean() if len(market_data) > 1 else 0
                    market_trend = float(market_trend_raw) if market_trend_raw is not None else 0.0
                    
                    competition_level = float(len(competitor_data))
                    
                    state_features = {
                        'client_value': client_value,
                        'market_trend': market_trend,
                        'competition_level': competition_level,
                        'seasonal_factor': 1.0,  # Simplified
                        'demand_index': 1.0  # Simplified
                    }
                    
                    if self.q_learning_agent is not None:
                        state = self.q_learning_agent.get_state(state_features)
                        
                        # Select action (price point)
                        action = self.q_learning_agent.get_action(state, training=True)
                        
                        # Calculate reward (simplified)
                        service_usage_raw = client.get('service_usage_frequency', 5)
                        service_usage = float(service_usage_raw) if service_usage_raw is not None else 5.0
                        revenue = action * service_usage
                        cost = revenue * 0.3  # Assume 30% cost
                        client_retention = 0.8 if action < 120 else 0.6  # Simplified retention model
                        market_share = 0.1  # Simplified
                        competitor_avg_price = float(competitor_data['avg_price'].mean() if not competitor_data.empty else 100)
                        
                        if self.reward_function is not None:
                            reward = self.reward_function.calculate_reward(
                                revenue, cost, client_retention, market_share, competitor_avg_price
                            )
                        else:
                            reward = 0
                        
                        # Update Q-value
                        # For simplicity, we'll use the same state as next state
                        self.q_learning_agent.update_q_value(state, action, reward, state, done=True)
                        
                        episode_reward += reward
                
                # Decay exploration rate
                if self.q_learning_agent is not None:
                    self.q_learning_agent.decay_epsilon()
                
                total_rewards.append(episode_reward)
                
                # Log progress
                if (episode + 1) % 20 == 0:
                    avg_reward = np.mean(total_rewards[-20:])
                    logger.info(f"Episode {episode + 1}/{episodes}, Average Reward: {avg_reward:.2f}")
            
            # Get final policy
            if self.q_learning_agent is not None:
                policy = self.q_learning_agent.get_policy()
                q_table_size = len(self.q_learning_agent.q_table)
            else:
                policy = {}
                q_table_size = 0
            
            rl_results = {
                'total_episodes': episodes,
                'final_policy': policy,
                'total_rewards': total_rewards,
                'average_final_reward': float(np.mean(total_rewards[-10:])) if total_rewards else 0,
                'q_table_size': q_table_size
            }
            
            logger.info("Reinforcement learning optimization completed")
            return rl_results
            
        except Exception as e:
            logger.error(f"Error optimizing pricing with RL: {e}")
            return {}
    
    async def run_complete_pricing_analysis(self, client_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Run complete pricing analysis pipeline
        
        Args:
            client_id: Specific client ID to analyze (optional)
            
        Returns:
            Dictionary with complete analysis results
        """
        try:
            logger.info("Starting complete pricing analysis pipeline")
            
            # 1. Prepare data
            logger.info("Step 1: Preparing data")
            data = await self.prepare_data()
            
            if not data:
                logger.error("Failed to prepare data")
                return {'status': 'error', 'message': 'Failed to prepare data'}
            
            # 2. Analyze market conditions
            logger.info("Step 2: Analyzing market conditions")
            market_analysis = await self.analyze_market_conditions(
                data['market_rates'], data['competitive_pricing']
            )
            
            # 3. Generate price recommendations
            logger.info("Step 3: Generating price recommendations")
            recommendations = await self.generate_price_recommendations(
                data['client_values'], data['service_complexity'],
                data['market_rates'], data['competitive_pricing'], client_id
            )
            
            # 4. Predict client acceptance
            logger.info("Step 4: Predicting client acceptance")
            acceptance_probs = await self.predict_client_acceptance(
                data['client_values'], recommendations, data['pricing_history']
            )
            
            # 5. Calculate ROI
            logger.info("Step 5: Calculating pricing ROI")
            roi_metrics = await self.calculate_pricing_roi(data['pricing_history'], recommendations)
            
            # 6. Validate pricing strategy
            logger.info("Step 6: Validating pricing strategy")
            validation_results = await self.validate_pricing_strategy(
                recommendations, data['client_values'], 
                data['market_rates'], data['competitive_pricing']
            )
            
            # 7. Optimize with reinforcement learning (optional)
            logger.info("Step 7: Optimizing with reinforcement learning")
            rl_results = await self.optimize_pricing_with_rl(
                data['client_values'], data['market_rates'], data['competitive_pricing']
            )
            
            # Compile complete results
            complete_analysis = {
                'status': 'success',
                'timestamp': datetime.now().isoformat(),
                'data_prepared': True,
                'market_analysis': market_analysis,
                'price_recommendations': recommendations,
                'client_acceptance_probabilities': acceptance_probs,
                'roi_metrics': roi_metrics,
                'validation_results': validation_results,
                'rl_optimization_results': rl_results,
                'summary': self._generate_analysis_summary(
                    recommendations, acceptance_probs, roi_metrics, validation_results
                )
            }
            
            logger.info("Complete pricing analysis pipeline finished successfully")
            return complete_analysis
            
        except Exception as e:
            logger.error(f"Error in complete pricing analysis pipeline: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _generate_analysis_summary(self, recommendations: Dict[str, Any],
                                acceptance_probs: Dict[str, float],
                                roi_metrics: Dict[str, Any],
                                validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate summary of analysis results
        
        Args:
            recommendations: Price recommendations
            acceptance_probs: Client acceptance probabilities
            roi_metrics: ROI metrics
            validation_results: Validation results
            
        Returns:
            Dictionary with analysis summary
        """
        try:
            # Calculate key summary metrics
            total_clients = len(recommendations)
            
            # Average recommended price change
            price_changes = [float(rec.get('price_change_percentage', 0)) for rec in recommendations.values()] if recommendations else []
            avg_price_change = float(np.mean(price_changes)) if price_changes else 0.0
            
            # Average acceptance probability
            acceptance_values = list(acceptance_probs.values()) if acceptance_probs else []
            avg_acceptance = float(np.mean(acceptance_values)) if acceptance_values else 0.0
            
            # Expected revenue impact
            expected_revenue = float(roi_metrics.get('revenue_increase_percentage', 0)) if roi_metrics else 0.0
            
            # Risk assessment
            risk_level = validation_results.get('risk_assessment', 'unknown') if validation_results else 'unknown'
            
            summary = {
                'total_clients_analyzed': total_clients,
                'average_price_change_percentage': float(avg_price_change),
                'average_client_acceptance_probability': float(avg_acceptance),
                'expected_revenue_change_percentage': float(expected_revenue),
                'risk_assessment': risk_level,
                'recommendation': self._generate_overall_recommendation(
                    avg_price_change, avg_acceptance, expected_revenue, risk_level
                )
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating analysis summary: {e}")
            return {'summary_status': 'error'}
    
    def _generate_overall_recommendation(self, avg_price_change: float,
                                      avg_acceptance: float,
                                      expected_revenue: float,
                                      risk_level: str) -> str:
        """
        Generate overall recommendation based on analysis results
        
        Args:
            avg_price_change: Average price change percentage
            avg_acceptance: Average acceptance probability
            expected_revenue: Expected revenue change percentage
            risk_level: Risk assessment level
            
        Returns:
            Recommendation string
        """
        if risk_level == 'high':
            return "High risk detected - consider conservative pricing adjustments"
        elif avg_acceptance < 0.6:
            return "Low client acceptance predicted - review pricing strategy"
        elif expected_revenue > 10:
            return "Positive revenue impact expected - proceed with implementation"
        elif avg_price_change > 15:
            return "Significant price increases proposed - monitor client reactions closely"
        else:
            return "Balanced pricing strategy - implementation recommended with monitoring"


# Global instance for easy access
dynamic_pricing_engine_instance = None


async def get_dynamic_pricing_engine() -> DynamicPricingEngine:
    """Get singleton dynamic pricing engine instance"""
    global dynamic_pricing_engine_instance
    if dynamic_pricing_engine_instance is None:
        dynamic_pricing_engine_instance = DynamicPricingEngine()
    return dynamic_pricing_engine_instance


# Example usage function
async def run_dynamic_pricing_analysis():
    """Example function to run complete dynamic pricing analysis"""
    try:
        engine = await get_dynamic_pricing_engine()
        results = await engine.run_complete_pricing_analysis()
        return results
    except Exception as e:
        logger.error(f"Error running dynamic pricing analysis: {e}")
        return {'status': 'error', 'message': str(e)}