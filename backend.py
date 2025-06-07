from flask import Flask, request, jsonify

app = Flask(__name__)
user_commands = {}

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

if __name__ == "__main__":
    app.run()
