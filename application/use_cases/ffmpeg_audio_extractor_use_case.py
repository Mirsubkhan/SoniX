from core.entities.file import File
from core.ports.audio_extractor import AudioExtractor
from pathlib import Path
from core.entities.file_dto import FileInputDTO, FileOutputDTO

class FFMpegAudioExtractorUseCase:
    def __init__(self, extractor: AudioExtractor):
        self.extractor = extractor

    async def extract(self, file_input: FileInputDTO) -> FileOutputDTO:
        return await self.extractor.extract_audio_from_video(file_input)