import logging
import os
import traceback

from aiogram import Router

from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from interfaces_adapters.ports_impl.demucs_separator import DemucsSeparator
from interfaces_adapters.ports_impl.faster_whisper_transcriber import FasterWhisperTranscriber
from infrastructure.telegram.inline_keyboard import return_as_file_keyboard, transform_options_keyboard
from application.use_cases.demucs_separator_use_case import DemucsSeparatorUseCase
from application.use_cases.ascii_converter_use_case import AsciiConverterUseCase
from interfaces_adapters.ports_impl.ascii_converter import AsciiConverter
from core.entities.file import File
from application.use_cases.faster_whisper_transcriber_use_case import TranscribeAudioUseCase

router = Router()

@router.callback_query(lambda f: f.data in ["transcribe", "transform_to_ascii", "remove_bg", "remove_noise", "separate"])
async def handle_file(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

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
        edit_msg = await callback.message.answer("Слушаю музыку...")

        async def progress_callback(percent: int):
            hearts = "💚" * (percent // 10) + "🤍" * (10 - (percent // 10))
            try:
                await callback.bot.edit_message_text(
                    chat_id=callback.message.chat.id,
                    message_id=edit_msg.message_id,
                    text=f"🎧 Разделение музыки...\n{hearts} | {percent}%"
                )
            except Exception as e:
                pass

        separator = DemucsSeparator()
        separated_path = await DemucsSeparatorUseCase(separator=separator).separate(file, on_progress=progress_callback)

        if separated_path:
            await callback.bot.delete_message(message_id=edit_msg.message_id, chat_id=file.user_id)
            await callback.message.answer_document(FSInputFile(separated_path.joinpath("vocals.mp3")))
            await callback.message.answer_document(FSInputFile(separated_path.joinpath("no_vocals.mp3")))

            os.remove(separated_path)
        else:
            await callback.message.answer("Чёт не получилось извлечь вокал/инструментал из музыки 😬")

    elif action == "transform_to_ascii":
        await callback.message.answer(
            text=(
                "<b>Отлично!</b>\n\n"
                "Тебе результат скинуть в чёрно-белом ASCII или в цветом ASCII варианте?"
            ),
            reply_markup=transform_options_keyboard,
            parse_mode="HTML"
        )


@router.callback_query(lambda f: f.data in ['file', 'no_file'])
async def transcribe_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    file: File = data.get("file")
    action = callback.data.lower()

    edit_msg = await callback.message.answer("Слушаю файл...")
    message_id = edit_msg.message_id
    transcriber = FasterWhisperTranscriber()

    if action == "file":
        async def transcribe_progress_callback(filled: int):
            hearts = "💚" * filled + "🤍" * (10 - filled)
            res = f"📝 Транскрибация...\n{hearts} | {filled * 10}%"

            await callback.bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=message_id,
                text=res
            )


        result = await TranscribeAudioUseCase(transcriber=transcriber).transcribe(file, on_progress=transcribe_progress_callback)
        await callback.message.answer_document(FSInputFile(result), caption="📝 Транскрибация файла готова!")
        await callback.bot.delete_message(chat_id=edit_msg.chat.id, message_id=edit_msg.message_id)
    else:
        async def dynamic_progress_callback(text: str):
            nonlocal message_id
            try:
                await callback.bot.edit_message_text(
                    chat_id=callback.message.chat.id,
                    message_id=message_id,
                    text=text
                )
            except Exception as e:
                # traceback.print_exc()
                new_edit_msg = await callback.message.answer(text.removeprefix(edit_msg.text).strip())
                message_id = new_edit_msg.message_id

        await TranscribeAudioUseCase(transcriber=transcriber).transcribe_dynamic(file, on_progress=dynamic_progress_callback)

@router.callback_query(lambda f: f.data in ("color", "no_color"))
async def convert_to_ascii_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    file: File = data.get("file")
    action = callback.data.lower()

    edit_msg = await callback.message.answer("🔢 Преобразую в ASCII...")
    converter = AsciiConverter()

    result_path = await AsciiConverterUseCase(converter=converter).convert(file=file, add_color=True if action == "color" else False)

    await callback.message.answer_document(FSInputFile(result_path), caption="📝 Преобразование фото в ASCII готово!")
    await callback.bot.delete_message(chat_id=edit_msg.chat.id, message_id=edit_msg.message_id)