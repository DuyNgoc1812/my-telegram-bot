import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import requests

BOT_TOKEN = "8923714024:AAET1b1u4Z0gi-SCVg6IIHwT_mi4gkgTL98"
API_KEY_ZERMANGO = "sk_141319a73c800049894a887a1fb07f8d"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Chào bạn! Hãy gửi Key của bạn để tôi thực hiện reset HWID.")

async def handle_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_key = update.message.text.strip()
    url = "https://zermango.com/api/seller/reset-hwid"
    params = {"api_key": API_KEY_ZERMANGO, "key": user_key, "type": "aimbot"}
    try:
        response = requests.get(url, params=params).json()
        if response.get("success"):
            await update.message.reply_text(f"✅ Thành công: {response.get('message')}")
        else:
            await update.message.reply_text(f"❌ Lỗi: {response.get('message')}")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Hệ thống đang gặp lỗi: {str(e)}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_key))
    print("Bot đang chạy...")
    application.run_polling()