import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Дані
BOT_TOKEN = os.getenv("BOT_TOKEN")
AUTHORIZED_USER_ID = 384210176
VIDEO_LINK = 'https://t.me/c/1294934054/299430'

# Основний обробник повідомлень
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == AUTHORIZED_USER_ID:
        await update.message.reply_video(video=VIDEO_LINK)  # якщо відео доступне, надсилає як відео
    else:
        await update.message.reply_text("Доступ заборонено.")

# Старт
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Отримуємо URL Render-проєкту
    WEBHOOK_HOST = os.getenv("RENDER_EXTERNAL_URL")
    WEBHOOK_PATH = "/webhook"
    WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

    print(f"Встановлюю Webhook: {WEBHOOK_URL}")
    await app.bot.set_webhook(WEBHOOK_URL)

    await app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8443)),
        webhook_path=WEBHOOK_PATH,
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
