import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import router
import database as db
from aiogram.client.session.aiohttp import AiohttpSession


async def main():
    logging.basicConfig(level=logging.INFO)
    db.init_db()

    session = AiohttpSession(proxy="socks5://127.0.0.1:10808")

    bot = Bot(token=BOT_TOKEN, session=session)
    dp = Dispatcher()
    dp.include_router(router)

    print("Бот Кафе успешно запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
