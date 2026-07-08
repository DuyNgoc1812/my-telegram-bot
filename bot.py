from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import requests
import os
import threading

app = Flask(__name__)

# Route giả để Render không tắt bot
@app.route('/')
def home():
    return "Bot is running!"

# Hàm xử lý bot của bạn
TOKEN = "8923714024:AAET1b1u4Z0gi-SCVg6IIHwT_mi4gkgTL98"
API_KEY = "sk_141319a73c800049894a887a1fb07f8d"

async def handle_key(update, context):
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
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_key))
    application.run_polling()

if __name__ == '__main__':
    # Chạy bot trong luồng riêng
    threading.Thread(target=run_bot, daemon=True).start()
    
    # Lấy PORT từ biến môi trường, nếu không có thì mặc định là 8080
    port = int(os.getenv("PORT", 8080))
    app.run(host='0.0.0.0', port=port)