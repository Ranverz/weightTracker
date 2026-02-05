import asyncio
import json
import logging

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from psycopg import connect

from bot.app.config import BotConfig
from bot.app.logging_config import configure_logging

logger = logging.getLogger(__name__)

config = BotConfig.from_env()
bot = Bot(token=config.bot_token)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: types.Message):
    kb = [
        [types.KeyboardButton(
            text="Открыть приложение",
            web_app=types.WebAppInfo(url=f"{config.webapp_url}/miniapp")
        )]
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )

    await message.answer("Отройте мини-апп через синюю кнопку снизу")


@dp.message(F.web_app_data)
async def webapp_data(message: types.Message):

    data = json.loads(message.web_app_data.data)
    weight = float(data["weight"])

    # Сохраняем в базу
    with connect(config.database_url) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO weights(user_id, weight)
                VALUES (%s, %s)
            """, (message.from_user.id, weight))
            conn.commit()

    await message.answer(f"Вес сохранён: {weight} кг")


async def main():
    configure_logging()
    logger.info("Bot started...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
