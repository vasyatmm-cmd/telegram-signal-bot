import os
import time
from telegram import Bot

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

def send_signal():
    text = (
        "📊 SIGNAL\n\n"
        "Pair: EUR/USD OTC\n"
        "Direction: ⬆️ BUY\n"
        "Timeframe: 30 sec\n\n"
        "⚡️ Automated signal"
    )
    bot.send_message(chat_id=CHAT_ID, text=text)

if __name__ == "__main__":
    while True:
        send_signal()
        time.sleep(180)  # каждые 3 минуты
