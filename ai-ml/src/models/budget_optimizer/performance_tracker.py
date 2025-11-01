"""
Performance Tracking for Budget Optimization Model
Handles budget performance tracking and ROI maximization strategies
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


class BudgetPerformanceTracker:
    """Tracks budget performance and measures ROI"""
    
    def __init__(self):
        """Initialize performance tracker"""
        logger.info("Budget Performance Tracker initialized")
    
    def track_budget_performance(self, budget_allocations: Dict[str, Any],
                               actual_outcomes: pd.DataFrame,
                               time_period: str = 'monthly') -> Dict[str, Any]:
        """
        Track actual budget performance against allocations
        
        Args:
            budget_allocations: Budget allocation results
            actual_outcomes: DataFrame with actual outcomes
            time_period: Time period for tracking ('daily', 'weekly', 'monthly', 'quarterly', 'yearly')
            
        Returns:
            Dictionary with performance metrics
        """
        try:
            # Extract allocations
            allocations = budget_allocations.get('allocations', {})
            total_budget = budget_allocations.get('total_budget', 0)
            
            # Calculate performance metrics
            performance_metrics = self._calculate_performance_metrics(
                allocations, actual_outcomes, total_budget
            )
            
            # Calculate ROI metrics
            roi_metrics = self._calculate_roi_metrics(allocations, actual_outcomes)
            
            # Calculate variance analysis
            variance_analysis = self._calculate_variance_analysis(allocations, actual_outcomes)
            
            performance_tracking = {
                'timestamp': datetime.now().isoformat(),
                'time_period': time_period,
                'total_budget': total_budget,
                'actual_spent': actual_outcomes['actual_spent'].sum() if 'actual_spent' in actual_outcomes.columns else 0,
                'performance_metrics': performance_metrics,
                'roi_metrics': roi_metrics,
                'variance_analysis': variance_analysis,
                'efficiency_score': self._calculate_efficiency_score(performance_metrics, roi_metrics)
            }
            
            logger.info("Budget performance tracking completed")
            return performance_tracking
            
        except Exception as e:
            logger.error(f"Error tracking budget performance: {e}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _calculate_performance_metrics(self, allocations: Dict[str, float],
                                    actual_outcomes: pd.DataFrame,
                                    total_budget: float) -> Dict[str, float]:
        """Calculate key performance metrics"""
        # Total spent
        total_spent = actual_outcomes['actual_spent'].sum() if 'actual_spent' in actual_outcomes.columns else 0
        
        # Budget utilization
        budget_utilization = total_spent / total_budget if total_budget > 0 else 0
        
        # Revenue generated
        total_revenue = actual_outcomes['revenue_generated'].sum() if 'revenue_generated' in actual_outcomes.columns else 0
        
        # Cost efficiency
        cost_efficiency = total_revenue / total_spent if total_spent > 0 else 0
        
        # Service-level metrics
        service_metrics = {}
        for service_id, allocation in allocations.items():
            service_data = actual_outcomes[actual_outcomes['service_id'] == service_id] if 'service_id' in actual_outcomes.columns else pd.DataFrame()
            
            if not service_data.empty:
                actual_spent = service_data['actual_spent'].sum() if 'actual_spent' in service_data.columns else allocation
                revenue = service_data['revenue_generated'].sum() if 'revenue_generated' in service_data.columns else actual_spent * 1.2
                
                service_metrics[service_id] = {
                    'allocation': allocation,
                    'actual_spent': actual_spent,
                    'revenue_generated': revenue,
                    'utilization_rate': actual_spent / allocation if allocation > 0 else 0,
                    'roi': (revenue - actual_spent) / actual_spent if actual_spent > 0 else 0
                }
        
        return {
            'total_budget': total_budget,
            'total_spent': total_spent,
            'budget_utilization_rate': budget_utilization,
            'total_revenue_generated': total_revenue,
            'cost_efficiency_ratio': cost_efficiency,
            'service_level_metrics': service_metrics
        }
    
    def _calculate_roi_metrics(self, allocations: Dict[str, float],
                             actual_outcomes: pd.DataFrame) -> Dict[str, float]:
        """Calculate ROI-related metrics"""
        total_allocation = sum(allocations.values())
        total_spent = actual_outcomes['actual_spent'].sum() if 'actual_spent' in actual_outcomes.columns else 0
        total_revenue = actual_outcomes['revenue_generated'].sum() if 'revenue_generated' in actual_outcomes.columns else 0
        
        # Overall ROI
        overall_roi = (total_revenue - total_spent) / total_spent if total_spent > 0 else 0
        
        # ROI by service
        service_roi = {}
        for service_id, allocation in allocations.items():
            service_data = actual_outcomes[actual_outcomes['service_id'] == service_id] if 'service_id' in actual_outcomes.columns else pd.DataFrame()
            
            if not service_data.empty:
                actual_spent = service_data['actual_spent'].sum() if 'actual_spent' in service_data.columns else allocation
                revenue = service_data['revenue_generated'].sum() if 'revenue_generated' in service_data.columns else actual_spent * 1.2
                
                roi = (revenue - actual_spent) / actual_spent if actual_spent > 0 else 0
                service_roi[service_id] = roi
        
        # Annualized ROI (assuming monthly data)
        annualized_roi = ((1 + overall_roi) ** 12) - 1
        
        return {
            'overall_roi': overall_roi,
            'annualized_roi': annualized_roi,
            'service_level_roi': service_roi,
            'roi_improvement': 0,  # To be calculated against baseline
            'benchmark_roi': 0.15  # Industry benchmark (15%)
        }
    
    def _calculate_variance_analysis(self, allocations: Dict[str, float],
                                   actual_outcomes: pd.DataFrame) -> Dict[str, float]:
        """Calculate budget variance analysis"""
        total_allocation = sum(allocations.values())
        total_spent = actual_outcomes['actual_spent'].sum() if 'actual_spent' in actual_outcomes.columns else 0
        
        # Overall variance
        overall_variance = total_spent - total_allocation
        variance_percentage = (overall_variance / total_allocation * 100) if total_allocation > 0 else 0
        
        # Service-level variance
        service_variance = {}
        for service_id, allocation in allocations.items():
            service_data = actual_outcomes[actual_outcomes['service_id'] == service_id] if 'service_id' in actual_outcomes.columns else pd.DataFrame()
            
            if not service_data.empty:
                actual_spent = service_data['actual_spent'].sum() if 'actual_spent' in service_data.columns else allocation
                variance = actual_spent - allocation
                variance_pct = (variance / allocation * 100) if allocation > 0 else 0
                
                service_variance[service_id] = {
                    'allocation': allocation,
                    'actual_spent': actual_spent,
                    'variance': variance,
                    'variance_percentage': variance_pct
                }
        
        return {
            'total_allocation': total_allocation,
            'total_actual_spent': total_spent,
            'overall_variance': overall_variance,
            'variance_percentage': variance_percentage,
            'service_level_variance': service_variance,
            'favorable_variances': len([v for v in service_variance.values() if v['variance'] < 0]),
            'unfavorable_variances': len([v for v in service_variance.values() if v['variance'] > 0])
        }
    
    def _calculate_efficiency_score(self, performance_metrics: Dict[str, Any],
                                  roi_metrics: Dict[str, Any]) -> float:
        """Calculate overall efficiency score (0-100)"""
        try:
            # Weighted score based on key metrics
            budget_utilization = performance_metrics.get('budget_utilization_rate', 0)
            cost_efficiency = performance_metrics.get('cost_efficiency_ratio', 0)
            overall_roi = roi_metrics.get('overall_roi', 0)
            
            # Normalize metrics to 0-100 scale
            utilization_score = min(budget_utilization * 100, 100)  # Cap at 100
            efficiency_score = min(cost_efficiency * 20, 100)  # Scale factor
            roi_score = min((overall_roi + 1) * 50, 100)  # Adjust for negative ROI
            
            # Weighted average (40% utilization, 30% efficiency, 30% ROI)
            efficiency_score = (
                utilization_score * 0.4 +
                efficiency_score * 0.3 +
                roi_score * 0.3
            )
            
            return efficiency_score
        except Exception:
            return 50.0  # Default score


class ROIMaximizationStrategy:
    """ROI maximization strategies and recommendations"""
    
    def __init__(self):
        """Initialize ROI maximization strategy"""
        logger.info("ROI Maximization Strategy initialized")
    
    def generate_maximization_strategies(self, performance_data: Dict[str, Any],
                                       market_conditions: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate ROI maximization strategies based on performance and market data
        
        Args:
            performance_data: Current performance tracking data
            market_conditions: Current market conditions
            
        Returns:
            List of ROI maximization strategies
        """
        try:
            strategies = []
            
            # Extract key metrics
            performance_metrics = performance_data.get('performance_metrics', {})
            roi_metrics = performance_data.get('roi_metrics', {})
            variance_analysis = performance_data.get('variance_analysis', {})
            
            # Generate strategies based on performance gaps
            strategies.extend(self._generate_allocation_strategies(performance_metrics))
            strategies.extend(self._generate_cost_optimization_strategies(performance_metrics))
            strategies.extend(self._generate_revenue_enhancement_strategies(roi_metrics, market_conditions))
            strategies.extend(self._generate_variance_correction_strategies(variance_analysis))
            
            # Sort strategies by impact score
            strategies.sort(key=lambda x: x.get('impact_score', 0), reverse=True)
            
            logger.info(f"Generated {len(strategies)} ROI maximization strategies")
            return strategies
            
        except Exception as e:
            logger.error(f"Error generating ROI maximization strategies: {e}")
            return []
    
    def _generate_allocation_strategies(self, performance_metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate strategies for better budget allocation"""
        strategies = []
        service_metrics = performance_metrics.get('service_level_metrics', {})
        
        # Identify high-performing services
        high_performers = [
            service_id for service_id, metrics in service_metrics.items()
            if metrics.get('roi', 0) > 0.25  # 25% ROI threshold
        ]
        
        # Identify low-performing services
        low_performers = [
            service_id for service_id, metrics in service_metrics.items()
            if metrics.get('roi', 0) < 0.1  # 10% ROI threshold
        ]
        
        if high_performers:
            strategies.append({
                'strategy_id': 'allocation_shift_to_high_performers',
                'title': 'Shift Budget to High-Performing Services',
                'description': f'Reallocate resources from lower-performing to high-performing services ({len(high_performers)} identified)',
                'action': 'Increase allocation to high-performing services by 15-25%',
                'impact_score': 85,
                'implementation_effort': 'Medium',
                'expected_roi_improvement': 0.15,
                'time_horizon': '2-3 months'
            })
        
        if low_performers:
            strategies.append({
                'strategy_id': 'allocation_reduction_for_low_performers',
                'title': 'Reduce Allocation to Low-Performing Services',
                'description': f'Reduce budget allocation to underperforming services ({len(low_performers)} identified)',
                'action': 'Decrease allocation to low-performing services by 20-40%',
                'impact_score': 75,
                'implementation_effort': 'Low',
                'expected_roi_improvement': 0.10,
                'time_horizon': '1-2 months'
            })
        
        return strategies
    
    def _generate_cost_optimization_strategies(self, performance_metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate cost optimization strategies"""
        strategies = []
        cost_efficiency = performance_metrics.get('cost_efficiency_ratio', 0)
        
        if cost_efficiency < 1.5:  # Less than 1.5x revenue per dollar spent
            strategies.append({
                'strategy_id': 'cost_optimization_initiative',
                'title': 'Implement Cost Optimization Initiatives',
                'description': 'Initiate cost reduction programs to improve cost efficiency',
                'action': 'Identify and eliminate inefficiencies, negotiate better rates, consolidate services',
                'impact_score': 80,
                'implementation_effort': 'High',
                'expected_roi_improvement': 0.20,
                'time_horizon': '3-6 months'
            })
        
        return strategies
    
    def _generate_revenue_enhancement_strategies(self, roi_metrics: Dict[str, Any],
                                               market_conditions: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate revenue enhancement strategies"""
        strategies = []
        overall_roi = roi_metrics.get('overall_roi', 0)
        benchmark_roi = roi_metrics.get('benchmark_roi', 0.15)
        
        if overall_roi < benchmark_roi:
            strategies.append({
                'strategy_id': 'revenue_enhancement_program',
                'title': 'Launch Revenue Enhancement Program',
                'description': 'Implement strategies to increase revenue generation',
                'action': 'Expand service offerings, improve pricing strategies, enhance customer retention',
                'impact_score': 90,
                'implementation_effort': 'High',
                'expected_roi_improvement': 0.25,
                'time_horizon': '6-12 months'
            })
        
        return strategies
    
    def _generate_variance_correction_strategies(self, variance_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate strategies to correct budget variances"""
        strategies = []
        unfavorable_variances = variance_analysis.get('unfavorable_variances', 0)
        
        if unfavorable_variances > 0:
            strategies.append({
                'strategy_id': 'variance_management',
                'title': 'Implement Variance Management Controls',
                'description': 'Strengthen budget monitoring and control mechanisms',
                'action': 'Enhance forecasting accuracy, implement variance reporting, establish approval thresholds',
                'impact_score': 70,
                'implementation_effort': 'Medium',
                'expected_roi_improvement': 0.05,
                'time_horizon': '1-3 months'
            })
        
        return strategies


class BudgetBenchmarking:
    """Budget benchmarking against industry standards and historical performance"""
    
    def __init__(self):
        """Initialize budget benchmarking"""
        logger.info("Budget Benchmarking initialized")
    
    def benchmark_performance(self, performance_data: Dict[str, Any],
                            industry_benchmarks: Dict[str, float],
                            historical_performance: pd.DataFrame) -> Dict[str, Any]:
        """
        Benchmark performance against industry standards and historical data
        
        Args:
            performance_data: Current performance data
            industry_benchmarks: Industry benchmark metrics
            historical_performance: Historical performance data
            
        Returns:
            Dictionary with benchmarking results
        """
        try:
            # Extract current metrics
            performance_metrics = performance_data.get('performance_metrics', {})
            roi_metrics = performance_data.get('roi_metrics', {})
            
            # Calculate benchmark comparisons
            benchmark_comparisons = self._calculate_benchmark_comparisons(
                performance_metrics, roi_metrics, industry_benchmarks
            )
            
            # Calculate trend analysis
            trend_analysis = self._calculate_trend_analysis(historical_performance)
            
            # Calculate percentile rankings
            percentile_rankings = self._calculate_percentile_rankings(
                performance_metrics, roi_metrics, industry_benchmarks
            )
            
            benchmarking_results = {
                'timestamp': datetime.now().isoformat(),
                'benchmark_comparisons': benchmark_comparisons,
                'trend_analysis': trend_analysis,
                'percentile_rankings': percentile_rankings,
                'performance_rating': self._calculate_performance_rating(benchmark_comparisons, percentile_rankings)
            }
            
            logger.info("Budget benchmarking completed")
            return benchmarking_results
            
        except Exception as e:
            logger.error(f"Error in budget benchmarking: {e}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _calculate_benchmark_comparisons(self, performance_metrics: Dict[str, Any],
                                       roi_metrics: Dict[str, Any],
                                       industry_benchmarks: Dict[str, float]) -> Dict[str, Any]:
        """Calculate comparisons against industry benchmarks"""
        comparisons = {}
        
        # ROI comparison
        overall_roi = roi_metrics.get('overall_roi', 0)
        benchmark_roi = industry_benchmarks.get('roi', 0.15)
        roi_comparison = {
            'current': overall_roi,
            'benchmark': benchmark_roi,
            'difference': overall_roi - benchmark_roi,
            'performance_ratio': overall_roi / benchmark_roi if benchmark_roi > 0 else 0
        }
        comparisons['roi'] = roi_comparison
        
        # Cost efficiency comparison
        cost_efficiency = performance_metrics.get('cost_efficiency_ratio', 0)
        benchmark_efficiency = industry_benchmarks.get('cost_efficiency', 2.0)
        efficiency_comparison = {
            'current': cost_efficiency,
            'benchmark': benchmark_efficiency,
            'difference': cost_efficiency - benchmark_efficiency,
            'performance_ratio': cost_efficiency / benchmark_efficiency if benchmark_efficiency > 0 else 0
        }
        comparisons['cost_efficiency'] = efficiency_comparison
        
        # Budget utilization comparison
        utilization_rate = performance_metrics.get('budget_utilization_rate', 0)
        benchmark_utilization = industry_benchmarks.get('budget_utilization', 0.85)
        utilization_comparison = {
            'current': utilization_rate,
            'benchmark': benchmark_utilization,
            'difference': utilization_rate - benchmark_utilization,
            'performance_ratio': utilization_rate / benchmark_utilization if benchmark_utilization > 0 else 0
        }
        comparisons['budget_utilization'] = utilization_comparison
        
        return comparisons
    
    def _calculate_trend_analysis(self, historical_performance: pd.DataFrame) -> Dict[str, Any]:
        """Calculate performance trends over time"""
        if historical_performance.empty:
            return {'trend_available': False}
        
        # Calculate trends for key metrics
        trends = {}
        
        # Assuming historical_performance has monthly data with ROI columns
        if 'roi' in historical_performance.columns:
            rois = historical_performance['roi'].dropna().values
            if len(rois) > 1:
                # Calculate trend using linear regression
                x = np.arange(len(rois))
                slope, _ = np.polyfit(x, rois, 1)
                trends['roi_trend'] = {
                    'slope': float(slope),
                    'direction': 'improving' if slope > 0 else 'declining' if slope < 0 else 'stable',
                    'magnitude': abs(slope)
                }
        
        return {
            'trend_available': True,
            'trends': trends,
            'data_points': len(historical_performance)
        }
    
    def _calculate_percentile_rankings(self, performance_metrics: Dict[str, Any],
                                     roi_metrics: Dict[str, Any],
                                     industry_benchmarks: Dict[str, float]) -> Dict[str, float]:
        """Calculate percentile rankings against benchmarks"""
        # Simplified percentile calculation based on benchmark ratios
        percentile_rankings = {}
        
        # ROI percentile (assuming normal distribution around benchmark)
        overall_roi = roi_metrics.get('overall_roi', 0)
        benchmark_roi = industry_benchmarks.get('roi', 0.15)
        roi_percentile = min(max((overall_roi / benchmark_roi) * 50, 0), 100) if benchmark_roi > 0 else 50
        percentile_rankings['roi_percentile'] = roi_percentile
        
        # Cost efficiency percentile
        cost_efficiency = performance_metrics.get('cost_efficiency_ratio', 0)
        benchmark_efficiency = industry_benchmarks.get('cost_efficiency', 2.0)
        efficiency_percentile = min(max((cost_efficiency / benchmark_efficiency) * 50, 0), 100) if benchmark_efficiency > 0 else 50
        percentile_rankings['cost_efficiency_percentile'] = efficiency_percentile
        
        return percentile_rankings
    
    def _calculate_performance_rating(self, benchmark_comparisons: Dict[str, Any],
                                    percentile_rankings: Dict[str, float]) -> str:
        """Calculate overall performance rating"""
        try:
            # Average of key percentile rankings
            roi_percentile = percentile_rankings.get('roi_percentile', 50)
            efficiency_percentile = percentile_rankings.get('cost_efficiency_percentile', 50)
            average_percentile = (roi_percentile + efficiency_percentile) / 2
            
            if average_percentile >= 80:
                return 'Excellent'
            elif average_percentile >= 60:
                return 'Good'
            elif average_percentile >= 40:
                return 'Average'
            elif average_percentile >= 20:
                return 'Below Average'
            else:
                return 'Poor'
        except Exception:
            return 'Unknown'


# Global instances for easy access
budget_performance_tracker_instance = None
roi_maximization_strategy_instance = None
budget_benchmarking_instance = None


def get_budget_performance_tracker() -> BudgetPerformanceTracker:
    """Get singleton budget performance tracker instance"""
    global budget_performance_tracker_instance
    if budget_performance_tracker_instance is None:
        budget_performance_tracker_instance = BudgetPerformanceTracker()
    return budget_performance_tracker_instance


def get_roi_maximization_strategy() -> ROIMaximizationStrategy:
    """Get singleton ROI maximization strategy instance"""
    global roi_maximization_strategy_instance
    if roi_maximization_strategy_instance is None:
        roi_maximization_strategy_instance = ROIMaximizationStrategy()
    return roi_maximization_strategy_instance


def get_budget_benchmarking() -> BudgetBenchmarking:
    """Get singleton budget benchmarking instance"""
    global budget_benchmarking_instance
    if budget_benchmarking_instance is None:
        budget_benchmarking_instance = BudgetBenchmarking()
    return budget_benchmarking_instance