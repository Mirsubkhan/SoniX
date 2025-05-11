from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from enum import Enum

class FileType(Enum):
    AUDIO = "audio"
    VIDEO = "video"
    PHOTO = "photo"

class OperationType(Enum):
    TRANSCRIBE = "transcribe"
    SEPARATE = "separate"
    TRANSFORM_TO_ASKII = "transform_to_askii"
    REMOVE_BG = "remove_bg"
    REMOVE_NOISE = "remove_noise"
    NO_OP = "none"

@dataclass
class File:
    user_id: int
    file_id: str
    file_path: Path
    file_type: FileType
    file_duration: timedelta | None
    file_format: str
    operation: OperationType = OperationType.NO_OP