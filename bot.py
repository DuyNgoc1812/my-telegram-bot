import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import requests

# DÁN TOKEN THẬT CỦA BẠN VÀO ĐÂY (Lấy từ @BotFather)
TOKEN = "8923714024:AAET1b1u4Z0gi-SCVg6IIHwT_mi4gkgTL98" 
API_KEY = "sk_141319a73c800049894a887a1fb07f8d"

# Hàm xử lý lệnh /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Chào bạn! Hãy nhập mã Key của bạn để tôi thực hiện reset HWID.")

# Hàm xử lý khi người dùng nhập mã Key
async def handle_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_key = update.message.text.strip()
    if user_key.startswith('/'):
        return

    base_url = "https://zermango.com/api/seller/reset-hwid"
    params = {"api_key": API_KEY, "key": user_key, "type": "aimbot"}
    
    await update.message.reply_text("Đang xử lý, vui lòng đợi trong giây lát...")
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        await update.message.reply_text(f"Kết quả từ Zermango:\n{response.text}")
    except Exception as e:
        await update.message.reply_text(f"Lỗi hệ thống: {str(e)}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_key))
    
    print("Bot đã sẵn sàng và đang lắng nghe...")
    application.run_polling(drop_pending_updates=True)