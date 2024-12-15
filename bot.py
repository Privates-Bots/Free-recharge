import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from flask import Flask, request

# Hardcoded Bot Token (Not recommended for production)
BOT_TOKEN = "7527990182:AAH6qYNs_UteKYi7KZ0jeMOT_d2I_ZEViEw"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

app = Flask(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hi! Welcome to my simple bot.')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

# Initialize bot
application = ApplicationBuilder().token(BOT_TOKEN).build()

start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

application.add_handler(start_handler)
application.add_handler(echo_handler)

# Set up your Flask route (this will be used by Vercel to handle requests)
@app.route('/')
def index():
    return "Bot is running!"

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
