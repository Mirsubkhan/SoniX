from domain.entities.file import File
from domain.repositories.converter import IAudioConverter
from pathlib import Path

class ConvertAudioToWavUseCase:
    def __init__(self, converter: IAudioConverter):
        self.converter = converter

    async def convert(self, file) -> Path:
        return await self.converter.convert_to_wav(file)