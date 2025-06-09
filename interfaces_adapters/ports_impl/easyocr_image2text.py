from concurrent.futures.thread import ThreadPoolExecutor
from core.ports.image2text import Image2Text
from pathlib import Path
import easyocr
import asyncio


class EasyOCRImage2Text(Image2Text):
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.reader = easyocr.Reader(['en', 'ru'], gpu=True)

    async def image_to_text(self, fpath: Path) -> str:
        result = await asyncio.to_thread(lambda: self.reader.readtext(str(fpath)))
        extracted_text = ' '.join(item[1] for item in result)

        return "П-У-С-Т-О / E-M-P-T-Y" if not extracted_text else extracted_text