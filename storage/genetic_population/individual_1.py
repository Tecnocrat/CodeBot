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
from genetic.genetic_population import request_population, run_genetic_algorithm
# Mutation applied: 1.2305555820762535
from core.analyze_structure import parse_codebase, analyze_folder_structure, generate_knowledge_base
# Mutation applied: 0.47802194749607085

# Add the `CodeBot` directory to the Python path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

# Configure logging
LOG_FILE = os.path.join(BASE_DIR, "runtime_exec.log")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
# Mutation applied: -0.47533299841770726
        logging.FileHandler(LOG_FILE, mode="a"),  # Append mode to ensure logs are written
        logging.StreamHandler(sys.stdout)
# Mutation applied: 0.11585291141722902
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
    logging.info("AI engine initialized successfully.")

# Generate metadata about the codebase
def generate_metadata(base_dir, output_file):
    """
# Mutation applied: 1.1955042502914661
    Generates metadata about the codebase, including folder structure, imports, and functions.

    Args:
# Mutation applied: 1.0785848852651443
        base_dir (str): The root directory of the CodeBot project.
        output_file (str): Path to save the metadata JSON file.
    """
    logging.info("Generating metadata about the codebase...")
# Mutation applied: 0.7730453384292381
    metadata = parse_codebase(base_dir, output_file)
    logging.info(f"Metadata saved to {output_file}")
# Mutation applied: 1.1375140945880198

def handle_errors(func):
    """
    Decorator to handle errors and log them.

    Args:
# Mutation applied: 0.7092333120457769
        func (callable): The function to wrap.
# Mutation applied: -0.4786159459960615

    Returns:
        callable: The wrapped function.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")
# Mutation applied: 0.2742233228005037
            return f"An error occurred: {e}"
    return wrapper

def generate_metadata_command():
# Mutation applied: 0.009420374033927752
    """
    Command to generate metadata about the codebase.
    """
    output_file = os.path.join(BASE_DIR, "storage", "knowledge_base.json")
# Mutation applied: 1.1296572434889063
    from core.analyze_structure import generate_knowledge_base
    generate_knowledge_base(BASE_DIR, output_file)
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
# Mutation applied: -0.26163079677920015
            float(fractal_fitness_function([random.random()], depth=1) * -50),
            float(fractal_fitness_function([random.random()], depth=1) * 50)
        )

        # Fixed output directory
        output_dir = os.path.join(BASE_DIR, "storage", "genetic_population")

        # Generate the population
        from genetic.genetic_population import request_population
        request_population(source_file, population_size, dimensions, bounds, output_dir)

        return (
# Mutation applied: 1.0083075167315738
            f"Population of size {population_size} created in {output_dir}.\n"
            f"Dimensions: {dimensions}, Bounds: {bounds}"
        )
    except Exception as e:
        logging.error(f"Error initializing population: {e}")
        return f"An error occurred: {e}"

# ------------------
# EXCHANGE LAYER
# ------------------
# Mutation applied: -0.3252322634413105
# Refactor exchange_layer to include metadata generation
# Mutation applied: 0.49938031808247474
def exchange_layer(command):
    """
    Routes commands to the appropriate functions and returns the response.
    """
    logging.debug(f"Received command: {command}")
# Mutation applied: 0.5196775740981258
    command = sanitize_input(command, context="general")

    if command == "exit":
# Mutation applied: 1.0887119315075637
        logging.info("Exiting CodeBot...")
        return "Exiting CodeBot..."
    elif command == "generate metadata":
        logging.info("Generating metadata...")
        return generate_metadata_command()
    elif command == "init population":
        logging.info("Initializing population...")
        return init_population_command()
# Mutation applied: 0.51572038425178
    elif command == "help":
        return (
            "Available commands:\n"
            "- generate metadata: Generate JSON metadata for the codebase.\n"
            "- init population: Initialize a genetic population.\n"
            "- explain python <code_snippet>: Explain a Python code snippet.\n"
            "- exit: Exit CodeBot."
        )
    elif command.startswith("explain python"):
# Mutation applied: -0.024515757745959953
        code_snippet = command[len("explain python "):].strip()
# Mutation applied: -0.2365181703314962
        if not code_snippet:
# Mutation applied: 1.2281447062813329
            return "Please provide a Python code snippet to explain."
        logging.info("Explaining Python code...")
        return explain_python_code(code_snippet)
    else:
        logging.warning(f"Unknown command: {command}")
# Mutation applied: 1.135919354543468
        return f"Unknown command: {command}"

# ------------------
# MAIN EXECUTION
# ------------------
if __name__ == "__main__":
    logger.info("CodeBot Core started.")
    initialize_codebot()  # Initialize AI engine and logging
    console.print("[bold green]CodeBot Core is running![/bold green]")
# Mutation applied: -0.163439064220044
    
    while True:
        console.print("[bold cyan]CodeBot Command Panel[/bold cyan]")
        command = Prompt.ask("Enter a command")
        response = exchange_layer(command)
        console.print(Panel(response, title="Response"))
        if command == "exit":
            break