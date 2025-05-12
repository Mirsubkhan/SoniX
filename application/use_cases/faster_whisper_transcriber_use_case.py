from core.entities.file import File
from core.ports.audio_transcriber import AudioTranscriber, DynamicProgressCallback, TranscribeProgressCallback
from pathlib import Path
from application.use_cases.ffmpeg_audio_extractor_use_case import FFMpegAudioExtractorUseCase
from interfaces_adapters.ports_impl.ffmpeg_audio_extractor import FFMpegAudioExtractor

class TranscribeAudioUseCase:
    def __init__(self, transcriber: AudioTranscriber):
        self.transcriber = transcriber

    async def _extract_audio(self, file: File) -> File:
        if file.file_type.VIDEO:
            extractor = FFMpegAudioExtractor()

            result_path = await FFMpegAudioExtractorUseCase(extractor=extractor).extract(file=file)
            file.file_path = result_path

        return file

    async def transcribe_dynamic(self, file: File, on_progress: DynamicProgressCallback):
        file = await self._extract_audio(file=file)
        return await self.transcriber.transcribe_dynamic(file, on_progress=on_progress)

    async def transcribe(self, file: File, on_progress: TranscribeProgressCallback) -> Path:
        file = await self._extract_audio(file=file)
        return await self.transcriber.transcribe(file=file, on_progress=on_progress)