from core.ports.audio_extractor import AudioExtractor
from core.entities.file_dto import FileInputDTO, FileOutputDTO

class AudioExtractorUseCase:
    def __init__(self, extractor: AudioExtractor):
        self.extractor = extractor

    async def extract(self, file_input: FileInputDTO) -> FileOutputDTO:
        return await self.extractor.extract_audio(file_input)