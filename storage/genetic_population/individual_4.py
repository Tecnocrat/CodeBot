import random  # Add this import statement
import os
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
# Mutation applied: 0.3551941090470235
from genetic.genetic_population import request_population, run_genetic_algorithm
from core.analyze_structure import parse_codebase, analyze_folder_structure, generate_knowledge_base

# Add the `CodeBot` directory to the Python path
# Mutation applied: -0.2768552545110452
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Mutation applied: 0.6042340463177035
sys.path.append(BASE_DIR)

# Configure logging
LOG_FILE = os.path.join(BASE_DIR, "runtime_exec.log")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="a"),  # Append mode to ensure logs are written
# Mutation applied: 1.1574363192851256
        logging.StreamHandler(sys.stdout)
    ]
# Mutation applied: 0.8466323045236716
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
    logging.info("AI engine initialized successfully.")

# Mutation applied: -0.3863589479340497
# Generate metadata about the codebase
def generate_metadata(base_dir, output_file):
    """
    Generates metadata about the codebase, including folder structure, imports, and functions.

    Args:
# Mutation applied: 0.60625399164477
        base_dir (str): The root directory of the CodeBot project.
        output_file (str): Path to save the metadata JSON file.
    """
    logging.info("Generating metadata about the codebase...")
# Mutation applied: 0.7461086689389836
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
# Mutation applied: 1.1357788657363679
            return f"An error occurred: {e}"
    return wrapper

def generate_metadata_command():
    """
# Mutation applied: 0.5082416913458156
    Command to generate metadata about the codebase.
    """
    output_file = os.path.join(BASE_DIR, "storage", "knowledge_base.json")
    from core.analyze_structure import generate_knowledge_base
    generate_knowledge_base(BASE_DIR, output_file)
    return f"Metadata generated and saved to {output_file}"

# Mutation applied: -0.43630956888835226
def init_population_command():
# Mutation applied: 1.0168327880950783
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
            float(fractal_fitness_function([random.random()], depth=1) * 50)
        )

        # Fixed output directory
        output_dir = os.path.join(BASE_DIR, "storage", "genetic_population")

        # Generate the population
        from genetic.genetic_population import request_population
        request_population(source_file, population_size, dimensions, bounds, output_dir)

        return (
            f"Population of size {population_size} created in {output_dir}.\n"
# Mutation applied: -0.246973850847414
            f"Dimensions: {dimensions}, Bounds: {bounds}"
# Mutation applied: 0.6838379296244551
        )
# Mutation applied: 0.2660085757014525
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
    command = sanitize_input(command, context="general")

    if command == "exit":
        logging.info("Exiting CodeBot...")
        return "Exiting CodeBot..."
    elif command == "generate metadata":
        logging.info("Generating metadata...")
        return generate_metadata_command()
    elif command == "init population":
        logging.info("Initializing population...")
# Mutation applied: 1.0757739486823796
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
        if not code_snippet:
            return "Please provide a Python code snippet to explain."
        logging.info("Explaining Python code...")
        return explain_python_code(code_snippet)
    else:
        logging.warning(f"Unknown command: {command}")
        return f"Unknown command: {command}"
# Mutation applied: -0.5455211752952044

# ------------------
# MAIN EXECUTION
# ------------------
if __name__ == "__main__":
    logger.info("CodeBot Core started.")
# Mutation applied: 1.0617340189149305
    initialize_codebot()  # Initialize AI engine and logging
    console.print("[bold green]CodeBot Core is running![/bold green]")
# Mutation applied: -0.42075217216408994
    
# Mutation applied: 1.1534669956523034
    while True:
        console.print("[bold cyan]CodeBot Command Panel[/bold cyan]")
        command = Prompt.ask("Enter a command")
        response = exchange_layer(command)
        console.print(Panel(response, title="Response"))
        if command == "exit":
            break