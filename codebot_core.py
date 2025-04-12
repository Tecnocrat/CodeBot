import random  # Add this import statement
import shutil  # Add this import statement
import os
import sys
import logging
import json
import subprocess  # Add this import for launching the web UI
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from core.self_improvement import analyze_logs
from core.ai_engine import explain_python_code, parse_codebase, preload_model
from genetic.genetic_iteration import manage_iterations
from genetic.genetic_optimizer import sanitize_input, get_valid_file_path, analyze_code
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
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Initialize Rich Console
console = Console()

# Initialize AI engine and logging
def initialize_codebot():
    """
    Initializes CodeBot by preloading the AI engine, setting up logging, and generating metadata.
    """
    preload_model()  # Load the AI engine
    logging.info("AI engine initialized successfully.")

    # Ensure the knowledge_base directory exists
    knowledge_base_dir = os.path.join(BASE_DIR, "storage", "knowledge_base")
    os.makedirs(knowledge_base_dir, exist_ok=True)

    # Generate metadata for knowledge_base.json
    knowledge_base_file = os.path.join(knowledge_base_dir, "knowledge_base.json")
    from core.analyze_structure import generate_knowledge_base
    generate_knowledge_base(BASE_DIR, knowledge_base_file)
    logging.info(f"Knowledge base generated and saved to {knowledge_base_file}")

    # Generate folder structure for folder_structure.json
    folder_structure_file = os.path.join(knowledge_base_dir, "folder_structure.json")
    from core.analyze_structure import analyze_folder_structure
    folder_structure = analyze_folder_structure(BASE_DIR, ignore_git=True)
    with open(folder_structure_file, "w", encoding="utf-8") as f:
        json.dump(folder_structure, f, indent=4)
    logging.info(f"Folder structure generated and saved to {folder_structure_file}")

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

def generate_metadata_command():
    """
    Command to generate metadata about the codebase.
    """
    output_dir = os.path.join(BASE_DIR, "storage", "knowledge_base")
    os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
    output_file = os.path.join(output_dir, "knowledge_base.json")

    from core.analyze_structure import generate_knowledge_base
    generate_knowledge_base(BASE_DIR, output_file)
    return f"Metadata generated and saved to {output_file}"

def generate_folder_structure_command():
    """
    Command to generate the folder structure and save it to folder_structure.json.

    Returns:
        str: A message indicating the result of the operation.
    """
    try:
        output_dir = os.path.join(BASE_DIR, "storage", "knowledge_base")
        os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
        output_file = os.path.join(output_dir, "folder_structure.json")

        from core.analyze_structure import analyze_folder_structure
        folder_structure = analyze_folder_structure(BASE_DIR, ignore_git=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(folder_structure, f, indent=4)
        return f"Folder structure generated and saved to {output_file}"
    except Exception as e:
        logging.error(f"Error generating folder structure: {e}")
        return f"An error occurred: {e}"

def init_population_command():
    """
    Command to initialize a genetic population with codebot_core.py as the source file.

    Returns:
        str: A message indicating the result of the operation.
    """
    try:
        # Display warning and require confirmation
        console.print("[bold yellow]WARNING: Initializing a new population may lead to exponential growth of base populations.[/bold yellow]")
        confirmation = Prompt.ask("Do you want to proceed? (yes/no)", default="no")
        if confirmation.lower() != "yes":
            return "Population initialization canceled."

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
            f"Dimensions: {dimensions}, Bounds: {bounds}"
        )
    except Exception as e:
        logging.error(f"Error initializing population: {e}")
        return f"An error occurred: {e}"

