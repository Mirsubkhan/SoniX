import asyncio
from pathlib import Path

from core.entities.file import FileType
from core.entities.file_dto import FileInputDTO, FileOutputDTO
from core.ports.image_upscaler import ImageUpscaler
from interfaces_adapters.ports_impl.bg_remover import BgRemover


class UpscalerUseCase:
    def __init__(self, upscaler: ImageUpscaler):
        self.upscaler = upscaler

    async def upscale(self, file: FileInputDTO) -> FileOutputDTO:
        return await self.upscaler.upscale_image(file_input=file)



