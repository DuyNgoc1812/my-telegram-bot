import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import requests

# Thay API_KEY_ZERMANGO bằng chuỗi ký tự thật từ web Zermango
API_KEY_ZERMANGO = "sk_141319a73c800049894a887a1fb07f8d"
BOT_TOKEN = "8923714024:AAET1b1u4Z0gi-SCVg6IIHwT_mi4gkgTL98"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Chào bạn! Hãy gửi Key để reset HWID.")

async def handle_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_key = update.message.text.strip()
    url = "https://zermango.com/api/seller/reset-hwid"
    
    # Dùng params thay vì headers để tránh lỗi mã hóa và cú pháp
    params = {
        "api_key": API_KEY_ZERMANGO,
        "key": user_key,
        "type": "aimbot"
    }
    
    try:
        response = requests.post(url, data=params, timeout=10)
        await update.message.reply_text(f"Kết quả: {response.text[:200]}")
    except Exception as e:
        await update.message.reply_text(f"Lỗi: {str(e)}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Thêm các handler của bạn ở đây
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_key))
    
    print("Bot đang khởi động...")
    # LƯU Ý: drop_pending_updates=True là chìa khóa để hết lỗi Conflict
    application.run_polling(drop_pending_updates=True)