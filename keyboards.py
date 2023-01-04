from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

keyboard = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Нажми, если хочешь внести контакт", callback_data="1"),
    InlineKeyboardButton("Нажми, если хочешь кого-то найти", callback_data="2"),
    InlineKeyboardButton("Нажми, если хочешь посмотреть все контакты", callback_data="3"),
)
but = KeyboardButton("Menu", callback_data="start")
kb_but = InlineKeyboardMarkup().add(but)
