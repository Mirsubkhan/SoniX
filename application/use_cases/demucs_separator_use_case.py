from core.entities.file import File
from core.ports.audio_separator import AudioSeparator, ProgressCallback
from pathlib import Path

class DemucsSeparatorUseCase:
    def __init__(self, separator: AudioSeparator):
        self.separator = separator

    async def separate(self, file: File, on_progress: ProgressCallback) -> Path:
        return await self.separator.separate(file, on_progress=on_progress)