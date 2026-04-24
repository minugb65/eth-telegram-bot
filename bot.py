import os
import requests
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# 환경변수
TOKEN = os.getenv("TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

bot = Bot(token=TOKEN)

# 30분봉 데이터 (Bybit)
def get_candle():
    url = "https://api.bybit.com/v5/market/kline?category=linear&symbol=ETHUSDT&interval=30&limit=2"
    data = requests.get(url).json()["result"]["list"]
    prev_close = float(data[1][4])
    last_close = float(data[0][4])
    return prev_close, last_close

def make_message():
    prev, last = get_candle()
    diff = last - prev

    if diff > 0:
        trend = "📈 상승"
    elif diff < 0:
        trend = "📉 하락"
    else:
        trend = "➖ 동일"

    return f"{trend}\nETH/USDT\n이전: {prev}\n현재: {last}\n변동: {round(diff, 2)}"

# 메시지 전송
def send(chat_id):
    bot.send_message(chat_id=chat_id, text=make_message())

# /start
def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("🔄 현재 가격", callback_data="price")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("ETH 알림 봇 실행됨", reply_markup=reply_markup)
    send(update.effective_chat.id)

# 버튼 클릭
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=make_message())

# 자동 실행 (30분)
def auto_loop():
    import time
    while True:
        send(int(CHAT_ID))
        time.sleep(1800)

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    import threading
    threading.Thread(target=auto_loop).start()

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
