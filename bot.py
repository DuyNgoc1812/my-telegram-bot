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
    
    # Sử dụng 'params' thay vì 'headers' để truyền API Key
    # Đây là cách URL trong tài liệu Zermango hiển thị (có dấu ?)
    params = {
        "api_key": sk_141319a73c800049894a887a1fb07f8d,
        "key": user_key,
        "type": "aimbot"
    }
    
    try:
        # Gửi request
        response = requests.post(url, data=params, timeout=10)
        
        # Gửi phản hồi lại Telegram để bạn biết chuyện gì đang xảy ra
        await update.message.reply_text(f"Trạng thái: {response.status_code}\nNội dung: {response.text[:100]}")
            
    except Exception as e:
        await update.message.reply_text(f"Lỗi kết nối: {str(e)}")

# --- CHẠY BOT ---
# ... code cũ của bạn
if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    # ... add handlers ...
    
    print("Bot đang chạy...")
    # Thêm dòng này để ép xóa các phiên kết nối bị treo
    application.run_polling(drop_pending_updates=True)