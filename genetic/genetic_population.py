import os
import random
import shutil
import logging
import hashlib
import autopep8
import ast
import requests
import json
import time  # Fix: Import `time` for execution timing
import subprocess  # Fix: Import `subprocess` for running scripts
import venv  # Fix: Import `venv` for virtual environment creation

# Add the parent directory to sys.path
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import KNOWLEDGE_BASE_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Base directories
BASE_DIR = "c:\\dev"
CODEBOT_DIR = os.path.join(BASE_DIR, "CodeBot")
ADN_TRASH_CODE_DIR = os.path.join(CODEBOT_DIR, "adn_trash_code")
STORAGE_DIR = os.path.join(CODEBOT_DIR, "storage")

def request_population(source_file, population_size, dimensions, bounds, output_dir):
    """
    Generates a complex population based on the source file and various parameters.

    Args:
        source_file (str): Path to the source file to replicate and mutate.
        population_size (int): Number of individuals in the population.
        dimensions (int): Number of dimensions for each individual.
        bounds (tuple): Bounds for each dimension (min, max).
        output_dir (str): Directory to store the generated population.

    Returns:
        list: A list of paths to the generated individuals.
    """
    os.makedirs(output_dir, exist_ok=True)
    population = []

    for i in range(population_size):
        individual_path = os.path.join(output_dir, f"individual_{i}.py")
        shutil.copy(source_file, individual_path)

        # Apply mutations based on dimensions and bounds
        with open(individual_path, 'a') as f:
            for dim in range(dimensions):
                mutation = random.uniform(bounds[0], bounds[1])
                f.write(f"# Mutation {dim}: {mutation}\n")

        # Auto-format the individual for consistency
        with open(individual_path, 'r') as f:
            code = f.read()
        formatted_code = autopep8.fix_code(code)
        with open(individual_path, 'w') as f:
            f.write(formatted_code)

        population.append(individual_path)

    logging.info(f"Generated population of size {population_size} in {output_dir}")
    return population

def log_to_os(namespace, level, message):
    """
    Sends a log message to OS/main.py for centralized logging.
    """
    try:
        # Example: Replace with actual inter-process communication if needed
        requests.post(
            "http://localhost:5000/log",  # Assuming OS/main.py runs a logging server
            json={"namespace": namespace, "level": level, "message": message}
        )
    except Exception as e:
        print(f"Failed to send log to OS: {e}")

