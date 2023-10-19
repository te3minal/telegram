# Import necessary libraries
import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Define your gofiles.io API key (get one from gofiles.io)
GOFILES_API_KEY = 'YOUR_GOFILES_API_KEY'

# Define a function to start the bot
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! I am your Telegram bot. Send me a file, and I will upload it to gofiles.io.")

# Define a function to handle incoming documents (files)
def handle_document(update: Update, context: CallbackContext):
    file_id = update.message.document.file_id
    file = context.bot.get_file(file_id)
    file.download('downloaded_file')

    # Upload the file to gofiles.io
    upload_url = 'https://apiv2.gofile.io/uploadFile'
    files = {'file': open('downloaded_file', 'rb')}
    response = requests.post(upload_url, files=files, headers={'apiKey': GOFILES_API_KEY})

    if response.status_code == 200:
        download_link = response.json().get('data').get('downloadPage')
        update.message.reply_text(f"File uploaded successfully. Download link: {download_link}")
    else:
        update.message.reply_text("File upload failed. Please try again later.")

# Define the main function to start the bot
def main():
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token from BotFather
    updater = Updater(token='6779955678:AAEq0We41p8_jylc4jYx5x6kPGQ-Acnuet0', use_context=True)
    dispatcher = updater.dispatcher

    # Register command and message handlers
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    document_handler = MessageHandler(Filters.document.mime('application/pdf'), handle_document)
    dispatcher.add_handler(document_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
