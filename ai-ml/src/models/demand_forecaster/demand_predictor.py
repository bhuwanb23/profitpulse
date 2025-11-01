"""
Demand Prediction System for Service Demand Forecaster
Implements ensemble forecasting, resource planning recommendations, and capacity planning insights
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


class EnsembleForecaster:
    """Ensemble forecasting system combining multiple models"""
    
    def __init__(self):
        """Initialize ensemble forecaster"""
        self.models = {}
        self.weights = {}
        logger.info("Ensemble Forecaster initialized")
    
    def add_model(self, name: str, model: Any, weight: float = 1.0):
        """
        Add a model to the ensemble
        
        Args:
            name: Name of the model
            model: Model object
            weight: Weight for the model in ensemble predictions
        """
        self.models[name] = model
        self.weights[name] = weight
        logger.info(f"Model {name} added to ensemble with weight {weight}")
    
    def predict(self, data: pd.DataFrame, steps: int = 30) -> Dict[str, Any]:
        """
        Make ensemble predictions
        
        Args:
            data: Input data for prediction
            steps: Number of steps to predict
            
        Returns:
            Dictionary with ensemble predictions
        """
        try:
            predictions = {}
            
            # Get predictions from all models
            for name, model in self.models.items():
                if hasattr(model, 'predict'):
                    pred_result = model.predict(data, steps)
                    if pred_result.get('success', False):
                        predictions[name] = {
                            'predictions': pred_result.get('predictions', []),
                            'weight': self.weights.get(name, 1.0)
                        }
            
            if not predictions:
                logger.warning("No valid predictions from ensemble models")
                return {
                    'success': False,
                    'message': 'No valid predictions from ensemble models',
                    'ensemble_predictions': [],
                    'model_contributions': {}
                }
            
            # Combine predictions using weighted average
            ensemble_predictions = self._combine_predictions(predictions, steps)
            
            logger.info(f"Ensemble prediction completed for {steps} steps")
            return {
                'success': True,
                'message': 'Ensemble prediction completed',
                'ensemble_predictions': ensemble_predictions,
                'model_contributions': predictions,
                'prediction_steps': steps
            }
            
        except Exception as e:
            logger.error(f"Error in ensemble prediction: {e}")
            return {
                'success': False,
                'message': f'Ensemble prediction error: {str(e)}',
                'ensemble_predictions': [],
                'model_contributions': {}
            }
    
    def _combine_predictions(self, predictions: Dict[str, Dict], steps: int) -> List[float]:
        """Combine predictions using weighted average"""
        if not predictions:
            return []
        
        # Initialize combined predictions
        combined = np.zeros(steps)
        total_weight = 0.0
        
        # Combine predictions from all models
        for model_name, model_pred in predictions.items():
            weight = model_pred.get('weight', 1.0)
            preds = model_pred.get('predictions', [])
            
            # Ensure we have the right number of predictions
            if len(preds) >= steps:
                combined += np.array(preds[:steps]) * weight
                total_weight += weight
            elif len(preds) > 0:
                # If we have fewer predictions, use what we have
                padded_preds = preds + [preds[-1]] * (steps - len(preds))  # Pad with last value
                combined += np.array(padded_preds) * weight
                total_weight += weight
        
        # Normalize by total weight
        if total_weight > 0:
            combined = combined / total_weight
        
        return combined.tolist()


class ResourcePlanner:
    """Resource planning recommendation system"""
    
    def __init__(self):
        """Initialize resource planner"""
        logger.info("Resource Planner initialized")
    
    def generate_resource_recommendations(self, demand_forecast: List[float], 
                                       current_capacity: pd.DataFrame,
                                       resource_types: List[str]) -> Dict[str, Any]:
        """
        Generate resource planning recommendations based on demand forecast
        
        Args:
            demand_forecast: Predicted demand levels
            current_capacity: Current resource capacity data
            resource_types: Types of resources to plan for
            
        Returns:
            Dictionary with resource recommendations
        """
        try:
            recommendations = {}
            
            # Calculate average forecasted demand
            avg_demand = np.mean(demand_forecast) if demand_forecast else 0
            peak_demand = np.max(demand_forecast) if demand_forecast else 0
            
            # Generate recommendations for each resource type
            for resource_type in resource_types:
                # Find current capacity for this resource type
                resource_capacity = current_capacity[
                    current_capacity['resource_type'] == resource_type
                ] if 'resource_type' in current_capacity.columns else pd.DataFrame()
                
                if not resource_capacity.empty:
                    current_utilization = resource_capacity['utilization_rate'].mean()
                    available_capacity = resource_capacity['available_capacity_hours'].mean()
                    
                    # Calculate required capacity based on demand
                    required_capacity = self._calculate_required_capacity(
                        float(avg_demand), float(peak_demand), resource_type
                    )
                    
                    # Generate recommendation
                    recommendation = self._generate_resource_recommendation(
                        resource_type, float(current_utilization), float(available_capacity), 
                        float(required_capacity)
                    )
                    
                    recommendations[resource_type] = recommendation
                else:
                    # Default recommendation if no data
                    recommendations[resource_type] = {
                        'action': 'maintain',
                        'reasoning': 'Insufficient capacity data available',
                        'required_capacity': avg_demand,
                        'current_utilization': 0.0,
                        'recommendation': 'Monitor resource utilization'
                    }
            
            logger.info("Resource planning recommendations generated")
            return {
                'success': True,
                'message': 'Resource recommendations generated',
                'recommendations': recommendations,
                'average_forecasted_demand': avg_demand,
                'peak_forecasted_demand': peak_demand
            }
            
        except Exception as e:
            logger.error(f"Error generating resource recommendations: {e}")
            return {
                'success': False,
                'message': f'Resource recommendation error: {str(e)}',
                'recommendations': {},
                'error': str(e)
            }
    
    def _calculate_required_capacity(self, avg_demand: float, peak_demand: float, 
                                  resource_type: str) -> float:
        """Calculate required capacity for a resource type"""
        # Base capacity calculation
        base_capacity = avg_demand * 1.2  # 20% buffer
        
        # Resource-specific adjustments
        if resource_type == 'Developer':
            capacity = base_capacity * 1.5  # Developers need more capacity
        elif resource_type == 'Designer':
            capacity = base_capacity * 1.2
        elif resource_type == 'QA Engineer':
            capacity = base_capacity * 1.0
        elif resource_type == 'DevOps':
            capacity = base_capacity * 0.8  # DevOps more efficient
        elif resource_type == 'Support':
            capacity = base_capacity * 1.3  # Support needs buffer for emergencies
        else:
            capacity = base_capacity
        
        # Add peak demand consideration
        peak_buffer = (peak_demand - avg_demand) * 0.5
        capacity += peak_buffer
        
        return capacity
    
    def _generate_resource_recommendation(self, resource_type: str, 
                                       current_utilization: float,
                                       available_capacity: float,
                                       required_capacity: float) -> Dict[str, Any]:
        """Generate specific recommendation for a resource type"""
        utilization_ratio = required_capacity / available_capacity if available_capacity > 0 else 0
        
        if utilization_ratio > 1.2:
            action = 'hire'
            reasoning = f'High demand forecast requires {utilization_ratio:.1f}x current capacity'
            recommendation = f'Consider hiring {max(1, int(utilization_ratio - 1))} additional {resource_type}(s)'
        elif utilization_ratio > 0.9:
            action = 'optimize'
            reasoning = f'Demand forecast near capacity limit ({utilization_ratio:.1f}x)'
            recommendation = f'Optimize resource allocation and consider temporary support'
        elif utilization_ratio > 0.7:
            action = 'maintain'
            reasoning = f'Adequate capacity with buffer ({utilization_ratio:.1f}x)'
            recommendation = 'Maintain current resource levels with regular monitoring'
        else:
            action = 'reduce'
            reasoning = f'Excess capacity available ({utilization_ratio:.1f}x)'
            recommendation = f'Consider reducing resources or reallocating to other projects'
        
        return {
            'action': action,
            'reasoning': reasoning,
            'required_capacity': required_capacity,
            'current_utilization': current_utilization,
            'utilization_ratio': utilization_ratio,
            'recommendation': recommendation
        }


class CapacityPlanner:
    """Capacity planning insights generator"""
    
    def __init__(self):
        """Initialize capacity planner"""
        logger.info("Capacity Planner initialized")
    
    def generate_capacity_insights(self, demand_forecast: List[float],
                                historical_data: pd.DataFrame,
                                seasonal_patterns: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate capacity planning insights
        
        Args:
            demand_forecast: Predicted demand levels
            historical_data: Historical demand data
            seasonal_patterns: Seasonal pattern data
            
        Returns:
            Dictionary with capacity insights
        """
        try:
            # Calculate key metrics
            avg_forecast = np.mean(demand_forecast) if demand_forecast else 0
            peak_forecast = np.max(demand_forecast) if demand_forecast else 0
            
            # Historical analysis
            historical_avg = historical_data['ticket_count'].mean() if not historical_data.empty and 'ticket_count' in historical_data.columns else 0
            historical_peak = historical_data['ticket_count'].max() if not historical_data.empty and 'ticket_count' in historical_data.columns else 0
            
            # Growth rate calculation
            growth_rate = ((avg_forecast - historical_avg) / historical_avg * 100) if historical_avg > 0 else 0
            
            # Seasonal analysis
            seasonal_insights = self._analyze_seasonal_patterns(seasonal_patterns)
            
            # Capacity requirements
            capacity_requirements = self._calculate_capacity_requirements(
                float(avg_forecast), float(peak_forecast), float(historical_avg), float(historical_peak)
            )
            
            insights = {
                'demand_forecast_analysis': {
                    'average_forecast': avg_forecast,
                    'peak_forecast': peak_forecast,
                    'forecast_horizon_days': len(demand_forecast)
                },
                'historical_comparison': {
                    'historical_average': historical_avg,
                    'historical_peak': historical_peak,
                    'growth_rate_percent': growth_rate
                },
                'seasonal_insights': seasonal_insights,
                'capacity_requirements': capacity_requirements,
                'risk_assessment': self._assess_capacity_risks(float(avg_forecast), float(peak_forecast), historical_data)
            }
            
            logger.info("Capacity planning insights generated")
            return {
                'success': True,
                'message': 'Capacity insights generated',
                'insights': insights
            }
            
        except Exception as e:
            logger.error(f"Error generating capacity insights: {e}")
            return {
                'success': False,
                'message': f'Capacity insight error: {str(e)}',
                'insights': {},
                'error': str(e)
            }
    
    def _analyze_seasonal_patterns(self, seasonal_patterns: pd.DataFrame) -> Dict[str, Any]:
        """Analyze seasonal patterns for capacity planning"""
        if seasonal_patterns.empty:
            return {
                'seasonal_trend': 'unknown',
                'peak_season': 'unknown',
                'low_season': 'unknown',
                'seasonal_adjustment_factor': 1.0
            }
        
        # Analyze monthly patterns
        if 'monthly_seasonality' in seasonal_patterns.columns:
            avg_monthly = seasonal_patterns['monthly_seasonality'].mean()
            max_monthly = seasonal_patterns['monthly_seasonality'].max()
            min_monthly = seasonal_patterns['monthly_seasonality'].min()
            
            if max_monthly > 1.2:
                peak_season = 'High season detected'
            elif min_monthly < 0.8:
                peak_season = 'Low season detected'
            else:
                peak_season = 'Stable seasonal pattern'
            
            return {
                'seasonal_trend': 'calculated',
                'peak_season': peak_season,
                'low_season': 'Notable variations detected' if min_monthly < 0.8 else 'Relatively stable',
                'seasonal_adjustment_factor': avg_monthly
            }
        
        return {
            'seasonal_trend': 'unknown',
            'peak_season': 'unknown',
            'low_season': 'unknown',
            'seasonal_adjustment_factor': 1.0
        }
    
    def _calculate_capacity_requirements(self, avg_forecast: float, peak_forecast: float,
                                      historical_avg: float, historical_peak: float) -> Dict[str, Any]:
        """Calculate capacity requirements"""
        # Base requirements
        base_capacity = avg_forecast * 1.2  # 20% buffer
        peak_capacity = peak_forecast * 1.3  # 30% buffer for peaks
        
        # Compare with historical
        historical_capacity = historical_avg * 1.2
        historical_peak_capacity = historical_peak * 1.3
        
        return {
            'base_required_capacity': base_capacity,
            'peak_required_capacity': peak_capacity,
            'historical_base_capacity': historical_capacity,
            'historical_peak_capacity': historical_peak_capacity,
            'capacity_increase_percent': ((base_capacity - historical_capacity) / historical_capacity * 100) if historical_capacity > 0 else 0
        }
    
    def _assess_capacity_risks(self, avg_forecast: float, peak_forecast: float,
                            historical_data: pd.DataFrame) -> Dict[str, Any]:
        """Assess capacity-related risks"""
        risks = []
        
        # High demand risk
        if avg_forecast > 50:  # Threshold for high demand
            risks.append({
                'risk_type': 'high_demand',
                'severity': 'high',
                'description': 'Forecast indicates high service demand',
                'recommendation': 'Ensure adequate resource allocation'
            })
        
        # Peak demand risk
        if peak_forecast > 100:  # Threshold for peak demand
            risks.append({
                'risk_type': 'peak_demand',
                'severity': 'medium',
                'description': 'Forecast indicates significant peak demand periods',
                'recommendation': 'Plan for surge capacity'
            })
        
        # Volatility risk
        if not historical_data.empty and 'ticket_count' in historical_data.columns:
            volatility = historical_data['ticket_count'].std() / historical_data['ticket_count'].mean() if historical_data['ticket_count'].mean() > 0 else 0
            if volatility > 0.5:  # High volatility
                risks.append({
                    'risk_type': 'demand_volatility',
                    'severity': 'medium',
                    'description': 'Historical demand shows high volatility',
                    'recommendation': 'Maintain flexible resource allocation'
                })
        
        return {
            'identified_risks': risks,
            'risk_count': len(risks),
            'overall_risk_level': 'high' if len([r for r in risks if r['severity'] == 'high']) > 0 else 'medium' if len(risks) > 0 else 'low'
        }


