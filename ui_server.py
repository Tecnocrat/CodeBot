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
import os
import logging
import random  # Fix: Import the random module

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

@app.route("/")
def serve_index():
    """Serve the main index.html file for the web UI."""
    return send_from_directory(app.static_folder, "index.html")

@app.route("/favicon.ico")
def serve_favicon():
    """Serve the favicon.ico file for the web UI."""
    return send_from_directory(app.static_folder, "favicon.ico")

@app.route("/command", methods=["POST"])
def handle_command():
    """Handle commands sent from the web UI."""
    command = request.json.get("command", "").lower().strip()
    args = request.json.get("args", {})  # Additional arguments for commands

    try:
        if command == "init population":
            population_size = int(args.get("population_size", 10))
            dimensions = int(args.get("dimensions", 5))
            bounds = tuple(args.get("bounds", (0.0, 1.0)))
            output_dir = os.path.join("storage", "genetic_population")
            generate_population(source_file, population_size, dimensions, bounds, output_dir)
            logging.info("Population initialized successfully.")
            return jsonify({"response": "Population initialized successfully."})

        elif command == "list population":
            population_dir = os.path.join("storage", "genetic_population")
            population = list_population(population_dir)
            logging.info("Population listed successfully.")
            return jsonify({"response": "Population listed successfully.", "data": population})

        elif command == "evaluate population":
            population_dir = os.path.join("storage", "genetic_population")
            ai_engine = lambda log: random.uniform(0, 1)  # Example AI engine
            fitness_scores = evaluate_population(population_dir, ai_engine)
            logging.info("Population evaluated successfully.")
            return jsonify({"response": "Population evaluated successfully.", "data": fitness_scores})

        elif command == "deduplicate population":
            output_dir = os.path.join("storage", "genetic_population")
            deduplicate_population(output_dir)
            logging.info("Population deduplicated successfully.")
            return jsonify({"response": "Population deduplicated successfully."})

        elif command == "log":
            message = args.get("message", "")
            logging.info(message)
            return jsonify({"response": "Log received."})

        else:
            return jsonify({"response": "Command not recognized."})

    except Exception as e:
        logging.error(f"Error processing command '{command}': {e}")
        return jsonify({"response": f"Error: {e}"})

if __name__ == "__main__":
    logging.info("Starting CodeBot Web UI server...")
    app.run(debug=True)