# filepath: c:\CodeBot\ui_server.py
from flask import Flask, request, jsonify
from codebot_core import exchange_layer

app = Flask(__name__)

@app.route("/command", methods=["POST"])
def handle_command():
    command = request.json.get("command", "")
    response = exchange_layer(command)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)