from flask import Flask, request
import telebot
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    message = data.get("message", "Без сообщения")
    bot.send_message(CHAT_ID, message)
    return "OK"

@app.route("/", methods=["GET"])
def index():
    return "Bot is alive"

if __name__ == "__main__":
    app.run()
