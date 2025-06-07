from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Stores commands per user
commands = {}

@app.route("/push", methods=["POST"])
def push_command():
    data = request.json
    user_id = data.get("user_id")
    command = data.get("command")
    if user_id and command:
        commands[user_id] = command
        return jsonify({"status": "success"}), 200
    return jsonify({"error": "Invalid request"}), 400

@app.route("/get", methods=["GET"])
def get_command():
    user_id = request.args.get("user_id")
    command = commands.get(user_id)
    
    # Immediately clear the command after returning
    if command:
        commands[user_id] = None
        return jsonify({"command": command}), 200
    
    return jsonify({"command": None}), 200
