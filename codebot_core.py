import random
import shutil
import os
import sys
import logging
import json
import subprocess
import webbrowser  # Add this import for launching the browser
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
        logging.FileHandler(LOG_FILE, mode="a"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Initialize Rich Console
console = Console()

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

def launch_web_ui():
    """
    Launches the Flask server for the web UI and opens it in the Edge browser or default browser.
    """
    try:
        logging.info("Starting the Web UI...")
        # Open the web UI in the default browser
        web_ui_url = "http://127.0.0.1:5000"
        logging.info(f"Opening the web UI at {web_ui_url} in the default browser...")
        webbrowser.open(web_ui_url)

        # Start the Flask server and block until it is stopped
        subprocess.run(["python", "ui_server.py"], check=True)
    except KeyboardInterrupt:
        logging.info("Web UI stopped by user.")
    except Exception as e:
        logging.error(f"Error launching Web UI: {e}")

def exchange_layer(command):
    """
    Routes commands to the appropriate functions and returns the response.
    """
    logging.debug(f"Received command: {command}")
    command = command.lower().strip()

    # Handle commands
    if command == "help":
        return (
            "Available commands:\n"
            "- init population: Initialize a genetic population.\n"
            "- evaluate population: Evaluate a genetic population.\n"
            "- evaluate results: Review evaluation results.\n"
            "- create subpopulation: Create a new subpopulation from a chosen individual.\n"
            "- exit: Exit CodeBot."
        )
    elif command == "init population":
        return "Initializing population..."
    elif command == "evaluate population":
        return "Evaluating population..."
    elif command == "evaluate results":
        return "Reviewing evaluation results..."
    elif command == "create subpopulation":
        return "Creating subpopulation..."
    elif command == "exit":
        return "Exiting CodeBot..."
    else:
        return "Invalid command. Please enter a valid option."

if __name__ == "__main__":
    logger.info("CodeBot Core started.")
    initialize_codebot()  # Initialize AI engine and logging
    launch_web_ui()  # Launch the Web UI