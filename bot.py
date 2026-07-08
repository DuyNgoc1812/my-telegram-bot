import os
import asyncio
import threading
import requests
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# CẤU HÌNH
TOKEN = "8923714024:AAET1b1u4Z0gi-SCVg6IIHwT_mi4gkgTL98"
API_KEY = "sk_141319a73c800049894a887a1fb07f8d"

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Chào bạn! Hãy nhập mã Key của bạn.")

async def handle_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_key = update.message.text.strip()
    if user_key.startswith('/'): return
    
    url = "https://zermango.com/api/seller/reset-hwid"
    params = {"api_key": API_KEY, "key": user_key, "type": "aimbot"}
    
    # Thêm Header giả lập trình duyệt Chrome để đánh lừa Cloudflare
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://zermango.com/"
    }
    
    try:
        # Sử dụng thêm headers vào lệnh request
        res = requests.get(url, params=params, headers=headers, timeout=10)
        
        # Kiểm tra xem có bị Cloudflare chặn không (trả về HTML thay vì nội dung)
        if "cloudflare" in res.text.lower() or "<title>Just a moment...</title>" in res.text:
            await update.message.reply_text("Lỗi: Server Zermango đang chặn kết nối từ Bot. Vui lòng thử lại sau.")
        else:
            # Nếu thành công, gửi kết quả
            response_text = res.text
            if len(response_text) > 4000:
                for i in range(0, len(response_text), 4000):
                    await update.message.reply_text(response_text[i:i+4000])
            else:
                await update.message.reply_text(f"Kết quả: {response_text}")
            
    except Exception as e:
        await update.message.reply_text(f"Lỗi kết nối: {str(e)}")

async def main():
    # Khởi động Flask trong luồng phụ
    threading.Thread(target=run_flask, daemon=True).start()
    
    # Khởi tạo và chạy bot ở luồng chính
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_key))
    
    print("Bot đang chạy...")
    await application.initialize()
    await application.start()
    await application.updater.start_polling(drop_pending_updates=True)
    
    # Giữ chương trình chạy
    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())