import asyncio
from infrastructure.telegram.bot import create_dispatcher

async def main():
    dp, bot = await create_dispatcher()

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())




