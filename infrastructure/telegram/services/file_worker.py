from config import FILE_TYPE_MAP, KEYBOARD_MAP, EXTENSION_MAP, SUPPORTED_DOCUMENTS
from core.entities.file import FileType, File
from aiogram.types import Message
from datetime import timedelta
from pathlib import Path
from aiogram import Bot
import uuid


class TelegramFileWorker:
    def __init__(self):
        self.downloads_dir = Path("downloads").resolve()
        self.downloads_dir.mkdir(parents=True, exist_ok=True)

    async def download_file(self, bot: Bot, file_id, file_format: str) -> Path:
        file = await bot.get_file(file_id=file_id)
        dest = (self.downloads_dir / f"{uuid.uuid4().hex}.{file_format}").resolve()

        await bot.download_file(file.file_path, destination=dest)
        return dest

    @staticmethod
    async def detect_file_type(message: Message):
        for attr, (f_format, f_type) in FILE_TYPE_MAP.items():
            if getattr(message, attr, None):
                return f_format, f_type

        if message.document:
            mime = message.document.mime_type
            if mime in SUPPORTED_DOCUMENTS:
                return EXTENSION_MAP[mime], FileType.PHOTO

        if message.sticker:
            return "webp", FileType.PHOTO

    @staticmethod
    async def return_keyboard(file_type: FileType):
        return KEYBOARD_MAP[file_type]

    async def get_message_file(self, message: Message):
        message_file = (
                message.audio or message.video or message.voice or
                message.video_note or message.photo or message.document or
                message.sticker
        )

        if message.photo:
            file_duration = None
            file_id = message.photo[-1].file_id
        elif message.document:
            file_duration = None
            file_id = message.document.file_id
        else:
            if message.sticker:
                file_duration = None
            else:
                file_duration = timedelta(seconds=message_file.duration)
            file_id = message_file.file_id

        file_format, file_type = await self.detect_file_type(message)
        file_path = await self.download_file(message.bot, file_id=file_id, file_format=file_format)

        return File(
            user_id=message.from_user.id,
            message_id=None,
            file_id=file_id,
            file_path=file_path,
            file_type=file_type,
            file_format=file_format,
            file_duration=file_duration
        )