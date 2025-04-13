# filepath: c:\CodeBot\ui_server.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from codebot_core import exchange_layer  # Ensure this import works
import os

app = Flask(__name__, static_folder="frontend", static_url_path="/")  # Serve the frontend folder
CORS(app)  # Enable CORS for all routes

@app.route("/")
def serve_index():
    """
    Serve the main index.html file for the web UI.
    """
    return send_from_directory(app.static_folder, "index.html")

@app.route("/favicon.ico")
def serve_favicon():
    """
    Serve the favicon.ico file for the web UI.
    """
    return send_from_directory(app.static_folder, "favicon.ico")

@app.route("/command", methods=["POST"])
def handle_command():
    """
    Handle commands sent from the web UI.
    """
    command = request.json.get("command", "")
    if command == "evaluate population":
        # Example list of genetic individuals (replace with actual logic)
        genetic_individuals = [
            {"id": 1, "name": "Individual 1", "fitness": 0.85},
            {"id": 2, "name": "Individual 2", "fitness": 0.78},
            {"id": 3, "name": "Individual 3", "fitness": 0.92},
        ]
        return jsonify({"response": "List of genetic individuals", "data": genetic_individuals})
    else:
        response = exchange_layer(command)
        return jsonify({"response": response})

if __name__ == "__main__":
    print("Starting CodeBot Web UI server...")
    app.run(debug=True)