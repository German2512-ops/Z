from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! Use /collect to collect data.')

def collect(update: Update, context: CallbackContext) -> None:
    # Example collection and response
    data = {"value": 42}  # Replace with real data collection
    update.message.reply_text(f"Data collected: {data}")

def start_bot():
    updater = Updater("YOUR_TOKEN")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("collect", collect))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    try:
        start_bot()
    except Exception as e:
        print(f"An error occurred in the bot: {e}")