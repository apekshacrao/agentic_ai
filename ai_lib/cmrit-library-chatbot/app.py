from flask import Flask, jsonify, render_template, request
from chatbot import chatbot_response

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message")

    if not isinstance(user_message, str):
        return jsonify({"error": "Message must be a string."}), 400

    user_message = user_message.strip()
    if not user_message:
        return jsonify({"error": "Please enter a message."}), 400
    if len(user_message) > 500:
        return jsonify({"error": "Message must be 500 characters or fewer."}), 400

    return jsonify({"response": chatbot_response(user_message)})


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.errorhandler(413)
def request_too_large(_error):
    return jsonify({"error": "Request is too large."}), 413


if __name__ == "__main__":
    app.run(debug=True)