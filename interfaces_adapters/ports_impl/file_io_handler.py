import asyncio
from pathlib import Path

import aiofiles
import cv2
from PIL import Image

from core.entities.file_dto import FileOutputDTO
from core.ports.file_handler import FileHandler
from numpy import ndarray

class FileIOHandler(FileHandler):
    async def open_img(self, path: Path) -> Image:
        return await asyncio.to_thread(
            lambda: Image.open(fp=path).convert("RGB")
        )

    async def save_img(self, im: Image.Image, fpath: Path) -> FileOutputDTO:
        await asyncio.to_thread(lambda: im.save(fp=fpath))

        return FileOutputDTO(file_path=fpath)

    async def save_as_txt(self, fpath: Path, text: str) -> FileOutputDTO:
        async with aiofiles.open(fpath, "w") as f:
            await f.write(text)

        return FileOutputDTO(file_path=fpath, file_txt=text)

    async def open_img_with_cv2(self, fpath: Path):
        return await asyncio.to_thread(lambda: cv2.imread(str(fpath), cv2.IMREAD_COLOR))

    async def save_img_with_cv2(self, image: ndarray, fpath: Path) -> FileOutputDTO:
        await asyncio.to_thread(lambda: cv2.imwrite(str(fpath), image))

        return FileOutputDTO(file_path=fpath)