def analyze_code(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    tree = ast.parse(code)
    # Analyze the AST for improvements (e.g., unused imports, redundant code)
    # Add logic to identify areas for improvement
    return "Analysis complete. Suggestions: [...]"

def auto_format_code(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    formatted_code = autopep8.fix_code(code)
    with open(file_path, 'w') as file:
        file.write(formatted_code)
    return "Code formatted successfully."

def analyze_adn_trash_code():
    """
    Recursively analyzes the contents of adn_trash_code and returns insights.
    """
    insights = []
    for root, _, files in os.walk(ADN_TRASH_CODE_DIR):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    code = f.read()
                try:
                    ast.parse(code)  # Ensure the code is syntactically valid
                    insights.append((file_path, len(code)))  # Example: Add more analysis here
                except Exception as e:
                    print(f"Error analyzing {file_path}: {e}")
    return insights

def ingest_knowledge(file_path):
    """
    Ingests external knowledge into the knowledge_base.
    """
    target_path = os.path.join(KNOWLEDGE_BASE_DIR, os.path.basename(file_path))
    shutil.copy(file_path, target_path)
    print(f"Ingested knowledge from {file_path} to {target_path}")

def generate_population(source_file, population_size, output_dir):
    """
    Generates the initial population by copying the source file.

    Args:
        source_file (str): Path to the source file.
        population_size (int): Number of individuals in the population.
        output_dir (str): Directory to store the generated population.

    Returns:
        list: A list of paths to the generated individuals.
    """
    os.makedirs(output_dir, exist_ok=True)
    population = []

    for i in range(population_size):
        individual_path = os.path.join(output_dir, f"individual_{i}.py")
        shutil.copy(source_file, individual_path)

        # Apply mutations
        with open(individual_path, 'a') as f:
            mutation = random.uniform(-1, 1)  # Example mutation
            f.write(f"# Mutation: {mutation}\n")

        # Auto-format the individual for consistency
        with open(individual_path, 'r') as f:
            code = f.read()
        formatted_code = autopep8.fix_code(code)
        with open(individual_path, 'w') as f:
            f.write(formatted_code)

        population.append(individual_path)

    logging.info(f"Generated population of size {population_size} in {output_dir}")
    return population

def deduplicate_population(output_dir):
    """
    Removes duplicate files in the genetic population folder by comparing file hashes.
    """
    file_hashes = {}
    for file_name in os.listdir(output_dir):
        file_path = os.path.join(output_dir, file_name)
        if os.path.isfile(file_path):
            with open(file_path, "rb") as f:
                file_hash = hash(f.read())
            if file_hash in file_hashes:
                os.remove(file_path)
                logging.info(f"Removed duplicate file: {file_path}")
            else:
                file_hashes[file_hash] = file_path

def select_parents(population, fitness_function):
    """
    Selects the top two individuals from the population based on fitness.

    Args:
        population (list): List of file paths representing the population.
        fitness_function (callable): Function to evaluate the fitness of an individual.

    Returns:
        list: The top two individuals.
    """
    population.sort(key=fitness_function)  # Sort by fitness (lower is better)
    return population[:2]  # Select top 2 individuals

def crossover(parent1, parent2, output_file):
    """
    Combines two parent files to create a child file.
    """
    with open(parent1, "r") as file1, open(parent2, "r") as file2:
        code1 = file1.read()
        code2 = file2.read()
    midpoint = len(code1) // 2
    child_code = code1[:midpoint] + code2[midpoint:]
    with open(output_file, "w") as file:
        file.write(child_code)
    logging.info(f"Created child file: {output_file}")

def mutate(file_path):
    """
    Applies random changes to the code in the file.
    """
    with open(file_path, "r") as file:
        code = file.read()
    mutated_code = code.replace(" ", "  ")  # Example mutation: Add extra spaces
    with open(file_path, "w") as file:
        file.write(mutated_code)
    logging.info(f"Mutated file: {file_path}")

def create_virtual_environment(env_dir):
    """
    Creates a virtual environment in the specified directory.
    """
    venv.create(env_dir, with_pip=True)
    logging.info(f"Virtual environment created at {env_dir}")

def execute_in_virtual_environment(script_path, env_dir):
    """
    Executes a Python script in a virtual environment and logs execution time.
    """
    start_time = time.time()
    try:
        python_executable = os.path.join(env_dir, "Scripts", "python") if os.name == "nt" else os.path.join(env_dir, "bin", "python")
        result = subprocess.run([python_executable, script_path], capture_output=True, text=True)
        execution_time = time.time() - start_time
        logging.info(f"Executed {script_path} in {execution_time:.2f} seconds")
        if result.returncode == 0:
            logging.info(f"Output: {result.stdout}")
        else:
            logging.error(f"Error: {result.stderr}")
    except Exception as e:
        logging.error(f"Failed to execute {script_path}: {e}")

def run_genetic_algorithm(source_file, generations, initial_population_size, output_dir):
    """
    Runs the genetic algorithm with optimized population management and logging.
    """
    logging.info("Starting genetic algorithm...")
    output_dir = os.path.join(BASE_DIR, output_dir)
    os.makedirs(output_dir, exist_ok=True)
    population = generate_population(source_file, initial_population_size, output_dir)
    for generation in range(generations):
        logging.info(f"Generation {generation + 1}: Population size = {len(population)}")
        parents = select_parents(population)
        new_population = []
        # Limit population growth to avoid resource exhaustion
        for i in range(min(len(population), 10)):  # Limit to 10 children per generation
            child_path = os.path.join(output_dir, f"child_{generation}_{i}.py")
            crossover(parents[0], parents[1], child_path)
            mutate(child_path)
            new_population.append(child_path)
        # Execute and evaluate new population
        for child in new_population:
            env_dir = os.path.join(output_dir, f"env_{generation}_{i}")
            create_virtual_environment(env_dir)
            execute_in_virtual_environment(child, env_dir)
        population = new_population
    logging.info("Genetic algorithm completed.")