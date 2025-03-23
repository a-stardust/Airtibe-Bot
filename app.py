import os
import requests
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import CommandHandler, MessageHandler, filters, ApplicationBuilder

# Load environment variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Set this in Render's Environment Variables
PM_URL = "https://your-pm-service.com/api/messages"  # Replace with PM's API URL

# Initialize Flask app
app = Flask(__name__)

# Initialize Telegram bot
bot = Bot(token=TOKEN)

# Webhook route for Telegram
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    handle_message(update)
    return "OK", 200

# Function to process user messages
def handle_message(update):
    chat_id = update.message.chat_id
    text = update.message.text

    if text.lower() == "/start":
        bot.send_message(chat_id, "Welcome! Please enter your phone number to continue.")
    
    elif text.isdigit() and len(text) >= 10:
        # Send phone number to PM
        response = requests.post(PM_URL, json={"phone": text, "chat_id": chat_id})
        bot.send_message(chat_id, "Thanks! Your request is being processed.")
    
    else:
        bot.send_message(chat_id, "Invalid input. Please enter a valid phone number.")

# Route to send messages from PM to user
@app.route("/send_message", methods=["POST"])
def send_message():
    data = request.json
    chat_id = data.get("chat_id")
    message = data.get("message")

    if chat_id and message:
        bot.send_message(chat_id, message)
        return {"status": "success"}, 200
    else:
        return {"error": "Missing chat_id or message"}, 400

# Set webhook when app starts
@app.route("/set_webhook", methods=["GET"])
def set_webhook():
    webhook_url = f"https://your-render-app.onrender.com/{TOKEN}"  # Replace with your Render URL
    bot.set_webhook(webhook_url)
    return f"Webhook set to {webhook_url}", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
