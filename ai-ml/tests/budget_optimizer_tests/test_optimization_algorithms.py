"""
Tests for Budget Optimization Algorithms Module
"""

import sys
import os
import unittest
import pandas as pd
import numpy as np

# Add the src directory to the path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
sys.path.insert(0, src_path)

from src.models.budget_optimizer.optimization_algorithms import (
    LinearProgrammingOptimizer,
    GeneticAlgorithmOptimizer,
    SimulatedAnnealingOptimizer,
    ParticleSwarmOptimizer,
    MultiObjectiveOptimizer
)


class TestOptimizationAlgorithms(unittest.TestCase):
    """Tests for optimization algorithms"""
    
    def test_linear_programming_optimizer_initialization(self):
        """Test Linear Programming optimizer initialization"""
        optimizer = LinearProgrammingOptimizer()
        self.assertIsNotNone(optimizer)
        self.assertTrue(hasattr(optimizer, 'available'))
    
    def test_genetic_algorithm_optimizer_initialization(self):
        """Test Genetic Algorithm optimizer initialization"""
        optimizer = GeneticAlgorithmOptimizer()
        self.assertIsNotNone(optimizer)
        self.assertTrue(hasattr(optimizer, 'population_size'))
        self.assertTrue(hasattr(optimizer, 'generations'))
    
    def test_simulated_annealing_optimizer_initialization(self):
        """Test Simulated Annealing optimizer initialization"""
        optimizer = SimulatedAnnealingOptimizer()
        self.assertIsNotNone(optimizer)
        self.assertTrue(hasattr(optimizer, 'initial_temperature'))
        self.assertTrue(hasattr(optimizer, 'cooling_rate'))
    
    def test_particle_swarm_optimizer_initialization(self):
        """Test Particle Swarm optimizer initialization"""
        optimizer = ParticleSwarmOptimizer()
        self.assertIsNotNone(optimizer)
        self.assertTrue(hasattr(optimizer, 'num_particles'))
        self.assertTrue(hasattr(optimizer, 'max_iterations'))
    
    def test_multi_objective_optimizer_initialization(self):
        """Test Multi-objective optimizer initialization"""
        optimizer = MultiObjectiveOptimizer()
        self.assertIsNotNone(optimizer)
    
    def test_linear_programming_simple_optimization(self):
        """Test simple Linear Programming optimization"""
        optimizer = LinearProgrammingOptimizer()
        
        # Simple optimization problem: maximize x + y subject to x + 2y <= 3, 2x + y <= 3, x,y >= 0
        objective_coeffs = [1.0, 1.0]  # Maximize x + y
        constraint_matrix = [[1.0, 2.0], [2.0, 1.0]]  # Constraints
        constraint_bounds = [(0.0, 3.0), (0.0, 3.0)]  # Bounds for constraints
        variable_bounds = [(0.0, 1000.0), (0.0, 1000.0)]  # Variable bounds
        
        result = optimizer.solve_budget_allocation(
            objective_coeffs, constraint_matrix, constraint_bounds, variable_bounds
        )
        
        self.assertTrue(isinstance(result, dict))
        self.assertIn('success', result)
        # Note: Actual success depends on SciPy availability
    
    def test_genetic_algorithm_simple_optimization(self):
        """Test simple Genetic Algorithm optimization"""
        optimizer = GeneticAlgorithmOptimizer(population_size=10, generations=5)
        
        # Simple objective function: maximize -(x-2)^2 (maximum at x=2)
        def objective_function(x):
            return -(x[0] - 2) ** 2
        
        variable_bounds = [(0.0, 5.0)]
        
        result = optimizer.optimize_budget_allocation(objective_function, variable_bounds)
        
        self.assertTrue(isinstance(result, dict))
        self.assertIn('success', result)
        self.assertTrue(result['success'])


if __name__ == '__main__':
    unittest.main()