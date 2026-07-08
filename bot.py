import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import requests

# Thay TOKEN của bạn
BOT_TOKEN = "8923714024:AAET1b1u4Z0gi-SCVg6IIHwT_mi4gkgTL98"

async def handle_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_key = update.message.text.strip()
    
    # URL cố định theo đúng cấu trúc bạn đã gửi
    # Lưu ý: Thay API_KEY của bạn vào đây
    url = f"https://zermango.com/api/seller/reset-hwid?api_key=sk_141319a73c800049894a887a1fb07f8d&key={user_key}&type=aimbot"
    
    try:
        # Dùng requests.get là đủ vì đây là URL trực tiếp
        response = requests.get(url, timeout=10)
        
        # Phản hồi lại cho bạn biết
        await update.message.reply_text(f"Kết quả: {response.text}")
            
    except Exception as e:
        await update.message.reply_text(f"Lỗi kết nối: {str(e)}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_key))
    application.run_polling(drop_pending_updates=True)