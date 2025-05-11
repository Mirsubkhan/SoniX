import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from aiogram.fsm.storage.memory import MemoryStorage
from infrastructure.telegram.handlers import messages, callbacks, commands
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp import ClientTimeout

timeout = ClientTimeout(total=60)
session = AiohttpSession(timeout=60)

async def on_shutdown(dp: Dispatcher):
    await dp.storage.close()
    await session.close()

async def main():
    load_dotenv()

    bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'), session=session)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(
        commands.router,
        messages.router,
        callbacks.router
    )
    dp.shutdown.register(on_shutdown)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
