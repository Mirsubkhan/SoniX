import datetime
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from enum import Enum

class FileType(Enum):
    AUDIO = "audio"
    VIDEO = "video"
    PHOTO = "photo"

@dataclass
class File:
    user_id: int
    file_id: str
    file_path: Path
    file_type: FileType
    file_duration: timedelta | None
    file_format: str
