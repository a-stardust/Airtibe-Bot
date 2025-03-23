from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Replace with your actual Telegram Bot Token
TELEGRAM_BOT_TOKEN = "7800035843:AAFDh2mK3ZczP5GeXRqW3VEUyeQBU1pJNxg"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{7800035843:AAFDh2mK3ZczP5GeXRqW3VEUyeQBU1pJNxg}/sendMessage"

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json  # Receiving JSON data from PM
    phone = data.get("phone")
    message = data.get("message")

    if not phone or not message:
        return jsonify({"error": "Missing phone or message"}), 400

    # Send message to the candidate (Replace `phone` with `chat_id` from PM)
    send_telegram_message(phone, message)

    return jsonify({"status": "Message sent"}), 200

def send_telegram_message(chat_id, text):
    """Send a message to Telegram using the Bot API."""
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(TELEGRAM_API_URL, json=payload)
    return response.json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
