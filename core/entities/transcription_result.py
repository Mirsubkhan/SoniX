from dataclasses import dataclass
from datetime import timedelta
from typing import List

@dataclass
class TranscriptionSegment:
    start: timedelta
    end: timedelta
    text: str

@dataclass
class TranscriptionResult:
    segments: List[TranscriptionSegment]
    full_text: str