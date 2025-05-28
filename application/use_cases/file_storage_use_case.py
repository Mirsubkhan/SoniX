from typing import Union
from core.entities.file import File
from core.entities.file_dto import FileInputDTO
from core.ports.file_storage import FileStorage


class FileStorageUseCase:
    def __init__(self, redis: FileStorage):
        self.redis = redis

    async def save(self, file: File) -> None:
        await self.redis.save(file=file, ttl_seconds=2600)

    async def get_file_by_uid(self, user_id: int) -> Union[FileInputDTO, None]:
        return await self.redis.get_file_by_user_id(user_id=user_id)

    async def delete_file_by_uid(self, user_id: int) -> None:
        return await self.redis.delete_file_by_user_id(user_id=user_id)