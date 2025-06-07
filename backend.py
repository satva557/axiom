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

    # generate 6-digit code
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    link_codes[code] = user_id
    return jsonify({"code": code}), 200
    
@app.route("/get-user-id", methods=["GET"])
def get_user_id():
    code = request.args.get("code", "").strip().upper()
    user_id = link_codes.get(code)
    if user_id:
        return jsonify({"user_id": user_id}), 200
    return jsonify({"error": "Invalid code"}), 404
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory fake storage for now
link_codes = {}

@app.route("/")
def home():
    return "SPARK AI is running", 200

# This is the route Alexa skill will hit to pull the link code
@app.route("/pull/<user_id>", methods=["GET"])
def pull_code(user_id):
    code = link_codes.get(user_id)
    if code:
        return jsonify({"code": code})
    else:
        return jsonify({"error": "No code found"}), 404

# This is the route you call to store a code for a user
@app.route("/push", methods=["POST"])
def push_code():
    data = request.json
    user_id = data.get("user_id")
    code = data.get("code")
    if user_id and code:
        link_codes[user_id] = code
        return jsonify({"status": "saved"}), 200
    else:
        return jsonify({"error": "Missing user_id or code"}), 400


@app.route("/get", methods=["GET"])
def get_command():
    user_id = request.args.get("user_id")
    command = commands.get(user_id)
    if command:
        commands[user_id] = None
        return jsonify({"command": command}), 200
    return jsonify({"command": None}), 200

# ✅ Run on port 10001
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10001, debug=True)
