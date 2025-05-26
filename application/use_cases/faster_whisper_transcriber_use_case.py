from core.ports.audio_transcriber import AudioTranscriber, DynamicProgressCallback, TranscribeProgressCallback
from application.use_cases.ffmpeg_audio_extractor_use_case import FFMpegAudioExtractorUseCase
from core.entities.file_dto import FileInputDTO, FileOutputDTO

class TranscribeAudioUseCase:
    def __init__(self, transcriber: AudioTranscriber, extractor: FFMpegAudioExtractorUseCase):
        self.transcriber = transcriber
        self.extractor = extractor

    async def _extract_audio(self, file_input: FileInputDTO) -> FileInputDTO:
        if file_input.file_type.VIDEO:
            file_output = await self.extractor.extract(file_input=file_input)
            file_input.file_path = file_output.file_path

        return file_input

    async def transcribe_dynamic(self, file_input: FileInputDTO, on_progress: DynamicProgressCallback):
        file_input = await self._extract_audio(file_input=file_input)
        return await self.transcriber.transcribe_dynamic(file_input, on_progress=on_progress)

    async def transcribe(self, file_input: FileInputDTO, on_progress: TranscribeProgressCallback) -> FileOutputDTO:
        file_input = await self._extract_audio(file_input=file_input)
        return await self.transcriber.transcribe(file_input=file_input, on_progress=on_progress)