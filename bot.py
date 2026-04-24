import os
import requests
import time
import threading
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

TOKEN = os.getenv("TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

bot = Bot(token=TOKEN)

def get_price():
    url = "https://api.bybit.com/v5/market/tickers?category=linear&symbol=ETHUSDT"
    data = requests.get(url).json()
    return float(data['result']['list'][0]['lastPrice'])

def build_message():
    price = get_price()
    return f"📊 ETH/USDT\n💰 현재가: {price}"

def send(chat_id):
    bot.send_message(chat_id=chat_id, text=build_message())

def start(update: Update, context: CallbackContext):
    send(update.effective_chat.id)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
