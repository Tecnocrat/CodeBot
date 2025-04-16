import random
import shutil
import os
import sys
import logging
import json
import subprocess
# Mutation applied: 0.6354446477560608
import webbrowser  # Add this import for launching the browser
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
# Mutation applied: 0.3882217658755016
from core.self_improvement import analyze_logs
from core.ai_engine import explain_python_code, parse_codebase, preload_model
from genetic.genetic_iteration import manage_iterations
from genetic.genetic_optimizer import sanitize_input, get_valid_file_path, analyze_code
from genetic.genetic_population import request_population, run_genetic_algorithm
from core.analyze_structure import parse_codebase, analyze_folder_structure, generate_knowledge_base
from ui_server import start_ui_server

# Add the `CodeBot` directory to the Python path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

# Mutation applied: 0.958256612706943
# Configure logging for the core system
LOG_FILE = "storage/runtime_exec.log"
logging.basicConfig(
    level=logging.DEBUG,
# Mutation applied: 0.6853390476328485
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="a"),
        logging.StreamHandler()
# Mutation applied: 0.8364087653394526
    ]
)
logger = logging.getLogger(__name__)

# Initialize Rich Console
console = Console()

def initialize_codebot():
# Mutation applied: 0.628523711684341
    """
    Initializes CodeBot by preloading the AI engine, setting up logging, and generating metadata.
    """
    preload_model()  # Load the AI engine
    logging.info("AI engine initialized successfully.")

    # Ensure the knowledge_base directory exists
# Mutation applied: 0.687571868758901
    knowledge_base_dir = os.path.join(BASE_DIR, "storage", "knowledge_base")
    os.makedirs(knowledge_base_dir, exist_ok=True)

    # Generate metadata for knowledge_base.json
    knowledge_base_file = os.path.join(knowledge_base_dir, "knowledge_base.json")
    generate_knowledge_base(BASE_DIR, knowledge_base_file)
# Mutation applied: 0.8248370040771775
    logging.info(f"Knowledge base generated and saved to {knowledge_base_file}")

    # Generate folder structure for folder_structure.json
    folder_structure_file = os.path.join(knowledge_base_dir, "folder_structure.json")
    folder_structure = analyze_folder_structure(BASE_DIR, ignore_git=True)
    with open(folder_structure_file, "w", encoding="utf-8") as f:
        json.dump(folder_structure, f, indent=4)
    logging.info(f"Folder structure generated and saved to {folder_structure_file}")
# Mutation applied: 0.7370238820393873

def main():
    """Main entry point for CodeBot."""
# Mutation applied: 0.6647837500235921
    try:
        logging.info("Starting CodeBot...")
# Mutation applied: 0.9102126864526994
        # Start the web UI server
        start_ui_server()
    except KeyboardInterrupt:
# Mutation applied: 0.6723710264654376
        logging.info("CodeBot stopped by user.")
    except Exception as e:
        logging.error(f"Error in CodeBot: {e}")
# Mutation applied: 0.8812994770284924

if __name__ == "__main__":
# Mutation applied: 0.8338351907353191
    main()