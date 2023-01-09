from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

keyboard = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Нажми, если хочешь внести контакт", callback_data="4"),
    InlineKeyboardButton("Нажми, если хочешь кого-то найти", callback_data="5"),
    InlineKeyboardButton("Нажми, если хочешь посмотреть все контакты", callback_data="6"),
    InlineKeyboardButton("Вернуться в главное меню", callback_data="7"),
)
# but = KeyboardButton("Menu", callback_data="start")
# kb_but = InlineKeyboardMarkup().add(but)
keybd = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Могу быть телефонной книгой", callback_data="1"),
    InlineKeyboardButton("Знаю кое-что про космос + крутое фото дня от NASA", callback_data="2"),
    InlineKeyboardButton("Подскажу, что по погоде", callback_data="3"))

