import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from datetime import datetime

# ====== Настройка переменных окружения ======
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")
ADMIN_ID = os.getenv("ADMIN_ID")

if not BOT_TOKEN or not GROUP_CHAT_ID or not ADMIN_ID:
    raise ValueError("Переменные окружения BOT_TOKEN, GROUP_CHAT_ID или ADMIN_ID не установлены!")

# ====== Список участников (кто должен ответить) ======
PARTICIPANTS = [
    "@aipankratova",
    "@fohiik",
    "@freddiequeen",
    "@valhlk",
    "@murad_turdiev",
    "@Matsuba19",
    "@milkatrin19"
]

# Состояние текущего анонса
announcement_state = {
    "message_id": None,
    "responded": set()
}

# ====== Команда для ручного запуска анонса ======
async def announce_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await context.bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text="Прошу прислать ваши пожелания по графику"
    )
    announcement_state["message_id"] = msg.message_id
    announcement_state["responded"] = set()
    await update.message.reply_text("Анонс отправлен!")

# ====== Отслеживание ответов участников ======
async def reply_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if announcement_state["message_id"] is None:
        return  # Анонс ещё не был отправлен

    username = update.message.from_user.username
    if username in PARTICIPANTS:
        announcement_state["responded"].add(username)

    # Проверка, все ли ответили (кроме админа)
    if announcement_state["responded"] == set(PARTICIPANTS):
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text="Все участники отправили ответы!"
        )
        # Сбрасываем состояние
        announcement_state["message_id"] = None
        announcement_state["responded"] = set()

# ====== Еженедельный анонс (пример) ======
async def weekly_announcement(context: ContextTypes.DEFAULT_TYPE):
    msg = await context.bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text="Прошу прислать ваши пожелания по графику"
    )
    announcement_state["message_id"] = msg.message_id
    announcement_state["responded"] = set()

# ====== Планировщик для Railway ======
async def scheduler(app):
    while True:
        now = datetime.now()
        # Если сегодня среда и время 10:00 утра (пример)
        if now.weekday() == 2 and now.hour == 10 and now.minute == 0:
            await weekly_announcement(app)
            await asyncio.sleep(60)  # ждем минуту, чтобы не отправить несколько раз
        await asyncio.sleep(30)  # проверяем каждые 30 секунд

# ====== Основная функция ======
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Команды и обработчики
    app.add_handler(CommandHandler("announce", announce_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_handler))

    # Запуск бота
    await app.start()
    print("Бот запущен!")

    # Запуск планировщика
    asyncio.create_task(scheduler(app))

    await app.updater.start_polling()
    await app.updater.idle()

# ====== Старт ======
if __name__ == "__main__":
    asyncio.run(main())
