import json
import os
import traceback
from datetime import timedelta
from pathlib import Path
from typing import Union

from redis.asyncio import Redis
from core.entities.file import File, FileType
from core.entities.file_dto import FileInputDTO
from core.ports.file_storage import FileStorage


class RedisFileStorage(FileStorage):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def save(self, file: File) -> None:
        key = f"user:{file.user_id}:file"
        data = {
            "file_id": str(file.file_id),
            "file_path": str(file.file_path),
            "file_type": file.file_type.value,
            "file_duration": file.file_duration.total_seconds() if file.file_duration else None,
            "file_format": file.file_format,
        }
        json_data = json.dumps(data)

        await self.redis.set(key, json_data)

    async def get_file_by_user_id(self, user_id: int) -> Union[FileInputDTO, None]:
        raw = await self.redis.get(f"user:{user_id}:file")

        if raw:
            data = json.loads(raw)
            return FileInputDTO(
                file_path=Path(data["file_path"]),
                file_duration=timedelta(seconds=data["file_duration"]) if data["file_duration"] else None,
                file_type=FileType(data["file_type"])
            )
        return None

    async def delete_file_by_user_id(self, user_id: int) -> None:
        key = f"user:{user_id}:file"

        raw = await self.redis.get(f"user:{user_id}:file")

        if raw:
            data = json.loads(raw)
            file_path = Path(data["file_path"])
            if file_path.exists():
                try:
                    os.remove(file_path)
                except Exception as e:
                    traceback.print_exc()
            await self.redis.delete(key)

