"""
Budget Allocation System for Budget Optimization Model
Handles optimal distribution calculation, efficiency gain estimation, and resource reallocation recommendations
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


class BudgetAllocator:
    """Main budget allocation system"""
    
    def __init__(self):
        """Initialize budget allocator"""
        logger.info("Budget Allocator initialized")
    
    def calculate_optimal_distribution(self, budget_data: pd.DataFrame,
                                    service_costs: pd.DataFrame,
                                    client_priorities: pd.DataFrame,
                                    roi_data: pd.DataFrame,
                                    resource_data: pd.DataFrame,
                                    total_budget: float) -> Dict[str, Any]:
        """
        Calculate optimal budget distribution across services and clients
        
        Args:
            budget_data: DataFrame with budget constraints
            service_costs: DataFrame with service cost data
            client_priorities: DataFrame with client priority data
            roi_data: DataFrame with ROI data
            resource_data: DataFrame with resource data
            total_budget: Total available budget
            
        Returns:
            Dictionary with allocation results
        """
        try:
            # Calculate priority scores for services
            service_scores = self._calculate_service_scores(service_costs, roi_data)
            
            # Calculate client allocation weights
            client_weights = self._calculate_client_weights(client_priorities)
            
            # Calculate resource requirements
            resource_requirements = self._calculate_resource_requirements(service_costs, resource_data)
            
            # Simple allocation algorithm (can be enhanced with optimization)
            allocations = self._allocate_budget_simple(
                service_scores, client_weights, resource_requirements, total_budget
            )
            
            # Calculate efficiency gains
            efficiency_gains = self._estimate_efficiency_gains(allocations, service_costs, roi_data)
            
            allocation_results = {
                'total_budget': total_budget,
                'allocations': allocations,
                'efficiency_gains': efficiency_gains,
                'resource_utilization': resource_requirements,
                'service_scores': service_scores,
                'client_weights': client_weights
            }
            
            logger.info(f"Calculated optimal distribution for ${total_budget:,.2f} budget")
            return allocation_results
            
        except Exception as e:
            logger.error(f"Error calculating optimal distribution: {e}")
            return {
                'total_budget': total_budget,
                'allocations': {},
                'efficiency_gains': {},
                'error': str(e)
            }
    
    def _calculate_service_scores(self, service_costs: pd.DataFrame, 
                                roi_data: pd.DataFrame) -> Dict[str, float]:
        """Calculate priority scores for services"""
        service_scores = {}
        
        # Score based on ROI data
        for _, item in roi_data.iterrows():
            if 'service' in item['investment_type'].lower():
                service_id = item['item_id'].replace('ITEM-', 'SERVICE-')
                service_scores[service_id] = item['roi_percentage'] * 100  # Scale ROI to score
        
        # Score based on service costs and profitability
        for _, service in service_costs.iterrows():
            service_id = service['service_id']
            if service_id not in service_scores:
                # Profitability score (higher margin = higher score)
                profitability_score = service['profit_margin'] * 50
                
                # Market rate advantage (higher advantage = higher score)
                market_advantage = (service['market_rate'] - service['unit_cost']) / service['unit_cost'] * 20
                
                service_scores[service_id] = profitability_score + market_advantage
        
        # Normalize scores
        if service_scores:
            max_score = max(service_scores.values())
            if max_score > 0:
                service_scores = {k: v/max_score * 100 for k, v in service_scores.items()}
        
        return service_scores
    
    def _calculate_client_weights(self, client_priorities: pd.DataFrame) -> Dict[str, float]:
        """Calculate allocation weights for clients"""
        client_weights = {}
        
        # Weight based on multiple factors
        for _, client in client_priorities.iterrows():
            client_id = client['client_id']
            
            # Revenue contribution weight (0-30%)
            revenue_weight = (client['revenue_contribution'] / 200000) * 30
            
            # Strategic importance weight (0-25%)
            strategic_weight = (client['strategic_importance'] / 10) * 25
            
            # Growth potential weight (0-20%)
            growth_weight = (client['growth_potential'] / 100) * 20
            
            # Loyalty score weight (0-15%)
            loyalty_weight = (client['loyalty_score'] / 100) * 15
            
            # Satisfaction weight (0-10%)
            satisfaction_weight = (client['client_satisfaction'] / 10) * 10
            
            total_weight = (
                revenue_weight + strategic_weight + growth_weight + 
                loyalty_weight + satisfaction_weight
            )
            
            client_weights[client_id] = min(total_weight, 100)  # Cap at 100
        
        # Normalize weights
        if client_weights:
            total_weight = sum(client_weights.values())
            if total_weight > 0:
                client_weights = {k: v/total_weight for k, v in client_weights.items()}
        
        return client_weights
    
    def _calculate_resource_requirements(self, service_costs: pd.DataFrame,
                                       resource_data: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """Calculate resource requirements for services"""
        resource_requirements = {}
        
        # Calculate requirements based on service costs
        for _, service in service_costs.iterrows():
            service_id = service['service_id']
            requirements = {
                'personnel_hours': service['average_duration_hours'] * service['resource_requirements'],
                'equipment_cost': service['unit_cost'] * 0.3,  # 30% equipment cost
                'software_cost': service['unit_cost'] * 0.2,   # 20% software cost
                'facility_cost': service['unit_cost'] * 0.1    # 10% facility cost
            }
            resource_requirements[service_id] = requirements
        
        return resource_requirements
    
    def _allocate_budget_simple(self, service_scores: Dict[str, float],
                              client_weights: Dict[str, float],
                              resource_requirements: Dict[str, Dict[str, float]],
                              total_budget: float) -> Dict[str, float]:
        """Simple budget allocation algorithm"""
        allocations = {}
        
        # Allocate based on service scores and client weights
        total_score = sum(service_scores.values()) if service_scores else 1
        
        for service_id, score in service_scores.items():
            # Base allocation based on service score
            score_allocation = (score / total_score) * total_budget * 0.7  # 70% based on service score
            
            # Additional allocation based on client weights (simplified)
            client_allocation = total_budget * 0.3 / len(service_scores) if service_scores else 0
            
            allocations[service_id] = score_allocation + client_allocation
        
        # Ensure total allocation doesn't exceed budget
        current_total = sum(allocations.values())
        if current_total > 0:
            scaling_factor = total_budget / current_total
            allocations = {k: v * scaling_factor for k, v in allocations.items()}
        
        return allocations
    
    def _estimate_efficiency_gains(self, allocations: Dict[str, float],
                                 service_costs: pd.DataFrame,
                                 roi_data: pd.DataFrame) -> Dict[str, float]:
        """Estimate efficiency gains from budget allocation"""
        efficiency_gains = {}
        
        # Estimate gains based on ROI improvement
        for service_id, allocation in allocations.items():
            # Find corresponding ROI data
            roi_items = roi_data[roi_data['item_id'].str.contains(service_id.replace('SERVICE-', 'ITEM-'), na=False)]
            
            if not roi_items.empty:
                avg_roi = roi_items['roi_percentage'].mean()
                # Efficiency gain proportional to ROI and allocation
                gain = allocation * avg_roi * 0.1  # 10% of ROI-weighted allocation
                efficiency_gains[service_id] = max(gain, 0)
            else:
                # Default gain estimation
                efficiency_gains[service_id] = allocation * 0.05  # 5% default gain
        
        return efficiency_gains


class ResourceReallocator:
    """Resource reallocation recommendation system"""
    
    def __init__(self):
        """Initialize resource reallocator"""
        logger.info("Resource Reallocator initialized")
    
    def generate_reallocation_recommendations(self, current_allocations: Dict[str, float],
                                           performance_data: pd.DataFrame,
                                           budget_constraints: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Generate resource reallocation recommendations
        
        Args:
            current_allocations: Current budget allocations
            performance_data: DataFrame with performance metrics
            budget_constraints: DataFrame with budget constraints
            
        Returns:
            List of reallocation recommendations
        """
        try:
            recommendations = []
            
            # Analyze performance vs allocation
            performance_analysis = self._analyze_performance(current_allocations, performance_data)
            
            # Generate reallocation suggestions
            for service_id, metrics in performance_analysis.items():
                recommendation = self._generate_recommendation(
                    service_id, metrics, current_allocations.get(service_id, 0)
                )
                if recommendation:
                    recommendations.append(recommendation)
            
            # Sort recommendations by impact
            recommendations.sort(key=lambda x: x.get('impact_score', 0), reverse=True)
            
            logger.info(f"Generated {len(recommendations)} reallocation recommendations")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating reallocation recommendations: {e}")
            return []
    
    def _analyze_performance(self, allocations: Dict[str, float],
                           performance_data: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """Analyze performance metrics vs allocations"""
        analysis = {}
        
        for service_id, allocation in allocations.items():
            # Find performance data for this service
            service_performance = performance_data[
                performance_data['service_id'] == service_id
            ] if 'service_id' in performance_data.columns else pd.DataFrame()
            
            if not service_performance.empty:
                metrics = {
                    'allocation': allocation,
                    'revenue_generated': service_performance['revenue_generated'].sum() if 'revenue_generated' in service_performance.columns else 0,
                    'cost_incurred': service_performance['cost_incurred'].sum() if 'cost_incurred' in service_performance.columns else allocation,
                    'efficiency_ratio': 0,
                    'performance_score': 0
                }
                
                # Calculate efficiency ratio
                if metrics['cost_incurred'] > 0:
                    metrics['efficiency_ratio'] = metrics['revenue_generated'] / metrics['cost_incurred']
                
                # Calculate performance score (ROI-like metric)
                if allocation > 0:
                    metrics['performance_score'] = (metrics['revenue_generated'] - metrics['cost_incurred']) / allocation
                
                analysis[service_id] = metrics
            else:
                # Default analysis for services without performance data
                analysis[service_id] = {
                    'allocation': allocation,
                    'revenue_generated': allocation * 1.2,  # Assume 20% ROI
                    'cost_incurred': allocation,
                    'efficiency_ratio': 1.2,
                    'performance_score': 0.2
                }
        
        return analysis
    
    def _generate_recommendation(self, service_id: str, metrics: Dict[str, float],
                               current_allocation: float) -> Optional[Dict[str, Any]]:
        """Generate reallocation recommendation for a service"""
        # Determine recommendation based on performance
        if metrics['performance_score'] > 0.3:
            # High performing - increase allocation
            recommended_change = current_allocation * 0.2  # +20%
            action = 'increase'
            impact_score = metrics['performance_score'] * 100
        elif metrics['performance_score'] < 0.1:
            # Poor performing - decrease allocation
            recommended_change = -current_allocation * 0.3  # -30%
            action = 'decrease'
            impact_score = abs(metrics['performance_score']) * 50
        else:
            # Moderate performing - small adjustment
            recommended_change = current_allocation * 0.05  # +5%
            action = 'increase' if metrics['performance_score'] > 0.15 else 'decrease'
            impact_score = metrics['performance_score'] * 25
        
        # Ensure recommendations are reasonable
        if abs(recommended_change) < 100:  # Minimum $100 change
            return None
        
        return {
            'service_id': service_id,
            'action': action,
            'current_allocation': current_allocation,
            'recommended_change': recommended_change,
            'new_allocation': current_allocation + recommended_change,
            'impact_score': impact_score,
            'efficiency_ratio': metrics['efficiency_ratio'],
            'performance_score': metrics['performance_score'],
            'reasoning': self._generate_reasoning(action, metrics)
        }
    
    def _generate_reasoning(self, action: str, metrics: Dict[str, float]) -> str:
        """Generate reasoning for recommendation"""
        if action == 'increase':
            if metrics['performance_score'] > 0.3:
                return "High ROI performance - increasing allocation for greater returns"
            else:
                return "Moderate performance with potential for improvement"
        else:
            if metrics['performance_score'] < 0.1:
                return "Low ROI performance - reallocating resources to higher performing areas"
            else:
                return "Optimizing resource distribution for better efficiency"


class EfficiencyGainEstimator:
    """Efficiency gain estimation models"""
    
    def __init__(self):
        """Initialize efficiency gain estimator"""
        logger.info("Efficiency Gain Estimator initialized")
    
    def estimate_gains(self, budget_proposal: Dict[str, Any],
                      historical_data: pd.DataFrame) -> Dict[str, float]:
        """
        Estimate efficiency gains from budget proposal
        
        Args:
            budget_proposal: Proposed budget allocation
            historical_data: Historical performance data
            
        Returns:
            Dictionary with estimated gains
        """
        try:
            gains = {}
            
            # Extract allocations
            allocations = budget_proposal.get('allocations', {})
            
            # Estimate gains for each allocation
            for service_id, allocation in allocations.items():
                gain = self._estimate_service_gain(service_id, allocation, historical_data)
                gains[service_id] = gain
            
            # Calculate total estimated gains
            total_gain = sum(gains.values())
            
            gain_estimates = {
                'service_gains': gains,
                'total_estimated_gain': total_gain,
                'roi_improvement': total_gain / sum(allocations.values()) if allocations else 0,
                'efficiency_multiplier': (sum(allocations.values()) + total_gain) / sum(allocations.values()) if allocations else 1
            }
            
            logger.info(f"Estimated total efficiency gains: ${total_gain:,.2f}")
            return gain_estimates
            
        except Exception as e:
            logger.error(f"Error estimating efficiency gains: {e}")
            return {
                'service_gains': {},
                'total_estimated_gain': 0,
                'error': str(e)
            }
    
    def _estimate_service_gain(self, service_id: str, allocation: float,
                             historical_data: pd.DataFrame) -> float:
        """Estimate gain for a specific service"""
        # Find historical data for this service
        service_history = historical_data[
            historical_data['service_id'] == service_id
        ] if 'service_id' in historical_data.columns else pd.DataFrame()
        
        if not service_history.empty:
            # Calculate historical ROI
            total_revenue = service_history['revenue_generated'].sum() if 'revenue_generated' in service_history.columns else allocation * 1.1
            total_cost = service_history['cost_incurred'].sum() if 'cost_incurred' in service_history.columns else allocation
            
            historical_roi = (total_revenue - total_cost) / total_cost if total_cost > 0 else 0.1
            
            # Estimate gain based on improved allocation
            # Assume 10-30% improvement in efficiency
            improvement_factor = 1 + np.random.uniform(0.1, 0.3)
            estimated_gain = allocation * historical_roi * improvement_factor - allocation * historical_roi
            
            return max(estimated_gain, 0)
        else:
            # Default estimation
            return allocation * 0.15  # Assume 15% gain


# Global instances for easy access
budget_allocator_instance = None
resource_reallocator_instance = None
efficiency_gain_estimator_instance = None


def get_budget_allocator() -> BudgetAllocator:
    """Get singleton budget allocator instance"""
    global budget_allocator_instance
    if budget_allocator_instance is None:
        budget_allocator_instance = BudgetAllocator()
    return budget_allocator_instance


def get_resource_reallocator() -> ResourceReallocator:
    """Get singleton resource reallocator instance"""
    global resource_reallocator_instance
    if resource_reallocator_instance is None:
        resource_reallocator_instance = ResourceReallocator()
    return resource_reallocator_instance


def get_efficiency_gain_estimator() -> EfficiencyGainEstimator:
    """Get singleton efficiency gain estimator instance"""
    global efficiency_gain_estimator_instance
    if efficiency_gain_estimator_instance is None:
        efficiency_gain_estimator_instance = EfficiencyGainEstimator()
    return efficiency_gain_estimator_instance