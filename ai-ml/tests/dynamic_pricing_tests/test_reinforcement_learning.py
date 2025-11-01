"""
Tests for Dynamic Pricing Reinforcement Learning Module
"""

import sys
import os
import unittest
import numpy as np

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'models'))

class TestReinforcementLearning(unittest.TestCase):
    """Test cases for reinforcement learning components"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        from dynamic_pricing.reinforcement_learning import QLearningPricingAgent, MultiArmedBanditPricingAgent
        self.q_agent = QLearningPricingAgent()
        self.bandit_agent = MultiArmedBanditPricingAgent(n_arms=5)
    
    def test_q_learning_agent_initialization(self):
        """Test Q-learning agent initialization"""
        self.assertIsNotNone(self.q_agent)
        self.assertEqual(self.q_agent.learning_rate, 0.1)
        self.assertEqual(self.q_agent.discount_factor, 0.9)
        self.assertEqual(self.q_agent.epsilon, 0.1)
    
    def test_multi_armed_bandit_initialization(self):
        """Test multi-armed bandit agent initialization"""
        self.assertIsNotNone(self.bandit_agent)
        self.assertEqual(self.bandit_agent.n_arms, 5)
        self.assertEqual(self.bandit_agent.learning_rate, 0.1)
    
    def test_action_selection(self):
        """Test action selection functionality"""
        # Test Q-learning action selection
        state = "test_state"
        action = self.q_agent.get_action(state)
        self.assertIsInstance(action, float)
        
        # Test bandit action selection
        arm = self.bandit_agent.select_arm()
        self.assertIsInstance(arm, int)
        self.assertGreaterEqual(arm, 0)
        self.assertLess(arm, self.bandit_agent.n_arms)

if __name__ == '__main__':
    unittest.main()