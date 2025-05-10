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

    # async def get_formatted(self):
    #     if self.with_timestamps:
    #         return "/n".join([f"[{seg.start}-{seg.end}]: {seg.text}" for seg in self.segments])
    #     return self.full_text