from abc import ABC, abstractmethod

from core.entities.file import File
from core.entities.file_dto import FileInputDTO


class FileStorage(ABC):
    @abstractmethod
    async def save(self , file: File, ttl_seconds: int) -> None:
        pass

    @abstractmethod
    async def get_by_file_user_id(self, user_id: int) -> FileInputDTO | None:
        pass

    @abstractmethod
    async def delete_file_by_user_id(self, user_id: int) -> None:
        pass