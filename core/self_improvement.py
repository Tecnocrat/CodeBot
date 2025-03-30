# filepath: c:\dev\CodeBot\self_improvement.py
import os
import ast
import autopep8
import random
import shutil
import hashlib
import subprocess
import time
import venv
import requests
from core.ai_engine import explain_python_code  # Example of cross-module import
import sys
import os
sys.path.append(os.path.abspath("C:\\dev\\CodeBot\\modules"))
from genetic.genetic_optimizer import get_valid_file_path  # Updated import

# Base directory for all operations
BASE_DIR = "c:\\dev"
CODEBOT_DIR = os.path.join(BASE_DIR, "CodeBot")
ADN_TRASH_CODE_DIR = os.path.join(CODEBOT_DIR, "adn_trash_code")
KNOWLEDGE_BASE_DIR = os.path.join(CODEBOT_DIR, "knowledge_base")  # Updated path

# Replace logging calls with requests to OS/main.py
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

# Fitness function to evaluate code quality
def fitness_function(file_path):
    try:
        with open(file_path, 'r') as file:
            code = file.read()
        ast.parse(code)  # Check if the code is syntactically valid
        fitness = len(code)  # Example: shorter code is better (adjust as needed)
        log_to_os("codebot", "info", f"Evaluated fitness for {file_path}: {fitness}")
        return fitness
    except Exception as e:
        log_to_os("codebot", "error", f"Error evaluating fitness for {file_path}: {e}")
        return float('inf')  # Invalid code gets the worst score

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
    os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)
    shutil.copy(file_path, target_path)
    print(f"Ingested knowledge from {file_path} to {target_path}")

# Generate initial population (copies of the original code)
def generate_population(source_file, population_size, output_dir):
    """
    Generates the initial population by copying the source file.
    """
    output_dir = os.path.join(ADN_TRASH_CODE_DIR, output_dir)
    os.makedirs(output_dir, exist_ok=True)
    population = []
    insights = analyze_adn_trash_code()  # Use insights to guide randomization
    for i in range(population_size):
        individual_path = os.path.join(output_dir, f"individual_{i}.py")
        shutil.copy(source_file, individual_path)
        # Apply guided randomization based on insights
        if insights:
            with open(individual_path, 'a') as f:
                f.write(f"# Insight-based mutation: {random.choice(insights)}\n")
        population.append(individual_path)
    return population

