import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# Стартуємо фейковий HTTP-сервер (для Render)
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive")

def run_http_server():
    port = int(os.environ.get('PORT', 10000))  # Render задає PORT як env
    server = HTTPServer(('', port), SimpleHandler)
    print(f"HTTP-сервер працює на порту {port}")
    server.serve_forever()

# Запускаємо HTTP-сервер у фоновому потоці
threading.Thread(target=run_http_server, daemon=True).start()

# Telegram bot
BOT_TOKEN = os.getenv("BOT_TOKEN")
AUTHORIZED_USER_ID = 384210176
VIDEO_LINK = 'https://t.me/c/1294934054/299430'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == AUTHORIZED_USER_ID:
        await update.message.reply_text(VIDEO_LINK)

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Telegram-бот запущено на Render через polling")
    app.run_polling()
