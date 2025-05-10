import os

from aiogram import Router

from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from humanfriendly.terminal import message

from infrastructure.file_processing.demucs_separator import DemucsSeparator
from infrastructure.file_processing.faster_whisper_transcriber import FasterWhisperTranscriber
from presentation.telegram.inline_keyboard import return_as_file_keyboard, transform_options_keyboard
from use_cases.demucs_separator_use_case import DemucsSeparatorUseCase
from presentation.telegram.fsm_states import FileProcessing
from domain.entities.file import File
from use_cases.transcribe_audio_use_case import TranscribeAudioUseCase
from infrastructure.file_processing.ffmpeg_audio_converter import FFMpegAudioConverter
from infrastructure.file_processing.ffmpeg_audio_extractor import FFMpegAudioExtractor
from use_cases.extract_audio_from_video_use_case import ExtractAudioFromVideoUseCase
from use_cases.convert_audio_to_wav_use_case import ConvertAudioToWavUseCase

router = Router()

@router.callback_query(lambda f: f.data in ["transcribe", "transform_to_ascii", "remove_bg", "remove_noise", "separate"])
async def handle_file(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    file: File = data.get("file")

    if not file:
        await callback.message.answer(
            text=(
            "<b>Упс!</b>\n\n"
            "Данные к файлу где-то затерялись. "
            "Скинь его снова, пожалуйста 🥺"
            ),
            parse_mode="HTML"
        )
        await state.clear()
        return

    action = callback.data.lower()

    if action == "transcribe":
        await callback.message.answer(
            text=(
                "<b>Отлично!</b>\n\n"
                "Тебе результат скинуть файлом (.txt) или в этом чате (динамично)?"
            ),
            reply_markup=return_as_file_keyboard,
            parse_mode="HTML"
        )

    elif action == "separate":
        await callback.message.edit_reply_markup()
        edit_msg = await callback.message.answer("Минуточку...")
        separator = DemucsSeparator()
        separated_path = await DemucsSeparatorUseCase(separator=separator).separate(file, message=callback.message)

        if separated_path:
            await callback.bot.delete_message(message_id=edit_msg.message_id, chat_id=file.user_id)
            await callback.message.answer_document(FSInputFile(separated_path.joinpath("vocals.mp3")))
            await callback.message.answer_document(FSInputFile(separated_path.joinpath("no_vocals.mp3")))

            os.remove(separated_path)
        else:
            await callback.message.answer("Чёт не получилось извлечь вокал/инструментал из музыки 😬")

    await callback.answer()

@router.callback_query(lambda f: f.data in ['file', 'no_file'])
async def transcribe_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    file: File = data.get("file")
    action = callback.data.lower()

    rm_msg = await callback.message.answer("Минуточку...")
    transcriber = FasterWhisperTranscriber()
    print(action)
    if action == "file":
        result = await TranscribeAudioUseCase(transcriber=transcriber).transcribe(file, message=callback.message, mid=rm_msg.message_id, rafile=True)
        await callback.message.answer_document(FSInputFile(result))
        await callback.bot.delete_message(chat_id=rm_msg.chat.id, message_id=rm_msg.message_id)
    else:
        await TranscribeAudioUseCase(transcriber=transcriber).transcribe(file, message=callback.message, mid=rm_msg.message_id, rafile=False)

    await callback.answer()



