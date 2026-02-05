from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        symbol = data.get('symbol', 'N/A')
        price = data.get('price', 'N/A')
        msg = f"🚨 TradingView Alert\nSymbol: {symbol}\nPrice: {price}"
        
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={'chat_id': CHAT_ID, 'text': msg})
        
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return "✅ Telegram Bot is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
