"""
Reinforcement Learning for Dynamic Pricing Engine
Implements Q-Learning and Multi-armed bandit algorithms for optimal pricing decisions
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


class QLearningPricingAgent:
    """Q-Learning agent for dynamic pricing decisions"""
    
    def __init__(self, learning_rate: float = 0.1, discount_factor: float = 0.9, 
                 epsilon: float = 0.1, epsilon_decay: float = 0.995):
        """
        Initialize Q-Learning agent
        
        Args:
            learning_rate: Learning rate for Q-learning updates
            discount_factor: Discount factor for future rewards
            epsilon: Exploration rate for epsilon-greedy policy
            epsilon_decay: Decay rate for epsilon over time
        """
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        
        # Q-table: state-action values
        self.q_table = defaultdict(lambda: defaultdict(float))
        
        # State and action spaces
        self.state_space = []
        self.action_space = []
        
        # Episode tracking
        self.episode = 0
        self.total_rewards = []
        
        logger.info("Q-Learning Pricing Agent initialized")
    
    def define_state_space(self, state_features: List[str]):
        """
        Define the state space for the pricing agent
        
        Args:
            state_features: List of features that define states
        """
        self.state_space = state_features
        logger.info(f"State space defined with {len(state_features)} features")
    
    def define_action_space(self, price_points: List[float]):
        """
        Define the action space for the pricing agent
        
        Args:
            price_points: List of possible price points (actions)
        """
        self.action_space = price_points
        logger.info(f"Action space defined with {len(price_points)} price points")
    
    def get_state(self, features: Dict[str, Any]) -> str:
        """
        Convert features to a state representation
        
        Args:
            features: Dictionary of feature values
            
        Returns:
            State representation as string
        """
        # Simple state representation (can be enhanced with more sophisticated methods)
        state_parts = []
        for feature in self.state_space:
            if feature in features:
                # Discretize continuous features
                value = features[feature]
                if isinstance(value, (int, float)):
                    # Round to nearest 10 for discretization
                    discretized = round(value / 10) * 10
                    state_parts.append(f"{feature}:{discretized}")
                else:
                    state_parts.append(f"{feature}:{value}")
            else:
                state_parts.append(f"{feature}:unknown")
        
        return "|".join(state_parts)
    
    def get_action(self, state: str, training: bool = True) -> float:
        """
        Select an action (price point) based on the current state
        
        Args:
            state: Current state representation
            training: Whether in training mode (allows exploration)
            
        Returns:
            Selected action (price point)
        """
        if not self.action_space:
            logger.warning("Action space not defined, returning default price")
            return 100.0
        
        # Epsilon-greedy policy
        if training and np.random.random() < self.epsilon:
            # Exploration: random action
            action = np.random.choice(self.action_space)
            logger.debug(f"Exploration: selected random action {action}")
        else:
            # Exploitation: best known action
            if state in self.q_table and self.q_table[state]:
                # Select action with highest Q-value
                action = max(self.q_table[state].keys(), key=lambda a: self.q_table[state][a])
                logger.debug(f"Exploitation: selected best action {action}")
            else:
                # No Q-values for this state, select random action
                action = np.random.choice(self.action_space)
                logger.debug(f"No Q-values for state, selected random action {action}")
        
        return action
    
    def update_q_value(self, state: str, action: float, reward: float, 
                       next_state: str, done: bool = False):
        """
        Update Q-value based on observed reward and next state
        
        Args:
            state: Current state
            action: Action taken
            reward: Reward received
            next_state: Next state
            done: Whether episode is complete
        """
        if state not in self.q_table:
            self.q_table[state] = defaultdict(float)
        
        # Current Q-value
        current_q = self.q_table[state][action]
        
        # Next Q-value (max Q-value of next state)
        if done or next_state not in self.q_table:
            next_q = 0
        else:
            next_q = max(self.q_table[next_state].values()) if self.q_table[next_state] else 0
        
        # Q-learning update rule
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * next_q - current_q)
        self.q_table[state][action] = new_q
        
        logger.debug(f"Updated Q-value for state {state}, action {action}: {current_q} -> {new_q}")
    
    def decay_epsilon(self):
        """Decay exploration rate"""
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(0.01, self.epsilon)  # Minimum exploration rate
        logger.debug(f"Decayed epsilon to {self.epsilon}")
    
    def get_policy(self) -> Dict[str, float]:
        """
        Get the current policy (best action for each state)
        
        Returns:
            Dictionary mapping states to optimal actions
        """
        policy = {}
        for state in self.q_table:
            if self.q_table[state]:
                policy[state] = max(self.q_table[state].keys(), key=lambda a: self.q_table[state][a])
        return policy
    
    def get_state_action_values(self, state: str) -> Dict[float, float]:
        """
        Get Q-values for all actions in a given state
        
        Args:
            state: State to get Q-values for
            
        Returns:
            Dictionary mapping actions to Q-values
        """
        return dict(self.q_table.get(state, {}))


class MultiArmedBanditPricingAgent:
    """Multi-armed bandit agent for dynamic pricing decisions"""
    
    def __init__(self, n_arms: int, learning_rate: float = 0.1):
        """
        Initialize Multi-armed Bandit agent
        
        Args:
            n_arms: Number of arms (price points)
            learning_rate: Learning rate for updates
        """
        self.n_arms = n_arms
        self.learning_rate = learning_rate
        
        # Track rewards and counts for each arm
        self.rewards = np.zeros(n_arms)
        self.counts = np.zeros(n_arms)
        self.values = np.zeros(n_arms)
        
        # Softmax temperature for action selection
        self.temperature = 1.0
        
        logger.info(f"Multi-armed Bandit Pricing Agent initialized with {n_arms} arms")
    
    def select_arm(self) -> int:
        """
        Select an arm (price point) using softmax action selection
        
        Returns:
            Index of selected arm
        """
        # Softmax action selection
        if self.temperature > 0:
            # Compute softmax probabilities
            exp_values = np.exp(self.values / self.temperature)
            probabilities = exp_values / np.sum(exp_values)
            
            # Select arm based on probabilities
            arm = int(np.random.choice(self.n_arms, p=probabilities))
        else:
            # Select best arm
            arm = int(np.argmax(self.values))
        
        logger.debug(f"Selected arm {arm} with value {self.values[arm]:.2f}")
        return arm
    
    def update(self, arm: int, reward: float):
        """
        Update the value of an arm based on observed reward
        
        Args:
            arm: Index of arm that was selected
            reward: Reward received
        """
        # Update counts and rewards
        self.counts[arm] += 1
        self.rewards[arm] += reward
        
        # Update value using incremental formula
        # Value = Value + learning_rate * (Reward - Value)
        self.values[arm] += self.learning_rate * (reward - self.values[arm])
        
        logger.debug(f"Updated arm {arm}: count={self.counts[arm]}, reward={reward:.2f}, value={self.values[arm]:.2f}")
    
    def decay_temperature(self, decay_rate: float = 0.99):
        """
        Decay the temperature for softmax action selection
        
        Args:
            decay_rate: Rate at which to decay temperature
        """
        self.temperature *= decay_rate
        self.temperature = max(0.1, self.temperature)  # Minimum temperature
        logger.debug(f"Decayed temperature to {self.temperature}")
    
    def get_best_arm(self) -> int:
        """
        Get the arm with the highest value
        
        Returns:
            Index of best arm
        """
        return int(np.argmax(self.values))
    
    def get_arm_values(self) -> np.ndarray:
        """
        Get values for all arms
        
        Returns:
            Array of arm values
        """
        return self.values.copy()


class PricingRewardFunction:
    """Reward function for dynamic pricing"""
    
    def __init__(self):
        """Initialize reward function"""
        logger.info("Pricing Reward Function initialized")
    
    def calculate_reward(self, revenue: float, cost: float, client_retention: float, 
                        market_share: float, competitor_pricing: float) -> float:
        """
        Calculate reward based on pricing outcomes
        
        Args:
            revenue: Revenue generated
            cost: Cost of service delivery
            client_retention: Client retention rate (0-1)
            market_share: Market share (0-1)
            competitor_pricing: Competitor pricing level
            
        Returns:
            Reward value
        """
        # Profit calculation
        profit = revenue - cost
        
        # Weighted reward components
        profit_reward = profit * 0.5
        retention_reward = client_retention * 1000 * 0.3  # Weight retention heavily
        market_share_reward = market_share * 500 * 0.2  # Weight market share
        
        # Competitive positioning reward/penalty
        if revenue > competitor_pricing:
            competitive_reward = -100  # Penalty for overpricing
        elif revenue < competitor_pricing * 0.8:
            competitive_reward = -50  # Penalty for underpricing
        else:
            competitive_reward = 100  # Reward for competitive pricing
        
        total_reward = profit_reward + retention_reward + market_share_reward + competitive_reward
        
        logger.debug(f"Reward calculation: profit={profit_reward:.2f}, retention={retention_reward:.2f}, "
                    f"market={market_share_reward:.2f}, competitive={competitive_reward:.2f}, "
                    f"total={total_reward:.2f}")
        
        return total_reward


# Global instances for easy access
q_learning_agent_instance = None
multi_armed_bandit_instance = None
reward_function_instance = None


def get_q_learning_agent(learning_rate: float = 0.1, discount_factor: float = 0.9, 
                        epsilon: float = 0.1) -> QLearningPricingAgent:
    """Get singleton Q-learning agent instance"""
    global q_learning_agent_instance
    if q_learning_agent_instance is None:
        q_learning_agent_instance = QLearningPricingAgent(learning_rate, discount_factor, epsilon)
    return q_learning_agent_instance


def get_multi_armed_bandit_agent(n_arms: int = 10, learning_rate: float = 0.1) -> MultiArmedBanditPricingAgent:
    """Get singleton multi-armed bandit agent instance"""
    global multi_armed_bandit_instance
    if multi_armed_bandit_instance is None:
        multi_armed_bandit_instance = MultiArmedBanditPricingAgent(n_arms, learning_rate)
    return multi_armed_bandit_instance


def get_pricing_reward_function() -> PricingRewardFunction:
    """Get singleton pricing reward function instance"""
    global reward_function_instance
    if reward_function_instance is None:
        reward_function_instance = PricingRewardFunction()
    return reward_function_instance