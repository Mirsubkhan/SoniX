from aiogram.types import Message

from domain.entities.file import File
from domain.repositories.separator import ISeparator
from pathlib import Path

class DemucsSeparatorUseCase:
    def __init__(self, separator: ISeparator):
        self.separator = separator

    async def separate(self, file: File, message: Message) -> Path:
        return await self.separator.separate(file, message=message)