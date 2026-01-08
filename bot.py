import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# --------------------------
# 1️⃣ Получаем переменные окружения
# --------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")

if not BOT_TOKEN or not ADMIN_ID or not GROUP_CHAT_ID:
    raise ValueError("Переменные окружения BOT_TOKEN, ADMIN_ID или GROUP_CHAT_ID не установлены!")

ADMIN_ID = str(ADMIN_ID)  # на всякий случай строка
GROUP_CHAT_ID = str(GROUP_CHAT_ID)

# --------------------------
# 2️⃣ Функция анонса
# --------------------------
async def weekly_announcement(context: CallbackContext):
    """Отправляет сообщение в группу и сохраняет message_id"""
    msg = await context.bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text="Прошу прислать ваши пожелания по графику"
    )
    # Сохраняем message_id в context для дальнейшей проверки
    context.job_data['last_announcement_id'] = msg.message_id

# --------------------------
# 3️⃣ Команда /start
# --------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот запущен и работает!")

# --------------------------
# 4️⃣ Главная функция
# --------------------------
async def main():
    # Создаём приложение бота
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Регистрируем команду /start
    app.add_handler(CommandHandler("start", start))

    # Настраиваем scheduler для анонса каждую неделю
    scheduler = AsyncIOScheduler()
    scheduler.add_job(lambda: asyncio.create_task(weekly_announcement(app.bot)), 'interval', weeks=1)
    scheduler.start()

    print("Bot started...")

    # Запуск бота (поллинг)
    await app.run_polling()

# --------------------------
# 5️⃣ Старт бота
# --------------------------
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print("Ошибка при запуске бота:", e)
