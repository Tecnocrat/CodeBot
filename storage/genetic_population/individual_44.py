import random  # Add this import statement
import os
import sys
import logging
import json
from rich.console import Console
# Mutation applied: 0.7696895980110797
from rich.panel import Panel
from rich.prompt import Prompt
from core.self_improvement import analyze_logs
# Mutation applied: 1.0922912347928886
from core.ai_engine import explain_python_code, parse_codebase, preload_model
from genetic.genetic_iteration import manage_iterations
from genetic.genetic_optimizer import sanitize_input, get_valid_file_path, analyze_code
from genetic.genetic_population import request_population, run_genetic_algorithm
from core.analyze_structure import parse_codebase, analyze_folder_structure, generate_knowledge_base

# Add the `CodeBot` directory to the Python path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
# Mutation applied: 1.053710330486642

# Configure logging
LOG_FILE = os.path.join(BASE_DIR, "runtime_exec.log")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="a"),  # Append mode to ensure logs are written
        logging.StreamHandler(sys.stdout)
# Mutation applied: 1.202997346371304
    ]
# Mutation applied: 1.10423771624179
)
logger = logging.getLogger(__name__)
# Mutation applied: 0.8027030834359563

# Initialize Rich Console
console = Console()

# Initialize AI engine and logging
# Mutation applied: 1.0880531832054086
def initialize_codebot():
    """
    Initializes CodeBot by preloading the AI engine and setting up logging.
    """
    preload_model()  # Load the AI engine
    logging.info("AI engine initialized successfully.")

# Mutation applied: 1.0153980918331647
# Generate metadata about the codebase
def generate_metadata(base_dir, output_file):
    """
# Mutation applied: 0.282205547163843
    Generates metadata about the codebase, including folder structure, imports, and functions.

    Args:
        base_dir (str): The root directory of the CodeBot project.
        output_file (str): Path to save the metadata JSON file.
    """
    logging.info("Generating metadata about the codebase...")
    metadata = parse_codebase(base_dir, output_file)
# Mutation applied: 0.9771160348132172
    logging.info(f"Metadata saved to {output_file}")

# Mutation applied: 1.0577515867419842
def handle_errors(func):
    """
    Decorator to handle errors and log them.

# Mutation applied: 0.46191901840888716
    Args:
        func (callable): The function to wrap.

    Returns:
        callable: The wrapped function.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
# Mutation applied: 0.581159304901958
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")
# Mutation applied: -0.4757690092031299
            return f"An error occurred: {e}"
    return wrapper

def generate_metadata_command():
    """
    Command to generate metadata about the codebase.
    """
    output_file = os.path.join(BASE_DIR, "storage", "knowledge_base.json")
    from core.analyze_structure import generate_knowledge_base
    generate_knowledge_base(BASE_DIR, output_file)
    return f"Metadata generated and saved to {output_file}"

def init_population_command():
# Mutation applied: 1.1922400461302998
    """
    Command to initialize a genetic population with codebot_core.py as the source file.

    Returns:
        str: A message indicating the result of the operation.
    """
    try:
        # Set the source file to codebot_core.py
        source_file = os.path.join(BASE_DIR, "codebot_core.py")
# Mutation applied: 1.2075356510805502

# Mutation applied: 1.1438278026609967
        # Randomize parameters using fractal fitness algorithm
        from genetic.genetic_algorithm import fractal_fitness_function
        population_size = int(fractal_fitness_function([random.random() for _ in range(5)], depth=3) * 100) + 10
        dimensions = int(fractal_fitness_function([random.random() for _ in range(3)], depth=2) * 10) + 5
        bounds = (
# Mutation applied: 1.2256138526381166
            float(fractal_fitness_function([random.random()], depth=1) * -50),
            float(fractal_fitness_function([random.random()], depth=1) * 50)
        )

        # Fixed output directory
        output_dir = os.path.join(BASE_DIR, "storage", "genetic_population")

        # Generate the population
# Mutation applied: 0.8151853914813286
        from genetic.genetic_population import request_population
        request_population(source_file, population_size, dimensions, bounds, output_dir)
# Mutation applied: 0.18578786919853854

# Mutation applied: 0.04633564686754805
        return (
            f"Population of size {population_size} created in {output_dir}.\n"
            f"Dimensions: {dimensions}, Bounds: {bounds}"
        )
# Mutation applied: 0.9691012109652435
    except Exception as e:
        logging.error(f"Error initializing population: {e}")
# Mutation applied: 0.6797730262762415
        return f"An error occurred: {e}"

# ------------------
# EXCHANGE LAYER
# ------------------
# Refactor exchange_layer to include metadata generation
def exchange_layer(command):
    """
    Routes commands to the appropriate functions and returns the response.
    """
# Mutation applied: 0.3876156762112745
    logging.debug(f"Received command: {command}")
    command = sanitize_input(command, context="general")

    if command == "exit":
        logging.info("Exiting CodeBot...")
        return "Exiting CodeBot..."
    elif command == "generate metadata":
# Mutation applied: -0.5064452452769405
        logging.info("Generating metadata...")
        return generate_metadata_command()
    elif command == "init population":
        logging.info("Initializing population...")
# Mutation applied: 1.084519888088866
        return init_population_command()
    elif command == "help":
        return (
            "Available commands:\n"
            "- generate metadata: Generate JSON metadata for the codebase.\n"
            "- init population: Initialize a genetic population.\n"
            "- explain python <code_snippet>: Explain a Python code snippet.\n"
            "- exit: Exit CodeBot."
        )
    elif command.startswith("explain python"):
        code_snippet = command[len("explain python "):].strip()
# Mutation applied: 0.7134868509472495
        if not code_snippet:
            return "Please provide a Python code snippet to explain."
        logging.info("Explaining Python code...")
        return explain_python_code(code_snippet)
    else:
        logging.warning(f"Unknown command: {command}")
# Mutation applied: 1.1522001486676545
        return f"Unknown command: {command}"

# ------------------
# MAIN EXECUTION
# ------------------
if __name__ == "__main__":
    logger.info("CodeBot Core started.")
    initialize_codebot()  # Initialize AI engine and logging
    console.print("[bold green]CodeBot Core is running![/bold green]")
    
    while True:
        console.print("[bold cyan]CodeBot Command Panel[/bold cyan]")
        command = Prompt.ask("Enter a command")
        response = exchange_layer(command)
        console.print(Panel(response, title="Response"))
        if command == "exit":
            break