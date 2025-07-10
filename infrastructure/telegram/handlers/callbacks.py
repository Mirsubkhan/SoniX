import asyncio
import shutil
from pathlib import Path

from aiogram import Router
from aiogram.types import CallbackQuery, FSInputFile, InlineKeyboardMarkup
from application.use_cases.audio_extractor_use_case import AudioExtractorUseCase
from application.use_cases.file_handler_use_case import FileHandlerUseCase
from application.use_cases.image2text_use_case import Image2TextUseCase
from application.use_cases.file_storage_use_case import FileStorageUseCase
from application.use_cases.bg_remover_use_case import BgRemoverUseCase
from application.use_cases.image_upscaler_use_case import ImageUpscalerUseCase
from core.entities.file import FileType, File
from core.entities.file_dto import FileInputDTO
from core.ports.audio_extractor import AudioExtractor
from core.ports.audio_separator import AudioSeparator
from core.ports.audio_transcriber import AudioTranscriber
from core.ports.bg_remover import BgRemover
from core.ports.file_handler import FileHandler
from core.ports.file_storage import FileStorage
from core.ports.image2text import Image2Text
from core.ports.image_upscaler import ImageUpscaler
from core.ports.art_converter import ArtConverter
from infrastructure.telegram.bot_answers import data_lost, transcribe_options, listening_file, demucs_error, \
    ascii_options, ascii_wait_message, ascii_ready, transcribe_ready, removing_bg, ocr_error, bg_error, extracting_text, \
    upscaling, realesrgan_error, transcribe_options2
from infrastructure.telegram.services.progress_bar import TelegramProgressBarRenderer
from infrastructure.telegram.inline_keyboard import return_as_file_keyboard, transform_options_keyboard, \
    transcribe_separate_options_keyboard
from application.use_cases.audio_separator_use_case import AudioSeparatorUseCase
from application.use_cases.ascii_converter_use_case import ASCIIConverterUseCase
from application.use_cases.audio_transcriber_use_case import AudioTranscriberUseCase


