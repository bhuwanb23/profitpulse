"""
Tests for Budget Allocator Module
"""

import sys
import os
import unittest
import pandas as pd
import numpy as np

# Add the src directory to the path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
sys.path.insert(0, src_path)

from src.models.budget_optimizer.budget_allocator import (
    BudgetAllocator,
    ResourceReallocator,
    EfficiencyGainEstimator
)


class TestBudgetAllocator(unittest.TestCase):
    """Tests for budget allocator components"""
    
    def test_budget_allocator_initialization(self):
        """Test BudgetAllocator initialization"""
        allocator = BudgetAllocator()
        self.assertIsNotNone(allocator)
    
    def test_resource_reallocator_initialization(self):
        """Test ResourceReallocator initialization"""
        reallocator = ResourceReallocator()
        self.assertIsNotNone(reallocator)
    
    def test_efficiency_gain_estimator_initialization(self):
        """Test EfficiencyGainEstimator initialization"""
        estimator = EfficiencyGainEstimator()
        self.assertIsNotNone(estimator)
    
    def test_simple_allocation_calculation(self):
        """Test simple allocation calculation"""
        allocator = BudgetAllocator()
        
        # Create mock data
        budget_data = pd.DataFrame({
            'budget_id': ['BUDGET-001'],
            'total_budget': [100000],
            'allocated_amount': [50000],
            'remaining_budget': [50000]
        })
        
        service_costs = pd.DataFrame({
            'service_id': ['SERVICE-001', 'SERVICE-002'],
            'service_name': ['Service A', 'Service B'],
            'unit_cost': [1000, 2000],
            'profit_margin': [0.2, 0.3]
        })
        
        client_priorities = pd.DataFrame({
            'client_id': ['CLIENT-001', 'CLIENT-002'],
            'client_name': ['Client A', 'Client B'],
            'revenue_contribution': [50000, 30000],
            'priority_score': [80, 60]
        })
        
        roi_data = pd.DataFrame({
            'item_id': ['ITEM-001', 'ITEM-002'],
            'investment_type': ['Software', 'Equipment'],
            'roi_percentage': [0.25, 0.15]
        })
        
        resource_data = pd.DataFrame({
            'resource_id': ['RESOURCE-001', 'RESOURCE-002'],
            'resource_name': ['Resource A', 'Resource B'],
            'hourly_rate': [50, 75]
        })
        
        # Test allocation calculation
        result = allocator.calculate_optimal_distribution(
            budget_data, service_costs, client_priorities, roi_data, resource_data, 100000
        )
        
        self.assertTrue(isinstance(result, dict))
        self.assertIn('allocations', result)
        self.assertIn('total_budget', result)
    
    def test_resource_reallocation_recommendations(self):
        """Test resource reallocation recommendations"""
        reallocator = ResourceReallocator()
        
        # Create mock data
        current_allocations = {
            'SERVICE-001': 50000.0,
            'SERVICE-002': 30000.0
        }
        
        performance_data = pd.DataFrame({
            'service_id': ['SERVICE-001', 'SERVICE-002'],
            'revenue_generated': [60000, 35000],
            'cost_incurred': [50000, 30000]
        })
        
        budget_constraints = pd.DataFrame({
            'budget_id': ['BUDGET-001'],
            'total_budget': [100000]
        })
        
        # Test recommendation generation
        recommendations = reallocator.generate_reallocation_recommendations(
            current_allocations, performance_data, budget_constraints
        )
        
        self.assertTrue(isinstance(recommendations, list))
    
    def test_efficiency_gain_estimation(self):
        """Test efficiency gain estimation"""
        estimator = EfficiencyGainEstimator()
        
        # Create mock data
        budget_proposal = {
            'allocations': {
                'SERVICE-001': 50000,
                'SERVICE-002': 30000
            },
            'total_budget': 80000
        }
        
        historical_data = pd.DataFrame({
            'service_id': ['SERVICE-001', 'SERVICE-002'],
            'revenue_generated': [60000, 35000],
            'cost_incurred': [50000, 30000]
        })
        
        # Test gain estimation
        estimates = estimator.estimate_gains(budget_proposal, historical_data)
        
        self.assertTrue(isinstance(estimates, dict))
        self.assertIn('service_gains', estimates)
        self.assertIn('total_estimated_gain', estimates)


if __name__ == '__main__':
    unittest.main()