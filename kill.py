from telegram.ext import ApplicationBuilder, CommandHandler
import asyncio
import sys

TOKEN = "8579753971:AAF4Uu9mbCSiUEydp5YY0RLjSVzt3egHIv8"

async def start(update, context):
    await update.message.reply_text("Бот запущен!")

if __name__ == "__main__":
    # Для Windows обязательно
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Создаём приложение
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("Бот запущен, ожидание команд...")

    # Запускаем polling напрямую, без asyncio.run() и без ручного loop
    app.run_polling()
