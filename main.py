from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# Вставь токен от BotFather
BOT_TOKEN = '8068457846:AAFn2T1xdzUswHhMWwwWVMBhA6tDd_U6qIs'

# Реальный Telegram user_id пользователя, которому разрешено писать
AUTHORIZED_USER_ID = 384210176

# Ссылка на видео
VIDEO_LINK = 'https://t.me/c/1294934054/299430'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == AUTHORIZED_USER_ID:
        await update.message.reply_text(VIDEO_LINK)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Бот запущен...")
app.run_polling()
