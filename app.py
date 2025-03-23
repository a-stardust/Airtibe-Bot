from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Replace with your actual bot token from BotFather
TOKEN = "TELEGRAM_BOT_TOKEN"

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hello! I am your Airtribe screening bot. Let's get started!")

def main():
    app = Application.builder().token(TOKEN).build()

    # Start command
    app.add_handler(CommandHandler("start", start))

    # Start the bot
    app.run_polling()

if __name__ == "__main__":
    main()
