from domain.entities.file import File
from domain.repositories.audio_extractor import IAudioExtractor
from pathlib import Path

class ExtractAudioFromVideoUseCase:
    def __init__(self, extractor: IAudioExtractor):
        self.extractor = extractor


    async def extract(self, file) -> Path:
        return await self.extractor.extract_audio_from_video(file)