def evaluate_population_command():
    """
    Command to evaluate a genetic population or individual with pagination.

    Returns:
        str: A message indicating the result of the evaluation.
    """
    try:
        # Fixed population directory
        population_dir = os.path.join(BASE_DIR, "storage", "genetic_population")
        populations = [p for p in os.listdir(population_dir) if os.path.isdir(os.path.join(population_dir, p))]

        if not populations:
            return "No populations available for evaluation."

        # Pagination variables
        page_size = 10
        current_page = 0
        total_pages = (len(populations) + page_size - 1) // page_size

        while True:
            # Display populations for the current page
            console.print(f"[bold cyan]Available Populations (Page {current_page + 1}/{total_pages}):[/bold cyan]")
            start_index = current_page * page_size
            end_index = min(start_index + page_size, len(populations))
            for idx, population in enumerate(populations[start_index:end_index], start=1):
                console.print(f"{idx}. {population}")

            # Display navigation options
            console.print("[bold yellow]Options:[/bold yellow]")
            console.print("1-10: Select a population")
            console.print("'.': Next page")
            console.print("',': Previous page")
            console.print("'0': Cancel")

            # Get user input
            choice = Prompt.ask("Enter your choice")

            if choice == "0":
                return "Evaluation canceled."
            elif choice == ".":
                if current_page < total_pages - 1:
                    current_page += 1
                else:
                    console.print("[bold red]You are already on the last page.[/bold red]")
            elif choice == ",":
                if current_page > 0:
                    current_page -= 1
                else:
                    console.print("[bold red]You are already on the first page.[/bold red]")
            elif choice.isdigit() and 1 <= int(choice) <= (end_index - start_index):
                selected_population = populations[start_index + int(choice) - 1]
                break
            else:
                console.print("[bold red]Invalid choice. Please try again.[/bold red]")

        # Evaluate the selected population
        from genetic.genetic_population import evaluate_population
        from core.ai_engine import analyze_execution_logs
        fitness_scores = evaluate_population(
            os.path.join(population_dir, selected_population),
            analyze_execution_logs,
            evaluation_mode="single"
        )

        # Log and return the results
        results = "\n".join([f"{ind}: {score}" for ind, score in fitness_scores.items()])
        logging.info(f"Population evaluation completed:\n{results}")
        return f"Population evaluation completed for {selected_population}:\n{results}"
    except Exception as e:
        logging.error(f"Error evaluating population: {e}")
        return f"An error occurred: {e}"

def evaluate_results_command():
    """
    Command to review the content of the evaluation_results folder.

    Returns:
        str: A message listing the evaluation results.
    """
    try:
        evaluation_dir = os.path.join(BASE_DIR, "storage", "genetic_population", "evaluation_results")
        if not os.path.exists(evaluation_dir):
            return "No evaluation results found."

        results = []
        for file in os.listdir(evaluation_dir):
            results.append(file)

        if not results:
            return "The evaluation_results folder is empty."

        return "Evaluation Results:\n" + "\n".join(results)
    except Exception as e:
        logging.error(f"Error reviewing evaluation results: {e}")
        return f"An error occurred: {e}"

def create_subpopulation_command():
    """
    Command to create a new subpopulation from a chosen individual.

    Returns:
        str: A message indicating the result of the operation.
    """
    try:
        # Prompt user for the individual to use as the base
        evaluation_dir = os.path.join(BASE_DIR, "storage", "genetic_population", "evaluation_results")
        if not os.path.exists(evaluation_dir):
            return "No evaluation results found. Please evaluate a population first."

        console.print("[bold cyan]Available Individuals:[/bold cyan]")
        individuals = [file for file in os.listdir(evaluation_dir) if file.endswith(".py")]
        if not individuals:
            return "No individuals available in evaluation results."

        for idx, individual in enumerate(individuals, start=1):
            console.print(f"{idx}. {individual}")

        choice = Prompt.ask("Select an individual by number", default="1")
        try:
            chosen_individual = individuals[int(choice) - 1]
        except (IndexError, ValueError):
            return "Invalid selection."

        # Create a new subpopulation folder
        subpopulation_dir = os.path.join(BASE_DIR, "storage", "genetic_population", f"subpopulation_{chosen_individual}")
        os.makedirs(subpopulation_dir, exist_ok=True)

        # Copy the chosen individual into the subpopulation folder
        source_path = os.path.join(evaluation_dir, chosen_individual)
        for i in range(5):  # Create 5 mutated copies
            target_path = os.path.join(subpopulation_dir, f"{chosen_individual}_variant_{i}.py")
            shutil.copy(source_path, target_path)

            # Apply mutations to the copied file
            from genetic.genetic_population import mutate_file
            mutate_file(target_path, dimensions=5, bounds=(-10, 10))

        return f"Subpopulation created in {subpopulation_dir}."
    except Exception as e:
        logging.error(f"Error creating subpopulation: {e}")
        return f"An error occurred: {e}"

