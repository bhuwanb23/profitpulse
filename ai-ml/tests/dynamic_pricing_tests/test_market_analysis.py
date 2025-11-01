"""
Tests for Dynamic Pricing Market Analysis Module
"""

import sys
import os
import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'models'))

class TestMarketAnalysis(unittest.TestCase):
    """Test cases for market analysis components"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        from dynamic_pricing.market_analysis import MarketTrendAnalyzer, CompetitiveIntelligenceAnalyzer
        self.trend_analyzer = MarketTrendAnalyzer()
        self.competitive_analyzer = CompetitiveIntelligenceAnalyzer()
    
    def test_market_trend_analyzer_initialization(self):
        """Test market trend analyzer initialization"""
        self.assertIsNotNone(self.trend_analyzer)
    
    def test_competitive_intelligence_analyzer_initialization(self):
        """Test competitive intelligence analyzer initialization"""
        self.assertIsNotNone(self.competitive_analyzer)
    
    def test_trend_calculation(self):
        """Test trend calculation functionality"""
        # Create mock market data
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), periods=30, freq='D')
        market_data = pd.DataFrame({
            'date': dates,
            'market_rate': np.linspace(100, 120, 30) + np.random.normal(0, 5, 30)
        })
        
        # Test trend calculation
        trend_result = self.trend_analyzer._calculate_trend(market_data, 'market_rate')
        self.assertIsInstance(trend_result, dict)
        self.assertIn('slope', trend_result)
        self.assertIn('r_squared', trend_result)

if __name__ == '__main__':
    unittest.main()