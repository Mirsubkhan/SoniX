from core.entities.file import File
from core.ports.audio_converter import AudioConverter
from pathlib import Path
from core.entities.file_dto import FileInputDTO, FileOutputDTO

class FFMpegAudioConverterUseCase:
    def __init__(self, converter: AudioConverter):
        self.converter = converter

    async def convert(self, file_input: FileInputDTO) -> FileOutputDTO:
        return await self.converter.convert_to_wav(file_input)