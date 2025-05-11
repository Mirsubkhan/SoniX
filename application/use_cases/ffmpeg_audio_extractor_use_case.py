from core.entities.file import File
from core.ports.audio_extractor import AudioExtractor
from pathlib import Path

class FFMpegAudioExtractorUseCase:
    def __init__(self, extractor: AudioExtractor):
        self.extractor = extractor

    async def extract(self, file: File) -> Path:
        return await self.extractor.extract_audio_from_video(file)