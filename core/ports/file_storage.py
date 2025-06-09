from abc import ABC, abstractmethod

from core.entities.file import File
from core.entities.file_dto import FileInputDTO
from typing import Union


class FileStorage(ABC):
    @abstractmethod
    async def save(self , file: File) -> None:
        pass

    @abstractmethod
    async def get_file_by_user_id(self, user_id: int) -> Union[FileInputDTO, None]:
        pass

    @abstractmethod
    async def delete_file_by_user_id(self, user_id: int) -> None:
        pass