import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import requests
import os
from flask import Flask
import threading

# CẤU HÌNH TOKEN (Lấy từ BotFather)
TOKEN = "8923714024:AAET1b1u4Z0gi-SCVg6IIHwT_mi4gkgTL98" # Thay Token của bạn vào đây
API_KEY = "sk_141319a73c800049894a887a1fb07f8d"

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Chào bạn! Hãy nhập mã Key của bạn.")

async def handle_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_key = update.message.text.strip()
    if user_key.startswith('/'): return
    
    url = "https://zermango.com/api/seller/reset-hwid"
    params = {"api_key": API_KEY, "key": user_key, "type": "aimbot"}
    
    try:
        res = requests.get(url, params=params, timeout=5)
        await update.message.reply_text(f"Kết quả: {res.text}")
    except Exception as e:
        await update.message.reply_text(f"Lỗi: {str(e)}")

def run_bot():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_key))
    application.run_polling()

if __name__ == '__main__':
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)