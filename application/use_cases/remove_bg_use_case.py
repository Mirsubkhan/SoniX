import asyncio
from pathlib import Path

from core.entities.file import FileType
from core.entities.file_dto import FileInputDTO, FileOutputDTO
from core.ports.background_remover import BackgroundRemover
from interfaces_adapters.ports_impl.bg_remover import BgRemover


class BgRemoverUseCase:
    def __init__(self, remover: BackgroundRemover):
        self.remover = remover

    async def remove_bg(self, file: FileInputDTO) -> FileOutputDTO:
        return await self.remover.remove_bg(file=file)



