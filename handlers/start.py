from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📘 Обучение", callback_data='learning')],
        [InlineKeyboardButton("📝 Экзамен", callback_data='ekzamen')],
        [InlineKeyboardButton("📊 Топ экзамена", callback_data='exam_top')],
        [InlineKeyboardButton("📊Топ недели", callback_data='weekly_top')],
        [InlineKeyboardButton("⭐ Задача недели", callback_data="weekly_task")],
        [InlineKeyboardButton("💯 Отзывы", callback_data='show_feedback')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text("Здравствуйте! Выберите раздел:", reply_markup=reply_markup)
    else:
        await update.callback_query.message.reply_text("Здравствуйте! Выберите раздел:", reply_markup=reply_markup)