def deduplicate_population(output_dir):
    """
    Removes duplicate files in the genetic population folder by comparing file hashes.
    """
    output_dir = os.path.join(BASE_DIR, output_dir)  # Ensure output_dir is within BASE_DIR
    file_hashes = {}
    for file_name in os.listdir(output_dir):
        file_path = os.path.join(output_dir, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                file_hash = hashlib.md5(file.read()).hexdigest()
            if file_hash in file_hashes:
                os.remove(file_path)  # Delete duplicate file
            else:
                file_hashes[file_hash] = file_name

# Select parents based on fitness
def select_parents(population):
    population.sort(key=fitness_function)  # Sort by fitness (lower is better)
    return population[:2]  # Select top 2 individuals

# Crossover: Combine two parents to create a child
def crossover(parent1, parent2, output_file):
    with open(parent1, 'r') as file1, open(parent2, 'r') as file2:
        code1 = file1.readlines()
        code2 = file2.readlines()
    midpoint = len(code1) // 2
    child_code = code1[:midpoint] + code2[midpoint:]
    with open(output_file, 'w') as file:
        file.writelines(child_code)

# Mutate: Apply random changes to the code
def mutate(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    mutated_code = autopep8.fix_code(code)  # Example: auto-format as mutation
    with open(file_path, 'w') as file:
        file.write(mutated_code)

def create_virtual_environment(env_dir):
    """
    Creates a virtual environment in the specified directory.
    """
    venv.create(env_dir, with_pip=True)
    log_to_os("codebot", "info", f"Virtual environment created at {env_dir}")

def execute_in_virtual_environment(script_path, env_dir):
    """
    Executes a Python script in a virtual environment and logs execution time.
    """
    start_time = time.time()
    try:
        python_executable = os.path.join(env_dir, "Scripts", "python") if os.name == "nt" else os.path.join(env_dir, "bin", "python")
        result = subprocess.run([python_executable, script_path], capture_output=True, text=True)
        execution_time = time.time() - start_time
        log_to_os("codebot", "info", f"Executed {script_path} in {execution_time:.2f} seconds")
        if result.returncode == 0:
            log_to_os("codebot", "info", f"Output: {result.stdout}")
        else:
            log_to_os("codebot", "error", f"Error: {result.stderr}")
    except Exception as e:
        log_to_os("codebot", "error", f"Failed to execute {script_path}: {e}")

def analyze_logs(log_file_path):
    """
    Analyzes the given log file and returns a summary.

    Args:
        log_file_path (str): The path to the log file.

    Returns:
        str: A summary of the log analysis.
    """
    try:
        if not os.path.exists(log_file_path):
            return f"Log file not found: {log_file_path}"

        with open(log_file_path, 'r') as log_file:
            logs = log_file.readlines()

        # Example analysis: Count the number of errors, warnings, and info messages
        error_count = sum(1 for line in logs if "ERROR" in line)
        warning_count = sum(1 for line in logs if "WARNING" in line)
        info_count = sum(1 for line in logs if "INFO" in line)

        # Return a summary of the analysis
        summary = (
            f"Log Analysis Summary:\n"
            f"Total lines: {len(logs)}\n"
            f"Errors: {error_count}\n"
            f"Warnings: {warning_count}\n"
            f"Info messages: {info_count}\n"
        )
        return summary
    except Exception as e:
        return f"An error occurred during log analysis: {e}"

# Run the genetic algorithm
def run_genetic_algorithm(source_file, generations, initial_population_size, output_dir):
    start_time = time.time()
    try:
        output_dir = os.path.join(BASE_DIR, output_dir)  # Ensure output_dir is within BASE_DIR
        os.makedirs(os.path.join(BASE_DIR, "CodeBot", "genetic_population"), exist_ok=True)
        log_to_os("codebot", "info", "Starting genetic algorithm...")
        population_size = initial_population_size
        population = generate_population(source_file, population_size, output_dir)

        for generation in range(generations):
            log_to_os("codebot", "info", f"Generation {generation + 1} started.")
            parents = select_parents(population)
            new_population = []

            # Exponential growth: Each individual produces two children
            for i in range(len(population)):
                child_path = os.path.join(output_dir, f"child_{generation}_{i}.py")
                crossover(parents[0], parents[1], child_path)
                mutate(child_path)
                new_population.append(child_path)

                # Create a virtual environment for the child and execute it
                env_dir = os.path.join(output_dir, f"env_{generation}_{i}")
                create_virtual_environment(env_dir)
                execute_in_virtual_environment(child_path, env_dir)

            # Add new population to the existing one
            population.extend(new_population)

            # Deduplicate population
            deduplicate_population(output_dir)
            log_to_os("codebot", "info", f"Generation {generation + 1} completed.")

            population_size *= 2  # Double the population size for the next generation

        # Return the best individual
        best_individual = population[0]
        log_to_os("codebot", "info", f"Best individual: {best_individual} with fitness {fitness_function(best_individual)}")
        log_to_os("codebot", "info", f"Genetic algorithm completed in {time.time() - start_time:.2f} seconds.")
        return best_individual
    except Exception as e:
        log_to_os("codebot", "error", f"Error during genetic algorithm: {e}")
        raise

# Example usage
def analyze_code_with_path():
    file_path = get_valid_file_path("Enter the path of the code file to analyze: ")
    return analyze_code(file_path)

if __name__ == "__main__":
    source_file = os.path.join(BASE_DIR, "CodeBot", "example.py")
    output_dir = os.path.join(BASE_DIR, "CodeBot", "genetic_population")
    best_code = run_genetic_algorithm(source_file, generations=5, initial_population_size=5, output_dir=output_dir)
    print(f"Best code is located at: {best_code}")