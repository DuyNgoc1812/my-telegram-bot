import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import requests

# Thay TOKEN của bot vào đây
BOT_TOKEN = "DÁN_TOKEN_BOT_TELEGRAM_CỦA_BẠN"

async def handle_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Lấy key người dùng gửi vào
    user_key = update.message.text.strip()
    
    # URL hoàn chỉnh, chỉ thay đổi phần {user_key}
    url = f"https://zermango.com/api/seller/reset-hwid?api_key=sk_141319a73c800049894a887a1fb07f8d&key={user_key}&type=aimbot"
    
    try:
        # Bot giả lập việc truy cập link như trình duyệt của bạn
        response = requests.get(url, timeout=10)
        
        # Phản hồi kết quả cho bạn
        await update.message.reply_text(f"Kết quả từ Zermango:\n{response.text}")
            
    except Exception as e:
        await update.message.reply_text(f"Lỗi: {str(e)}")

# Thêm hàm xử lý lệnh /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Chào bạn! Hãy gửi Key để thực hiện reset HWID.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Handler cho lệnh /start
    application.add_handler(CommandHandler("start", start))
    
    # Handler cho mọi tin nhắn văn bản thông thường
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_key))
    
    application.run_polling(drop_pending_updates=True)