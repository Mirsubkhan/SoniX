from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from core.entities.file import FileType

@dataclass
class FileInputDTO:
    file_path: Path
    file_type: FileType
    file_duration: timedelta | None

@dataclass
class FileOutputDTO:
    file_path: Path
