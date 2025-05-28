import asyncio
from pathlib import Path
from PIL import Image
from core.ports.image_handler import ImageHandler

class ImageIOHandler(ImageHandler):
    async def open_img(self, path: Path) -> Image:
        return await asyncio.to_thread(
            lambda: Image.open(fp=path).convert("RGB")
        )

    async def save_img(self, im: Image.Image, path: Path) -> None:
        await asyncio.to_thread(lambda: im.save(fp=path))