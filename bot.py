from config import BOT_TOKEN

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import MenuButtonWebApp, WebAppInfo
import sqlite3
import json
import asyncio

# Настройка бота
bot = Bot(token= BOT_TOKEN)
dp = Dispatcher()

# Создаем БД SQLite
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id INTEGER,
            data TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Обработчик /start - устанавливает кнопку Mini App
@dp.message(Command("start"))
async def start(message: types.Message):
    await bot.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=MenuButtonWebApp(
            text="Open Mini App",
            web_app=WebAppInfo(url="https://colddusssh.github.io/bam/")  # Замените на ваш URL
        )
    )
    await message.answer("Нажмите кнопку ниже, чтобы открыть Mini App!")

# Обработчик данных из Mini App
@dp.message(F.web_app_data)
async def handle_web_app_data(message: types.Message):
    user_id = message.from_user.id
    data = message.web_app_data.data  # Данные в формате JSON
    
    # Сохраняем в SQLite
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_data (user_id, data) VALUES (?, ?)", (user_id, data))
    conn.commit()
    conn.close()
    
    await message.answer(f"✅ Данные сохранены: {data}")

# Запуск бота
async def main():
    init_db()  # Инициализация БД
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())