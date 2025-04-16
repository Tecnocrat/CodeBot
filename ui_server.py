# filepath: c:\CodeBot\ui_server.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from genetic.genetic_population import (
    generate_population,
    list_population,
    evaluate_population,
    deduplicate_population,
    select_parents,
    crossover,
    mutate_file
)
from core.ai_engine import preload_model
import os
import logging
import random  # Fix: Import the random module
import threading
import webbrowser  # Import for launching the browser

# Configure logging
LOG_FILE = os.path.join("storage", "runtime_exec.log")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="a"),
        logging.StreamHandler()
    ]
)

# Flask app setup
app = Flask(__name__, static_folder="frontend", static_url_path="/")
CORS(app)

# Track AI engine state
ai_engine_state = {"status": "off"}

@app.route("/")
def serve_index():
    """Serve the main index.html file for the web UI."""
    return send_from_directory(app.static_folder, "index.html")

@app.route("/favicon.ico")
def serve_favicon():
    """Serve the favicon.ico file for the web UI."""
    return send_from_directory(app.static_folder, "favicon.ico")

@app.route("/check-population", methods=["GET"])
def check_population():
    """Check if the genetic_population folder is already populated."""
    population_dir = os.path.join("storage", "genetic_population")
    if os.listdir(population_dir):  # Check if the folder is not empty
        return jsonify({"status": "populated"})
    return jsonify({"status": "empty"})

@app.route("/command", methods=["POST"])
def handle_command():
    """Handle commands sent from the web UI."""
    command = request.json.get("command", "").lower().strip()
    args = request.json.get("args", {})  # Additional arguments for commands

    try:
        if command == "init population":
            action = args.get("action", "fresh")
            population_dir = os.path.join("storage", "genetic_population")
            source_file = args.get("source_file")

            # Validate the source file
            if not source_file or not os.path.exists(source_file):
                raise FileNotFoundError(f"Source file '{source_file}' does not exist.")

            if action == "delete":
                # Delete current population
                for file in os.listdir(population_dir):
                    file_path = os.path.join(population_dir, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                logging.info("Deleted current population.")

            if action in ["fresh", "delete"]:
                # Initialize a new population
                population_size = int(args.get("population_size", 10))
                dimensions = int(args.get("dimensions", 5))
                bounds = tuple(map(float, args.get("bounds", (0.0, 1.0))))
                generate_population(source_file, population_size, dimensions, bounds, population_dir)
                return jsonify({"response": "Population initialized successfully."})

            if action == "grow":
                # Grow the current population
                existing_files = [f for f in os.listdir(population_dir) if f.startswith("individual_")]
                last_individual = max(int(f.split("_")[1].split(".")[0]) for f in existing_files)
                population_size = int(args.get("population_size", 10))
                dimensions = int(args.get("dimensions", 5))
                bounds = tuple(map(float, args.get("bounds", (0.0, 1.0))))
                generate_population(source_file, population_size, dimensions, bounds, population_dir, start_index=last_individual + 1)
                return jsonify({"response": "Population grown successfully."})

        else:
            return jsonify({"response": "Command not recognized."})

    except Exception as e:
        logging.error(f"Error processing command '{command}': {e}")
        return jsonify({"response": f"Error: {e}"})

@app.route("/ai-engine/on", methods=["POST"])
def turn_on_ai_engine():
    """Turn ON the AI engine."""
    global ai_engine_state
    try:
        ai_engine_state["status"] = "loading"
        preload_model()  # Load the AI engine
        ai_engine_state["status"] = "on"
        return jsonify({"status": "loading"})
    except Exception as e:
        logging.error(f"Error loading AI engine: {e}")
        ai_engine_state["status"] = "off"
        return jsonify({"status": "error", "message": str(e)})

@app.route("/ai-engine/off", methods=["POST"])
def turn_off_ai_engine():
    """Turn OFF the AI engine."""
    global ai_engine_state
    ai_engine_state["status"] = "off"
    return jsonify({"status": "off"})

def start_ui_server():
    """Start the Flask server and launch the browser."""
    def open_browser():
        """Open the default web browser."""
        url = "http://127.0.0.1:5000"
        logging.info(f"Launching browser to open {url}")
        try:
            webbrowser.get().open(url)
        except webbrowser.Error as e:
            logging.error(f"Failed to open browser: {e}")

    # Prevent double browser opening caused by Flask's reloader
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Timer(1.0, open_browser).start()

    # Start the Flask server
    logging.info("Starting CodeBot Web UI server...")
    app.run(debug=True, use_reloader=False)