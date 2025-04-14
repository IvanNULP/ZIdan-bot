import os
from aiohttp import web
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
AUTHORIZED_USER_ID = 412991871
VIDEO_PATH = "IMG_5922.MOV"

# Обробник повідомлень
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        print("Отримано update без повідомлення")
        return
    if update.effective_user and update.effective_user.id == AUTHORIZED_USER_ID:
        print(f"✅ Повідомлення від дозволеного користувача: {update.effective_user.id}")
        with open(VIDEO_PATH, "rb") as video_file:
            await update.message.reply_video(video=video_file)

# Ініціалізація Telegram-бота
application = ApplicationBuilder().token(BOT_TOKEN).build()
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# aiohttp веб-додаток
app = web.Application()

# Встановлення webhook під час запуску
async def on_startup(app: web.Application):
    await application.initialize()
    webhook_url = os.getenv("RENDER_EXTERNAL_URL") + "/webhook"
    await application.bot.set_webhook(webhook_url)
    print(f"📡 Webhook встановлено: {webhook_url}")
    app["application"] = application

# Обробка запитів Telegram
async def handle_webhook(request: web.Request):
    data = await request.json()
    print("🔔 Отримано запит на /webhook:")
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return web.Response()

app.router.add_post("/webhook", handle_webhook)
app.on_startup.append(on_startup)

# Запуск сервера
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Запуск сервера на порту {port}")
    web.run_app(app, host="0.0.0.0", port=port)