def setup_handlers(
        router: Router,
        transcriber: AudioTranscriber,
        extractor: AudioExtractor,
        ascii_converter: ArtConverter,
        separator: AudioSeparator,
        progress_bar: TelegramProgressBarRenderer,
        bg_remover: BgRemover,
        image_text_extractor: Image2Text,
        upscaler: ImageUpscaler,
        file_handler: FileHandler,
        client: FileStorage
) -> Router:
    async def get_file_safe(callback: CallbackQuery, full: bool = False):
        redis = FileStorageUseCase(redis=client)
        file = await redis.get_file_by_uid(user_id=callback.from_user.id, full=full)

        if not file:
            await callback.message.answer(text=data_lost, parse_mode="HTML")
            return None, redis
        return file, redis
    async def send_message(callback: CallbackQuery, text: str, keyboard: InlineKeyboardMarkup = None):
        return await callback.message.answer(
            text=text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )

    async def transcribe_demucs_process(redis, file: File, callback: CallbackQuery, event: str):
        folder_path = None
        if event == "transcribe_with_demucs":
            folder_path = await handle_separate(callback=callback, file=file, event="", redis=redis)
            if folder_path:
                new_file_path = folder_path / "vocals.mp3"
                if new_file_path.exists():
                    file = File(
                        file_id="",
                        message_id=callback.message.message_id,
                        file_path=new_file_path,
                        file_format=".mp3",
                        file_type=FileType.AUDIO,
                        user_id=file.user_id,
                        file_duration=file.file_duration
                    )
                    await redis.save(file=file)

        await callback.message.answer(
            text=transcribe_options2,
            reply_markup=return_as_file_keyboard,
            parse_mode="HTML"
        )
    async def transcribe_whisper(redis, file: File, callback: CallbackQuery, return_as_txt: bool):
        edit_msg = await callback.message.answer(text=listening_file, parse_mode="HTML")
        progress_bar.bot = callback.bot
        progress_bar.message_id = edit_msg.message_id
        progress_bar.chat_id = callback.message.chat.id
        file_input = FileInputDTO(file_path=file.file_path, file_duration=file.file_duration, file_type=file.file_type)

        if return_as_txt:
            file_output = await AudioTranscriberUseCase(
                transcriber=transcriber,
                extractor=AudioExtractorUseCase(extractor=extractor),
                f_handler=FileHandlerUseCase(file_repo=file_handler)
            ).transcribe(file_input, on_progress=progress_bar.static_whisper_progress_callback)

            await callback.message.answer_document(
                FSInputFile(file_output.file_path),
                caption=transcribe_ready,
                parse_mode="HTML"
            )
            await callback.bot.delete_message(chat_id=edit_msg.chat.id, message_id=edit_msg.message_id)
            return file_output.file_path
        else:
            await AudioTranscriberUseCase(
                transcriber=transcriber,
                extractor=AudioExtractorUseCase(extractor=extractor),
                f_handler=FileHandlerUseCase(file_repo=file_handler)
            ).transcribe_dynamic(
                file_input,
                on_progress=progress_bar.dynamic_whisper_progress_callback
            )
            await callback.message.answer("<b>Транскрипция готова! ☝️</b>", parse_mode="HTML")
            return None
    async def handle_separate(redis, file: File, callback: CallbackQuery, event: str = ""):
        edit_msg = await callback.message.answer(listening_file, parse_mode="HTML")

        progress_bar.bot = callback.bot
        progress_bar.message_id = edit_msg.message_id
        progress_bar.chat_id = callback.message.chat.id
        file_input = FileInputDTO(file_path=file.file_path, file_duration=file.file_duration, file_type=file.file_type)
        file_output = await AudioSeparatorUseCase(
            separator=separator,
            extractor=AudioExtractorUseCase(extractor=extractor)
        ).separate(
            file_input, on_progress=progress_bar.demucs_progress_callback
        )

        await callback.bot.delete_message(message_id=edit_msg.message_id, chat_id=callback.message.chat.id)

        if not file_output:
            await callback.message.answer(demucs_error)
            return None

        if event in ("no_vocals.mp3", "vocals.mp3"):
            target_file = file_output.file_path / event
            if target_file.exists():
                await callback.message.answer_document(FSInputFile(target_file))
                return file_output.file_path
            return None

        return file_output.file_path
    async def process_remove_bg(redis, callback: CallbackQuery, file: File):
        edit_msg = await callback.message.answer(removing_bg, parse_mode="HTML")
        file_input = FileInputDTO(file_path=file.file_path, file_duration=file.file_duration,
                                  file_type=file.file_type)
        file_output = await BgRemoverUseCase(
            remover=bg_remover,
            f_handler=FileHandlerUseCase(file_repo=file_handler)
        ).remove_bg(f_input=file_input)

        if file_output:
            await callback.message.answer_document(FSInputFile(file_output.file_path))
            await callback.bot.delete_message(message_id=edit_msg.message_id, chat_id=callback.message.chat.id)
            return file_output.file_path
        else:
            await callback.message.answer(bg_error)
            return None
    async def process_ocr(redis, callback: CallbackQuery, file: File):
        edit_msg = await callback.message.answer(extracting_text, parse_mode="HTML")
        file_input = FileInputDTO(file_path=file.file_path, file_duration=file.file_duration,
                                  file_type=file.file_type)
        file_output = await Image2TextUseCase(
            converter=image_text_extractor,
            file_handler=FileHandlerUseCase(file_repo=file_handler)
        ).image_to_text(f_input=file_input)

        if file_output:
            await callback.message.answer(text=f"{str(file_output.file_txt)}")
            await callback.message.answer_document(
                caption="<b>Также для любителей файлов — результат в текстовом формате:</b>",
                document=FSInputFile(file_output.file_path),
                parse_mode="HTML"
            )
            await callback.bot.delete_message(message_id=edit_msg.message_id, chat_id=callback.message.chat.id)
            return file_output.file_path
        else:
            await callback.message.answer(ocr_error)
            return None
    async def process_image_upscaling(redis, callback: CallbackQuery, file: File):
        edit_msg = await callback.message.answer(upscaling, parse_mode="HTML")
        file_input = FileInputDTO(file_path=file.file_path, file_duration=file.file_duration,
                                  file_type=file.file_type)
        file_output = await ImageUpscalerUseCase(
            upscaler=upscaler,
            file_handler=FileHandlerUseCase(file_repo=file_handler)
        ).upscale(file=file_input)

        if file_output:
            await callback.message.answer_document(FSInputFile(file_output.file_path))
            await callback.bot.delete_message(message_id=edit_msg.message_id, chat_id=callback.message.chat.id)
            return file_output.file_path
        else:
            await callback.message.answer(realesrgan_error)
            return None
    async def process_ascii(redis, callback: CallbackQuery, file: File):
        char_width = int(callback.data.split(":")[1].lower())
        file_input = FileInputDTO(file_path=file.file_path, file_duration=file.file_duration,
                                  file_type=file.file_type)

        edit_msg = await callback.message.answer(ascii_wait_message, parse_mode="HTML")
        progress_bar.bot = callback.bot
        progress_bar.message_id = edit_msg.message_id
        progress_bar.chat_id = callback.message.chat.id

        file_output = await ASCIIConverterUseCase(
            converter=ascii_converter,
            file_handler=FileHandlerUseCase(file_repo=file_handler)
        ).convert(f_input=file_input, char_width=char_width)

        await callback.message.answer_document(FSInputFile(file_output.file_path), caption=ascii_ready,
                                               parse_mode="HTML")
        await callback.bot.delete_message(chat_id=edit_msg.chat.id, message_id=edit_msg.message_id)

        return file_output.file_path

    handle_actions = {
        "transcribe": lambda *args, **kwargs: send_message(*args, keyboard=transcribe_separate_options_keyboard,
                                                           text=transcribe_options, **kwargs),
        "transform_to_ascii": lambda *args, **kwargs: send_message(*args, keyboard=transform_options_keyboard,
                                                                   text=ascii_options, **kwargs)
    }
    process_actions = {
        "transcribe_with_demucs": lambda *args, **kwargs: transcribe_demucs_process(*args,
                                                                                    event="transcribe_with_demucs",
                                                                                    **kwargs),
        "transcribe_without_demucs": lambda *args, **kwargs: transcribe_demucs_process(*args,
                                                                                       event="transcribe_without_demucs",
                                                                                       **kwargs),
        "transcribe_in_file": lambda *args, **kwargs: transcribe_whisper(*args, return_as_txt=True, **kwargs),
        "transcribe_in_chat": lambda *args, **kwargs: transcribe_whisper(*args, return_as_txt=False, **kwargs),
        "remove_bg": process_remove_bg,
        "extract_text": process_ocr,
        "upscale_image": process_image_upscaling,
        "100": process_ascii,
        "200": process_ascii,
        "300": process_ascii,
        "vocals.mp3": lambda *args, **kwargs: handle_separate(*args, event="vocals.mp3", **kwargs),
        "no_vocals.mp3": lambda *args, **kwargs: handle_separate(*args, event="no_vocals.mp3", **kwargs)
    }

    @router.callback_query(lambda f: f.data.startswith("handle") or f.data.startswith("process"))
    async def handle_file(callback: CallbackQuery):
        await callback.message.delete()
        await callback.answer()

        file, redis = await get_file_safe(callback=callback, full=True)
        if not file:
            return

        action, event = callback.data.lower().split(":")
        temp_path = None

        try:
            if action == "handle":
                await handle_actions[event](callback=callback)
            elif action == "process" and event in process_actions:
                temp_path = await process_actions[event](callback=callback, redis=redis, file=file)
        finally:
            if action == "process" and event in process_actions and event not in ("transcribe_without_demucs" or "transcribe_with_demucs"):
                if file and file.file_path.exists():
                    if "mdx_extra" in str(file.file_path):
                        if not file.file_path.is_dir():
                            file.file_path = file.file_path.parent
                        await asyncio.to_thread(lambda: shutil.rmtree(file.file_path, ignore_errors=True))

                    else:
                        await asyncio.to_thread(file.file_path.unlink, missing_ok=True)

                if temp_path:
                    if isinstance(temp_path, Path) and temp_path.exists():
                        await asyncio.to_thread(temp_path.unlink, missing_ok=True)

                await redis.delete_file_by_uid(user_id=callback.message.from_user.id)

    return router