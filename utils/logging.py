import os
import random
import logging

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def fitness_function(file_path):
    """
    A simple fitness function to evaluate code quality.
    For example, shorter files with fewer lines are considered better.
    """
    with open(file_path, "r") as f:
        lines = f.readlines()
    return -len(lines)  # Negative because shorter is better

def mutate_file(file_path):    
    """
    Randomly removes lines from a file to simulate mutation.
    """
    with open(file_path, "r") as f:
        lines = f.readlines()
    if len(lines) > 1:
        lines.pop(random.randint(0, len(lines) - 1))
    with open(file_path, "w") as f:
        f.writelines(lines)

def genetic_algorithm(base_dir, generations=10, population_size=5):
    """
    Runs a genetic algorithm to optimize the codebase.
    """
    files = [os.path.join(base_dir, f) for f in os.listdir(base_dir) if f.endswith(".py")]
    if not files:
        raise ValueError(f"No Python files found in {base_dir}. Ensure the directory contains valid `.py` files.")
    
    population = random.sample(files, min(population_size, len(files)))

    for generation in range(generations):
        print(f"Generation {generation + 1}")
        population.sort(key=fitness_function)
        best_file = population[0]
        print(f"Best file: {best_file} (Fitness: {fitness_function(best_file)})")
        # Mutate the worst-performing files
        for file in population[1:]:
            mutate_file(file)
    return best_file

def analyze_logs(log_file):
    if not os.path.exists(log_file):
        logger.error(f"Log file not found: {log_file}")
        return
    
    logger.info(f"Analyzing logs: {log_file}")
    with open(log_file, "r") as file:
        for line in file:
            print(line.strip())

if __name__ == "__main__":
    base_dir = "c:\\dev\\CodeBot\\optimized_code"
    best_file = genetic_algorithm(base_dir)
    print(f"Best optimized file: {best_file}")

    log_file = "c:\\dev\\CodeBot\\logs\\codebot_genetic.log"
    analyze_logs(log_file)