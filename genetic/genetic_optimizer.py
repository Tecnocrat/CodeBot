# filepath: c:\dev\CodeBot\self_improvement.py
import ast
import autopep8
import random
import shutil
import os
import requests
import hashlib
import subprocess
import time
import venv
import logging
import sys
import os
import logging

sys.path.append(os.path.abspath("C:\\dev\\CodeBot\\core"))
sys.path.append(os.path.abspath("C:\\dev\\CodeBot\\genetic"))
sys.path.append(os.path.abspath("C:\\dev\\CodeBot\\modules"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

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

def select_parents(population):
    population.sort(key=fitness_function)  # Sort by fitness (lower is better)
    return population[:2]  # Select top 2 individuals

def crossover(parent1, parent2, output_file):
    with open(parent1, 'r') as file1, open(parent2, 'r') as file2:
        code1 = file1.readlines()
        code2 = file2.readlines()
    midpoint = len(code1) // 2
    child_code = code1[:midpoint] + code2[midpoint:]
    with open(output_file, 'w') as file:
        file.writelines(child_code)

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

from genetic.genetic_population import request_population

def run_genetic_algorithm(source_file, generations, population_size, dimensions, bounds, output_dir):
    """
    Runs the genetic algorithm with a requested population.
    """
    logging.info("Starting genetic algorithm...")
    population = request_population(source_file, population_size, dimensions, bounds, output_dir)

    for generation in range(generations):
        logging.info(f"Generation {generation + 1}: Population size = {len(population)}")
        # Add logic for crossover, mutation, and selection
        # ...

    logging.info("Genetic algorithm completed.")

def handle_exception(logger, error_message, exception):
    """
    Logs an error and returns a user-friendly error message.

    Args:
        logger (logging.Logger): The logger instance to use for logging.
        error_message (str): The error message to log.
        exception (Exception): The exception to log.

    Returns:
        str: A user-friendly error message.
    """
    logger.error(f"{error_message}: {exception}")
    return error_message

def sanitize_input(user_input, context="general"):
    """
    Sanitizes user input to prevent security vulnerabilities and adapts to specific contexts.

    Args:
        user_input (str): The raw input provided by the user.
        context (str): The context in which the input is being sanitized. 
                       Options: "general", "code", "file_path", "html", "json".

    Returns:
        str: The sanitized input.
    """
    import html
    import json
    import re

    # Base sanitization: strip whitespace and escape HTML characters
    sanitized = user_input.strip()

    if context == "general":
        # Escape HTML characters to prevent injection attacks
        sanitized = html.escape(sanitized)

    elif context == "code":
        # Remove dangerous Python keywords or characters
        dangerous_keywords = ["exec", "eval", "__import__", "os.system", "subprocess"]
        for keyword in dangerous_keywords:
            sanitized = sanitized.replace(keyword, "[REDACTED]")
        # Remove any backticks or shell execution symbols
        sanitized = re.sub(r"[`$]", "", sanitized)

    elif context == "file_path":
        # Normalize file paths and remove dangerous characters
        sanitized = os.path.normpath(sanitized)
        sanitized = re.sub(r"[<>:\"|?*]", "", sanitized)  # Remove invalid file path characters

    elif context == "html":
        # Escape HTML characters and remove potentially dangerous tags
        sanitized = html.escape(sanitized)
        sanitized = re.sub(r"<(script|iframe|object|embed).*?>.*?</\1>", "", sanitized, flags=re.IGNORECASE)

    elif context == "json":
        # Ensure the input is valid JSON
        try:
            json.loads(sanitized)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON input.")

    else:
        raise ValueError(f"Unknown context: {context}")

    return sanitized

def get_valid_file_path(prompt="Enter file path: "):
    """
    Prompts the user for a file path and validates its existence.
    """
    while True:
        file_path = input(prompt).strip()
        if os.path.exists(file_path):
            return file_path
        print("Invalid file path. Please try again.")

# Example usage
if __name__ == "__main__":
    source_file = os.path.join(BASE_DIR, "CodeBot", "example.py")
    output_dir = os.path.join(BASE_DIR, "CodeBot", "genetic_population")
    best_code = run_genetic_algorithm(source_file, generations=5, initial_population_size=5, output_dir=output_dir)
    print(f"Best code is located at: {best_code}")