def display_main_menu():
    """
    Displays the main menu options.
    """
    console.print("[bold cyan]Main Menu:[/bold cyan]")
    console.print("1. Init Population")
    console.print("2. Evaluate Population")
    console.print("3. Evaluate Results")
    console.print("4. Create Subpopulation")
    console.print("0. Exit")

def main_menu():
    """
    Displays the main menu and handles user input.
    """
    console.print("[bold cyan]Main Menu:[/bold cyan]")
    console.print("1. Terminal UI")
    console.print("2. Web UI")
    console.print("0. Exit")

    choice = Prompt.ask("Select an option (1/2/0)", default="1")
    if choice == "1":
        terminal_ui()
    elif choice == "2":
        launch_web_ui()
    elif choice == "0":
        console.print("[bold green]Exiting CodeBot...[/bold green]")
        sys.exit(0)
    else:
        console.print("[bold red]Invalid choice. Please try again.[/bold red]")
        main_menu()

def terminal_ui():
    """
    Starts the terminal-based UI.
    """
    while True:
        display_main_menu()
        command = Prompt.ask("Enter a command (number)", default="0")
        response = exchange_layer(command)
        console.print(Panel(response, title="Response"))
        if command == "0":  # Exit
            break

def launch_web_ui():
    """
    Launches the web UI by starting the Flask server.
    """
    console.print("[bold green]Starting Web UI...[/bold green]")
    try:
        subprocess.run(["python", "ui_server.py"], check=True)
    except KeyboardInterrupt:
        console.print("[bold yellow]Web UI stopped by user.[/bold yellow]")
    except Exception as e:
        console.print(f"[bold red]Error launching Web UI: {e}[/bold red]")

# ------------------
# EXCHANGE LAYER
# ------------------
# Refactor exchange_layer to include metadata generation
def exchange_layer(command):
    """
    Routes commands to the appropriate functions and returns the response.
    """
    logging.debug(f"Received command: {command}")
    command = sanitize_input(command, context="general").lower()

    # Handle numeric commands (for terminal UI)
    if command == "1":  # Init population
        logging.info("Initializing population...")
        return init_population_command()
    elif command == "2":  # Evaluate population
        logging.info("Evaluating population...")
        return evaluate_population_command()
    elif command == "3":  # Evaluate results
        logging.info("Reviewing evaluation results...")
        return evaluate_results_command()
    elif command == "4":  # Create subpopulation
        logging.info("Creating subpopulation...")
        return create_subpopulation_command()
    elif command == "0":  # Exit
        logging.info("Exiting CodeBot...")
        return "Exiting CodeBot..."

    # Handle text-based commands (for web UI)
    elif command == "help":
        return (
            "Available commands:\n"
            "- init population: Initialize a genetic population.\n"
            "- evaluate population: Evaluate a genetic population.\n"
            "- evaluate results: Review evaluation results.\n"
            "- create subpopulation: Create a new subpopulation from a chosen individual.\n"
            "- exit: Exit CodeBot."
        )
    elif command == "init population":
        return init_population_command()
    elif command == "evaluate population":
        return evaluate_population_command()
    elif command == "evaluate results":
        return evaluate_results_command()
    elif command == "create subpopulation":
        return create_subpopulation_command()
    elif command == "exit":
        return "Exiting CodeBot..."
    else:
        return "Invalid command. Please enter a valid option."

# ------------------
# MAIN EXECUTION
# ------------------
if __name__ == "__main__":
    logger.info("CodeBot Core started.")
    initialize_codebot()  # Initialize AI engine and logging
    console.print("[bold green]CodeBot Core is running![/bold green]")
    main_menu()