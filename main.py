import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import requests
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция для получения факта о числе
def get_number_fact(number, fact_type="trivia"):
    url = f"http://numbersapi.com/{number}/{fact_type}"
    response = requests.get(url)
    return response.text if response.status_code == 200 else "Факт не найден."

# Функция для получения факта о дате
def get_date_fact(month, day):
    url = f"http://numbersapi.com/{month}/{day}/date"
    response = requests.get(url)
    return response.text if response.status_code == 200 else "Факт о дате не найден."

# Функция для получения факта о годе
def get_year_fact(year):
    url = f"http://numbersapi.com/{year}/year"
    response = requests.get(url)
    return response.text if response.status_code == 200 else "Факт о годе не найден."

# Команда для получения общего факта о числе
@dp.message(Command("fact"))
async def send_number_fact(message: Message):
    try:
        number = int(message.text.split()[1])  # Получаем число от пользователя
        fact = get_number_fact(number)
        await message.answer(fact)
    except (IndexError, ValueError):
        await message.answer("Введите число после команды /fact. Пример: /fact 42")

# Команда для получения математического факта о числе
@dp.message(Command("math"))
async def send_math_fact(message: Message):
    try:
        number = int(message.text.split()[1])
        fact = get_number_fact(number, "math")
        await message.answer(fact)
    except (IndexError, ValueError):
        await message.answer("Введите число после команды /math. Пример: /math 5")

# Команда для получения факта о дате
@dp.message(Command("date"))
async def send_date_fact(message: Message):
    try:
        parts = message.text.split()
        month = int(parts[1])
        day = int(parts[2])
        fact = get_date_fact(month, day)
        await message.answer(fact)
    except (IndexError, ValueError):
        await message.answer("Введите месяц и день после команды /date. Пример: /date 11 12")

# Команда для получения факта о годе
@dp.message(Command("year"))
async def send_year_fact(message: Message):
    try:
        year = int(message.text.split()[1])
        fact = get_year_fact(year)
        await message.answer(fact)
    except (IndexError, ValueError):
        await message.answer("Введите год после команды /year. Пример: /year 1970")

# Команда для получения случайного факта
@dp.message(Command("random"))
async def send_random_fact(message: Message):
    fact_type = message.text.split()[1] if len(message.text.split()) > 1 else "trivia"
    fact = get_number_fact("random", fact_type)
    await message.answer(fact)

# Основная функция для запуска бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
