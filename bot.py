from config import BOT_TOKEN

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import MenuButtonWebApp, WebAppInfo
import sqlite3
import asyncio

# Настройка бота
bot = Bot(token =BOT_TOKEN)  # Замените на реальный токен!
dp = Dispatcher()

# Инициализация БД (теперь с проверкой)
def init_db():
    try:
        conn = sqlite3.connect("database.db", check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        print("✅ База данных готова!")
    except Exception as e:
        print(f"❌ Ошибка при создании БД: {e}")
    finally:
        conn.close()

# Команда /start
@dp.message(Command("start"))
async def start(message: types.Message):
    try:
        await bot.set_chat_menu_button(
            chat_id=message.chat.id,
            menu_button=MenuButtonWebApp(
                text="📝 Добавить заметку",
                web_app=WebAppInfo(url="https://colddusssh.github.io/bam/")  # Замените URL!
            )
        )
        await message.answer("Нажмите кнопку ниже, чтобы открыть Mini App!")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

# Обработка данных из Mini App
@dp.message(F.web_app_data)
async def handle_web_app_data(message: types.Message):
    try:
        user_id = message.from_user.id
        text = message.web_app_data.data
        
        conn = sqlite3.connect("database.db", check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user_notes (user_id, text) VALUES (?, ?)",
            (user_id, text)
        )
        conn.commit()
        
        # Проверяем запись
        cursor.execute(
            "SELECT text, created_at FROM user_notes WHERE user_id = ? ORDER BY id DESC LIMIT 1",
            (user_id,)
        )
        last_note = cursor.fetchone()
        conn.close()
        
        if last_note:
            await message.answer(
                f"✅ Заметка сохранена!\n"
                f"📄 Текст: {last_note[0]}\n"
                f"⏰ Время: {last_note[1]}"
            )
        else:
            await message.answer("❌ Не удалось сохранить заметку.")
    except Exception as e:
        await message.answer(f"Ошибка при сохранении: {e}")

# Запуск
async def main():
    init_db()
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())