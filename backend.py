from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import string

app = Flask(__name__)
CORS(app)

# Store: code → user_id and user_id → command
link_codes = {}
commands = {}

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@app.route("/link-code", methods=["POST"])
def link_code():
    data = request.json
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    # Reuse if already linked
    for code, uid in link_codes.items():
        if uid == user_id:
            return jsonify({"code": code}), 200

    code = generate_code()
    link_codes[code] = user_id
    return jsonify({"code": code}), 200

@app.route("/get-user-id", methods=["GET"])
def get_user_id():
    code = request.args.get("code", "").strip().upper()
    user_id = link_codes.get(code)
    if user_id:
        return jsonify({"user_id": user_id}), 200
    return jsonify({"error": "Invalid code"}), 404

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
    if command:
        commands[user_id] = None
        return jsonify({"command": command}), 200
    return jsonify({"command": None}), 200
