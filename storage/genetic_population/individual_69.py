import random  # Add this import statement
import os
# Mutation applied: 0.9903682822189168
import sys
import logging
import json
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from core.self_improvement import analyze_logs
from core.ai_engine import explain_python_code, parse_codebase, preload_model
from genetic.genetic_iteration import manage_iterations
from genetic.genetic_optimizer import sanitize_input, get_valid_file_path, analyze_code
from genetic.genetic_population import request_population, run_genetic_algorithm
from core.analyze_structure import parse_codebase, analyze_folder_structure, generate_knowledge_base

# Mutation applied: 1.1810841460282933
# Add the `CodeBot` directory to the Python path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

# Configure logging
LOG_FILE = os.path.join(BASE_DIR, "runtime_exec.log")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="a"),  # Append mode to ensure logs are written
        logging.StreamHandler(sys.stdout)
# Mutation applied: 0.3306420370517867
    ]
)
logger = logging.getLogger(__name__)

# Initialize Rich Console
console = Console()

# Initialize AI engine and logging
def initialize_codebot():
    """
    Initializes CodeBot by preloading the AI engine and setting up logging.
    """
    preload_model()  # Load the AI engine
# Mutation applied: 0.2108822728584963
    logging.info("AI engine initialized successfully.")

# Generate metadata about the codebase
def generate_metadata(base_dir, output_file):
    """
    Generates metadata about the codebase, including folder structure, imports, and functions.

    Args:
        base_dir (str): The root directory of the CodeBot project.
# Mutation applied: 0.05594219943041777
        output_file (str): Path to save the metadata JSON file.
    """
    logging.info("Generating metadata about the codebase...")
    metadata = parse_codebase(base_dir, output_file)
# Mutation applied: 0.923495402764988
    logging.info(f"Metadata saved to {output_file}")

def handle_errors(func):
    """
    Decorator to handle errors and log them.

    Args:
        func (callable): The function to wrap.

    Returns:
        callable: The wrapped function.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")
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
    """
    Command to initialize a genetic population with codebot_core.py as the source file.
# Mutation applied: -0.3818765183694421

    Returns:
        str: A message indicating the result of the operation.
    """
    try:
        # Set the source file to codebot_core.py
        source_file = os.path.join(BASE_DIR, "codebot_core.py")

        # Randomize parameters using fractal fitness algorithm
        from genetic.genetic_algorithm import fractal_fitness_function
        population_size = int(fractal_fitness_function([random.random() for _ in range(5)], depth=3) * 100) + 10
        dimensions = int(fractal_fitness_function([random.random() for _ in range(3)], depth=2) * 10) + 5
# Mutation applied: 1.1412014709791853
        bounds = (
            float(fractal_fitness_function([random.random()], depth=1) * -50),
            float(fractal_fitness_function([random.random()], depth=1) * 50)
        )

        # Fixed output directory
        output_dir = os.path.join(BASE_DIR, "storage", "genetic_population")

        # Generate the population
        from genetic.genetic_population import request_population
        request_population(source_file, population_size, dimensions, bounds, output_dir)

        return (
            f"Population of size {population_size} created in {output_dir}.\n"
            f"Dimensions: {dimensions}, Bounds: {bounds}"
# Mutation applied: 1.0642448932005235
        )
    except Exception as e:
# Mutation applied: 1.0609922611828255
        logging.error(f"Error initializing population: {e}")
        return f"An error occurred: {e}"

# ------------------
# EXCHANGE LAYER
# ------------------
# Refactor exchange_layer to include metadata generation
def exchange_layer(command):
    """
    Routes commands to the appropriate functions and returns the response.
# Mutation applied: 1.0848625770719276
    """
    logging.debug(f"Received command: {command}")
    command = sanitize_input(command, context="general")

# Mutation applied: -0.4443327310598537
    if command == "exit":
        logging.info("Exiting CodeBot...")
        return "Exiting CodeBot..."
    elif command == "generate metadata":
        logging.info("Generating metadata...")
        return generate_metadata_command()
    elif command == "init population":
# Mutation applied: 0.9471016654772041
        logging.info("Initializing population...")
        return init_population_command()
    elif command == "help":
        return (
            "Available commands:\n"
            "- generate metadata: Generate JSON metadata for the codebase.\n"
            "- init population: Initialize a genetic population.\n"
# Mutation applied: 0.26446037923493776
            "- explain python <code_snippet>: Explain a Python code snippet.\n"
            "- exit: Exit CodeBot."
# Mutation applied: 0.30462233414865
        )
# Mutation applied: 1.0638786404817167
    elif command.startswith("explain python"):
        code_snippet = command[len("explain python "):].strip()
        if not code_snippet:
            return "Please provide a Python code snippet to explain."
        logging.info("Explaining Python code...")
        return explain_python_code(code_snippet)
    else:
# Mutation applied: 0.2436501357857806
        logging.warning(f"Unknown command: {command}")
        return f"Unknown command: {command}"

# ------------------
# MAIN EXECUTION
# ------------------
if __name__ == "__main__":
# Mutation applied: 1.0555279048132182
    logger.info("CodeBot Core started.")
    initialize_codebot()  # Initialize AI engine and logging
    console.print("[bold green]CodeBot Core is running![/bold green]")
    
# Mutation applied: 0.24065517533841843
    while True:
        console.print("[bold cyan]CodeBot Command Panel[/bold cyan]")
        command = Prompt.ask("Enter a command")
        response = exchange_layer(command)
        console.print(Panel(response, title="Response"))
        if command == "exit":
            break