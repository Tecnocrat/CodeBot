# filepath: c:\CodeBot\ui_server.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from genetic.genetic_population import list_population, evaluate_population  # Import both functions
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
    page = request.json.get("page", 1)  # Current page for pagination

    if command == "evaluate population":
        # Path to the genetic_population folder
        population_dir = os.path.join("storage", "genetic_population")
        if not os.path.exists(population_dir):
            return jsonify({"response": "No genetic population found.", "data": []})

        # Use the list_population function to list individuals
        try:
            population = list_population(population_dir)
        except Exception as e:
            return jsonify({"response": f"Error listing population: {e}", "data": []})

        # Pagination logic (10 individuals per page)
        items_per_page = 10
        start_index = (page - 1) * items_per_page
        end_index = start_index + items_per_page
        paginated_population = population[start_index:end_index]

        # Determine if there are more pages
        total_pages = (len(population) + items_per_page - 1) // items_per_page

        # Format the response to display "Individual X"
        formatted_population = [
            {"name": f"Individual {ind['mutation_number'] + 1}"}
            for ind in paginated_population
        ]

        return jsonify({
            "response": f"Page {page} of {total_pages}",
            "data": formatted_population,
            "total_pages": total_pages
        })

    else:
        return jsonify({"response": "Command not recognized."})

if __name__ == "__main__":
    print("Starting CodeBot Web UI server...")
    app.run(debug=True)