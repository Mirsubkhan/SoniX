from aiogram.types import Message
from aiogram import Router
from aiogram.filters import CommandStart, Command

router = Router()

@router.message(CommandStart())
async def start_message(message: Message):
    await message.answer(
        text=(
            "<b>Приветствую! 🤝</b>\n\n"
            "Я бот, который умеет обрабатывать мультимедийные файлы 😎 "
            "<b>Больше подробностей по команде /help</b>\n<i>P.S. <span class='tg-spoiler'>Ток не ленись пж 😊</span></i>"
        ),
        parse_mode="HTML"
    )

@router.message(Command(commands="help"))
async def help_message(message: Message):
    await message.answer(
        text=(
            "<b>Вот он! Человек, который решил всё таки прочитать документацию к использованию бота 😏</b>\n\n"
            "<blockquote><b>Что я умею? 🤔</b></blockquote>\n"
            "1. Извлекать текст из аудио, видео, голосовых сообщений и видео кружков;\n"
            "2. Разделять музыку на вокал и инструментал (минсусовка);\n"
            "3. Удалять фон из фото;\n"
            "4. Удалять шум из аудио;\n"
            "5. Трансформировать видео и фото в ASCII арт\n\n"
            "<blockquote><b>Какие файлы поддерживаются? 🤔</b></blockquote>\n"
            "Я принимаю только: <b>аудио, голосовые сообщения, видео, видео-кружки и фото.</b>\n\n"
            "<b>Вот видишь как просто? А ты не хотел читать 😉</b>"
        ),
        parse_mode="HTML"
    )