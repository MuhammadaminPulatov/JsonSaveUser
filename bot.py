import asyncio
import logging
import json

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from config import TOKEN
from handlers import get_phone

class Registration(StatesGroup):
    name = State()
    phone = State()
    age = State()

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Registration.name)
    await message.answer(text="Ismingizni kiriting")

@dp.message(Registration.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Registration.phone)
    await message.answer(text="Endi tel nomer jo'nating", reply_markup=get_phone)

@dp.message(Registration.phone)
async def get_phone_number(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(Registration.age)
    await message.answer(text="Yoshingizni kiriting", reply_markup=ReplyKeyboardRemove())

@dp.message(Registration.phone)
async def get_phone_number(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(Registration.age)
    await message.answer(text="Yoshingizni kiriting", reply_markup=ReplyKeyboardRemove())

@dp.message(Registration.age, F.text == "/help")
async def help_age(message: Message, state: FSMContext):
    await message.answer("Example:\n17")

@dp.message(Registration.age)
async def get_age(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(age=message.text)

        user_data = await state.get_data()

        try:
            with open('data.json', 'r') as f:
                existing_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = []

        existing_data.append(user_data)

        with open('data.json', 'w') as f:
            json.dump(existing_data, f, indent=4)

        await state.clear()
        await message.answer(text="Successfully")
    else:
        await message.answer("Raqam jonatishingiz kerak")

@dp.message(F.text == "/help")
async def help_handler(message: Message) -> None:
    await message.answer("Help komandasi: Ismingiz, telefon raqamingiz va yoshingizni kiriting.")

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
