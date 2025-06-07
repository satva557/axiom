from flask import Flask, request, jsonify
from flask_cors import CORS
import random, threading

app = Flask(__name__)
CORS(app)

commands = {}
link_codes = {}

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

@app.route("/link-code", methods=["POST"])
def create_link_code():
    data = request.json
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    code = ''.join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ23456789", k=4))
    link_codes[code] = user_id
    threading.Timer(300, lambda: link_codes.pop(code, None)).start()
    return jsonify({"code": code}), 200

@app.route("/get-user-id", methods=["GET"])
def get_user_id_from_code():
    code = request.args.get("code")
    user_id = link_codes.get(code)
    return jsonify({"user_id": user_id if user_id else None}), 200
