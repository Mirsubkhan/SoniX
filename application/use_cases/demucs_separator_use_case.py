from core.ports.audio_separator import AudioSeparator, ProgressCallback
from core.entities.file_dto import FileInputDTO, FileOutputDTO

class DemucsSeparatorUseCase:
    def __init__(self, separator: AudioSeparator):
        self.separator = separator

    async def separate(self, file_input: FileInputDTO, on_progress: ProgressCallback) -> FileOutputDTO:
        return await self.separator.separate(file_input, on_progress=on_progress)