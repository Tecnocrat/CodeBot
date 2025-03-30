import os
import sys
import logging
import shutil
import openai
import json
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from core.self_improvement import run_genetic_algorithm, analyze_logs
from core.ai_engine import explain_python_code, analyze_code, parse_codebase
from genetic.genetic_iteration import manage_iterations
from genetic.genetic_optimizer import handle_exception, sanitize_input, get_valid_file_path  # Updated import
from genetic.genetic_population import request_population
from modules.file_manager import setup_project_structure, inject_text

# Add the `CodeBot` directory to the Python path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

# Configure logging
LOG_FILE = os.path.join(BASE_DIR, "runtime_exec.log")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="w"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Initialize Rich Console
console = Console()

# ------------------
# EXCHANGE LAYER
# ------------------
def exchange_layer(command):
    """
    Routes commands to the appropriate functions and returns the response.

    Args:
        command (str): The command to process.

    Returns:
        str: The response to the command.
    """
    command = sanitize_input(command, context="general")

    if command.startswith("explain python"):
        code_snippet = command.replace("explain python", "").strip()
        if not code_snippet:
            return "Error: Please provide a Python code snippet to explain."
        return explain_python_code(code_snippet)

    elif command.startswith("validate json"):
        json_input = command.replace("validate json", "").strip()
        try:
            sanitize_input(json_input, context="json")
            return "Valid JSON input."
        except ValueError as e:
            return f"Invalid JSON input: {e}"

    elif command.startswith("run genetic algorithm"):
        source_file = os.path.join(BASE_DIR, "example.py")
        output_dir = os.path.join(BASE_DIR, "genetic_population")
        run_genetic_algorithm(source_file, generations=5, initial_population_size=5, output_dir=output_dir)
        return "Genetic algorithm executed successfully."

    elif command.startswith("analyze logs"):
        log_file = os.path.join(BASE_DIR, "logs", "codebot_genetic.log")
        return analyze_logs(log_file)

    elif command.startswith("inject text"):
        try:
            file_path = get_valid_file_path("Enter file path: ")
            text = input("Enter text to inject: ").strip()
            position = sanitize_input(input("Enter injection mode (append/overwrite/insert): "))
            line_number = None
            if position == "insert":
                try:
                    line_number = int(input("Enter line number for insertion: "))
                except ValueError:
                    return "Invalid line number."
            return inject_text(file_path, text, position, line_number)
        except Exception as e:
            return handle_exception(logger, "Error handling inject command", e)

    elif command.startswith("setup project"):
        setup_project_structure(BASE_DIR)
        return "Project structure setup completed successfully."

    elif command.startswith("request population"):
        try:
            source_file = input("Enter source file path: ").strip()
            population_size = int(input("Enter population size: "))
            dimensions = int(input("Enter number of dimensions: "))
            bounds = tuple(map(float, input("Enter bounds (min, max): ").split(',')))
            output_dir = input("Enter output directory: ").strip()

            population = request_population(source_file, population_size, dimensions, bounds, output_dir)
            print(f"Population generated in {output_dir}")

            # Analyze the population using AI
            for individual in population:
                analysis = analyze_code(individual)
                print(f"Analysis for {individual}: {analysis}")

        except Exception as e:
            print(f"Error: {e}")

    elif command.startswith("parse codebase"):
        base_dir = BASE_DIR
        parsed_structure = parse_codebase(base_dir)
        output_file = os.path.join(BASE_DIR, "codebot_parsed_structure.json")
        with open(output_file, "w") as f:
            json.dump(parsed_structure, f, indent=4)
        return f"Codebase parsed successfully. Output saved to {output_file}"

    else:
        return "Unknown command. Type 'help' for a list of commands."

# ------------------
# CHATBOT CLASS
# ------------------
class Chatbot:
    def __init__(self):
        """
        Initializes the Chatbot instance.
        """
        self.running = True
        logger.info("Chatbot initialized.")

    def start(self):
        """
        Starts the chatbot in interactive mode.
        """
        logger.info("Chatbot started.")
        console.print(Panel("Welcome to CodeBot Chatbot! Type 'help' for commands.", title="Chatbot"))
        while self.running:
            try:
                command = Prompt.ask("You")
                response = self.process_command(command)
                if response:
                    console.print(Panel(response, title="CodeBot"))
            except Exception as e:
                logger.error(f"Chatbot error: {e}")

    def process_command(self, command):
        """
        Processes a command using the exchange layer.

        Args:
            command (str): The command to process.

        Returns:
            str: The response to the command.
        """
        if command.strip().lower() == "quit":
            self.running = False
            return "Chatbot session ended. Goodbye!"
        return exchange_layer(command)

# ------------------
# MAIN EXECUTION
# ------------------
if __name__ == "__main__":
    logger.info("CodeBot Core started.")
    console.print("[bold green]CodeBot Core is running![/bold green]")
    
    while True:
        console.print("[bold cyan]CodeBot Command Panel[/bold cyan]")
        console.print("1. Run Chatbot\n2. Run Self-Improvement\n3. Run Log Analysis\n4. Run Iteration Manager\n5. Setup Project Structure\n6. Exit")
        choice = Prompt.ask("Enter your choice")
        if choice == "1":
            chatbot = Chatbot()
            chatbot.start()
        elif choice == "6":
            console.print(Panel("Exiting CodeBot. Goodbye!", title="Exit"))
            sys.exit(0)
        else:
            console.print(Panel("Invalid choice. Please try again.", title="Error"))