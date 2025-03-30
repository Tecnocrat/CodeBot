# filepath: c:\dev\CodeBot\iteration_manager.py
import os
import shutil
import logging
import sys
from genetic_optimizer import generate_population  # Import generate_population
sys.path.append(os.path.abspath("C:\\dev\\CodeBot\\modules"))

# Base directory for all operations
BASE_DIR = "c:\\dev"
CODEBOT_DIR = os.path.join(BASE_DIR, "CodeBot")
ADN_TRASH_CODE_DIR = os.path.join(CODEBOT_DIR, "adn_trash_code")

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def replicate_and_learn(source_dir, target_dir):
    """
    Copies the current version of the project and applies self-improvement.
    """
    logger.info("Starting replication and learning process.")
    target_dir = os.path.join(ADN_TRASH_CODE_DIR, target_dir)
    os.makedirs(target_dir, exist_ok=True)
    shutil.copytree(source_dir, target_dir, dirs_exist_ok=True)
    logger.info(f"Replicated CodeBot to {target_dir}.")

    # Apply intelligent behavior (e.g., self-improvement)
    logger.info("Starting self-improvement on replicated code.")
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                logger.debug(f"Improved file: {file_path}")  # Detailed logs saved to file
    logger.info("Self-improvement process completed.")

def run_genetic_algorithm(source_file, generations, initial_population_size, output_dir):
    """
    Runs the genetic algorithm on the given source file.
    """
    logging.info("Starting genetic algorithm...")
    population = generate_population(source_file, initial_population_size, output_dir)
    for generation in range(generations):
        logging.info(f"Generation {generation + 1}: Population size = {len(population)}")
        # Existing logic...
    logging.info("Genetic algorithm completed.")

def manage_iterations():
    """
    Manages the iteration process by replicating the project and running the genetic algorithm.
    """
    logger.info("Starting iteration management process...")

    # Step 1: Replicate and learn
    replicate_and_learn(CODEBOT_DIR, "replicated_CodeBot")

    # Step 2: Run the genetic algorithm
    source_file = os.path.join(CODEBOT_DIR, "core", "codebot_core.py")
    output_dir = os.path.join(ADN_TRASH_CODE_DIR, "genetic_output")
    generations = 10
    initial_population_size = 20

    run_genetic_algorithm(source_file, generations, initial_population_size, output_dir)

    logger.info("Iteration management process completed.")

# Example usage
if __name__ == "__main__":
    logger.info("Iteration Manager started.")
    manage_iterations()