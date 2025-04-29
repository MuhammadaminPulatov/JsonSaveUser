import asyncio
import logging

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
    name = message.text
    await state.set_state(Registration.phone)
    await message.answer(text="Endi tel nomer jo'nating", reply_markup=get_phone)

@dp.message(Registration.phone)
async def get_name(message: Message, state: FSMContext):
    phone = message.text
    await state.set_state(Registration.age)
    await message.answer(text="Yoahingizni kiriting", reply_markup=ReplyKeyboardRemove())

@dp.message(Registration.age, F.text == "/help")
async def get_name(message: Message, state: FSMContext):
    await message.answer("Example:\n 17")

@dp.message(Registration.age)
async def get_name(message: Message, state: FSMContext):
    age = message.text
    if age.isdigit():
        await state.clear()
        await message.answer(text="Successfully Registration")
    else:
        await message.answer("Siz yosh jo'natishingiz kk")

@dp.message(F.text == "/help")
async def echo_handler(message: Message) -> None:
        await message.answer("Help komandasi")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())