import torch

from infrastructure.telegram.bot_answers import loading_file, file_download_error, file_downloaded, unsupported_file
from infrastructure.telegram.services.file_worker import TelegramFileWorker
from application.use_cases.file_storage_use_case import FileStorageUseCase
from config import media_filter, not_supported_filter
from core.ports.file_storage import FileStorage
from aiogram.types import Message
from aiogram import Router
import traceback


def setup_handlers(router: Router, file_worker: TelegramFileWorker, client: FileStorage):
    @router.message(media_filter)
    async def media_handler(message: Message):
        torch.cuda.empty_cache()
        edit_msg = await message.reply(text=loading_file, parse_mode="HTML")

        try:
            redis = FileStorageUseCase(redis=client)
            old_file = await redis.get_file_by_uid(user_id=message.from_user.id, full=True)

            if old_file is not None:
                try:
                    await message.bot.delete_message(chat_id=message.chat.id, message_id=old_file.message_id)
                    await redis.delete_file_by_uid(message.from_user.id)
                except Exception as e:
                    pass

            file = await file_worker.get_message_file(message=message)

            actions = await message.reply(
                text=file_downloaded,
                reply_markup=await file_worker.return_keyboard(file.file_type),
                parse_mode="HTML"
            )

            file.message_id = actions.message_id
            await FileStorageUseCase(redis=client).save(file=file)
        except Exception as e:
            traceback.print_exc()
            await message.reply(text=file_download_error, parse_mode="HTML")
        finally:
            await message.bot.delete_message(message_id=edit_msg.message_id, chat_id=message.from_user.id)


    @router.message(not_supported_filter)
    async def warn_message(message: Message):
        await message.reply(text=unsupported_file, parse_mode="HTML")

    return router