import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# Отримуємо токен з середовища (а не прописуємо напряму!)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Телеграм user_id дозволеного користувача
AUTHORIZED_USER_ID = 384210176  # Заміни на реального користувача

# Посилання на відео, яке бот надсилає у відповідь
VIDEO_LINK = 'https://t.me/c/1294934054/299430'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == AUTHORIZED_USER_ID:
        await update.message.reply_text(VIDEO_LINK)

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущено на Render...")
    app.run_polling()
