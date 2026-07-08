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
    try:
        user_key = update.message.text.strip()
        url = "https://zermango.com/api/seller/reset-hwid"
        
        headers = {
            "x-api-key": "DÁN_KEY_CỦA_BẠN_VÀO_ĐÂY", 
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
        payload = {"key": user_key, "type": "aimbot"}
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        # Chỉ lấy 200 ký tự đầu tiên để tránh lỗi "Message too long"
        short_response = response.text[:200] 
        
        if response.status_code == 200:
            await update.message.reply_text(f"✅ Kết quả API: {short_response}")
        else:
            await update.message.reply_text(f"⚠️ Lỗi {response.status_code}: {short_response}")
            
    except Exception as e:
        await update.message.reply_text(f"⚠️ Lỗi hệ thống: {str(e)[:100]}")

if __name__ == '__main__':
    # Chạy Web Server trong luồng riêng
    threading.Thread(target=run_web_server, daemon=True).start()
    
    # Cấu hình và chạy Bot
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_key))
    
    print("Bot đang chạy...")
    # Thêm drop_pending_updates=True để xóa các phiên kết nối cũ
    application.run_polling(drop_pending_updates=True)