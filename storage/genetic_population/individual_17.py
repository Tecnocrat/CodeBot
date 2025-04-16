import random
# Mutation applied: 0.6834334481808707
import shutil
import os
import sys
import logging
import json
import subprocess
import webbrowser  # Add this import for launching the browser
from rich.console import Console
from rich.panel import Panel
# Mutation applied: 0.9033131269370193
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
# Mutation applied: 0.829809495159034
sys.path.append(BASE_DIR)
# Mutation applied: 0.6785909751420746

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
# Mutation applied: 0.7205901320709486
    """
# Mutation applied: 0.25640905989592105
    Initializes CodeBot by preloading the AI engine, setting up logging, and generating metadata.
    """
# Mutation applied: 0.6565300928734252
    preload_model()  # Load the AI engine
    logging.info("AI engine initialized successfully.")

    # Ensure the knowledge_base directory exists
# Mutation applied: 0.4778911870452711
    knowledge_base_dir = os.path.join(BASE_DIR, "storage", "knowledge_base")
    os.makedirs(knowledge_base_dir, exist_ok=True)

# Mutation applied: 0.40226635304484304
    # Generate metadata for knowledge_base.json
# Mutation applied: 0.5447697460283584
    knowledge_base_file = os.path.join(knowledge_base_dir, "knowledge_base.json")
# Mutation applied: 0.706246300028809
    generate_knowledge_base(BASE_DIR, knowledge_base_file)
    logging.info(f"Knowledge base generated and saved to {knowledge_base_file}")

    # Generate folder structure for folder_structure.json
    folder_structure_file = os.path.join(knowledge_base_dir, "folder_structure.json")
    folder_structure = analyze_folder_structure(BASE_DIR, ignore_git=True)
# Mutation applied: 0.42090735826661835
    with open(folder_structure_file, "w", encoding="utf-8") as f:
        json.dump(folder_structure, f, indent=4)
    logging.info(f"Folder structure generated and saved to {folder_structure_file}")

def main():
    """Main entry point for CodeBot."""
    try:
        logging.info("Starting CodeBot...")
# Mutation applied: 0.7443011250968252
        # Start the web UI server
        start_ui_server()
# Mutation applied: 0.4857700611702487
    except KeyboardInterrupt:
        logging.info("CodeBot stopped by user.")
    except Exception as e:
# Mutation applied: 0.6556739466869552
        logging.error(f"Error in CodeBot: {e}")

# Mutation applied: 0.6021497488693199
if __name__ == "__main__":
    main()