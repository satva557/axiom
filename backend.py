from flask import Flask, request, jsonify
import os

app = Flask(__name__)
user_commands = {}

@app.route("/")
def home():
    return "AXIOM Backend Online"

@app.route("/push", methods=["POST"])
def push():
    data = request.json
    user_id = data.get("user_id")
    command = data.get("command")
    
    if not user_id or not command:
        return jsonify({"error": "Missing user_id or command"}), 400
    
    user_commands[user_id] = command
    return jsonify({"message": "Command stored"}), 200

@app.route("/pull/<user_id>", methods=["GET"])
def pull(user_id):
    command = user_commands.pop(user_id, None)
    return jsonify({"command": command or ""}), 200

# ✅ Run on host=0.0.0.0 and PORT from env (required by Render)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
