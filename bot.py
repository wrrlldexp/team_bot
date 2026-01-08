import json
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import TOKEN, ADMIN_ID, GROUP_CHAT_ID, TEAM_IDS

STORAGE_FILE = "storage.json"

# -------------------------------
# Работа с состоянием
# -------------------------------
def load_storage():
    with open(STORAGE_FILE, "r") as f:
        return json.load(f)

def save_storage(data):
    with open(STORAGE_FILE, "w") as f:
        json.dump(data, f)

# -------------------------------
# Отправка еженедельного анонса
# -------------------------------
async def weekly_announcement(context: ContextTypes.DEFAULT_TYPE):
    storage = load_storage()
    msg = await context.bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text="Прошу прислать ваши пожелания по графику"
    )
    storage["message_id"] = msg.message_id
    storage["responded"] = []
    storage["completed"] = False
    save_storage(storage)

# -------------------------------
# Обработка ответов участников
# -------------------------------
async def handle_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.reply_to_message:
        return

    username = update.message.from_user.username
    chat_id = update.message.chat.id

    # Проверка: сообщение в нужной группе и не от админа
    if chat_id != GROUP_CHAT_ID and chat_id != ADMIN_ID:
        return
    if username == ADMIN_ID:
        return

    storage = load_storage()
    if storage.get("completed"):
        return

    # Проверяем, что сообщение отвечает на анонс
    if update.message.reply_to_message.message_id != storage.get("message_id"):
        return

    # Проверяем, что пользователь в команде
    if username not in TEAM_IDS:
        return

    # Проверяем, что ещё не отвечал
    if username in storage.get("responded", []):
        return

    storage["responded"].append(username)
    save_storage(storage)

    # Если все ответили — уведомляем админа
    if set(storage["responded"]) == set(TEAM_IDS):
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text="Все участники команды ответили на анонс ✅"
        )
        storage["completed"] = True
        save_storage(storage)

# -------------------------------
# Основная функция запуска бота
# -------------------------------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    loop = asyncio.get_event_loop()
    scheduler = AsyncIOScheduler(event_loop=loop)
    scheduler.add_job(
        weekly_announcement,
        "cron",
        day_of_week="wed",  # каждую среду
        hour=10,
        minute=0,
        args=[app.bot]
    )
    scheduler.start()

    app.add_handler(MessageHandler(filters.ALL, handle_reply))

    app.run_polling()

if __name__ == "__main__":
    main()

