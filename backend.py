from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import string

app = Flask(__name__)
CORS(app)

# Store: code → user_id and user_id → code
link_codes = {}     # user_id ↔ code
reverse_codes = {}  # code ↔ user_id
commands = {}       # user_id ↔ command

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# ✅ Home route for testing
@app.route("/")
def home():
    return "✅ SPARK AI Flask server is running", 200

# ✅ POST /link-code → generate a code for the device
@app.route("/link-code", methods=["POST"])
def link_code():
    data = request.json
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    code = generate_code()
    link_codes[user_id] = code
    reverse_codes[code] = user_id
    return jsonify({"code": code}), 200

# ✅ GET /get-user-id?code=XYZ → get the user_id from code
@app.route("/get-user-id", methods=["GET"])
def get_user_id():
    code = request.args.get("code", "").strip().upper()
    user_id = reverse_codes.get(code)
    if user_id:
        return jsonify({"user_id": user_id}), 200
    return jsonify({"error": "Invalid code"}), 404

# ✅ POST /push → PC sets code for Alexa to pull
@app.route("/push", methods=["POST"])
def push_code():
    data = request.json
    user_id = data.get("user_id")
    code = data.get("code")
    if user_id and code:
        link_codes[user_id] = code
        return jsonify({"status": "saved"}), 200
    return jsonify({"error": "Missing user_id or code"}), 400

# ✅ GET /pull/<user_id> → Alexa pulls code from PC
@app.route("/pull/<user_id>", methods=["GET"])
def pull_code(user_id):
    code = link_codes.get(user_id)
    if code:
        return jsonify({"code": code}), 200
    return jsonify({"error": "No code found"}), 404

# ✅ POST /send → Alexa sends command to PC
@app.route("/send", methods=["POST"])
def send_command():
    data = request.json
    user_id = data.get("user_id")
    command = data.get("command")
    if not user_id or not command:
        return jsonify({"error": "Missing user_id or command"}), 400
    commands[user_id] = command
    return jsonify({"status": "command received"}), 200

# ✅ GET /get?user_id=xyz → PC pulls command sent from Alexa
@app.route("/get", methods=["GET"])
def get_command():
    user_id = request.args.get("user_id")
    command = commands.get(user_id)
    if command:
        commands[user_id] = None  # clear after fetching
        return jsonify({"command": command}), 200
    return jsonify({"command": None}), 200

# ✅ Run on port 10001
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10001, debug=True)
