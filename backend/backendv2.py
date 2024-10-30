# backend.py

import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load environment variables
API_KEY = os.getenv("API_KEY")
STORAGE_PATH = os.getenv("STORAGE_PATH", "/data/storage.txt")

# Ensure storage path exists
if not os.path.exists(STORAGE_PATH):
    with open(STORAGE_PATH, "w") as f:
        pass  # Create an empty file if it doesn't exist

@app.route("/save_message", methods=["POST"])
def save_message():
    # Check API key
    req_api_key = request.headers.get("X-API-KEY")
    if req_api_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 403

    # Get the message from the request
    message = request.json.get("message")
    if not message:
        return jsonify({"error": "No message provided"}), 400

    # Append message to the storage file
    with open(STORAGE_PATH, "a") as f:
        f.write(f"{message}\n")

    return jsonify({"status": "Message saved"}), 200

@app.route("/get_messages", methods=["GET"])
def get_messages():
    with open(STORAGE_PATH, "r") as f:
        messages = f.readlines()

    return jsonify({"messages": messages}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
