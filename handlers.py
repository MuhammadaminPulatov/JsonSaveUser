from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

get_phone = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Raqam jo'natish", request_contact=True)]
    ],
    resize_keyboard=True
)