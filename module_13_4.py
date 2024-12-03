from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram import Router
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

TOKEN = ''

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

router = Router()
dp.include_router(router)

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.")

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@router.message(Command("calories"))
async def set_age(message: Message, state: FSMContext):
    await message.answer("Введите свой возраст:")
    await state.set_state(UserState.age)

@router.message(UserState.age)
async def set_growth(message: Message, state: FSMContext):
    try:
        age = int(message.text)
        if age <= 0:
            raise ValueError("Возраст должен быть положительным числом.")
        await state.update_data(age=age)
        await message.answer("Введите свой рост (в см):")
        await state.set_state(UserState.growth)
    except ValueError:
        await message.answer("Пожалуйста, введите корректный возраст (число больше 0).")


@router.message(UserState.growth)
async def set_weight(message: Message, state: FSMContext):
    try:
        growth = int(message.text)
        if growth <= 0:
            raise ValueError("Рост должен быть положительным числом.")
        await state.update_data(growth=growth)
        await message.answer("Введите свой вес (в кг):")
        await state.set_state(UserState.weight)
    except ValueError:
        await message.answer("Пожалуйста, введите корректный рост (число больше 0).")

@router.message(UserState.weight)
async def send_calories(message: Message, state: FSMContext):
    try:
        weight = int(message.text)
        if weight <= 0:
            raise ValueError("Вес должен быть положительным числом.")
        await state.update_data(weight=weight)

        data = await state.get_data()
        age = data['age']
        growth = data['growth']
        weight = data['weight']

        calories = 10 * weight + 6.25 * growth - 5 * age + 5

        await message.answer(f"Ваша норма калорий: {calories:.2f} ккал.")

        await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введите корректный вес (число больше 0).")

@router.message()
async def fallback_handler(message: Message):

    await message.answer("Я пока не понимаю это сообщение. Напишите /calories, чтобы начать.")

async def main():
    print("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



