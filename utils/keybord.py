from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_keyboard_with_back(buttons):
    keyboard = buttons[:]
    keyboard.append([InlineKeyboardButton('Назад', callback_data='back')])
    return InlineKeyboardMarkup(keyboard)