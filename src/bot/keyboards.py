from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Получить данные по товару")]
    ],
    input_field_placeholder="Нажмите кнопку ниже, чтобы получить данные по товару.",
    resize_keyboard=True
)
