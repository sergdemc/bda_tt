from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Получить данные по товару")]
    ],
    input_field_placeholder="Нажмите кнопку ниже, чтобы получить данные по товару.",
    resize_keyboard=True
)


# def get_product_keyboard() -> InlineKeyboardMarkup:
#     return InlineKeyboardMarkup(
#         inline_keyboard=[
#             [InlineKeyboardButton(text="Получить данные по товару", callback_data="get_product")]
#         ]
#     )

