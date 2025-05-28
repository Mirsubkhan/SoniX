import traceback
from datetime import timedelta

from aiogram import Router, F
from aiogram.types import Message

from application.use_cases.file_storage_use_case import RedisUseCase
from core.ports.file_storage import FileStorage
from infrastructure.telegram.bot_answers import loading_file, file_download_error, file_downloaded, unsupported_file
from core.entities.file import File
from infrastructure.telegram.services.file_worker import TelegramFileWorker


media_filter = F.video | F.audio | F.video_note | F.voice | F.photo
not_supported_filter = ~(F.video | F.audio | F.video_note | F.voice | F.photo | F.text)

def setup_handlers(router: Router, file_worker: TelegramFileWorker, client: FileStorage):
    @router.message(media_filter)
    async def media_handler(message: Message):
        message_file = message.audio or message.video or message.voice or message.video_note
        edit_msg = await message.reply(text=loading_file, parse_mode="HTML")

        try:
            file_id = message.photo[-1].file_id if message.photo else message_file.file_id
            file_format, file_type = await file_worker.detect_file_type(message)
            file_path = await file_worker.download_file(message.bot, file_id=file_id, file_format=file_format)

            file = File(
                user_id=message.from_user.id,
                file_id=file_id,
                file_path=file_path,
                file_type=file_type,
                file_format=file_format,
                file_duration=None if message.photo else timedelta(seconds=message_file.duration)
            )

            print(f"{file.file_id}\n"
                  f"{file.file_path}\n"
                  f"{file.file_type}\n"
                  f"{file.file_format}\n"
                  f"{file.user_id}\n"
                  f"{file.file_duration}")

            await RedisUseCase(redis=client).save(file=file)

            await message.reply(
                text=file_downloaded,
                reply_markup=await file_worker.return_keyboard(file.file_type),
                parse_mode="HTML"
            )
        except Exception as e:
            traceback.print_exc()
            await message.reply(text=file_download_error, parse_mode="HTML")
        finally:
            await message.bot.delete_message(message_id=edit_msg.message_id, chat_id=message.from_user.id)
            return

    @router.message(not_supported_filter)
    async def warn_message(message: Message):
        await message.reply(text=unsupported_file, parse_mode="HTML")

    return router