"""
Main Budget Optimization Engine Orchestrator
Coordinates all components of the budget optimization system
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
from .data_preparation import get_budget_data_preparator
from .optimization_algorithms import (
    get_linear_programming_optimizer,
    get_genetic_algorithm_optimizer,
    get_simulated_annealing_optimizer,
    get_particle_swarm_optimizer,
    get_multi_objective_optimizer
)
from .budget_allocator import (
    get_budget_allocator,
    get_resource_reallocator,
    get_efficiency_gain_estimator
)
from .performance_tracker import (
    get_budget_performance_tracker,
    get_roi_maximization_strategy,
    get_budget_benchmarking
)

logger = logging.getLogger(__name__)


class BudgetOptimizer:
    """Main orchestrator for the budget optimization engine"""
    
    def __init__(self):
        """Initialize the budget optimizer"""
        logger.info("Budget Optimizer initialized")
        
        # Initialize all components
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize all engine components"""
        try:
            # Data preparation
            self.data_preparator = None
            
            # Optimization algorithms
            self.lp_optimizer = None
            self.ga_optimizer = None
            self.sa_optimizer = None
            self.pso_optimizer = None
            self.mo_optimizer = None
            
            # Budget allocation
            self.budget_allocator = None
            self.resource_reallocator = None
            self.efficiency_estimator = None
            
            # Performance tracking
            self.performance_tracker = None
            self.roi_strategy = None
            self.benchmarking = None
            
            logger.info("Budget Optimizer components initialized")
            
        except Exception as e:
            logger.error(f"Error initializing engine components: {e}")
            raise
    
    async def initialize_data_preparator(self):
        """Initialize the data preparator"""
        if self.data_preparator is None:
            self.data_preparator = await get_budget_data_preparator()
    
    async def initialize_optimization_algorithms(self):
        """Initialize optimization algorithms"""
        if self.lp_optimizer is None:
            self.lp_optimizer = get_linear_programming_optimizer()
        
        if self.ga_optimizer is None:
            self.ga_optimizer = get_genetic_algorithm_optimizer()
        
        if self.sa_optimizer is None:
            self.sa_optimizer = get_simulated_annealing_optimizer()
        
        if self.pso_optimizer is None:
            self.pso_optimizer = get_particle_swarm_optimizer()
        
        if self.mo_optimizer is None:
            self.mo_optimizer = get_multi_objective_optimizer()
    
    async def initialize_budget_allocation_engines(self):
        """Initialize budget allocation engines"""
        if self.budget_allocator is None:
            self.budget_allocator = get_budget_allocator()
        
        if self.resource_reallocator is None:
            self.resource_reallocator = get_resource_reallocator()
        
        if self.efficiency_estimator is None:
            self.efficiency_estimator = get_efficiency_gain_estimator()
    
    async def initialize_performance_tracking_engines(self):
        """Initialize performance tracking engines"""
        if self.performance_tracker is None:
            self.performance_tracker = get_budget_performance_tracker()
        
        if self.roi_strategy is None:
            self.roi_strategy = get_roi_maximization_strategy()
        
        if self.benchmarking is None:
            self.benchmarking = get_budget_benchmarking()
    
    async def prepare_data(self, start_date: Optional[datetime] = None, 
                        end_date: Optional[datetime] = None) -> Dict[str, pd.DataFrame]:
        """
        Prepare all required data for budget optimization
        
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
                budget_data = await self.data_preparator.collect_budget_data(start_date, end_date)
                service_costs = await self.data_preparator.collect_service_cost_data(start_date, end_date)
                client_priorities = await self.data_preparator.collect_client_priority_data(start_date, end_date)
                roi_data = await self.data_preparator.collect_roi_data(start_date, end_date)
                resource_data = await self.data_preparator.collect_resource_data(start_date, end_date)
            else:
                # Return empty DataFrames if preparator failed to initialize
                budget_data = pd.DataFrame()
                service_costs = pd.DataFrame()
                client_priorities = pd.DataFrame()
                roi_data = pd.DataFrame()
                resource_data = pd.DataFrame()
            
            prepared_data = {
                'budget_data': budget_data,
                'service_costs': service_costs,
                'client_priorities': client_priorities,
                'roi_data': roi_data,
                'resource_data': resource_data
            }
            
            logger.info("Data preparation completed")
            return prepared_data
            
        except Exception as e:
            logger.error(f"Error preparing data: {e}")
            return {}
    
    async def optimize_budget_linear_programming(self, budget_data: pd.DataFrame,
                                              service_costs: pd.DataFrame,
                                              total_budget: float) -> Dict[str, Any]:
        """
        Optimize budget using Linear Programming
        
        Args:
            budget_data: Budget constraints data
            service_costs: Service cost data
            total_budget: Total available budget
            
        Returns:
            Dictionary with optimization results
        """
        try:
            await self.initialize_optimization_algorithms()
            
            # Prepare optimization problem
            # Simple example: maximize ROI subject to budget constraint
            num_services = len(service_costs)
            
            # Objective coefficients (ROI for each service)
            objective_coeffs = []
            for _, service in service_costs.iterrows():
                # Simplified ROI calculation
                roi = (service['market_rate'] - service['unit_cost']) / service['unit_cost']
                objective_coeffs.append(roi)
            
            # Constraint matrix (budget constraint)
            constraint_matrix = [service_costs['unit_cost'].tolist()]
            constraint_bounds = [(0.0, float(total_budget))]  # Total budget constraint
            
            # Variable bounds (non-negative allocations)
            variable_bounds = [(0.0, float(total_budget))] * num_services
            
            # Solve using Linear Programming
            if self.lp_optimizer is not None:
                lp_results = self.lp_optimizer.solve_budget_allocation(
                    objective_coeffs, constraint_matrix, constraint_bounds, variable_bounds
                )
            else:
                lp_results = {
                    'success': False,
                    'message': 'LP optimizer not available',
                    'optimal_allocation': [0.0] * num_services,
                    'optimal_value': 0.0
                }
            
            logger.info("Linear Programming optimization completed")
            return lp_results
            
        except Exception as e:
            logger.error(f"Error in Linear Programming optimization: {e}")
            return {
                'success': False,
                'message': str(e),
                'optimal_allocation': [],
                'optimal_value': 0.0
            }
    
    async def optimize_budget_genetic_algorithm(self, budget_data: pd.DataFrame,
                                             service_costs: pd.DataFrame,
                                             client_priorities: pd.DataFrame,
                                             total_budget: float) -> Dict[str, Any]:
        """
        Optimize budget using Genetic Algorithm
        
        Args:
            budget_data: Budget constraints data
            service_costs: Service cost data
            client_priorities: Client priority data
            total_budget: Total available budget
            
        Returns:
            Dictionary with optimization results
        """
        try:
            await self.initialize_optimization_algorithms()
            
            # Define objective function (maximize weighted ROI)
            def objective_function(allocation):
                total_value = 0
                for i, alloc in enumerate(allocation):
                    if i < len(service_costs):
                        service = service_costs.iloc[i]
                        # ROI calculation
                        roi = (service['market_rate'] - service['unit_cost']) / service['unit_cost']
                        # Weight by allocation
                        total_value += roi * alloc
                return total_value
            
            # Define constraint function (budget constraint)
            def constraint_function(allocation):
                total_spent = sum(allocation)
                return total_spent <= total_budget
            
            # Variable bounds
            variable_bounds = [(0.0, float(total_budget))] * len(service_costs)
            
            # Optimize using Genetic Algorithm
            if self.ga_optimizer is not None:
                ga_results = self.ga_optimizer.optimize_budget_allocation(
                    objective_function, variable_bounds, constraint_function
                )
            else:
                ga_results = {
                    'success': False,
                    'message': 'GA optimizer not available',
                    'optimal_allocation': [0.0] * len(service_costs),
                    'optimal_value': 0.0
                }
            
            logger.info("Genetic Algorithm optimization completed")
            return ga_results
            
        except Exception as e:
            logger.error(f"Error in Genetic Algorithm optimization: {e}")
            return {
                'success': False,
                'message': str(e),
                'optimal_allocation': [],
                'optimal_value': 0.0
            }
    
    async def calculate_budget_allocation(self, budget_data: pd.DataFrame,
                                       service_costs: pd.DataFrame,
                                       client_priorities: pd.DataFrame,
                                       roi_data: pd.DataFrame,
                                       resource_data: pd.DataFrame,
                                       total_budget: float) -> Dict[str, Any]:
        """
        Calculate optimal budget allocation
        
        Args:
            budget_data: Budget constraints data
            service_costs: Service cost data
            client_priorities: Client priority data
            roi_data: ROI data
            resource_data: Resource data
            total_budget: Total available budget
            
        Returns:
            Dictionary with allocation results
        """
        try:
            await self.initialize_budget_allocation_engines()
            
            # Calculate allocation using budget allocator
            if self.budget_allocator is not None:
                allocation_results = self.budget_allocator.calculate_optimal_distribution(
                    budget_data, service_costs, client_priorities, roi_data, resource_data, total_budget
                )
            else:
                allocation_results = {
                    'total_budget': total_budget,
                    'allocations': {},
                    'error': 'Budget allocator not available'
                }
            
            logger.info("Budget allocation calculation completed")
            return allocation_results
            
        except Exception as e:
            logger.error(f"Error calculating budget allocation: {e}")
            return {
                'total_budget': total_budget,
                'allocations': {},
                'error': str(e)
            }
    
    async def generate_reallocation_recommendations(self, current_allocations: Dict[str, Any],
                                                 performance_data: pd.DataFrame,
                                                 budget_constraints: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Generate resource reallocation recommendations
        
        Args:
            current_allocations: Current budget allocations
            performance_data: Performance metrics data
            budget_constraints: Budget constraints data
            
        Returns:
            List of reallocation recommendations
        """
        try:
            await self.initialize_budget_allocation_engines()
            
            # Generate recommendations using resource reallocator
            if self.resource_reallocator is not None:
                recommendations = self.resource_reallocator.generate_reallocation_recommendations(
                    current_allocations.get('allocations', {}), performance_data, budget_constraints
                )
            else:
                recommendations = []
            
            logger.info(f"Generated {len(recommendations)} reallocation recommendations")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating reallocation recommendations: {e}")
            return []
    
    async def estimate_efficiency_gains(self, budget_proposal: Dict[str, Any],
                                     historical_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Estimate efficiency gains from budget proposal
        
        Args:
            budget_proposal: Proposed budget allocation
            historical_data: Historical performance data
            
        Returns:
            Dictionary with estimated gains
        """
        try:
            await self.initialize_budget_allocation_engines()
            
            # Estimate gains using efficiency gain estimator
            if self.efficiency_estimator is not None:
                gain_estimates = self.efficiency_estimator.estimate_gains(
                    budget_proposal, historical_data
                )
            else:
                gain_estimates = {
                    'service_gains': {},
                    'total_estimated_gain': 0,
                    'error': 'Efficiency estimator not available'
                }
            
            logger.info("Efficiency gain estimation completed")
            return gain_estimates
            
        except Exception as e:
            logger.error(f"Error estimating efficiency gains: {e}")
            return {
                'service_gains': {},
                'total_estimated_gain': 0,
                'error': str(e)
            }
    
    async def track_performance(self, budget_allocations: Dict[str, Any],
                             actual_outcomes: pd.DataFrame,
                             time_period: str = 'monthly') -> Dict[str, Any]:
        """
        Track budget performance
        
        Args:
            budget_allocations: Budget allocation results
            actual_outcomes: Actual outcome data
            time_period: Time period for tracking
            
        Returns:
            Dictionary with performance tracking results
        """
        try:
            await self.initialize_performance_tracking_engines()
            
            # Track performance using performance tracker
            if self.performance_tracker is not None:
                performance_results = self.performance_tracker.track_budget_performance(
                    budget_allocations, actual_outcomes, time_period
                )
            else:
                performance_results = {
                    'error': 'Performance tracker not available',
                    'timestamp': datetime.now().isoformat()
                }
            
            logger.info("Budget performance tracking completed")
            return performance_results
            
        except Exception as e:
            logger.error(f"Error tracking budget performance: {e}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def generate_roi_strategies(self, performance_data: Dict[str, Any],
                                   market_conditions: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate ROI maximization strategies
        
        Args:
            performance_data: Current performance data
            market_conditions: Current market conditions
            
        Returns:
            List of ROI maximization strategies
        """
        try:
            await self.initialize_performance_tracking_engines()
            
            # Generate strategies using ROI strategy generator
            if self.roi_strategy is not None:
                strategies = self.roi_strategy.generate_maximization_strategies(
                    performance_data, market_conditions
                )
            else:
                strategies = []
            
            logger.info(f"Generated {len(strategies)} ROI maximization strategies")
            return strategies
            
        except Exception as e:
            logger.error(f"Error generating ROI strategies: {e}")
            return []
    
    async def run_complete_budget_analysis(self, total_budget: float,
                                        start_date: Optional[datetime] = None,
                                        end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Run complete budget analysis pipeline
        
        Args:
            total_budget: Total available budget
            start_date: Start date for data collection
            end_date: End date for data collection
            
        Returns:
            Dictionary with complete analysis results
        """
        try:
            logger.info("Starting complete budget analysis pipeline")
            
            # 1. Prepare data
            logger.info("Step 1: Preparing data")
            data = await self.prepare_data(start_date, end_date)
            
            if not data:
                logger.error("Failed to prepare data")
                return {'status': 'error', 'message': 'Failed to prepare data'}
            
            # 2. Optimize using Linear Programming
            logger.info("Step 2: Optimizing with Linear Programming")
            lp_results = await self.optimize_budget_linear_programming(
                data['budget_data'], data['service_costs'], total_budget
            )
            
            # 3. Optimize using Genetic Algorithm
            logger.info("Step 3: Optimizing with Genetic Algorithm")
            ga_results = await self.optimize_budget_genetic_algorithm(
                data['budget_data'], data['service_costs'], data['client_priorities'], total_budget
            )
            
            # 4. Calculate budget allocation
            logger.info("Step 4: Calculating budget allocation")
            allocation_results = await self.calculate_budget_allocation(
                data['budget_data'], data['service_costs'], data['client_priorities'],
                data['roi_data'], data['resource_data'], total_budget
            )
            
            # 5. Estimate efficiency gains
            logger.info("Step 5: Estimating efficiency gains")
            gain_estimates = await self.estimate_efficiency_gains(
                allocation_results, data['roi_data']
            )
            
            # 6. Generate reallocation recommendations
            logger.info("Step 6: Generating reallocation recommendations")
            recommendations = await self.generate_reallocation_recommendations(
                allocation_results, data['roi_data'], data['budget_data']
            )
            
            # 7. Track performance (simulated)
            logger.info("Step 7: Tracking performance")
            # Create simulated actual outcomes for performance tracking
            simulated_outcomes = self._simulate_actual_outcomes(allocation_results, data['service_costs'])
            performance_results = await self.track_performance(allocation_results, simulated_outcomes)
            
            # 8. Generate ROI strategies
            logger.info("Step 8: Generating ROI strategies")
            market_conditions = {'market_growth': 0.05, 'competition_level': 'medium'}  # Simulated
            roi_strategies = await self.generate_roi_strategies(performance_results, market_conditions)
            
            # Compile complete results
            complete_analysis = {
                'status': 'success',
                'timestamp': datetime.now().isoformat(),
                'total_budget': total_budget,
                'data_prepared': True,
                'linear_programming_results': lp_results,
                'genetic_algorithm_results': ga_results,
                'allocation_results': allocation_results,
                'efficiency_gains': gain_estimates,
                'reallocation_recommendations': recommendations,
                'performance_tracking': performance_results,
                'roi_strategies': roi_strategies,
                'summary': self._generate_analysis_summary(
                    lp_results, ga_results, allocation_results, gain_estimates
                )
            }
            
            logger.info("Complete budget analysis pipeline finished successfully")
            return complete_analysis
            
        except Exception as e:
            logger.error(f"Error in complete budget analysis pipeline: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _simulate_actual_outcomes(self, allocation_results: Dict[str, Any],
                                service_costs: pd.DataFrame) -> pd.DataFrame:
        """Simulate actual outcomes for performance tracking"""
        # Create simulated outcomes based on allocations
        outcomes_data = []
        allocations = allocation_results.get('allocations', {})
        
        for service_id, allocation in allocations.items():
            # Find corresponding service
            service_row = service_costs[service_costs['service_id'] == service_id]
            if not service_row.empty:
                service = service_row.iloc[0]
                # Simulate outcomes
                actual_spent = allocation * np.random.uniform(0.9, 1.1)  # ±10% variance
                revenue_generated = actual_spent * (1 + service['profit_margin']) * np.random.uniform(0.95, 1.05)
                
                outcomes_data.append({
                    'service_id': service_id,
                    'actual_spent': actual_spent,
                    'revenue_generated': revenue_generated,
                    'period': '2025-01'
                })
        
        return pd.DataFrame(outcomes_data)
    
    def _generate_analysis_summary(self, lp_results: Dict[str, Any],
                                 ga_results: Dict[str, Any],
                                 allocation_results: Dict[str, Any],
                                 gain_estimates: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary of analysis results"""
        try:
            # Extract key metrics
            lp_value = lp_results.get('optimal_value', 0)
            ga_value = ga_results.get('optimal_value', 0)
            total_allocation = sum(allocation_results.get('allocations', {}).values())
            total_gain = gain_estimates.get('total_estimated_gain', 0)
            
            summary = {
                'total_budget': allocation_results.get('total_budget', 0),
                'total_allocated': total_allocation,
                'lp_optimal_value': lp_value,
                'ga_optimal_value': ga_value,
                'total_estimated_gain': total_gain,
                'roi_improvement': total_gain / total_allocation if total_allocation > 0 else 0,
                'recommendation': self._generate_overall_recommendation(lp_value, ga_value, total_gain)
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating analysis summary: {e}")
            return {'summary_status': 'error'}
    
    def _generate_overall_recommendation(self, lp_value: float, ga_value: float,
                                       total_gain: float) -> str:
        """Generate overall recommendation based on analysis results"""
        if lp_value > 0 and ga_value > 0:
            if total_gain > 0:
                return "Positive optimization results - implementation recommended with monitoring"
            else:
                return "Optimization completed but limited gains - consider alternative approaches"
        else:
            return "Optimization challenges encountered - review constraints and data quality"


# Global instance for easy access
budget_optimizer_instance = None


async def get_budget_optimizer() -> BudgetOptimizer:
    """Get singleton budget optimizer instance"""
    global budget_optimizer_instance
    if budget_optimizer_instance is None:
        budget_optimizer_instance = BudgetOptimizer()
    return budget_optimizer_instance


# Example usage function
async def run_budget_optimization_analysis(total_budget: float = 1000000):
    """Example function to run complete budget optimization analysis"""
    try:
        engine = await get_budget_optimizer()
        results = await engine.run_complete_budget_analysis(total_budget)
        return results
    except Exception as e:
        logger.error(f"Error running budget optimization analysis: {e}")
        return {'status': 'error', 'message': str(e)}