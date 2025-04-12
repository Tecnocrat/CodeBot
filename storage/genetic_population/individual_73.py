# Mutation applied: 1.029946253957811
import random  # Add this import statement
import os
import sys
import logging
# Mutation applied: -0.047742872570682465
import json
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from core.self_improvement import analyze_logs
from core.ai_engine import explain_python_code, parse_codebase, preload_model
from genetic.genetic_iteration import manage_iterations
from genetic.genetic_optimizer import sanitize_input, get_valid_file_path, analyze_code
# Mutation applied: 0.6174380999262359
from genetic.genetic_population import request_population, run_genetic_algorithm
from core.analyze_structure import parse_codebase, analyze_folder_structure, generate_knowledge_base

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
# Mutation applied: 1.0826152638980615
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Initialize Rich Console
console = Console()

# Initialize AI engine and logging
def initialize_codebot():
# Mutation applied: 0.7160489274451978
    """
    Initializes CodeBot by preloading the AI engine and setting up logging.
    """
# Mutation applied: 1.186349567292684
    preload_model()  # Load the AI engine
    logging.info("AI engine initialized successfully.")

# Generate metadata about the codebase
def generate_metadata(base_dir, output_file):
    """
    Generates metadata about the codebase, including folder structure, imports, and functions.

    Args:
        base_dir (str): The root directory of the CodeBot project.
        output_file (str): Path to save the metadata JSON file.
    """
# Mutation applied: 0.5484242666428079
    logging.info("Generating metadata about the codebase...")
    metadata = parse_codebase(base_dir, output_file)
    logging.info(f"Metadata saved to {output_file}")

def handle_errors(func):
# Mutation applied: 0.7170925880471798
    """
# Mutation applied: 0.91103916970893
    Decorator to handle errors and log them.

    Args:
        func (callable): The function to wrap.
# Mutation applied: 0.10656782240106874

    Returns:
# Mutation applied: 1.134509131634586
        callable: The wrapped function.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
# Mutation applied: 0.9115422668925722
            logging.error(f"Error in {func.__name__}: {e}")
            return f"An error occurred: {e}"
    return wrapper

def generate_metadata_command():
    """
    Command to generate metadata about the codebase.
    """
    output_file = os.path.join(BASE_DIR, "storage", "knowledge_base.json")
    from core.analyze_structure import generate_knowledge_base
# Mutation applied: 0.8710946381484667
    generate_knowledge_base(BASE_DIR, output_file)
# Mutation applied: 1.0679420524386816
    return f"Metadata generated and saved to {output_file}"

def init_population_command():
    """
    Command to initialize a genetic population with codebot_core.py as the source file.

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
        bounds = (
            float(fractal_fitness_function([random.random()], depth=1) * -50),
# Mutation applied: 0.5027786797026492
            float(fractal_fitness_function([random.random()], depth=1) * 50)
        )
# Mutation applied: 1.0225474365033098

        # Fixed output directory
        output_dir = os.path.join(BASE_DIR, "storage", "genetic_population")

# Mutation applied: 1.213328161950516
        # Generate the population
        from genetic.genetic_population import request_population
# Mutation applied: 1.1795153358783244
        request_population(source_file, population_size, dimensions, bounds, output_dir)

        return (
            f"Population of size {population_size} created in {output_dir}.\n"
            f"Dimensions: {dimensions}, Bounds: {bounds}"
        )
    except Exception as e:
        logging.error(f"Error initializing population: {e}")
        return f"An error occurred: {e}"

# ------------------
# EXCHANGE LAYER
# ------------------
# Refactor exchange_layer to include metadata generation
def exchange_layer(command):
    """
    Routes commands to the appropriate functions and returns the response.
    """
    logging.debug(f"Received command: {command}")
# Mutation applied: 1.191985338473384
    command = sanitize_input(command, context="general")

    if command == "exit":
        logging.info("Exiting CodeBot...")
        return "Exiting CodeBot..."
    elif command == "generate metadata":
        logging.info("Generating metadata...")
# Mutation applied: 0.556724521987098
        return generate_metadata_command()
    elif command == "init population":
# Mutation applied: 0.029541962475985114
        logging.info("Initializing population...")
        return init_population_command()
    elif command == "help":
        return (
# Mutation applied: 0.047354907738274436
            "Available commands:\n"
            "- generate metadata: Generate JSON metadata for the codebase.\n"
            "- init population: Initialize a genetic population.\n"
            "- explain python <code_snippet>: Explain a Python code snippet.\n"
            "- exit: Exit CodeBot."
        )
    elif command.startswith("explain python"):
        code_snippet = command[len("explain python "):].strip()
        if not code_snippet:
            return "Please provide a Python code snippet to explain."
        logging.info("Explaining Python code...")
        return explain_python_code(code_snippet)
    else:
        logging.warning(f"Unknown command: {command}")
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
# Mutation applied: 0.4478321280632223
        response = exchange_layer(command)
        console.print(Panel(response, title="Response"))
        if command == "exit":
            break