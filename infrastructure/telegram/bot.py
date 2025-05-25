import os
from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from aiogram.fsm.storage.memory import MemoryStorage
from redis.asyncio import Redis

from infrastructure.telegram.handlers import messages, callbacks, commands
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp import ClientTimeout

from infrastructure.telegram.services.file_worker import TelegramFileWorker
from infrastructure.telegram.services.progress_bar import TelegramProgressBarRenderer
from interfaces_adapters.ports_impl.ascii_converter import AsciiConverter
from interfaces_adapters.ports_impl.bg_remover import BgRemover
from interfaces_adapters.ports_impl.demucs_separator import DemucsSeparator
from interfaces_adapters.ports_impl.easyocr_converter import EasyOCRImageToText
from interfaces_adapters.ports_impl.faster_whisper_transcriber import FasterWhisperTranscriber
from interfaces_adapters.ports_impl.ffmpeg_audio_extractor import FFMpegAudioExtractor
from interfaces_adapters.ports_impl.realesrgan_upscaler import RealERSGANUpscaler
from interfaces_adapters.ports_impl.redis_file_storage import RedisFileStorage

timeout = ClientTimeout(total=60)
session = AiohttpSession(timeout=60)
client = Redis()


async def on_shutdown(dp: Dispatcher):
    await dp.storage.close()
    await session.close()
    await client.close()

async def main():
    load_dotenv()

    bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'), session=session)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(
        commands.setup_handlers(router=Router()),
        messages.setup_handlers(router=Router(),
                                file_worker=TelegramFileWorker(),
                                client=RedisFileStorage(redis=client)),
        callbacks.setup_handlers(router=Router(),
                                 transcriber=FasterWhisperTranscriber(),
                                 extractor=FFMpegAudioExtractor(),
                                 photo_style_converter=AsciiConverter(),
                                 separator=DemucsSeparator(),
                                 progress_bar=TelegramProgressBarRenderer(),
                                 bg_remover=BgRemover(),
                                 ocr=EasyOCRImageToText(),
                                 upscaler=RealERSGANUpscaler(),
                                 client=RedisFileStorage(redis=client))
    )
    dp.shutdown.register(on_shutdown)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
