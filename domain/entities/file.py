from dataclasses import dataclass
from datetime import datetime, timedelta
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
    T_NONE = "none"

@dataclass
class File:
    user_id: int
    file_id: str
    file_path: Path
    file_type: FileType
    file_duration: timedelta
    file_format: str
    operation: OperationType = OperationType.T_NONE