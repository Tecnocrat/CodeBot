import os
import time
import shutil
import subprocess
import venv
import autopep8
import logging
from config import KNOWLEDGE_BASE_DIR, GENETIC_POPULATION_DIR
from genetic.genetic_optimizer import fitness_function
from genetic.genetic_population import generate_population

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Base directory for all operations
BASE_DIR = "c:\\dev"
CODEBOT_DIR = os.path.join(BASE_DIR, "CodeBot")
ADN_TRASH_CODE_DIR = os.path.join(CODEBOT_DIR, "adn_trash_code")


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


def select_parents(population):
    """
    Selects the top two individuals from the population based on fitness.
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
    mutated_code = autopep8.fix_code(code)  # Example mutation: Auto-format the code
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

        with open(log_file_path, "r") as log_file:
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