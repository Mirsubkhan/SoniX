import uuid
from pathlib import Path

from aiogram import Bot
from aiogram.types import Message

from core.entities.file import FileType
from infrastructure.telegram.inline_keyboard import photo_process_keyboard, video_process_keyboard, \
    audio_process_keyboard

downloads_dir = Path("downloads")
downloads_dir.mkdir(parents=True, exist_ok=True)

FILE_TYPE_MAP = {
    "photo": ("png", FileType.PHOTO),
    "video": ("mp4", FileType.VIDEO),
    "video_note": ("mp4", FileType.VIDEO),
    "voice": ("wav", FileType.AUDIO),
    "audio": ("wav", FileType.AUDIO),
}

KEYBOARD_MAP = {
    FileType.PHOTO: photo_process_keyboard,
    FileType.VIDEO: video_process_keyboard,
    FileType.AUDIO: audio_process_keyboard
}

class TelegramFileWorker:
    @staticmethod
    async def download_file(bot: Bot, file_id, file_format: str) -> Path:
        file = await bot.get_file(file_id=file_id)

        dest = downloads_dir / f"{uuid.uuid4().hex}.{file_format}"
        dest = dest.absolute()

        await bot.download_file(file.file_path, destination=dest)

        return dest

    @staticmethod
    async def detect_file_type(message: Message):
        for attr, (f_format, f_type) in FILE_TYPE_MAP.items():
            if getattr(message, attr, None):
                return f_format, f_type

    @staticmethod
    async def return_keyboard(file_type: FileType):
        return KEYBOARD_MAP[file_type]