class SeasonalAdjuster:
    """Seasonal adjustment algorithms for demand forecasting"""
    
    def __init__(self):
        """Initialize seasonal adjuster"""
        logger.info("Seasonal Adjuster initialized")
    
    def apply_seasonal_adjustment(self, forecast: List[float], 
                                seasonal_factors: List[float]) -> List[float]:
        """
        Apply seasonal adjustments to forecast
        
        Args:
            forecast: Base forecast values
            seasonal_factors: Seasonal adjustment factors
            
        Returns:
            Seasonally adjusted forecast
        """
        try:
            if not forecast or not seasonal_factors:
                return forecast
            
            # Extend seasonal factors to match forecast length
            extended_factors = self._extend_seasonal_factors(seasonal_factors, len(forecast))
            
            # Apply adjustments
            adjusted_forecast = [
                forecast[i] * extended_factors[i] for i in range(len(forecast))
            ]
            
            return adjusted_forecast
            
        except Exception as e:
            logger.error(f"Error applying seasonal adjustment: {e}")
            return forecast
    
    def _extend_seasonal_factors(self, factors: List[float], target_length: int) -> List[float]:
        """Extend seasonal factors to target length"""
        if not factors:
            return [1.0] * target_length
        
        extended = []
        for i in range(target_length):
            factor_index = i % len(factors)
            extended.append(factors[factor_index])
        
        return extended


