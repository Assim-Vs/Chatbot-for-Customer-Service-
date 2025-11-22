
# app/webapp.py

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from chatbot import get_response
from churn_predict import predict_single
import os

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_message = data.get("message", "")
    reply = get_response(user_message)
    return jsonify({"reply": reply})

@app.route("/api/predict_churn", methods=["POST"])
def api_predict_churn():
    payload = request.get_json(force=True)
    result = predict_single(payload)
    return jsonify(result)

if __name__ == "__main__":
    # host='0.0.0.0' if you want external access
    app.run(debug=True, port=5000)

