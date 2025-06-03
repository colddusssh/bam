from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import MenuButtonWebApp, WebAppInfo
import asyncio

bot = Bot(token="YOUR_BOT_TOKEN")  # Замените на реальный токен!
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    try:
        await bot.set_chat_menu_button(
            chat_id=message.chat.id,
            menu_button=MenuButtonWebApp(
                text="📝 Открыть Mini App",
                web_app=WebAppInfo(url="https://your-vercel-app.vercel.app")  # Ваш URL
            )
        )
        await message.answer("Нажмите кнопку меню, чтобы открыть Mini App!")
    except Exception as e:
        print(f"Ошибка: {e}")

@dp.message(F.web_app_data)
async def handle_web_app_data(message: types.Message):
    user_id = message.from_user.id
    text = message.web_app_data.data
    
    # Вместо сохранения в БД - вывод в консоль
    print("\n" + "="*30)
    print(f"Данные от пользователя {user_id}:")
    print(f"Текст: {text}")
    print(f"Время: {message.date}")  # Время получения сообщения
    print("="*30 + "\n")
    
    await message.answer(f"✅ Данные получены! Проверьте консоль.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())