class UncertaintyQuantifier:
    """Uncertainty quantification for demand forecasts"""
    
    def __init__(self):
        """Initialize uncertainty quantifier"""
        logger.info("Uncertainty Quantifier initialized")
    
    def quantify_uncertainty(self, forecasts: Dict[str, List[float]], 
                           historical_errors: List[float]) -> Dict[str, Any]:
        """
        Quantify uncertainty in forecasts
        
        Args:
            forecasts: Dictionary of forecasts from different models
            historical_errors: Historical forecast errors
            
        Returns:
            Dictionary with uncertainty metrics
        """
        try:
            # Calculate uncertainty metrics
            uncertainty_metrics = {}
            
            # Overall uncertainty from historical errors
            if historical_errors:
                mean_error = np.mean(historical_errors)
                std_error = np.std(historical_errors)
                uncertainty_metrics['historical_uncertainty'] = {
                    'mean_error': mean_error,
                    'std_error': std_error,
                    'confidence_interval_95': [mean_error - 1.96 * std_error, mean_error + 1.96 * std_error]
                }
            
            # Model-specific uncertainty
            model_uncertainty = {}
            for model_name, predictions in forecasts.items():
                if predictions:
                    # Simple uncertainty based on prediction range
                    pred_std = np.std(predictions) if len(predictions) > 1 else 0
                    model_uncertainty[model_name] = {
                        'prediction_std': pred_std,
                        'prediction_range': [np.min(predictions), np.max(predictions)],
                        'relative_uncertainty': pred_std / np.mean(predictions) if np.mean(predictions) > 0 else 0
                    }
            
            uncertainty_metrics['model_uncertainty'] = model_uncertainty
            
            # Ensemble uncertainty
            if len(forecasts) > 1:
                # Calculate disagreement between models
                all_predictions = list(forecasts.values())
                if all_predictions and all(len(pred) > 0 for pred in all_predictions):
                    # Calculate variance across models for each time step
                    ensemble_variance = []
                    for i in range(len(all_predictions[0])):
                        step_predictions = [pred[i] for pred in all_predictions if i < len(pred)]
                        if step_predictions:
                            ensemble_variance.append(np.var(step_predictions))
                        else:
                            ensemble_variance.append(0)
                    
                    uncertainty_metrics['ensemble_uncertainty'] = {
                        'mean_variance': np.mean(ensemble_variance) if ensemble_variance else 0,
                        'max_variance': np.max(ensemble_variance) if ensemble_variance else 0,
                        'model_disagreement': np.mean(ensemble_variance) / (np.mean([np.mean(pred) for pred in all_predictions]) or 1)
                    }
            
            logger.info("Uncertainty quantification completed")
            return {
                'success': True,
                'message': 'Uncertainty quantification completed',
                'uncertainty_metrics': uncertainty_metrics
            }
            
        except Exception as e:
            logger.error(f"Error quantifying uncertainty: {e}")
            return {
                'success': False,
                'message': f'Uncertainty quantification error: {str(e)}',
                'uncertainty_metrics': {}
            }


