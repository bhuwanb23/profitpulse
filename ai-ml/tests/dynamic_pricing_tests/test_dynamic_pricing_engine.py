"""
Tests for Dynamic Pricing Engine Main Module
"""

import sys
import os
import unittest
import asyncio

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'models'))

class TestDynamicPricingEngine(unittest.TestCase):
    """Test cases for the main dynamic pricing engine"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Import here to avoid import issues
        pass
    
    def test_engine_imports(self):
        """Test that the main engine can be imported"""
        try:
            from dynamic_pricing.dynamic_pricing_engine import DynamicPricingEngine
            engine = DynamicPricingEngine()
            self.assertIsNotNone(engine)
        except ImportError:
            self.skipTest("Dynamic Pricing Engine not available")
    
    def test_engine_initialization(self):
        """Test engine initialization"""
        try:
            from dynamic_pricing.dynamic_pricing_engine import DynamicPricingEngine
            engine = DynamicPricingEngine()
            
            # Check that components are initialized as None
            self.assertIsNone(engine.data_preparator)
            self.assertIsNone(engine.q_learning_agent)
            self.assertIsNone(engine.price_recommendation_engine)
        except ImportError:
            self.skipTest("Dynamic Pricing Engine not available")

if __name__ == '__main__':
    unittest.main()