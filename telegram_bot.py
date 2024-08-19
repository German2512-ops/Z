import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler

from text_processing import preprocess_text
from data_analysis import analyze_data
import matplotlib.pyplot as plt
from collections import Counter
import datetime

# Enable logging for debugging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.FileHandler('bot.log', encoding='utf-8'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

async def error_handler(update: Update, context: CallbackContext) -> None:
    """Логирует исключения, вызванные обработчиками."""
    logger.error("Exception while handling an update:", exc_info=context.error)

# Function to send a daily report
def daily_update(context: CallbackContext):
    job = context.job
    chat_id = job.context
    context.bot.send_message(chat_id=chat_id, text='Your daily report is ready!')

def schedule_daily(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    context.job_queue.run_daily(daily_update, time=datetime.time(8, 0, 0), context=chat_id)
    update.message.reply_text('You have subscribed to daily reports at 8:00 AM.')

# Generate a sentiment analysis plot
def generate_sentiment_plot(sentiments):
    labels, counts = zip(*Counter(sentiments).items())
    plt.figure(figsize=(10, 6))
    plt.bar(labels, counts, color='blue')
    plt.title('Sentiment Analysis')
    plt.savefig('sentiment_plot.png')
    plt.close()
    return 'sentiment_plot.png'

# Start message function
async def start(update: Update, context: CallbackContext) -> None:
    reply_keyboard = [['BTC', 'ETH'], ['XRP', 'LTC']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text('Welcome! I am a data analysis bot.My creater Herman Maksimov! Select a cryptocurrency:', reply_markup=markup)

# Analyze function to process user input
def analyze(update: Update, context: CallbackContext) -> None:
    from data_collection import collect_data  # Импорт внутри функции
    user_input = update.message.text.split()


    if len(user_input) != 2:
        update.message.reply_text('Please enter two parameters: cryptocurrency name and date (YYYY-MM-DD).')
        return

    currency, date = user_input
    update.message.reply_text(f'Collecting data for {currency} on {date}...')

    if ',' in currency:
        currencies = currency.split(',')
        for curr in currencies:
            raw_data = collect_data(curr.strip(), date)
            processed_data = preprocess_text(raw_data)
            analysis_results = analyze_data(processed_data)
            
            sentiment_plot = generate_sentiment_plot(analysis_results['sentiment'][curr.strip()])
            update.message.reply_photo(photo=open(sentiment_plot, 'rb'))

    else:
        raw_data = collect_data(currency, date)
        update.message.reply_text('Data collected. Starting preprocessing...')
        
        processed_data = preprocess_text(raw_data)
        update.message.reply_text('Preprocessing complete. Starting data analysis...')
        
        analysis_results = analyze_data(processed_data)
        
        response = "Sentiment analysis results:\\n"
        for source, sentiments in analysis_results['sentiment'].items():
            response += f"{source}: {Counter(sentiments)}\\n"
        
        response += "\\nKeywords:\\n"
        for source, keywords in analysis_results['keywords'].items():
            response += f"{source}: {', '.join(keywords)}\\n"
        
        update.message.reply_text(response)

        # Send plot
        sentiment_plot = generate_sentiment_plot(analysis_results['sentiment'][currency])
        update.message.reply_photo(photo=open(sentiment_plot, 'rb'))

# Command to change language
def set_language(update: Update, context: CallbackContext):
    user_lang = context.args[0]
    if user_lang in ['ru', 'en', 'es']:
        context.user_data['language'] = user_lang
        update.message.reply_text(f'Language set to {user_lang}.')
    else:
        update.message.reply_text('Supported languages are ru, en, and es.')

# Function to handle feedback from users
def feedback(update: Update, context: CallbackContext):
    feedback_text = ' '.join(context.args)
    update.message.reply_text('Thank you for your feedback!')
    # Here you can save or send the feedback for further analysis

# Error handling function
def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f'Update {update} caused error {context.error}')

def main():
    application = Application.builder().token("5824572723:AAGCCXn9pWrS8BLzS7eiMmCvG6G5DvWicZw").build()

    application.add_handler(CommandHandler("start", start))

    application.add_error_handler(error_handler)

    application.run_polling()

    dispatcher = application.dispatcher
    
    # Command /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Command /setlang
    dispatcher.add_handler(CommandHandler('setlang', set_language))

    # Command /feedback
    dispatcher.add_handler(CommandHandler('feedback', feedback))
    
    # Schedule daily reports
    dispatcher.add_handler(CommandHandler('daily', schedule_daily))
    
    # Handle text messages
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, analyze))
    
    # Log all errors
    dispatcher.add_error_handler(error)
    
    # Start the Bot
    updater.start_polling()
    
    updater.idle()

if __name__ == '__main__':
    main()