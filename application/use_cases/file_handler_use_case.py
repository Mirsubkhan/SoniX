from pathlib import Path
from PIL import Image

from core.entities.file_dto import FileOutputDTO
from core.ports.file_handler import FileHandler
from numpy import ndarray

class FileHandlerUseCase:
    def __init__(self, file_repo: FileHandler):
        self.file = file_repo

    async def open_img(self, fpath: Path) -> Image:
        return await self.file.open_img(fpath)

    async def save_img(self, image: Image.Image, fpath: Path) -> FileOutputDTO:
        return await self.file.save_img(image, fpath)

    async def save_as_txt(self, fpath: Path, text: str) -> FileOutputDTO:
        return await self.file.save_as_txt(fpath, text)

    async def open_img_with_cv2(self, fpath: Path):
        return await self.file.open_img_with_cv2(fpath)

    async def save_img_with_cv2(self, image: ndarray, fpath: Path) -> FileOutputDTO:
        return await self.file.save_img_with_cv2(image=image, fpath=fpath)