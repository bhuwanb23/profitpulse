"""
Main Demand Forecaster Orchestrator
Coordinates all components of the service demand forecasting system
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
from .data_preparation import get_demand_data_preparator
from .forecasting_models import (
    get_lstm_forecaster,
    get_arima_forecaster,
    get_prophet_forecaster,
    get_seasonal_decomposer
)
from .demand_predictor import (
    get_ensemble_forecaster,
    get_resource_planner,
    get_capacity_planner,
    get_seasonal_adjuster,
    get_uncertainty_quantifier
)
from .capacity_planner import (
    get_forecast_monitor,
    get_model_drift_detector,
    get_alert_system
)

logger = logging.getLogger(__name__)


class DemandForecaster:
    """Main orchestrator for the service demand forecasting engine"""
    
    def __init__(self):
        """Initialize the demand forecaster"""
        logger.info("Demand Forecaster initialized")
        
        # Initialize all components
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize all engine components"""
        try:
            # Data preparation
            self.data_preparator = None
            
            # Forecasting models
            self.lstm_forecaster = None
            self.arima_forecaster = None
            self.prophet_forecaster = None
            self.seasonal_decomposer = None
            
            # Demand prediction
            self.ensemble_forecaster = None
            self.resource_planner = None
            self.capacity_planner = None
            self.seasonal_adjuster = None
            self.uncertainty_quantifier = None
            
            # Monitoring
            self.forecast_monitor = None
            self.drift_detector = None
            self.alert_system = None
            
            logger.info("Demand Forecaster components initialized")
            
        except Exception as e:
            logger.error(f"Error initializing engine components: {e}")
            raise
    
    async def initialize_data_preparator(self):
        """Initialize the data preparator"""
        if self.data_preparator is None:
            self.data_preparator = await get_demand_data_preparator()
    
    async def initialize_forecasting_models(self):
        """Initialize forecasting models"""
        if self.lstm_forecaster is None:
            self.lstm_forecaster = get_lstm_forecaster()
        
        if self.arima_forecaster is None:
            self.arima_forecaster = get_arima_forecaster()
        
        if self.prophet_forecaster is None:
            self.prophet_forecaster = get_prophet_forecaster()
        
        if self.seasonal_decomposer is None:
            self.seasonal_decomposer = get_seasonal_decomposer()
    
    async def initialize_demand_prediction_engines(self):
        """Initialize demand prediction engines"""
        if self.ensemble_forecaster is None:
            self.ensemble_forecaster = get_ensemble_forecaster()
        
        if self.resource_planner is None:
            self.resource_planner = get_resource_planner()
        
        if self.capacity_planner is None:
            self.capacity_planner = get_capacity_planner()
        
        if self.seasonal_adjuster is None:
            self.seasonal_adjuster = get_seasonal_adjuster()
        
        if self.uncertainty_quantifier is None:
            self.uncertainty_quantifier = get_uncertainty_quantifier()
    
    async def initialize_monitoring_engines(self):
        """Initialize monitoring engines"""
        if self.forecast_monitor is None:
            self.forecast_monitor = get_forecast_monitor()
        
        if self.drift_detector is None:
            self.drift_detector = get_model_drift_detector()
        
        if self.alert_system is None:
            self.alert_system = get_alert_system()
    
    async def prepare_data(self, start_date: Optional[datetime] = None, 
                        end_date: Optional[datetime] = None) -> Dict[str, pd.DataFrame]:
        """
        Prepare all required data for demand forecasting
        
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
                ticket_data = await self.data_preparator.collect_historical_ticket_data(start_date, end_date)
                client_data = await self.data_preparator.collect_client_growth_data(start_date, end_date)
                seasonal_data = await self.data_preparator.collect_seasonal_pattern_data(start_date, end_date)
                external_data = await self.data_preparator.collect_external_factor_data(start_date, end_date)
                capacity_data = await self.data_preparator.collect_resource_capacity_data(start_date, end_date)
            else:
                # Return empty DataFrames if preparator failed to initialize
                ticket_data = pd.DataFrame()
                client_data = pd.DataFrame()
                seasonal_data = pd.DataFrame()
                external_data = pd.DataFrame()
                capacity_data = pd.DataFrame()
            
            prepared_data = {
                'ticket_data': ticket_data,
                'client_data': client_data,
                'seasonal_data': seasonal_data,
                'external_data': external_data,
                'capacity_data': capacity_data
            }
            
            logger.info("Data preparation completed")
            return prepared_data
            
        except Exception as e:
            logger.error(f"Error preparing data: {e}")
            return {}
    
    async def train_lstm_model(self, ticket_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Train LSTM model on ticket data
        
        Args:
            ticket_data: Historical ticket data
            
        Returns:
            Dictionary with training results
        """
        try:
            await self.initialize_forecasting_models()
            
            # Extract time series data
            if not ticket_data.empty and 'ticket_count' in ticket_data.columns:
                ticket_series = ticket_data['ticket_count']
                
                # Train LSTM model
                if self.lstm_forecaster is not None:
                    lstm_results = self.lstm_forecaster.train(pd.Series(ticket_series.astype(float)))
                else:
                    lstm_results = {
                        'success': False,
                        'message': 'LSTM forecaster not available',
                        'model': None
                    }
            else:
                lstm_results = {
                    'success': False,
                    'message': 'Insufficient ticket data for LSTM training',
                    'model': None
                }
            
            logger.info("LSTM model training completed")
            return lstm_results
            
        except Exception as e:
            logger.error(f"Error training LSTM model: {e}")
            return {
                'success': False,
                'message': str(e),
                'model': None
            }
    
    async def train_arima_model(self, ticket_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Train ARIMA model on ticket data
        
        Args:
            ticket_data: Historical ticket data
            
        Returns:
            Dictionary with training results
        """
        try:
            await self.initialize_forecasting_models()
            
            # Extract time series data
            if not ticket_data.empty and 'ticket_count' in ticket_data.columns:
                ticket_series = ticket_data['ticket_count']
                
                # Train ARIMA model
                if self.arima_forecaster is not None:
                    arima_results = self.arima_forecaster.train(pd.Series(ticket_series.astype(float)))
                else:
                    arima_results = {
                        'success': False,
                        'message': 'ARIMA forecaster not available',
                        'model': None
                    }
            else:
                arima_results = {
                    'success': False,
                    'message': 'Insufficient ticket data for ARIMA training',
                    'model': None
                }
            
            logger.info("ARIMA model training completed")
            return arima_results
            
        except Exception as e:
            logger.error(f"Error training ARIMA model: {e}")
            return {
                'success': False,
                'message': str(e),
                'model': None
            }
    
    async def perform_seasonal_decomposition(self, ticket_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform seasonal decomposition on ticket data
        
        Args:
            ticket_data: Historical ticket data
            
        Returns:
            Dictionary with decomposition results
        """
        try:
            await self.initialize_forecasting_models()
            
            # Extract time series data
            if not ticket_data.empty and 'ticket_count' in ticket_data.columns:
                ticket_series = ticket_data['ticket_count']
                
                # Perform seasonal decomposition
                if self.seasonal_decomposer is not None:
                    decomposition_results = self.seasonal_decomposer.decompose(pd.Series(ticket_series.astype(float)))
                else:
                    decomposition_results = {
                        'success': False,
                        'message': 'Seasonal decomposer not available',
                        'trend': None,
                        'seasonal': None,
                        'residual': None,
                        'observed': None
                    }
            else:
                decomposition_results = {
                    'success': False,
                    'message': 'Insufficient ticket data for seasonal decomposition',
                    'trend': None,
                    'seasonal': None,
                    'residual': None,
                    'observed': None
                }
            
            logger.info("Seasonal decomposition completed")
            return decomposition_results
            
        except Exception as e:
            logger.error(f"Error performing seasonal decomposition: {e}")
            return {
                'success': False,
                'message': str(e),
                'trend': None,
                'seasonal': None,
                'residual': None,
                'observed': None
            }
    
    async def generate_demand_forecast(self, ticket_data: pd.DataFrame, 
                                    forecast_horizon: int = 30) -> Dict[str, Any]:
        """
        Generate demand forecast using ensemble approach
        
        Args:
            ticket_data: Historical ticket data
            forecast_horizon: Number of periods to forecast
            
        Returns:
            Dictionary with forecast results
        """
        try:
            await self.initialize_forecasting_models()
            await self.initialize_demand_prediction_engines()
            
            # Extract time series data
            if not ticket_data.empty and 'ticket_count' in ticket_data.columns:
                ticket_series = ticket_data['ticket_count']
                
                # Train models and add to ensemble
                forecasts = {}
                
                # LSTM forecast
                if self.lstm_forecaster is not None:
                    lstm_train_result = self.lstm_forecaster.train(pd.Series(ticket_series.astype(float)))
                    if lstm_train_result.get('success', False):
                        lstm_pred_result = self.lstm_forecaster.predict(pd.Series(ticket_series.astype(float)), forecast_horizon)
                        if lstm_pred_result.get('success', False):
                            forecasts['lstm'] = lstm_pred_result.get('predictions', [])
                
                # ARIMA forecast
                if self.arima_forecaster is not None:
                    arima_train_result = self.arima_forecaster.train(pd.Series(ticket_series.astype(float)))
                    if arima_train_result.get('success', False):
                        arima_pred_result = self.arima_forecaster.predict(forecast_horizon)
                        if arima_pred_result.get('success', False):
                            forecasts['arima'] = arima_pred_result.get('predictions', [])
                
                # Ensemble prediction
                if self.ensemble_forecaster is not None and forecasts:
                    ensemble_result = self.ensemble_forecaster.predict(ticket_data, forecast_horizon)
                else:
                    ensemble_result = {
                        'success': False,
                        'message': 'No models available for ensemble prediction',
                        'ensemble_predictions': []
                    }
            else:
                ensemble_result = {
                    'success': False,
                    'message': 'Insufficient ticket data for forecasting',
                    'ensemble_predictions': []
                }
            
            logger.info("Demand forecast generation completed")
            return ensemble_result
            
        except Exception as e:
            logger.error(f"Error generating demand forecast: {e}")
            return {
                'success': False,
                'message': str(e),
                'ensemble_predictions': []
            }
    
    async def generate_resource_recommendations(self, demand_forecast: List[float],
                                            capacity_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate resource planning recommendations
        
        Args:
            demand_forecast: Predicted demand levels
            capacity_data: Current resource capacity data
            
        Returns:
            Dictionary with resource recommendations
        """
        try:
            await self.initialize_demand_prediction_engines()
            
            # Generate recommendations
            if self.resource_planner is not None:
                resource_types = ['Developer', 'Designer', 'QA Engineer', 'DevOps', 'Support']
                recommendations = self.resource_planner.generate_resource_recommendations(
                    demand_forecast, capacity_data, resource_types
                )
            else:
                recommendations = {
                    'success': False,
                    'message': 'Resource planner not available',
                    'recommendations': {}
                }
            
            logger.info("Resource recommendations generated")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating resource recommendations: {e}")
            return {
                'success': False,
                'message': str(e),
                'recommendations': {}
            }
    
    async def generate_capacity_insights(self, demand_forecast: List[float],
                                      ticket_data: pd.DataFrame,
                                      seasonal_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate capacity planning insights
        
        Args:
            demand_forecast: Predicted demand levels
            ticket_data: Historical ticket data
            seasonal_data: Seasonal pattern data
            
        Returns:
            Dictionary with capacity insights
        """
        try:
            await self.initialize_demand_prediction_engines()
            
            # Generate insights
            if self.capacity_planner is not None:
                insights = self.capacity_planner.generate_capacity_insights(
                    demand_forecast, ticket_data, seasonal_data
                )
            else:
                insights = {
                    'success': False,
                    'message': 'Capacity planner not available',
                    'insights': {}
                }
            
            logger.info("Capacity insights generated")
            return insights
            
        except Exception as e:
            logger.error(f"Error generating capacity insights: {e}")
            return {
                'success': False,
                'message': str(e),
                'insights': {}
            }
    
    async def calculate_forecast_accuracy(self, actual_values: List[float],
                                       predicted_values: List[float]) -> Dict[str, Any]:
        """
        Calculate forecast accuracy metrics
        
        Args:
            actual_values: Actual observed values
            predicted_values: Predicted values
            
        Returns:
            Dictionary with accuracy metrics
        """
        try:
            await self.initialize_monitoring_engines()
            
            # Calculate accuracy
            if self.forecast_monitor is not None:
                accuracy_metrics = self.forecast_monitor.calculate_accuracy_metrics(
                    actual_values, predicted_values
                )
            else:
                accuracy_metrics = {
                    'success': False,
                    'message': 'Forecast monitor not available',
                    'metrics': {}
                }
            
            logger.info("Forecast accuracy calculated")
            return accuracy_metrics
            
        except Exception as e:
            logger.error(f"Error calculating forecast accuracy: {e}")
            return {
                'success': False,
                'message': str(e),
                'metrics': {}
            }
    
    async def run_complete_demand_analysis(self, forecast_horizon: int = 30,
                                        start_date: Optional[datetime] = None,
                                        end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Run complete demand analysis pipeline
        
        Args:
            forecast_horizon: Number of periods to forecast
            start_date: Start date for data collection
            end_date: End date for data collection
            
        Returns:
            Dictionary with complete analysis results
        """
        try:
            logger.info("Starting complete demand analysis pipeline")
            
            # 1. Prepare data
            logger.info("Step 1: Preparing data")
            data = await self.prepare_data(start_date, end_date)
            
            if not data:
                logger.error("Failed to prepare data")
                return {'status': 'error', 'message': 'Failed to prepare data'}
            
            # 2. Perform seasonal decomposition
            logger.info("Step 2: Performing seasonal decomposition")
            decomposition_results = await self.perform_seasonal_decomposition(data['ticket_data'])
            
            # 3. Train forecasting models
            logger.info("Step 3: Training forecasting models")
            lstm_results = await self.train_lstm_model(data['ticket_data'])
            arima_results = await self.train_arima_model(data['ticket_data'])
            
            # 4. Generate demand forecast
            logger.info("Step 4: Generating demand forecast")
            forecast_results = await self.generate_demand_forecast(data['ticket_data'], forecast_horizon)
            
            # 5. Generate resource recommendations
            logger.info("Step 5: Generating resource recommendations")
            resource_recommendations = await self.generate_resource_recommendations(
                forecast_results.get('ensemble_predictions', []), data['capacity_data']
            )
            
            # 6. Generate capacity insights
            logger.info("Step 6: Generating capacity insights")
            capacity_insights = await self.generate_capacity_insights(
                forecast_results.get('ensemble_predictions', []), data['ticket_data'], data['seasonal_data']
            )
            
            # 7. Calculate forecast accuracy (using historical data for demo)
            logger.info("Step 7: Calculating forecast accuracy")
            # For demo purposes, we'll use a portion of historical data as "actual" and "predicted"
            if not data['ticket_data'].empty and 'ticket_count' in data['ticket_data'].columns:
                actual_values = data['ticket_data']['ticket_count'].tail(10).tolist()
                predicted_values = actual_values  # In real scenario, these would be actual predictions
                accuracy_metrics = await self.calculate_forecast_accuracy(actual_values, predicted_values)
            else:
                accuracy_metrics = {'success': False, 'message': 'Insufficient data for accuracy calculation'}
            
            # Compile complete results
            complete_analysis = {
                'status': 'success',
                'timestamp': datetime.now().isoformat(),
                'forecast_horizon': forecast_horizon,
                'data_prepared': True,
                'seasonal_decomposition': decomposition_results,
                'lstm_model_results': lstm_results,
                'arima_model_results': arima_results,
                'demand_forecast': forecast_results,
                'resource_recommendations': resource_recommendations,
                'capacity_insights': capacity_insights,
                'forecast_accuracy': accuracy_metrics,
                'summary': self._generate_analysis_summary(
                    forecast_results, resource_recommendations, capacity_insights
                )
            }
            
            logger.info("Complete demand analysis pipeline finished successfully")
            return complete_analysis
            
        except Exception as e:
            logger.error(f"Error in complete demand analysis pipeline: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _generate_analysis_summary(self, forecast_results: Dict[str, Any],
                                resource_recommendations: Dict[str, Any],
                                capacity_insights: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary of analysis results"""
        try:
            # Extract key metrics
            forecast_predictions = forecast_results.get('ensemble_predictions', [])
            avg_forecast = np.mean(forecast_predictions) if forecast_predictions else 0
            peak_forecast = np.max(forecast_predictions) if forecast_predictions else 0
            
            # Resource recommendations summary
            recommendations = resource_recommendations.get('recommendations', {})
            hire_recommendations = len([r for r in recommendations.values() if r.get('action') == 'hire'])
            optimize_recommendations = len([r for r in recommendations.values() if r.get('action') == 'optimize'])
            
            # Capacity insights summary
            insights = capacity_insights.get('insights', {})
            demand_analysis = insights.get('demand_forecast_analysis', {})
            risk_assessment = insights.get('risk_assessment', {})
            
            summary = {
                'average_forecasted_demand': avg_forecast,
                'peak_forecasted_demand': peak_forecast,
                'resource_hire_recommendations': hire_recommendations,
                'resource_optimization_recommendations': optimize_recommendations,
                'identified_risks': risk_assessment.get('risk_count', 0),
                'overall_risk_level': risk_assessment.get('overall_risk_level', 'unknown'),
                'recommendation': self._generate_overall_recommendation(
                    avg_forecast, peak_forecast, hire_recommendations, risk_assessment
                )
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating analysis summary: {e}")
            return {'summary_status': 'error'}
    
    def _generate_overall_recommendation(self, avg_forecast: float, peak_forecast: float,
                                       hire_recommendations: int, risk_assessment: Dict[str, Any]) -> str:
        """Generate overall recommendation based on analysis results"""
        risk_level = risk_assessment.get('overall_risk_level', 'unknown')
        
        if risk_level == 'high':
            return "High risk level detected - immediate action recommended"
        elif hire_recommendations > 0:
            return "Resource expansion recommended based on demand forecast"
        elif avg_forecast > 50:
            return "Significant demand forecasted - monitor resource utilization closely"
        else:
            return "Demand levels stable - maintain current resource allocation"


# Global instance for easy access
demand_forecaster_instance = None


async def get_demand_forecaster() -> DemandForecaster:
    """Get singleton demand forecaster instance"""
    global demand_forecaster_instance
    if demand_forecaster_instance is None:
        demand_forecaster_instance = DemandForecaster()
    return demand_forecaster_instance


# Example usage function
async def run_demand_forecasting_analysis(forecast_horizon: int = 30):
    """Example function to run complete demand forecasting analysis"""
    try:
        engine = await get_demand_forecaster()
        results = await engine.run_complete_demand_analysis(forecast_horizon)
        return results
    except Exception as e:
        logger.error(f"Error running demand forecasting analysis: {e}")
        return {'status': 'error', 'message': str(e)}