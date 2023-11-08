import logging
import sqlite3
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext, CallbackQueryHandler
from decouple import AutoConfig
import Library

#Load config file
config = AutoConfig('.env')

# Initialize the Telegram Bot
updater = Updater(token=config('kindle_this_token'), use_context=True)
dispatcher = updater.dispatcher

# Enable logging for debugging purposes
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Define states for the conversation
SET_KINDLE_EMAIL, SEARCH_BOOK = range(2)

# Dictionary to store user Kindle email addresses
user_kindle_emails = {}

#Method that refreshes the user_kindle_emails dict with the ones in the database
def copy_data_from_database_to_dictionary():
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    cursor.execute("SELECT user_id, kindle_email FROM users")
    rows = cursor.fetchall()
    connection.close()
    for row in rows:
        user_id, kindle_email = row
        user_kindle_emails[user_id] = kindle_email
copy_data_from_database_to_dictionary()

#Method that sets the email of certain user_id in the database
def set_email_to_db(user, email):
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    cursor.execute("INSERT OR REPLACE INTO users (user_id, kindle_email) VALUES (?, ?)", (user, email))
    connection.commit()
    connection.close()

# Command handler to start the bot
def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in user_kindle_emails:
        update.message.reply_text("Welcome to kindleThis Bot! Please use /set_kindle_email to set your Kindle email address.")
    else:
        update.message.reply_text("Welcome back! You can now use /search to start searching for books.")

# Command handler to set Kindle email
def set_kindle_email(update: Update, context: CallbackContext):
    update.message.reply_text("Please enter your Kindle email address.")
    return SET_KINDLE_EMAIL

# Function to save Kindle email address and move to the search state
def save_kindle_email(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    email = update.message.text
    set_email_to_db(user_id, email)
    copy_data_from_database_to_dictionary()
    update.message.reply_text("Kindle email address set to: " + update.message.text)
    update.message.reply_text("Remember to add green.panda.3.1415@gmail.com as a trusted email account on your kindle page preferences")
    update.message.reply_text("You can now use /search to start searching for books.")
    return SEARCH_BOOK  # Move to the SEARCH_BOOK state

# Command handler to search for books
def search(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    copy_data_from_database_to_dictionary()
    if user_id not in user_kindle_emails:
        update.message.reply_text("Please set your Kindle email address using /set_kindle_email before searching for books.")
        return SET_KINDLE_EMAIL  # Go back to SET_KINDLE_EMAIL state
    update.message.reply_text("Please enter the book title and author, separated by a semicolon (e.g., 'Book Title; Author').")
    return SEARCH_BOOK

# Define a message handler for receiving the book query
def receive_book_query(update: Update, context: CallbackContext):
    try:
        book_query = update.message.text
        # You can implement additional validation and formatting for the book query if needed

        # Call your existing script with the book_query and user's Kindle email
        user_id = update.message.from_user.id
        kindle_email = user_kindle_emails.get(user_id)
        if kindle_email:
            book_data = Library.getBookDataFromQuery(book_query)
            book_name = book_data[0]
            update.message.reply_text("Searching for " + book_data[0] + " from " + book_data[1])
            try:
                result = False
                result = Library.searchAndDownload(book_data)
            except:
                update.message.reply_text("There was an error while seeking for your book, y soporta panzona")
            if result:
                update.message.reply_text("'" + book_data[0] + " found!")
                update.message.reply_text("Sending the book to your Kindle...")
                try:
                    if Library.sendToKindle(book_name, kindle_email):
                        update.message.reply_text("Done! '" + book_data[0] + "' from '" + book_data[1] + "' was sent to " + kindle_email)
                        update.message.reply_text("I want to remind you that this is illegal, we both are probably going to jail ):")
                    else:
                        update.message.reply_text("Couldn't send it")
                except:
                    update.message.reply_text("There was an error while sending it, y soporta panzona")
            else:
                update.message.reply_text("Couldn't find the book, try another one... or just go and pay for it, you know, like a decent human being.")           
        else:
            update.message.reply_text("Please set your Kindle email address using /set_kindle_email before searching for books.")
    except Exception as e:
        update.message.reply_text(f"An error occurred: {str(e)}")

# Error handler
def error(update: Update, context: CallbackContext):
    logging.error(f"Update '{update}' caused error '{context.error}'")

# Create a ConversationHandler for setting Kindle email
kindle_email_conversation = ConversationHandler(
    entry_points=[CommandHandler("start", start), CommandHandler("search", search), CommandHandler("set_kindle_email", set_kindle_email)],
    states={
        SET_KINDLE_EMAIL: [MessageHandler(Filters.text & ~Filters.command, save_kindle_email)],
        SEARCH_BOOK: [MessageHandler(Filters.text & ~Filters.command, receive_book_query)]
    },
    fallbacks=[]
)
# Set up command and message handlers and conversation handler
dispatcher.add_handler(kindle_email_conversation)
dispatcher.add_error_handler(error)

# Start the bot
updater.start_polling()

# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
updater.idle()
