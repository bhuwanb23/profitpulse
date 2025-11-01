"""
Tests for Main Budget Optimizer Module
"""

import sys
import os
import unittest
import pandas as pd
import numpy as np
import asyncio

# Add the src directory to the path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
sys.path.insert(0, src_path)

from src.models.budget_optimizer.budget_optimizer import BudgetOptimizer


class TestBudgetOptimizer(unittest.TestCase):
    """Tests for BudgetOptimizer class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.optimizer = BudgetOptimizer()
    
    def test_engine_initialization(self):
        """Test budget optimizer engine initialization"""
        self.assertIsNotNone(self.optimizer)
        # Check that components are initialized
        self.assertTrue(hasattr(self.optimizer, 'data_preparator'))
        self.assertTrue(hasattr(self.optimizer, 'lp_optimizer'))
        self.assertTrue(hasattr(self.optimizer, 'ga_optimizer'))
    
    def test_component_initialization_methods(self):
        """Test component initialization methods"""
        # Test that initialization methods exist
        self.assertTrue(hasattr(self.optimizer, '_initialize_components'))
        self.assertTrue(hasattr(self.optimizer, 'initialize_data_preparator'))
        self.assertTrue(hasattr(self.optimizer, 'initialize_optimization_algorithms'))
        self.assertTrue(hasattr(self.optimizer, 'initialize_budget_allocation_engines'))
        self.assertTrue(hasattr(self.optimizer, 'initialize_performance_tracking_engines'))
    
    def test_data_preparation_initialization(self):
        """Test data preparator initialization"""
        # This is an async method, so we need to run it in an event loop
        async def test_async():
            await self.optimizer.initialize_data_preparator()
            self.assertIsNotNone(self.optimizer.data_preparator)
        
        # Run the async test
        asyncio.run(test_async())
    
    def test_optimization_algorithms_initialization(self):
        """Test optimization algorithms initialization"""
        # This is an async method, so we need to run it in an event loop
        async def test_async():
            await self.optimizer.initialize_optimization_algorithms()
            self.assertIsNotNone(self.optimizer.lp_optimizer)
            self.assertIsNotNone(self.optimizer.ga_optimizer)
            self.assertIsNotNone(self.optimizer.sa_optimizer)
            self.assertIsNotNone(self.optimizer.pso_optimizer)
            self.assertIsNotNone(self.optimizer.mo_optimizer)
        
        # Run the async test
        asyncio.run(test_async())
    
    def test_budget_allocation_engines_initialization(self):
        """Test budget allocation engines initialization"""
        # This is an async method, so we need to run it in an event loop
        async def test_async():
            await self.optimizer.initialize_budget_allocation_engines()
            self.assertIsNotNone(self.optimizer.budget_allocator)
            self.assertIsNotNone(self.optimizer.resource_reallocator)
            self.assertIsNotNone(self.optimizer.efficiency_estimator)
        
        # Run the async test
        asyncio.run(test_async())
    
    def test_performance_tracking_engines_initialization(self):
        """Test performance tracking engines initialization"""
        # This is an async method, so we need to run it in an event loop
        async def test_async():
            await self.optimizer.initialize_performance_tracking_engines()
            self.assertIsNotNone(self.optimizer.performance_tracker)
            self.assertIsNotNone(self.optimizer.roi_strategy)
            self.assertIsNotNone(self.optimizer.benchmarking)
        
        # Run the async test
        asyncio.run(test_async())


if __name__ == '__main__':
    unittest.main()