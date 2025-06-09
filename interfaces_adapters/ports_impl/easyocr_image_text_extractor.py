import easyocr
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from core.ports.image_text_extractor import ImageTextExtractor
from concurrent.futures.thread import ThreadPoolExecutor
from core.entities.file_dto import FileOutputDTO
from PIL.Image import Image
from pathlib import Path
import asyncio


class EasyOCRImageTextExtractor(ImageTextExtractor):
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)

        self.reader = easyocr.Reader(['en', 'ru'], gpu=True)

    async def image_to_text(
            self,
            fpath: Path
    ) -> str:
        return await asyncio.to_thread(lambda: self.reader.readtext(str(fpath)))