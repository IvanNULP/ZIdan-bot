import os
from aiohttp import web
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
AUTHORIZED_USER_ID = 384210176
VIDEO_LINK = 'https://t.me/c/1294934054/299430'

# Обробник повідомлень
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == AUTHORIZED_USER_ID:
        await update.message.reply_video(video=VIDEO_LINK)
    else:
        await update.message.reply_text("Доступ заборонено.")

# Основна логіка
async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Створення aiohttp web-серверу
    webhook_path = "/webhook"
    port = int(os.environ.get("PORT", 8443))
    site_url = os.getenv("RENDER_EXTERNAL_URL")  # Наприклад: https://your-service.onrender.com
    webhook_url = f"{site_url}{webhook_path}"

    await app.bot.set_webhook(webhook_url)
    return app

# Запуск aiohttp сервера
if __name__ == '__main__':
    from telegram.ext.webhookhandler import run_webhook
    import asyncio
    asyncio.run(run_webhook(
        main(),
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8443)),
        path="/webhook"
    ))
