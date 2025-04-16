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
    Requests a population by generating individuals based on a source file.

    Args:
        source_file (str): Path to the source file to replicate.
        population_size (int): Number of individuals in the population.
        dimensions (int): Number of dimensions for the population's parameter space.
        bounds (tuple[float, float]): Bounds for each dimension.
        output_dir (str): Directory to save the generated population.

    Returns:
        list[str]: List of file paths for the generated population.
    """
    logging.info("Requesting population...")
    return generate_population(source_file, population_size, dimensions, bounds, output_dir)

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

def generate_population(source_file, population_size, dimensions, bounds, output_dir, start_index=0):
    """
    Generates a population of Python scripts by replicating and mutating a source file.
    """
    # Validate the source file
    if not os.path.exists(source_file):
        raise FileNotFoundError(f"Source file '{source_file}' does not exist.")

    os.makedirs(output_dir, exist_ok=True)
    for i in range(start_index, start_index + population_size):
        individual_file = os.path.join(output_dir, f"individual_{i}.py")
        if os.path.exists(individual_file):
            logging.warning(f"Skipping existing individual: {individual_file}")
            continue
        shutil.copy(source_file, individual_file)
        mutate_file(individual_file, dimensions, bounds)
        logging.info(f"Generated individual: {individual_file}")

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

def mutate_file(file_path, dimensions, bounds):
    """
    Applies random mutations to a Python file to create diversity in the population.

    Args:
        file_path (str): Path to the file to mutate.
        dimensions (int): Number of dimensions for mutation parameters.
        bounds (tuple[float, float]): Bounds for mutation values.
    """
    from genetic.genetic_algorithm import fractal_fitness_function

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Apply random mutations to the file content
    mutated_lines = []
    for line in lines:
        if random.random() < 0.1:  # 10% chance to mutate a line
            # Generate a random mutation value using the fractal fitness function
            mutation_value = fractal_fitness_function([random.random() for _ in range(dimensions)], depth=3)
            mutation_value = max(bounds[0], min(bounds[1], mutation_value))  # Clamp to bounds
            mutated_lines.append(f"# Mutation applied: {mutation_value}\n")
        mutated_lines.append(line)

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(mutated_lines)

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

def evaluate_population(population_dir, ai_engine, evaluation_mode="all", target_population=None):
    """
    Evaluates populations or individual files based on the selected mode.

    Args:
        population_dir (str): Directory containing the population files.
        ai_engine (callable): AI engine function to analyze execution logs.
        evaluation_mode (str): Mode of evaluation ("all", "single", "compare").
        target_population (str or list): Target population(s) or file(s) for evaluation.

    Returns:
        dict: A dictionary mapping each individual to its fitness score.
    """
    fitness_scores = {}
    evaluation_subfolder = os.path.join(population_dir, "evaluation_results")
    os.makedirs(evaluation_subfolder, exist_ok=True)

    # Determine what to evaluate
    if evaluation_mode == "all":
        populations = [os.path.join(population_dir, p) for p in os.listdir(population_dir) if os.path.isdir(os.path.join(population_dir, p))]
    elif evaluation_mode == "single" and target_population:
        target_path = os.path.join(population_dir, target_population)
        if os.path.isfile(target_path):
            populations = [target_path]  # Single file
        elif os.path.isdir(target_path):
            populations = [target_path]  # Single directory
        else:
            raise ValueError(f"Target population '{target_population}' does not exist.")
    elif evaluation_mode == "compare" and target_population:
        populations = [os.path.join(population_dir, p) for p in target_population]
    else:
        raise ValueError("Invalid evaluation mode or target population.")

    for population in populations:
        if os.path.isfile(population):  # Evaluate a single file
            fitness_scores.update(_evaluate_individual(population, evaluation_subfolder, ai_engine))
        elif os.path.isdir(population):  # Evaluate all individuals in a directory
            for individual in os.listdir(population):
                individual_path = os.path.join(population, individual)
                if individual.endswith(".py"):
                    fitness_scores.update(_evaluate_individual(individual_path, evaluation_subfolder, ai_engine))

    return fitness_scores


def _evaluate_individual(individual_path, evaluation_subfolder, ai_engine):
    """
    Evaluates a single individual by executing it and analyzing the logs.

    Args:
        individual_path (str): Path to the individual file.
        evaluation_subfolder (str): Path to the evaluation results folder.
        ai_engine (callable): AI engine function to analyze execution logs.

    Returns:
        dict: A dictionary mapping the individual to its fitness score.
    """
    fitness_scores = {}
    individual_name = os.path.basename(individual_path)

    # Create a log file for the individual's execution
    log_file = os.path.join(evaluation_subfolder, f"{individual_name}_exec.log")
    with open(log_file, "w") as log:
        try:
            # Execute the individual in a subprocess
            subprocess.run(
                ["python", individual_path],
                stdout=log,
                stderr=log,
                check=True,
                timeout=10  # Timeout to prevent infinite loops
            )
            logging.info(f"Executed {individual_name} successfully.")
        except subprocess.TimeoutExpired:
            logging.warning(f"Execution of {individual_name} timed out.")
            log.write("Execution timed out.\n")
        except subprocess.CalledProcessError as e:
            logging.error(f"Execution of {individual_name} failed: {e}")
            log.write(f"Execution failed: {e}\n")

    # Analyze the log file using the AI engine
    with open(log_file, "r") as log:
        log_content = log.read()
        fitness_score = ai_engine(log_content)
        fitness_scores[individual_name] = fitness_score
        logging.info(f"Fitness score for {individual_name}: {fitness_score}")

    # Generate README.md for AI ingestion
    readme_path = os.path.join(evaluation_subfolder, f"{individual_name}_README.md")
    with open(readme_path, "w") as readme:
        readme.write(f"# Evaluation Report for {individual_name}\n\n")
        readme.write(f"## Fitness Score: {fitness_score}\n\n")
        readme.write("### Execution Log:\n")
        readme.write(log_content)

    return fitness_scores

def list_population(population_dir):
    """
    Lists all individuals in the genetic population directory.

    Args:
        population_dir (str): Directory containing the population files.

    Returns:
        list[dict]: A list of individuals with their names and mutation numbers.
    """
    individuals = []
    for filename in os.listdir(population_dir):
        if filename.endswith(".py") and filename.startswith("individual_"):
            # Extract the numeric part of the filename for sorting
            try:
                mutation_number = int(filename.split("_")[1].split(".")[0])
            except (IndexError, ValueError):
                mutation_number = float("inf")  # Place non-standard files at the end
            individuals.append({"name": filename, "mutation_number": mutation_number})

    # Sort individuals numerically by mutation number
    individuals.sort(key=lambda x: x["mutation_number"])
    return individuals