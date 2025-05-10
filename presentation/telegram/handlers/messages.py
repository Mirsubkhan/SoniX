import logging
import os
import traceback
from datetime import timedelta
from pathlib import Path

from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from presentation.telegram.inline_keyboard import video_process_keyboard, photo_process_keyboard, audio_process_keyboard
from presentation.telegram.fsm_states import FileProcessing
from domain.entities.file import File, FileType

router = Router()

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

async def _download_file(bot: Bot, file_id, file_format: str) -> Path:
    file = await bot.get_file(file_id=file_id)

    dest = downloads_dir / f"{file.file_id}.{file_format}"
    dest = dest.absolute()

    # print(f"Downloading file to: {dest}")
    await bot.download_file(file.file_path, destination=dest)

    return dest

async def _detect_file_type(message: Message):
    for attr, (fformat, ftype) in FILE_TYPE_MAP.items():
        if getattr(message, attr, None):
            return fformat, ftype

async def _return_keyboard(file_type: FileType):
    return KEYBOARD_MAP[file_type]

@router.message(lambda m: m.video or m.audio or m.video_note or m.voice or m.photo)
async def media_handler(message: Message, state: FSMContext):
    message_file = message.audio or message.video or message.voice or message.video_note

    rm_message = await message.answer(text="<i>Гружу файл...👍</i>", parse_mode="HTML")

    try:
        file_id = message.photo[-1].file_id if message.photo else message_file.file_id
        file_format, file_type = await _detect_file_type(message)
        file_path = await _download_file(message.bot, file_id=file_id, file_format=file_format)
    except Exception as e:
        traceback.print_exc()
        logging.exception("Error")
        await message.answer("Пупупу...Здесь ошибка при скачивании файла 😓\nПопробуй заново 🥺")
        return


    file = File(
        user_id=message.from_user.id,
        file_id=file_id,
        file_path=file_path,
        file_type=file_type,
        file_format=file_format,
        file_duration=timedelta(seconds=0 if message.photo else message_file.duration)
    )

    print(f"{file.file_id}\n{file.file_path}\n{file.file_type}\n{file.file_format}\n{file.user_id}\n{file.file_duration}")

    await state.set_state(FileProcessing.file_received)
    await state.update_data(file=file)

    await message.bot.delete_message(message_id=rm_message.message_id, chat_id=message.from_user.id)
    await message.answer(
        text="<b>Готово! Что хочешь сделать с файлом? 😏👇</b>",
        reply_markup=await _return_keyboard(file.file_type),
        parse_mode="HTML"
    )

@router.message(lambda m: not m.video and not m.video_note and not m.voice and not m.photo and not m.audio and not m.text)
async def warn_message(message: Message):
    await message.answer(
        text=(
            "<b>Упс! 😬</b>\n\n"
            "Проверь, что файл и его формат поддерживаются мною. Я принимаю только:\n"
            "<b>Аудио, голосовые сообщения, видео, видео-кружки и фото.</b>"
        ),
        parse_mode="HTML"
    )


# if file.file_type == FileType.AUDIO or file.file_format != "wav":
#     old_path = file.file_path
#
#     if file.file_type == FileType.VIDEO:
#         audio_extractor = FFMpegAudioExtractor()
#         file.file_path = await ExtractAudioFromVideoUseCase(audio_extractor).extract(file)
#         file.file_type = FileType.AUDIO
#
#     if file.file_format != "wav":
#         audio_converter = FFMpegAudioConverter()
#         file.file_path = await ConvertAudioToWavUseCase(audio_converter).convert(file)
#
#     os.remove(old_path)