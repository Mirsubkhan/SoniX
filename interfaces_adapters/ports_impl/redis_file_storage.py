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

    async def save(self, file: File, ttl_seconds: int) -> None:
        await self.dump()
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
        await self.dump()

    async def get_file_by_user_id(self, user_id: int) -> Union[FileInputDTO, None]:
        key = f"user:{user_id}:file"
        print(f"[GET] Getting key '{key}'")

        raw = await self.redis.get(f"user:{user_id}:file")

        if raw:
            data = json.loads(raw)
            print(f"[GET] Data found: {data}")
            return FileInputDTO(
                file_path=Path(data["file_path"]),
                file_duration=timedelta(seconds=data["file_duration"]) if data["file_duration"] else None,
                file_type=FileType(data["file_type"])
            )
        else:
            print(f"[GET] No data found for key '{key}'")
        return None

    async def delete_file_by_user_id(self, user_id: int) -> None:
        key = f"user:{user_id}:file"
        print(f"[DELETE] Deleting key '{key}'")

        raw = await self.redis.get(f"user:{user_id}:file")

        if raw:
            data = json.loads(raw)
            file_path = Path(data["file_path"])
            if file_path.exists():
                try:
                    os.remove(file_path)
                    print(f"[DELETE] File {file_path} removed.")
                except Exception as e:
                    print(f"[DELETE] Error removing file: {e}")
                    traceback.print_exc()
            await self.redis.delete(key)
            print(f"[DELETE] Key '{key}' deleted from Redis.")
        else:
            print(f"[DELETE] No file found in Redis for key '{key}'")

    async def dump(self):
        keys = await self.redis.keys("*")  # Получить все ключи

        if not keys:
            print("[REDIS DUMP] No keys found.")
            return

        print(f"[REDIS DUMP] Found {len(keys)} keys.")

        for key in keys:
            value = await self.redis.get(key)
            print(f"Key: {key.decode() if isinstance(key, bytes) else key}")
            if value:
                try:
                    decoded_value = value.decode()
                    print(f"Value: {decoded_value}")
                except Exception:
                    print(f"Value (binary): {value}")
            else:
                print("Value: None")


