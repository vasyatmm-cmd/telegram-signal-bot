from flask import Flask, request
import telebot

app = Flask(__name__)

TELEGRAM_TOKEN = "8580386795:AEAEWVjmwGyFYgEJqj7D11rotSTWJ8LiuQ"
CHAT_ID = "-1003864527690"
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.form
    ticker = data.get('ticker', 'N/A')
    price = data.get('price', 'N/A')
    signal = data.get('signal', 'N/A')
    
    message = f"🚨 СИГНАЛ: {signal}\nАктив: {ticker}\nЦена: {price}"
    bot.send_message(CHAT_ID, message)
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
