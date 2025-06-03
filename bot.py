from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.types import MenuButtonWebApp, WebAppInfo, WebAppData
from aiogram.filters import Command
import asyncio
import json
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    # Устанавливаем кнопку меню с Mini App
    await bot.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=MenuButtonWebApp(
            text="Open Mini App",
            web_app=WebAppInfo(url="https://abc123.ngrok.io/index.html")  # Замени на свой URL
        )
    )
    await message.answer("Привет! Нажми кнопку 'Open Mini App' в меню бота.")

@dp.message(F.web_app_data)
async def handle_webapp_data(message: WebAppData):
    data = json.loads(message.web_app_data.data)
    await message.answer(f"Получены данные из Mini App: {data}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())