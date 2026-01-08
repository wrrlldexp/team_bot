import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, JobQueue

# Конфиг через переменные окружения
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")

TEAM_IDS = [
    "aipankratova",
    "fohiik",
    "freddiequeen",
    "valhlk",
    "murad_turdiev",
    "Matsuba19",
    "milkatrin19"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот запущен и работает!")

async def weekly_announcement(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(GROUP_CHAT_ID, "Прошу прислать ваши пожелания по графику")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    job_queue: JobQueue = app.job_queue
    # Тест: каждые 10 секунд (для продакшена изменить на неделю)
    job_queue.run_repeating(weekly_announcement, interval=10, first=5)

    app.run_polling()

if __name__ == "__main__":
    main()
