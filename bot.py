import os
import asyncio
import ccxt
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, JobQueue

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")  # ID вашей группы/чата

# Глобальные переменные
bot_enabled = False
job_queue = None

# Подключение к бирже (например, Binance)
exchange = ccxt.binance({
    'enableRateLimit': True,
})

async def analyze_market():
    """Анализирует рынок и определяет сигналы"""
    try:
        # Получаем данные BTC/USDT
        ticker = exchange.fetch_ticker('BTC/USDT')
        ohlcv = exchange.fetch_ohlcv('BTC/USDT', '5m', limit=50)
        
        # Извлекаем цены закрытия
        closes = [candle[4] for candle in ohlcv]
        
        # Рассчитываем индикаторы (простой пример)
        ema_fast = sum(closes[-9:]) / 9 if len(closes) >= 9 else closes[-1]
        ema_slow = sum(closes[-21:]) / 21 if len(closes) >= 21 else closes[-1]
        current_price = closes[-1]
        
        # Логика сигналов (пример)
        signal = None
        if current_price > ema_fast > ema_slow:
            signal = "🟢 BUY BTC/USDT"
        elif current_price < ema_fast < ema_slow:
            signal = "🔴 SELL BTC/USDT"
        
        return signal, current_price
        
    except Exception as e:
        print(f"Ошибка анализа: {e}")
        return None, None

async def send_signal(context: ContextTypes.DEFAULT_TYPE):
    """Отправляет сигнал если бот включен"""
    global bot_enabled
    
    if not bot_enabled:
        return
    
    signal, price = await analyze_market()
    
    if signal:
        message = f"""
📊 **СИГНАЛ** 📊
{signal}
💰 Цена: ${price:,.2f}
🕐 Время: {datetime.now().strftime('%H:%M:%S')}
"""
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text=message,
            parse_mode='Markdown'
        )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start - включает бота и запускает проверку"""
    global bot_enabled, job_queue
    
    if not bot_enabled:
        bot_enabled = True
        
        # Запускаем периодическую проверку (каждые 5 минут)
        if job_queue is None:
            job_queue = context.job_queue
            job_queue.run_repeating(
                send_signal, 
                interval=300,  # 5 минут в секундах
                first=10       # Первая проверка через 10 секунд
            )
        
        await update.message.reply_text(
            "✅ **Бот включен!**\n"
            "Автоматическая проверка сигналов каждые 5 минут.\n"
            "Используйте /stop для выключения."
        )
    else:
        await update.message.reply_text("⚠️ Бот уже включен!")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /stop - выключает бота"""
    global bot_enabled
    
    if bot_enabled:
        bot_enabled = False
        
        # Останавливаем все задачи
        if context.job_queue:
            context.job_queue.stop()
        
        await update.message.reply_text(
            "⏸ **Бот выключен!**\n"
            "Используйте /start для повторного включения."
        )
    else:
        await update.message.reply_text("⚠️ Бот уже выключен!")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /status - статус бота"""
    global bot_enabled
    
    status_text = "🟢 ВКЛЮЧЕН" if bot_enabled else "🔴 ВЫКЛЮЧЕН"
    
    # Получаем последний сигнал
    signal, price = await analyze_market()
    
    response = f"""
📊 **СТАТУС БОТА**
Состояние: {status_text}
Последняя цена BTC: ${price:,.2f if price else 'N/A'}
Последний сигнал: {signal if signal else 'Нет сигнала'}
Используйте /start или /stop для управления.
"""
    await update.message.reply_text(response)

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /signal - ручная проверка сигнала"""
    signal, price = await analyze_market()
    
    if signal:
        message = f"""
📊 **РУЧНАЯ ПРОВЕРКА**
{signal}
💰 Цена: ${price:,.2f}
"""
        await update.message.reply_text(message)
    else:
        await update.message.reply_text("📈 Нет сигналов для торговли")

def main():
    app = Application.builder().token(TOKEN).build()
    
    # Добавляем обработчики команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("signal", signal))
    
    print("🤖 Бот запускается...")
    app.run_polling()

if __name__ == "__main__":
    main()
