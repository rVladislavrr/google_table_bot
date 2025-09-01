from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def main_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="/start"),
    )
    builder.row(
        KeyboardButton(text="/config"),
        KeyboardButton(text="/help"),
    )
    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

def cancel_kb():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="❌ Отмена"))
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def ready_kb():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="✅ Готово"))
    builder.add(KeyboardButton(text="❌ Отмена"))
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

