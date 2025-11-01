"""
Tests for Performance Tracker Module
"""

import sys
import os
import unittest
import pandas as pd
import numpy as np
from datetime import datetime

# Add the src directory to the path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
sys.path.insert(0, src_path)

from src.models.budget_optimizer.performance_tracker import (
    BudgetPerformanceTracker,
    ROIMaximizationStrategy,
    BudgetBenchmarking
)


class TestPerformanceTracker(unittest.TestCase):
    """Tests for performance tracker components"""
    
    def test_budget_performance_tracker_initialization(self):
        """Test BudgetPerformanceTracker initialization"""
        tracker = BudgetPerformanceTracker()
        self.assertIsNotNone(tracker)
    
    def test_roi_maximization_strategy_initialization(self):
        """Test ROIMaximizationStrategy initialization"""
        strategy = ROIMaximizationStrategy()
        self.assertIsNotNone(strategy)
    
    def test_budget_benchmarking_initialization(self):
        """Test BudgetBenchmarking initialization"""
        benchmarking = BudgetBenchmarking()
        self.assertIsNotNone(benchmarking)
    
    def test_budget_performance_tracking(self):
        """Test budget performance tracking"""
        tracker = BudgetPerformanceTracker()
        
        # Create mock data
        budget_allocations = {
            'allocations': {
                'SERVICE-001': 50000.0,
                'SERVICE-002': 30000.0
            },
            'total_budget': 80000.0
        }
        
        actual_outcomes = pd.DataFrame({
            'service_id': ['SERVICE-001', 'SERVICE-002'],
            'actual_spent': [48000, 32000],
            'revenue_generated': [60000, 35000]
        })
        
        # Test performance tracking
        results = tracker.track_budget_performance(budget_allocations, actual_outcomes)
        
        self.assertTrue(isinstance(results, dict))
        self.assertIn('performance_metrics', results)
        self.assertIn('roi_metrics', results)
    
    def test_roi_strategies_generation(self):
        """Test ROI strategies generation"""
        strategy = ROIMaximizationStrategy()
        
        # Create mock data
        performance_data = {
            'performance_metrics': {
                'total_budget': 100000,
                'total_spent': 95000,
                'budget_utilization_rate': 0.95,
                'total_revenue_generated': 120000,
                'cost_efficiency_ratio': 1.26
            },
            'roi_metrics': {
                'overall_roi': 0.26,
                'annualized_roi': 0.35
            }
        }
        
        market_conditions = {
            'market_growth': 0.05,
            'competition_level': 'medium'
        }
        
        # Test strategy generation
        strategies = strategy.generate_maximization_strategies(performance_data, market_conditions)
        
        self.assertTrue(isinstance(strategies, list))
    
    def test_benchmarking_analysis(self):
        """Test benchmarking analysis"""
        benchmarking = BudgetBenchmarking()
        
        # Create mock data
        performance_data = {
            'performance_metrics': {
                'total_budget': 100000,
                'total_spent': 95000,
                'budget_utilization_rate': 0.95,
                'total_revenue_generated': 120000,
                'cost_efficiency_ratio': 1.26
            },
            'roi_metrics': {
                'overall_roi': 0.26,
                'annualized_roi': 0.35
            }
        }
        
        industry_benchmarks = {
            'roi': 0.15,
            'cost_efficiency': 2.0,
            'budget_utilization': 0.85
        }
        
        historical_performance = pd.DataFrame({
            'period': ['2024-01', '2024-02', '2024-03'],
            'roi': [0.20, 0.23, 0.26],
            'revenue': [100000, 110000, 120000]
        })
        
        # Test benchmarking
        results = benchmarking.benchmark_performance(
            performance_data, industry_benchmarks, historical_performance
        )
        
        self.assertTrue(isinstance(results, dict))
        self.assertIn('benchmark_comparisons', results)


if __name__ == '__main__':
    unittest.main()