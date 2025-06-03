from config import BOT_TOKEN

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import MenuButtonWebApp, WebAppInfo
import asyncio
import logging

# Включаем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token= BOT_TOKEN)  # ЗАМЕНИТЕ НА РЕАЛЬНЫЙ ТОКЕН!
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    try:
        logger.info(f"Пользователь {message.from_user.id} запустил бота")
        
        await bot.set_chat_menu_button(
            chat_id=message.chat.id,
            menu_button=MenuButtonWebApp(
                text="📝 Открыть Mini App",
                web_app=WebAppInfo(url="https://colddusssh.github.io/bam/")  # Ваш URL
            )
        )
        await message.answer("Нажмите кнопку меню и отправьте текст из Mini App!")
    except Exception as e:
        logger.error(f"Ошибка в /start: {e}")
        await message.answer("Произошла ошибка :(")

@dp.message(F.web_app_data)
async def handle_web_app_data(message: types.Message):
    try:
        logger.info(f"\n{'='*30}\nПолучено сообщение с WebAppData!")
        logger.info(f"User ID: {message.from_user.id}")
        logger.info(f"Chat ID: {message.chat.id}")
        logger.info(f"Дата сообщения: {message.date}")
        logger.info(f"Данные: {message.web_app_data.data}")
        logger.info(f"Raw message: {message}\n{'='*30}")
        
        await message.answer(
            f"✅ Данные получены!\n"
            f"📝 Текст: {message.web_app_data.data}\n"
            f"⏰ Время: {message.date}"
        )
    except Exception as e:
        logger.error(f"Ошибка обработки WebAppData: {e}")
        await message.answer("Ошибка обработки данных")

async def main():
    logger.info("Запускаем бота...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())