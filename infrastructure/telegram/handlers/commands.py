from aiogram.types import Message
from aiogram import Router
from aiogram.filters import CommandStart, Command
from infrastructure.telegram.bot_answers import start_msg, help_msg

def setup_handlers(router: Router):
    @router.message(CommandStart())
    async def start_message(message: Message):
        await message.answer(text=start_msg,parse_mode="HTML")

    @router.message(Command(commands="help"))
    async def help_message(message: Message):
        await message.answer(text=help_msg, parse_mode="HTML")

    return router