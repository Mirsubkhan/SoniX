import os

from aiogram import Router

from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from interfaces_adapters.ports_impl.demucs_separator import DemucsSeparator
from interfaces_adapters.ports_impl.faster_whisper_transcriber import FasterWhisperTranscriber
from infrastructure.telegram.inline_keyboard import return_as_file_keyboard
from application.use_cases.demucs_separator_use_case import DemucsSeparatorUseCase
from core.entities.file import File
from application.use_cases.faster_whisper_transcriber_use_case import TranscribeAudioUseCase

router = Router()

async def progress_callback(percent: int):
    hearts = "💚" * (percent // 10) + "🤍" * (10 - (percent // 10))
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=edit_msg.message_id,
            text=f"🎧 Разделение музыки...\n{hearts} {percent}%"
        )
    except Exception as e:
        pass

async def transcribe_progress_callback(filled: int):
    hearts = "💚" * filled + "🤍" * (filled - 10)

    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=edit_msg.message_id,
            text=f"📝 Транскрибация аудио...\n{hearts} {filled * 10}%"
        )
    except Exception as e:
        pass

async def dynamic_progress_callback(text: str):
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=edit_msg.message_id,
            text=text
        )
    except Exception as e:
        edit_msg = await message.answer()

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



