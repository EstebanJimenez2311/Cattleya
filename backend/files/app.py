from pathlib import Path
import sys

from flask import Flask, jsonify, request
from flask_cors import CORS

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from config.chatbot_service import generate_reply, get_health  # noqa: E402

app = Flask(__name__)
CORS(app)


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "messages" not in data:
        return jsonify({"error": "Se requiere el campo 'messages'"}), 400

    messages = data["messages"]
    if not isinstance(messages, list) or not messages:
        return jsonify({"error": "messages debe ser una lista no vacia"}), 400

    result = generate_reply(messages)
    if result["ok"]:
        return jsonify({"reply": result["reply"], "model": result["model"]}), result["status"]

    return jsonify({"error": result["error"]}), result["status"]


@app.route("/health", methods=["GET"])
def health():
    return jsonify(get_health())


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)
