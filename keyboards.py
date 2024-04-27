from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from filters import Course


def choose_keyboard():
    choose_markup = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(
            text='1 курс', callback_data=Course(name='1 курс').pack()),
        InlineKeyboardButton(
            text='2 курс', callback_data=Course(name='2 курс').pack())
    ]
    for elem in buttons:
        choose_markup.row(elem)
    return choose_markup.as_markup()
