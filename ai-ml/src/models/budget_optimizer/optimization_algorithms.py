"""
Optimization Algorithms for Budget Optimization Model
Implements Linear Programming, Genetic Algorithm, Simulated Annealing, and Particle Swarm Optimization
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Try to import optimization libraries
try:
    from scipy.optimize import linprog, minimize
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    logging.warning("SciPy not available, some optimization features will be limited")

logger = logging.getLogger(__name__)


class LinearProgrammingOptimizer:
    """Linear Programming optimizer for budget allocation"""
    
    def __init__(self):
        """Initialize Linear Programming optimizer"""
        self.available = SCIPY_AVAILABLE
        logger.info("Linear Programming Optimizer initialized")
    
    def solve_budget_allocation(self, objective_coeffs: List[float], 
                              constraint_matrix: List[List[float]], 
                              constraint_bounds: List[Tuple[float, float]],
                              variable_bounds: List[Tuple[float, float]]) -> Dict[str, Any]:
        """
        Solve budget allocation problem using Linear Programming
        
        Args:
            objective_coeffs: Coefficients of the objective function (to maximize)
            constraint_matrix: Matrix of constraint coefficients
            constraint_bounds: Bounds for each constraint (min, max)
            variable_bounds: Bounds for each variable (min, max)
            
        Returns:
            Dictionary with optimization results
        """
        if not self.available:
            logger.warning("SciPy not available, returning default solution")
            return {
                'success': False,
                'message': 'SciPy not available',
                'optimal_allocation': [0.0] * len(objective_coeffs),
                'optimal_value': 0.0
            }
        
        try:
            # Convert maximization to minimization (negate objective)
            c = [-coeff for coeff in objective_coeffs]
            
            # Prepare constraints in standard form (Ax <= b)
            A_ub = []
            b_ub = []
            
            for i, (constraint_row, (lb, ub)) in enumerate(zip(constraint_matrix, constraint_bounds)):
                if lb > -np.inf:
                    # Convert >= constraint to <= by negating
                    A_ub.append([-val for val in constraint_row])
                    b_ub.append(-lb)
                if ub < np.inf:
                    A_ub.append(constraint_row)
                    b_ub.append(ub)
            
            # Solve the linear programming problem
            result = linprog(
                c=c,
                A_ub=A_ub if A_ub else None,
                b_ub=b_ub if b_ub else None,
                bounds=variable_bounds,
                method='highs'
            )
            
            if result.success:
                # Convert back to maximization value
                optimal_value = -result.fun
                logger.info(f"Linear Programming optimization successful, optimal value: {optimal_value:.2f}")
                return {
                    'success': True,
                    'message': 'Optimization successful',
                    'optimal_allocation': result.x.tolist(),
                    'optimal_value': float(optimal_value),
                    'iterations': result.nit
                }
            else:
                logger.warning("Linear Programming optimization failed")
                return {
                    'success': False,
                    'message': 'Optimization failed',
                    'optimal_allocation': [0.0] * len(objective_coeffs),
                    'optimal_value': 0.0
                }
                
        except Exception as e:
            logger.error(f"Error in Linear Programming optimization: {e}")
            return {
                'success': False,
                'message': f'Optimization error: {str(e)}',
                'optimal_allocation': [0.0] * len(objective_coeffs),
                'optimal_value': 0.0
            }


class GeneticAlgorithmOptimizer:
    """Genetic Algorithm optimizer for complex budget optimization"""
    
    def __init__(self, population_size: int = 50, generations: int = 100, 
                 mutation_rate: float = 0.1, crossover_rate: float = 0.8):
        """
        Initialize Genetic Algorithm optimizer
        
        Args:
            population_size: Number of individuals in population
            generations: Number of generations to evolve
            mutation_rate: Probability of mutation
            crossover_rate: Probability of crossover
        """
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        logger.info("Genetic Algorithm Optimizer initialized")
    
    def optimize_budget_allocation(self, objective_function, 
                                 variable_bounds: List[Tuple[float, float]],
                                 constraint_function=None) -> Dict[str, Any]:
        """
        Optimize budget allocation using Genetic Algorithm
        
        Args:
            objective_function: Function to maximize (takes allocation vector, returns fitness)
            variable_bounds: Bounds for each variable (min, max)
            constraint_function: Optional constraint function (takes allocation vector, returns bool)
            
        Returns:
            Dictionary with optimization results
        """
        try:
            # Initialize population
            num_variables = len(variable_bounds)
            population = self._initialize_population(variable_bounds)
            
            best_fitness = -np.inf
            best_solution = None
            fitness_history = []
            
            # Evolution loop
            for generation in range(self.generations):
                # Evaluate fitness
                fitness_scores = []
                for individual in population:
                    # Check constraints if provided
                    if constraint_function and not constraint_function(individual):
                        fitness_scores.append(-np.inf)  # Invalid solution
                    else:
                        fitness_scores.append(objective_function(individual))
                
                # Track best solution
                max_fitness_idx = np.argmax(fitness_scores)
                if fitness_scores[max_fitness_idx] > best_fitness:
                    best_fitness = fitness_scores[max_fitness_idx]
                    best_solution = population[max_fitness_idx].copy()
                
                fitness_history.append(best_fitness)
                
                # Selection (tournament selection)
                selected_population = self._tournament_selection(population, fitness_scores)
                
                # Crossover
                offspring_population = self._crossover(selected_population)
                
                # Mutation
                mutated_population = self._mutate(offspring_population, variable_bounds)
                
                # Replace population
                population = mutated_population
                
                # Log progress
                if (generation + 1) % 20 == 0:
                    logger.info(f"Generation {generation + 1}/{self.generations}, Best Fitness: {best_fitness:.2f}")
            
            logger.info(f"Genetic Algorithm optimization completed, best fitness: {best_fitness:.2f}")
            return {
                'success': True,
                'message': 'Optimization completed',
                'optimal_allocation': best_solution.tolist() if best_solution is not None else [0.0] * num_variables,
                'optimal_value': float(best_fitness),
                'generations': self.generations,
                'fitness_history': fitness_history
            }
            
        except Exception as e:
            logger.error(f"Error in Genetic Algorithm optimization: {e}")
            return {
                'success': False,
                'message': f'Optimization error: {str(e)}',
                'optimal_allocation': [0.0] * len(variable_bounds),
                'optimal_value': 0.0
            }
    
    def _initialize_population(self, variable_bounds: List[Tuple[float, float]]) -> np.ndarray:
        """Initialize random population"""
        population = []
        for _ in range(self.population_size):
            individual = []
            for min_val, max_val in variable_bounds:
                individual.append(np.random.uniform(min_val, max_val))
            population.append(individual)
        return np.array(population)
    
    def _tournament_selection(self, population: np.ndarray, 
                            fitness_scores: List[float], 
                            tournament_size: int = 3) -> np.ndarray:
        """Tournament selection"""
        selected = []
        for _ in range(len(population)):
            # Select random individuals for tournament
            tournament_indices = np.random.choice(len(population), tournament_size, replace=False)
            tournament_fitness = [fitness_scores[i] for i in tournament_indices]
            
            # Select winner (highest fitness)
            winner_idx = tournament_indices[np.argmax(tournament_fitness)]
            selected.append(population[winner_idx])
        
        return np.array(selected)
    
    def _crossover(self, population: np.ndarray) -> np.ndarray:
        """Uniform crossover"""
        offspring = []
        for i in range(0, len(population), 2):
            parent1 = population[i]
            if i + 1 < len(population):
                parent2 = population[i + 1]
                
                # Crossover with given probability
                if np.random.random() < self.crossover_rate:
                    # Uniform crossover
                    child1, child2 = parent1.copy(), parent2.copy()
                    for j in range(len(parent1)):
                        if np.random.random() < 0.5:
                            child1[j], child2[j] = child2[j], child1[j]
                    offspring.extend([child1, child2])
                else:
                    offspring.extend([parent1, parent2])
            else:
                offspring.append(parent1)
        
        return np.array(offspring)
    
    def _mutate(self, population: np.ndarray, 
                variable_bounds: List[Tuple[float, float]]) -> np.ndarray:
        """Gaussian mutation"""
        mutated = []
        for individual in population:
            mutated_individual = individual.copy()
            for i, (min_val, max_val) in enumerate(variable_bounds):
                if np.random.random() < self.mutation_rate:
                    # Gaussian mutation
                    mutation_strength = (max_val - min_val) * 0.1
                    mutated_individual[i] += np.random.normal(0, mutation_strength)
                    # Ensure bounds
                    mutated_individual[i] = np.clip(mutated_individual[i], min_val, max_val)
            mutated.append(mutated_individual)
        
        return np.array(mutated)


class SimulatedAnnealingOptimizer:
    """Simulated Annealing optimizer for budget optimization"""
    
    def __init__(self, initial_temperature: float = 1000, 
                 cooling_rate: float = 0.95, min_temperature: float = 1):
        """
        Initialize Simulated Annealing optimizer
        
        Args:
            initial_temperature: Initial temperature
            cooling_rate: Cooling rate (0 < rate < 1)
            min_temperature: Minimum temperature
        """
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.min_temperature = min_temperature
        logger.info("Simulated Annealing Optimizer initialized")
    
    def optimize_budget_allocation(self, objective_function, 
                                 initial_solution: List[float],
                                 variable_bounds: List[Tuple[float, float]],
                                 constraint_function=None) -> Dict[str, Any]:
        """
        Optimize budget allocation using Simulated Annealing
        
        Args:
            objective_function: Function to maximize (takes allocation vector, returns fitness)
            initial_solution: Starting solution
            variable_bounds: Bounds for each variable (min, max)
            constraint_function: Optional constraint function (takes allocation vector, returns bool)
            
        Returns:
            Dictionary with optimization results
        """
        try:
            # Initialize
            current_solution = np.array(initial_solution)
            current_fitness = objective_function(current_solution)
            
            best_solution = current_solution.copy()
            best_fitness = current_fitness
            
            temperature = self.initial_temperature
            iteration = 0
            fitness_history = []
            
            # Annealing loop
            while temperature > self.min_temperature:
                # Generate neighbor solution
                neighbor_solution = self._generate_neighbor(current_solution, variable_bounds)
                
                # Check constraints if provided
                if constraint_function and not constraint_function(neighbor_solution):
                    neighbor_fitness = -np.inf  # Invalid solution
                else:
                    neighbor_fitness = objective_function(neighbor_solution)
                
                # Accept or reject neighbor
                if self._accept_neighbor(current_fitness, neighbor_fitness, temperature):
                    current_solution = neighbor_solution
                    current_fitness = neighbor_fitness
                    
                    # Update best solution
                    if current_fitness > best_fitness:
                        best_solution = current_solution.copy()
                        best_fitness = current_fitness
                
                # Cool down
                temperature *= self.cooling_rate
                iteration += 1
                fitness_history.append(best_fitness)
                
                # Log progress
                if (iteration + 1) % 100 == 0:
                    logger.info(f"Iteration {iteration + 1}, Temperature: {temperature:.2f}, Best Fitness: {best_fitness:.2f}")
            
            logger.info(f"Simulated Annealing optimization completed, best fitness: {best_fitness:.2f}")
            return {
                'success': True,
                'message': 'Optimization completed',
                'optimal_allocation': best_solution.tolist(),
                'optimal_value': float(best_fitness),
                'iterations': iteration,
                'fitness_history': fitness_history
            }
            
        except Exception as e:
            logger.error(f"Error in Simulated Annealing optimization: {e}")
            return {
                'success': False,
                'message': f'Optimization error: {str(e)}',
                'optimal_allocation': initial_solution,
                'optimal_value': 0.0
            }
    
    def _generate_neighbor(self, solution: np.ndarray, 
                          variable_bounds: List[Tuple[float, float]]) -> np.ndarray:
        """Generate neighbor solution"""
        neighbor = solution.copy()
        # Select random variable to modify
        var_index = np.random.randint(len(solution))
        
        # Generate small perturbation
        min_val, max_val = variable_bounds[var_index]
        perturbation = np.random.normal(0, (max_val - min_val) * 0.1)
        neighbor[var_index] += perturbation
        
        # Ensure bounds
        neighbor[var_index] = np.clip(neighbor[var_index], min_val, max_val)
        
        return neighbor
    
    def _accept_neighbor(self, current_fitness: float, 
                        neighbor_fitness: float, 
                        temperature: float) -> bool:
        """Accept or reject neighbor solution"""
        if neighbor_fitness > current_fitness:
            return True
        else:
            # Accept with probability based on temperature
            probability = np.exp((neighbor_fitness - current_fitness) / temperature)
            return np.random.random() < probability


class ParticleSwarmOptimizer:
    """Particle Swarm Optimization for budget allocation"""
    
    def __init__(self, num_particles: int = 30, max_iterations: int = 100,
                 inertia_weight: float = 0.7, cognitive_coeff: float = 1.5,
                 social_coeff: float = 1.5):
        """
        Initialize Particle Swarm Optimizer
        
        Args:
            num_particles: Number of particles in swarm
            max_iterations: Maximum number of iterations
            inertia_weight: Inertia weight (w)
            cognitive_coeff: Cognitive coefficient (c1)
            social_coeff: Social coefficient (c2)
        """
        self.num_particles = num_particles
        self.max_iterations = max_iterations
        self.inertia_weight = inertia_weight
        self.cognitive_coeff = cognitive_coeff
        self.social_coeff = social_coeff
        logger.info("Particle Swarm Optimizer initialized")
    
    def optimize_budget_allocation(self, objective_function,
                                 variable_bounds: List[Tuple[float, float]],
                                 constraint_function=None) -> Dict[str, Any]:
        """
        Optimize budget allocation using Particle Swarm Optimization
        
        Args:
            objective_function: Function to maximize (takes allocation vector, returns fitness)
            variable_bounds: Bounds for each variable (min, max)
            constraint_function: Optional constraint function (takes allocation vector, returns bool)
            
        Returns:
            Dictionary with optimization results
        """
        try:
            num_dimensions = len(variable_bounds)
            
            # Initialize swarm
            particles = []
            velocities = []
            personal_best_positions = []
            personal_best_fitness = []
            
            # Global best
            global_best_position = None
            global_best_fitness = -np.inf
            
            # Initialize particles
            for _ in range(self.num_particles):
                # Random position within bounds
                position = []
                velocity = []
                for min_val, max_val in variable_bounds:
                    position.append(np.random.uniform(min_val, max_val))
                    velocity.append(np.random.uniform(-0.1 * (max_val - min_val), 0.1 * (max_val - min_val)))
                
                particles.append(np.array(position))
                velocities.append(np.array(velocity))
                
                # Evaluate fitness
                if constraint_function and not constraint_function(position):
                    fitness = -np.inf
                else:
                    fitness = objective_function(position)
                
                personal_best_positions.append(np.array(position))
                personal_best_fitness.append(fitness)
                
                # Update global best
                if fitness > global_best_fitness:
                    global_best_fitness = fitness
                    global_best_position = np.array(position)
            
            fitness_history = []
            
            # Main loop
            for iteration in range(self.max_iterations):
                for i in range(self.num_particles):
                    # Update velocity
                    r1, r2 = np.random.random(), np.random.random()
                    
                    cognitive_velocity = self.cognitive_coeff * r1 * (
                        personal_best_positions[i] - particles[i]
                    )
                    
                    social_velocity = self.social_coeff * r2 * (
                        global_best_position - particles[i]
                    )
                    
                    velocities[i] = (
                        self.inertia_weight * velocities[i] +
                        cognitive_velocity +
                        social_velocity
                    )
                    
                    # Update position
                    particles[i] += velocities[i]
                    
                    # Enforce bounds
                    for j, (min_val, max_val) in enumerate(variable_bounds):
                        particles[i][j] = np.clip(particles[i][j], min_val, max_val)
                    
                    # Evaluate fitness
                    if constraint_function and not constraint_function(particles[i]):
                        fitness = -np.inf
                    else:
                        fitness = objective_function(particles[i])
                    
                    # Update personal best
                    if fitness > personal_best_fitness[i]:
                        personal_best_fitness[i] = fitness
                        personal_best_positions[i] = particles[i].copy()
                        
                        # Update global best
                        if fitness > global_best_fitness:
                            global_best_fitness = fitness
                            global_best_position = particles[i].copy()
                
                fitness_history.append(global_best_fitness)
                
                # Log progress
                if (iteration + 1) % 20 == 0:
                    logger.info(f"Iteration {iteration + 1}/{self.max_iterations}, Best Fitness: {global_best_fitness:.2f}")
            
            logger.info(f"Particle Swarm Optimization completed, best fitness: {global_best_fitness:.2f}")
            return {
                'success': True,
                'message': 'Optimization completed',
                'optimal_allocation': global_best_position.tolist() if global_best_position is not None else [0.0] * num_dimensions,
                'optimal_value': float(global_best_fitness),
                'iterations': self.max_iterations,
                'fitness_history': fitness_history
            }
            
        except Exception as e:
            logger.error(f"Error in Particle Swarm Optimization: {e}")
            return {
                'success': False,
                'message': f'Optimization error: {str(e)}',
                'optimal_allocation': [0.0] * len(variable_bounds),
                'optimal_value': 0.0
            }


class MultiObjectiveOptimizer:
    """Multi-objective optimization framework"""
    
    def __init__(self):
        """Initialize Multi-objective optimizer"""
        logger.info("Multi-Objective Optimizer initialized")
    
    def weighted_sum_optimization(self, objectives: List[Dict[str, Any]], 
                                weights: List[float]) -> Dict[str, Any]:
        """
        Perform weighted sum multi-objective optimization
        
        Args:
            objectives: List of objective dictionaries with 'function' and 'bounds'
            weights: Weights for each objective
            
        Returns:
            Dictionary with optimization results
        """
        try:
            if len(objectives) != len(weights):
                raise ValueError("Number of objectives must match number of weights")
            
            # Normalize weights
            total_weight = sum(weights)
            if total_weight > 0:
                normalized_weights = [w / total_weight for w in weights]
            else:
                normalized_weights = [1.0 / len(weights)] * len(weights)
            
            # Combine objectives into single weighted objective
            def combined_objective(allocation):
                total_value = 0
                for i, obj in enumerate(objectives):
                    total_value += normalized_weights[i] * obj['function'](allocation)
                return total_value
            
            # Use first objective's bounds as combined bounds
            if objectives:
                variable_bounds = objectives[0]['bounds']
                
                # Simple optimization using random search for demonstration
                best_allocation = None
                best_value = -np.inf
                
                # Random search
                for _ in range(1000):
                    allocation = []
                    for min_val, max_val in variable_bounds:
                        allocation.append(np.random.uniform(min_val, max_val))
                    
                    value = combined_objective(allocation)
                    if value > best_value:
                        best_value = value
                        best_allocation = allocation
                
                logger.info(f"Multi-objective optimization completed, best value: {best_value:.2f}")
                return {
                    'success': True,
                    'message': 'Optimization completed',
                    'optimal_allocation': best_allocation if best_allocation else [0.0] * len(variable_bounds),
                    'optimal_value': float(best_value),
                    'evaluations': 1000
                }
            else:
                return {
                    'success': False,
                    'message': 'No objectives provided',
                    'optimal_allocation': [],
                    'optimal_value': 0.0
                }
                
        except Exception as e:
            logger.error(f"Error in Multi-objective optimization: {e}")
            return {
                'success': False,
                'message': f'Optimization error: {str(e)}',
                'optimal_allocation': [],
                'optimal_value': 0.0
            }


# Global instances for easy access
lp_optimizer_instance = None
ga_optimizer_instance = None
sa_optimizer_instance = None
pso_optimizer_instance = None
mo_optimizer_instance = None


def get_linear_programming_optimizer() -> LinearProgrammingOptimizer:
    """Get singleton Linear Programming optimizer instance"""
    global lp_optimizer_instance
    if lp_optimizer_instance is None:
        lp_optimizer_instance = LinearProgrammingOptimizer()
    return lp_optimizer_instance


def get_genetic_algorithm_optimizer(population_size: int = 50, generations: int = 100,
                                  mutation_rate: float = 0.1, crossover_rate: float = 0.8) -> GeneticAlgorithmOptimizer:
    """Get singleton Genetic Algorithm optimizer instance"""
    global ga_optimizer_instance
    if ga_optimizer_instance is None:
        ga_optimizer_instance = GeneticAlgorithmOptimizer(population_size, generations, mutation_rate, crossover_rate)
    return ga_optimizer_instance


def get_simulated_annealing_optimizer(initial_temperature: float = 1000,
                                    cooling_rate: float = 0.95, min_temperature: float = 1) -> SimulatedAnnealingOptimizer:
    """Get singleton Simulated Annealing optimizer instance"""
    global sa_optimizer_instance
    if sa_optimizer_instance is None:
        sa_optimizer_instance = SimulatedAnnealingOptimizer(initial_temperature, cooling_rate, min_temperature)
    return sa_optimizer_instance


def get_particle_swarm_optimizer(num_particles: int = 30, max_iterations: int = 100,
                               inertia_weight: float = 0.7, cognitive_coeff: float = 1.5,
                               social_coeff: float = 1.5) -> ParticleSwarmOptimizer:
    """Get singleton Particle Swarm optimizer instance"""
    global pso_optimizer_instance
    if pso_optimizer_instance is None:
        pso_optimizer_instance = ParticleSwarmOptimizer(num_particles, max_iterations, inertia_weight, cognitive_coeff, social_coeff)
    return pso_optimizer_instance


def get_multi_objective_optimizer() -> MultiObjectiveOptimizer:
    """Get singleton Multi-objective optimizer instance"""
    global mo_optimizer_instance
    if mo_optimizer_instance is None:
        mo_optimizer_instance = MultiObjectiveOptimizer()
    return mo_optimizer_instance