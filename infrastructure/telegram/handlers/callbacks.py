import os
from aiogram import Router
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from redis.asyncio import Redis

from application.use_cases.ffmpeg_audio_extractor_use_case import FFMpegAudioExtractorUseCase
from application.use_cases.redis_use_case import RedisUseCase
from core.entities.file_dto import FileInputDTO
from core.ports.audio_extractor import AudioExtractor
from core.ports.audio_separator import AudioSeparator
from core.ports.audio_transcriber import AudioTranscriber
from core.ports.file_storage import FileStorage
from core.ports.photo_style_converter import PhotoStyleConverter
from infrastructure.telegram.bot_answers import data_lost, transcribe_options, listening_file, demucs_error, \
    ascii_options, ascii_wait_message, ascii_ready, transcribe_ready
from infrastructure.telegram.services.progress_bar import TelegramProgressBarRenderer
from infrastructure.telegram.inline_keyboard import return_as_file_keyboard, transform_options_keyboard
from application.use_cases.demucs_separator_use_case import DemucsSeparatorUseCase
from application.use_cases.ascii_converter_use_case import AsciiConverterUseCase
from application.use_cases.faster_whisper_transcriber_use_case import TranscribeAudioUseCase

def setup_handlers(
        router: Router,
        transcriber: AudioTranscriber,
        extractor: AudioExtractor,
        photo_style_converter: PhotoStyleConverter,
        separator: AudioSeparator,
        progress_bar: TelegramProgressBarRenderer,
        client: FileStorage
):
    @router.callback_query(lambda f: f.data in ["transcribe", "transform_to_ascii", "remove_bg", "remove_noise", "separate"])
    async def handle_file(callback: CallbackQuery):
        await callback.message.delete()
        await callback.answer()

        redis = RedisUseCase(redis=client)
        file = await redis.get_file_by_uid(user_id=callback.message.from_user.id)

        if not file:
            await callback.message.answer(text=data_lost, parse_mode="HTML")
            return

        action = callback.data.lower()

        if action == "transcribe":
            await callback.message.answer(
                text=transcribe_options,
                reply_markup=return_as_file_keyboard,
                parse_mode="HTML"
            )

        elif action == "separate":
            await callback.message.edit_reply_markup()
            edit_msg = await callback.message.answer(listening_file, parse_mode="HTML")
            progress_bar.bot = callback.bot
            progress_bar.message_id = edit_msg.message_id
            progress_bar.chat_id = callback.message.chat.id
            file_input = FileInputDTO(file_path=file.file_path, file_duration=file.file_duration, file_type=file.file_type)
            file_output = await DemucsSeparatorUseCase(separator=separator).separate(file_input, on_progress=progress_bar.demucs_progress_callback)

            if file_output:
                await callback.message.answer_document(FSInputFile(file_output.file_path.joinpath("vocals.mp3")))
                await callback.message.answer_document(FSInputFile(file_output.file_path.joinpath("no_vocals.mp3")))
                await callback.bot.delete_message(message_id=edit_msg.message_id, chat_id=callback.message.chat.id)

                await redis.delete_file_by_uid(user_id=callback.message.from_user.id)
            else:
                await callback.message.answer(demucs_error)

        elif action == "transform_to_ascii":
            await callback.message.answer(
                text=ascii_options,
                reply_markup=transform_options_keyboard,
                parse_mode="HTML"
            )


    @router.callback_query(lambda f: f.data in ['file', 'no_file'])
    async def transcribe_callback(callback: CallbackQuery):
        await callback.message.delete()
        await callback.answer()

        redis = RedisUseCase(redis=client)
        file = await redis.get_file_by_uid(user_id=callback.message.from_user.id)
        action = callback.data.lower()

        edit_msg = await callback.message.answer(text=listening_file, parse_mode="HTML")
        progress_bar.bot = callback.bot
        progress_bar.message_id = edit_msg.message_id
        progress_bar.chat_id = callback.message.chat.id

        if action == "file":
            file_output = await TranscribeAudioUseCase(transcriber=transcriber, extractor=FFMpegAudioExtractorUseCase(extractor=extractor)).transcribe(file, on_progress=progress_bar.static_whisper_progress_callback)
            await callback.message.answer_document(FSInputFile(file_output.file_path), caption=transcribe_ready, parse_mode="HTML")
            await callback.bot.delete_message(chat_id=edit_msg.chat.id, message_id=edit_msg.message_id)
        else:
            await TranscribeAudioUseCase(transcriber=transcriber, extractor=FFMpegAudioExtractorUseCase(extractor=extractor)).transcribe_dynamic(file, on_progress=progress_bar.dynamic_whisper_progress_callback)

        await redis.delete_file_by_uid(user_id=callback.message.from_user.id)

    @router.callback_query(lambda f: f.data in ("color", "no_color"))
    async def convert_to_ascii_callback(callback: CallbackQuery):
        await callback.message.delete()
        await callback.answer()

        redis = RedisUseCase(redis=client)
        file = await redis.get_file_by_uid(user_id=callback.message.from_user.id)
        action = callback.data.lower()

        edit_msg = await callback.message.answer(ascii_wait_message, parse_mode="HTML")
        progress_bar.bot = callback.bot
        progress_bar.message_id = edit_msg.message_id
        progress_bar.chat_id = callback.message.chat.id

        file_output = await AsciiConverterUseCase(converter=photo_style_converter).convert(file_input=file, add_color=True if action == "color" else False)

        await callback.message.answer_document(FSInputFile(file_output.file_path), caption=ascii_ready, parse_mode="HTML")
        await callback.bot.delete_message(chat_id=edit_msg.chat.id, message_id=edit_msg.message_id)
        await redis.delete_file_by_uid(user_id=callback.message.from_user.id)

    return router