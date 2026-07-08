import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import requests

# --- CẤU HÌNH ---
# Thay TOKEN của bot và API_KEY của Zermango vào đây
BOT_TOKEN = "8923714024:AAET1b1u4Z0gi-SCVg6IIHwT_mi4gkgTL98"
API_KEY_ZERMANGO = "sk_141319a73c800049894a887a1fb07f8d"

# --- LOGGING ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- CÁC HÀM XỬ LÝ ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot đã sẵn sàng. Hãy gửi Key để thực hiện lệnh.")

async def handle_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_key = update.message.text.strip()
    url = "https://zermango.com/api/seller/reset-hwid"
    
    # Phần này sẽ chứa tham số gửi đi
    params = {
        "api_key": sk_141319a73c800049894a887a1fb07f8d,
        "key": user_key,
        "type": "aimbot"
    }
    
    try:
        # Gửi request tới Zermango
        response = requests.post(url, data=params, timeout=10)
        
        # Phản hồi kết quả cho người dùng
        if response.status_code == 200:
            await update.message.reply_text(f"Phản hồi từ API: {response.text[:200]}")
        else:
            await update.message.reply_text(f"Lỗi API (Mã {response.status_code}): {response.text[:100]}")
            
    except Exception as e:
        await update.message.reply_text(f"Lỗi hệ thống: {str(e)[:100]}")

# --- CHẠY BOT ---
if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_key))
    
    print("Bot đang khởi động...")
    application.run_polling(drop_pending_updates=True)