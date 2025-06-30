from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from enum import Enum
from typing import Union

class FileType(Enum):
    AUDIO = "audio"
    VIDEO = "video"
    PHOTO = "photo"

@dataclass
class File:
    user_id: int
    message_id: Union[int, None]
    file_id: str
    file_path: Path
    file_type: FileType
    file_duration: Union[timedelta, None]
    file_format: str
