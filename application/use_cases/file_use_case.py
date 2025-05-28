from pathlib import Path

from PIL import Image

from core.ports.file_repository import FileRepository


class FileUseCase:
    def __init__(self, file_repo: FileRepository):
        self.file = file_repo

    async def open_img(self, path: Path) -> Image:
        return await self.file.open_img(path)

    async def save_img(self, im: Image.Image, path: Path) -> None:
        await self.file.save_img(im, path)