from abc import ABC, abstractmethod

from aiogram.types import Message

from domain.entities.file import File
from pathlib import Path

class ISeparator(ABC):
    @abstractmethod
    async def separate(self, file: File, message: Message) -> Path:
        pass