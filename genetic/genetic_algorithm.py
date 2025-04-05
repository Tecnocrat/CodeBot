import os
import random
import math
import logging
import numpy as np
import shutil
from genetic.genetic_population import request_population
from core.ai_engine import parse_codebase
from core.self_improvement import fitness_function
from genetic.genetic_population import evaluate_population

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def flatten_directory(base_dir, target_dir):
    """
    Moves all files from nested directories into a single target directory.
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            src_path = os.path.join(root, file)
            dest_path = os.path.join(target_dir, file)
            if not os.path.exists(dest_path):
                shutil.move(src_path, dest_path)
            else:
                print(f"Duplicate file skipped: {dest_path}")

def fractal_fitness_function(position, depth=3):
    """
    A fractal-inspired fitness function that evaluates a position in a hyperspatial multidimensional space.
    The function uses fractal geometry concepts to create a complex fitness landscape.

    Args:
        position (list[float]): A position vector in the multidimensional space.
        depth (int): The depth of fractal complexity.

    Returns:
        float: The fitness value of the position.
    """
    fitness = 0
    for i, coord in enumerate(position):
        # Base fractal interactions
        fitness += math.sin(coord * math.pi) * math.cos(coord * (i + 1))
        fitness += np.linalg.norm(position) * math.sin(np.sum(position))

        # Add fractal depth complexity
        for d in range(1, depth + 1):
            fitness += (math.sin(coord * d) ** 2) / (1 + math.exp(-coord * d))
            fitness += math.log(abs(coord) + 1) * math.cos(d * coord)

    # Normalize fitness to avoid extreme values
    fitness /= (len(position) * depth)
    return float(fitness)

def initialize_population(size, dimensions, bounds):
    """
    Initializes a population of individuals in a multidimensional space.
    Each individual is represented as a position vector.
    """
    population = []
    for _ in range(size):
        individual = [random.uniform(bounds[0], bounds[1]) for _ in range(dimensions)]
        population.append(individual)
    return population

def mutate(individual, mutation_rate, bounds):
    """
    Applies mutation to an individual by slightly altering its position in the multidimensional space.
    """
    mutated = []
    for coord in individual:
        if random.random() < mutation_rate:
            coord += random.uniform(-0.1, 0.1)  # Small random change
            coord = max(min(coord, bounds[1]), bounds[0])  # Ensure within bounds
        mutated.append(coord)
    return mutated

def crossover(parent1, parent2):
    """
    Performs crossover between two parents to produce an offspring.
    """
    crossover_point = random.randint(1, len(parent1) - 1)
    return parent1[:crossover_point] + parent2[crossover_point:]

def fractal_genetic_algorithm(dimensions, generations, population_size, bounds, fractal_depth=3):
    """
    A fractal-based genetic algorithm that optimizes a hyperspatial multidimensional space.

    Args:
        dimensions (int): Number of dimensions in the hyperspatial space.
        generations (int): Number of generations to run the algorithm.
        population_size (int): Size of the population.
        bounds (tuple[float, float]): Bounds for each dimension.
        fractal_depth (int): Depth of fractal complexity for the fitness function.

    Returns:
        list[float]: The best individual found by the algorithm.
    """
    logging.info("Starting fractal genetic algorithm...")

    # Initialize population
    population = initialize_population(population_size, dimensions, bounds)
    logging.info(f"Initial population: {population}")

    for generation in range(generations):
        logging.info(f"Generation {generation + 1}")

        # Evaluate fitness
        fitness_scores = [fractal_fitness_function(individual, depth=fractal_depth) for individual in population]
        logging.info(f"Fitness scores: {fitness_scores}")

        # Select the top individuals (elitism)
        sorted_population = [x for _, x in sorted(zip(fitness_scores, population), reverse=True)]
        population = sorted_population[:population_size // 2]

        # Generate offspring through crossover
        offspring = []
        while len(offspring) < population_size // 2:
            parent1, parent2 = random.sample(population, 2)
            child = crossover(parent1, parent2)
            offspring.append(child)

        # Mutate offspring
        offspring = [mutate(child, mutation_rate=0.2, bounds=bounds) for child in offspring]

        # Combine parents and offspring to form the new population
        population += offspring

    # Return the best individual
    best_individual = max(population, key=lambda ind: fractal_fitness_function(ind, depth=fractal_depth))
    logging.info(f"Best individual: {best_individual}")
    return best_individual

def fractal_genetic_algorithm_with_population(source_file, generations, population_size, dimensions, bounds, fractal_depth, output_dir):
    """
    Runs a fractal-based genetic algorithm using a requested population.
    """
    logging.info("Requesting initial population...")
    population = request_population(source_file, population_size, dimensions, bounds, output_dir)

    for generation in range(generations):
        logging.info(f"Generation {generation + 1}: Population size = {len(population)}")
        # Add fractal-based logic
        # ...

    logging.info("Fractal genetic algorithm completed.")

def fractal_genetic_algorithm_with_parsing(base_dir, dimensions, generations, population_size, bounds, fractal_depth=3):
    """
    A fractal-based genetic algorithm that integrates codebase parsing.

    Args:
        base_dir (str): Root directory of the CodeBot project.
        dimensions (int): Number of dimensions in the hyperspatial space.
        generations (int): Number of generations to run the algorithm.
        population_size (int): Size of the population.
        bounds (tuple[float, float]): Bounds for each dimension.
        fractal_depth (int): Depth of fractal complexity for the fitness function.

    Returns:
        list[float]: The best individual found by the algorithm.
    """
    logging.info("Parsing codebase...")
    parsed_structure = parse_codebase(base_dir)
    logging.info(f"Parsed structure: {parsed_structure}")

    # Use parsed structure for population evaluation
    population = initialize_population(population_size, dimensions, bounds)
    for generation in range(generations):
        fitness_scores = [fractal_fitness_function(ind, fractal_depth) for ind in population]
        population = sorted(population, key=lambda ind: fractal_fitness_function(ind, fractal_depth), reverse=True)[:population_size // 2]
        offspring = [mutate(crossover(*random.sample(population, 2)), 0.2, bounds) for _ in range(population_size // 2)]
        population += offspring

    best_individual = max(population, key=lambda ind: fractal_fitness_function(ind, fractal_depth))
    logging.info(f"Best individual: {best_individual}")
    return best_individual

def evaluate_population(population_dir):
    """
    Evaluates the fitness of a population of individuals.

    Args:
        population_dir (str): Path to the directory containing the population.

    Returns:
        list[dict]: A list of dictionaries containing the individual and its fitness score.
    """
    if not os.path.exists(population_dir):
        raise FileNotFoundError(f"Population directory not found: {population_dir}")

    population = []
    for file_name in os.listdir(population_dir):
        file_path = os.path.join(population_dir, file_name)
        if os.path.isfile(file_path):
            try:
                fitness = fitness_function(file_path)
                population.append({"individual": file_name, "fitness": fitness})
                logging.info(f"Evaluated {file_name}: Fitness = {fitness}")
            except Exception as e:
                logging.error(f"Error evaluating {file_name}: {e}")

    # Sort the population by fitness (lower is better)
    population.sort(key=lambda x: x["fitness"])
    return population

if __name__ == "__main__":
    base_dir = "c:\\dev\\CodeBot\\adn_trash_code\\replicated_CodeBot"
    target_dir = "c:\\dev\\CodeBot\\optimized_code"
    flatten_directory(base_dir, target_dir)
    print(f"Files moved to {target_dir}")

    # Example usage
    dimensions = 5  # Number of dimensions in the hyperspatial space
    generations = 50  # Number of generations
    population_size = 20  # Size of the population
    bounds = (-10, 10)  # Bounds for each dimension
    fractal_depth = 4  # Depth of fractal complexity

    best_solution = fractal_genetic_algorithm(dimensions, generations, population_size, bounds, fractal_depth)
    print(f"Best solution found: {best_solution}")

    # Example usage for evaluate_population
    population_dir = "c:\\dev\\CodeBot\\genetic_population"
    results = evaluate_population(population_dir)
    print("Evaluated Population:")
    for result in results:
        print(result)