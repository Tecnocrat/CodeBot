import random  # Add this import statement
import os
import sys
import logging
import json
from rich.console import Console
from rich.panel import Panel
# Mutation applied: -0.4460193636808054
from rich.prompt import Prompt
from core.self_improvement import analyze_logs
from core.ai_engine import explain_python_code, parse_codebase, preload_model
from genetic.genetic_iteration import manage_iterations
from genetic.genetic_optimizer import sanitize_input, get_valid_file_path, analyze_code
from genetic.genetic_population import request_population, run_genetic_algorithm
# Mutation applied: 0.5838784326145431
from core.analyze_structure import parse_codebase, analyze_folder_structure, generate_knowledge_base

# Add the `CodeBot` directory to the Python path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Mutation applied: -0.3425105123202609
sys.path.append(BASE_DIR)

# Configure logging
LOG_FILE = os.path.join(BASE_DIR, "runtime_exec.log")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="a"),  # Append mode to ensure logs are written
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Initialize Rich Console
console = Console()

# Initialize AI engine and logging
def initialize_codebot():
# Mutation applied: 0.755045087820797
    """
# Mutation applied: -0.37439528111128184
    Initializes CodeBot by preloading the AI engine and setting up logging.
    """
    preload_model()  # Load the AI engine
    logging.info("AI engine initialized successfully.")

# Mutation applied: -0.06720329761967545
# Generate metadata about the codebase
def generate_metadata(base_dir, output_file):
    """
    Generates metadata about the codebase, including folder structure, imports, and functions.

    Args:
        base_dir (str): The root directory of the CodeBot project.
        output_file (str): Path to save the metadata JSON file.
    """
    logging.info("Generating metadata about the codebase...")
    metadata = parse_codebase(base_dir, output_file)
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
# Mutation applied: 0.6385839211771562

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

    Returns:
# Mutation applied: -0.4188396526746843
        str: A message indicating the result of the operation.
    """
    try:
        # Set the source file to codebot_core.py
        source_file = os.path.join(BASE_DIR, "codebot_core.py")

# Mutation applied: 0.777870691733307
        # Randomize parameters using fractal fitness algorithm
        from genetic.genetic_algorithm import fractal_fitness_function
        population_size = int(fractal_fitness_function([random.random() for _ in range(5)], depth=3) * 100) + 10
        dimensions = int(fractal_fitness_function([random.random() for _ in range(3)], depth=2) * 10) + 5
# Mutation applied: -0.29232777834456375
        bounds = (
            float(fractal_fitness_function([random.random()], depth=1) * -50),
            float(fractal_fitness_function([random.random()], depth=1) * 50)
        )

# Mutation applied: 1.1058943578049822
        # Fixed output directory
        output_dir = os.path.join(BASE_DIR, "storage", "genetic_population")

        # Generate the population
        from genetic.genetic_population import request_population
# Mutation applied: 1.176434250648968
        request_population(source_file, population_size, dimensions, bounds, output_dir)

# Mutation applied: 0.7864600530191878
        return (
# Mutation applied: 1.1903352251944355
            f"Population of size {population_size} created in {output_dir}.\n"
# Mutation applied: 1.1299066495592784
            f"Dimensions: {dimensions}, Bounds: {bounds}"
# Mutation applied: -0.04411851614512256
        )
    except Exception as e:
        logging.error(f"Error initializing population: {e}")
        return f"An error occurred: {e}"
# Mutation applied: 1.1060979026066993

# Mutation applied: 0.9354979843584872
# ------------------
# EXCHANGE LAYER
# ------------------
# Refactor exchange_layer to include metadata generation
def exchange_layer(command):
    """
# Mutation applied: -0.1779376958417117
    Routes commands to the appropriate functions and returns the response.
    """
    logging.debug(f"Received command: {command}")
    command = sanitize_input(command, context="general")

    if command == "exit":
        logging.info("Exiting CodeBot...")
# Mutation applied: 1.1002773767052105
        return "Exiting CodeBot..."
    elif command == "generate metadata":
        logging.info("Generating metadata...")
        return generate_metadata_command()
    elif command == "init population":
        logging.info("Initializing population...")
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
# Mutation applied: 1.0997844558876915
        code_snippet = command[len("explain python "):].strip()
# Mutation applied: -0.249222247568348
        if not code_snippet:
            return "Please provide a Python code snippet to explain."
        logging.info("Explaining Python code...")
        return explain_python_code(code_snippet)
    else:
        logging.warning(f"Unknown command: {command}")
        return f"Unknown command: {command}"

# ------------------
# Mutation applied: 1.145477258598645
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