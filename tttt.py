import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import openai
import time

# Setup OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Setup Telegram bot token
TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Define the start function
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! I am a chatbot powered by OpenAI GPT-3. Send me a message and I will try my best to respond to it.')

# Define the chat function
def chat(update: Update, context: CallbackContext) -> None:
    """Respond to the user's message."""
    message = update.message.text
    logging.info(f"Received message from {update.effective_user.username}: {message}")
    try:
        # Send message to OpenAI's GPT-3 API
        response = openai.Completion.create(
            engine="davinci",
            prompt=(f"User: {message}\nBot:"),
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )
        bot_response = response.choices[0].text
    except Exception as e:
        logging.error(f"Failed to get response from OpenAI: {e}")
        update.message.reply_text("Sorry, I'm having trouble processing your request right now. Please try again later.")
        return

    # Send bot response to user
    update.message.reply_text(bot_response)

# Define the main function
def main() -> None:
    """Run the bot."""
    # Set up the updater
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register the handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, chat))

    # Start the bot
    updater.start_polling()

    # Run the bot until it's stopped
    updater.idle()

if __name__ == '__main__':
    main()
