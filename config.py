from infrastructure.telegram.inline_keyboard import photo_process_keyboard, video_process_keyboard, audio_process_keyboard
from core.entities.file import FileType
from typing import Callable, Awaitable
from aiogram import F


STTCallback = Callable[[int], Awaitable[None]]
DynamicSSTCallback = Callable[[str, bool], Awaitable[None]]
SeparatorProgressCallback = Callable[[int], Awaitable[None]]

SUPPORTED_DOCUMENTS = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/jpg",
    "image/heif",
    "image/svg",
    "image/avif"
}

EXTENSION_MAP = {
    "image/jpeg": "jpeg",
    "image/png": "png",
    "image/webp": "webp",
    "image/avif": "avif",
    "image/heif": "heif",
    "image/svg": "svg",
    "image/jpg": "jpg"
}

sticker_condition = (
    F.sticker
    & (F.sticker.is_video == False)
    & (F.sticker.is_animated == False)
)

media_filter = (
        F.video |
        F.audio |
        F.video_note |
        F.voice |
        F.photo |
        sticker_condition |
        (F.document & F.document.mime_type.in_(SUPPORTED_DOCUMENTS))
)
not_supported_filter = ~media_filter

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

