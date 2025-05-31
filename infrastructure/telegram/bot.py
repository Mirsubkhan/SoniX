import os
from aiogram import Bot, Dispatcher, Router
from dotenv import load_dotenv
from aiogram.fsm.storage.memory import MemoryStorage
from redis.asyncio import Redis

from application.use_cases.file_handler_use_case import FileHandlerUseCase
from infrastructure.telegram.handlers import messages, callbacks, commands
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp import ClientTimeout

from infrastructure.telegram.services.file_worker import TelegramFileWorker
from infrastructure.telegram.services.progress_bar import TelegramProgressBarRenderer
from interfaces_adapters.ports_impl.file_io_handler import FileIOHandler
from interfaces_adapters.ports_impl.pil_ascii_converter import PilASCIIConverter
from interfaces_adapters.ports_impl.birefnet_bg_remover import BiRefNETBgRemover
from interfaces_adapters.ports_impl.demucs_separator import DemucsSeparator
from interfaces_adapters.ports_impl.tr_image_text_extractor import TrImageTextExtractor
from interfaces_adapters.ports_impl.fwhisper_transcriber import FWhisperTranscriber
from interfaces_adapters.ports_impl.ffmpeg_extractor import FFMpegAudioExtractor
from interfaces_adapters.ports_impl.realesrgan_upscaler import RealERSGANUpscaler
from interfaces_adapters.ports_impl.redis_file_storage import RedisFileStorage

timeout = ClientTimeout(total=60)
session = AiohttpSession(timeout=60)
client = Redis()


async def on_shutdown(dp: Dispatcher):
    await dp.storage.close()
    await session.close()
    await client.close()

async def create_dispatcher():
    load_dotenv()
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

    bot = Bot(token=BOT_TOKEN, session=session)
    dp = Dispatcher(storage=MemoryStorage())
    storage = RedisFileStorage(redis=client)

    dp.include_routers(
        commands.setup_handlers(router=Router()),
        messages.setup_handlers(router=Router(),
                                file_worker=TelegramFileWorker(),
                                client=storage),
        callbacks.setup_handlers(router=Router(),
                                 transcriber=FWhisperTranscriber(),
                                 extractor=FFMpegAudioExtractor(),
                                 ascii_converter=PilASCIIConverter(),
                                 separator=DemucsSeparator(),
                                 progress_bar=TelegramProgressBarRenderer(),
                                 bg_remover=BiRefNETBgRemover(),
                                 image_text_extractor=TrImageTextExtractor(),
                                 upscaler=RealERSGANUpscaler(),
                                 file_handler=FileIOHandler(),
                                 client=storage)
    )
    dp.shutdown.register(on_shutdown)

    return dp, bot
