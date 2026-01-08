import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# -------------------------
# 1️⃣ Переменные окружения
# -------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")
ADMIN_ID = os.getenv("ADMIN_ID")

if not BOT_TOKEN or not GROUP_CHAT_ID or not ADMIN_ID:
    raise ValueError("Переменные окружения BOT_TOKEN, GROUP_CHAT_ID или ADMIN_ID не установлены!")

# -------------------------
# 2️⃣ Функция анонса
# -------------------------
async def weekly_announcement(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text="Прошу прислать ваши пожелания по графику"
    )

# -------------------------
# 3️⃣ Команда /start
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот запущен и работает!")

# -------------------------
# 4️⃣ Главная функция
# -------------------------
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Регистрируем команду /start
    app.add_handler(CommandHandler("start", start))

    # Scheduler для анонса каждую неделю
    scheduler = AsyncIOScheduler()
    scheduler.add_job(lambda: asyncio.create_task(weekly_announcement(app.bot)), 'interval', weeks=1)
    scheduler.start()

    print("Bot started...")

    # Запуск бота
    await app.run_polling()

# -------------------------
# 5️⃣ Старт
# -------------------------
if __name__ == "__main__":
    asyncio.run(main())
