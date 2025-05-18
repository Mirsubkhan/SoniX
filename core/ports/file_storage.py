from abc import ABC, abstractmethod
from typing import List

from core.entities.file import File

class FileStorage(ABC):
    @abstractmethod
    async def save(self , file: File, ttl_seconds: int) -> None:
        pass

    @abstractmethod
    async def get_by_file_id(self, file_id: str) -> File | None:
        pass

    @abstractmethod
    async def delete_by_file_id(self, file_id: str) -> None:
        pass

    @abstractmethod
    async def get_all_by_uid(self, user_id: int) -> List[File] | None:
        pass

    async def delete_all_by_uid(self, user_id: int) -> None:
        pass