# Global instances for easy access
ensemble_forecaster_instance = None
resource_planner_instance = None
capacity_planner_instance = None
seasonal_adjuster_instance = None
uncertainty_quantifier_instance = None


def get_ensemble_forecaster() -> EnsembleForecaster:
    """Get singleton ensemble forecaster instance"""
    global ensemble_forecaster_instance
    if ensemble_forecaster_instance is None:
        ensemble_forecaster_instance = EnsembleForecaster()
    return ensemble_forecaster_instance


def get_resource_planner() -> ResourcePlanner:
    """Get singleton resource planner instance"""
    global resource_planner_instance
    if resource_planner_instance is None:
        resource_planner_instance = ResourcePlanner()
    return resource_planner_instance


def get_capacity_planner() -> CapacityPlanner:
    """Get singleton capacity planner instance"""
    global capacity_planner_instance
    if capacity_planner_instance is None:
        capacity_planner_instance = CapacityPlanner()
    return capacity_planner_instance


def get_seasonal_adjuster() -> SeasonalAdjuster:
    """Get singleton seasonal adjuster instance"""
    global seasonal_adjuster_instance
    if seasonal_adjuster_instance is None:
        seasonal_adjuster_instance = SeasonalAdjuster()
    return seasonal_adjuster_instance


def get_uncertainty_quantifier() -> UncertaintyQuantifier:
    """Get singleton uncertainty quantifier instance"""
    global uncertainty_quantifier_instance
    if uncertainty_quantifier_instance is None:
        uncertainty_quantifier_instance = UncertaintyQuantifier()
    return uncertainty_quantifier_instance