import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

bot_enabled = False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global bot_enabled
    bot_enabled = True
    await update.message.reply_text("▶️ Bot started")


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global bot_enabled
    bot_enabled = False
    await update.message.reply_text("⏹ Bot stopped")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))

    app.run_polling()


if __name__ == "__main__":
    main()
