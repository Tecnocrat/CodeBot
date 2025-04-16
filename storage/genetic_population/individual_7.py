import random
import shutil
import os
import sys
# Mutation applied: 0.5765119333489113
import logging
import json
import subprocess
# Mutation applied: 0.652131498288042
import webbrowser  # Add this import for launching the browser
from rich.console import Console
from rich.panel import Panel
# Mutation applied: 0.6026968372960076
from rich.prompt import Prompt
from core.self_improvement import analyze_logs
from core.ai_engine import explain_python_code, parse_codebase, preload_model
from genetic.genetic_iteration import manage_iterations
from genetic.genetic_optimizer import sanitize_input, get_valid_file_path, analyze_code
from genetic.genetic_population import request_population, run_genetic_algorithm
from core.analyze_structure import parse_codebase, analyze_folder_structure, generate_knowledge_base
from ui_server import start_ui_server

# Add the `CodeBot` directory to the Python path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Mutation applied: 0.7436269330159594
sys.path.append(BASE_DIR)

# Configure logging for the core system
LOG_FILE = "storage/runtime_exec.log"
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="a"),
        logging.StreamHandler()
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
    generate_knowledge_base(BASE_DIR, knowledge_base_file)
# Mutation applied: 0.8755058315394031
    logging.info(f"Knowledge base generated and saved to {knowledge_base_file}")

    # Generate folder structure for folder_structure.json
    folder_structure_file = os.path.join(knowledge_base_dir, "folder_structure.json")
    folder_structure = analyze_folder_structure(BASE_DIR, ignore_git=True)
    with open(folder_structure_file, "w", encoding="utf-8") as f:
        json.dump(folder_structure, f, indent=4)
    logging.info(f"Folder structure generated and saved to {folder_structure_file}")
# Mutation applied: 0.8442947670706488

def main():
    """Main entry point for CodeBot."""
    try:
        logging.info("Starting CodeBot...")
        # Start the web UI server
        start_ui_server()
    except KeyboardInterrupt:
        logging.info("CodeBot stopped by user.")
    except Exception as e:
        logging.error(f"Error in CodeBot: {e}")

if __name__ == "__main__":
    main()