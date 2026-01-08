import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")

if not BOT_TOKEN or not GROUP_CHAT_ID:
    raise ValueError("Переменные окружения BOT_TOKEN или GROUP_CHAT_ID не установлены!")

async def weekly_announcement(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text="Прошу прислать ваши пожелания по графику"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот запущен и работает!")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    # Scheduler
    scheduler = AsyncIOScheduler()
    scheduler.add_job(lambda: asyncio.create_task(weekly_announcement(app.bot)), 'interval', weeks=1)
    scheduler.start()

    print("Bot started...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
