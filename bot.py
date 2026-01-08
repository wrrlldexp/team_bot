import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, JobQueue

# =========================
# Конфигурация через переменные окружения
# =========================
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")

# Проверка переменных
if not TOKEN:
    raise ValueError("Переменная окружения BOT_TOKEN не установлена!")
if not ADMIN_ID:
    raise ValueError("Переменная окружения ADMIN_ID не установлена!")
if not GROUP_CHAT_ID:
    raise ValueError("Переменная окружения GROUP_CHAT_ID не установлена!")

# Список участников команды (Telegram usernames)
TEAM_IDS = [
    "aipankratova",
    "fohiik",
    "freddiequeen",
    "valhlk",
    "murad_turdiev",
    "Matsuba19",
    "milkatrin19"
]

# =========================
# Команда /start
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот запущен и работает!")

# =========================
# Анонс сообщения (для теста каждые 10 секунд, потом можно неделю)
# =========================
async def weekly_announcement(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(GROUP_CHAT_ID, "Прошу прислать ваши пожелания по графику")

# =========================
# Главная функция
# =========================
def main():
    # Создаём приложение
    app = ApplicationBuilder().token(TOKEN).build()

    # Добавляем обработчик команды /start
    app.add_handler(CommandHandler("start", start))

    # Job Queue для анонса
    job_queue: JobQueue = app.job_queue
    # Тест: каждые 10 секунд. Для продакшена менять на 7*24*3600 секунд
