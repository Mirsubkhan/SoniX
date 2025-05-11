from core.entities.file import File
from core.ports.audio_converter import AudioConverter
from pathlib import Path

class FFMpegAudioConverterUseCase:
    def __init__(self, converter: AudioConverter):
        self.converter = converter

    async def convert(self, file: File) -> Path:
        return await self.converter.convert_to_wav(file)