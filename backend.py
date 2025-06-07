from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory store for commands
command_store = {}

@app.route('/push', methods=['POST'])
def push_command():
    data = request.get_json()
    user_id = data.get('user_id')
    command = data.get('command')
    if user_id and command:
        command_store[user_id] = command
        return jsonify({"status": "ok"}), 200
    return jsonify({"status": "error"}), 400

@app.route('/get', methods=['GET'])
def get_command():
    user_id = request.args.get('user_id')
    if user_id is None:
        return jsonify({"error": "Missing user_id"}), 400

    command = command_store.pop(user_id, None)
    return jsonify({"command": command})  # Even if None, this is valid JSON

@app.route('/')
def index():
    return 'AXIOM Server is running!', 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)

