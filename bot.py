import logging
import os
import threading
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import requests

# Cấu hình bot
BOT_TOKEN = "8923714024:AAET1b1u4Z0gi-SCVg6IIHwT_mi4gkgTL98"
API_KEY_ZERMANGO = "sk_141319a73c800049894a887a1fb07f8d"

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Web server giả lập để Render nhận diện dịch vụ
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

def run_web_server():
    # Sử dụng cổng từ biến môi trường hoặc mặc định là 10000
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# Các hàm của Bot
async def start(update, context):
    await update.message.reply_text("Chào bạn! Hãy gửi Key để reset HWID.")

async def handle_key(update, context):
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
        await update.message.reply_text(f"⚠️ Lỗi hệ thống: {str(e)}")

if __name__ == '__main__':
    # Chạy Web Server trong luồng riêng
    threading.Thread(target=run_web_server).start()
    
    # Cấu hình và chạy Bot
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_key))
    
    print("Bot đang chạy...")
    application.run_polling()