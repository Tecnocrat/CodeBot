# filepath: c:\CodeBot\ui_server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from codebot_core import exchange_layer

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/command", methods=["POST"])
def handle_command():
    """
    Handle commands sent from the web UI.
    """
    command = request.json.get("command", "")
    response = exchange_layer(command)
    return jsonify({"response": response})

if __name__ == "__main__":
    print("Starting CodeBot Web UI server...")
    app.run(debug=True)