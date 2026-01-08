import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from datetime import datetime

# ====== Переменные окружения ======
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")
ADMIN_ID = os.getenv("ADMIN_ID")

if not BOT_TOKEN or not GROUP_CHAT_ID or not ADMIN_ID:
    raise ValueError("Переменные окружения BOT_TOKEN, GROUP_CHAT_ID или ADMIN_ID не установлены!")

PARTICIPANTS = [
    "@aipankratova",
    "@fohiik",
    "@freddiequeen",
    "@valhlk",
    "@murad_turdiev",
    "@Matsuba19",
    "@milkatrin19"
]

announcement_state = {
    "message_id": None,
    "responded": set()
}

# ====== Команда /announce ======
async def announce_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await context.bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text="Прошу прислать ваши пожелания по графику"
    )
    announcement_state["message_id"] = msg.message_id
    announcement_state["responded"] = set()
    await update.message.reply_text("Анонс отправлен!")

# ====== Обработчик ответов ======
async def reply_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if announcement_state["message_id"] is None:
        return

    username = update.message.from_user.username
    if username in PARTICIPANTS:
        announcement_state["responded"].add(username)

    if announcement_state["responded"] == set(PARTICIPANTS):
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text="Все участники отправили ответы!"
        )
        announcement_state["message_id"] = None
        announcement_state["responded"] = set()

# ====== Еженедельный анонс ======
async def weekly_announcement(context: ContextTypes.DEFAULT_TYPE):
    msg = await context.bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text="Прошу прислать ваши пожелания по графику"
    )
    announcement_state["message_id"] = msg.message_id
    announcement_state["responded"] = set()

# ====== Планировщик ======
async def scheduler(app):
    while True:
        now = datetime.now()
        # Пример: среда 10:00
        if now.weekday() == 2 and now.hour == 10 and now.minute == 0:
            await weekly_announcement(app)
            await asyncio.sleep(60)
        await asyncio.sleep(30)

# ====== Основная функция ======
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("announce", announce_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_handler))

    # Запуск бота
    print("Бот запускается...")
    # Запускаем polling
    await app.initialize()
    await app.start()
    asyncio.create_task(scheduler(app))
    await app.updater.start_polling()  # <-- УБРАТЬ если выдает ошибку, использовать только run_polling
    await app.updater.idle()

# ====== Запуск ======
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
