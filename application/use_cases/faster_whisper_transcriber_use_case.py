from core.entities.file import File
from core.ports.audio_transcriber import AudioTranscriber, DynamicProgressCallback, TranscribeProgressCallback
from pathlib import Path

class TranscribeAudioUseCase:
    def __init__(self, transcriber: AudioTranscriber):
        self.transcriber = transcriber

    async def transcribe_dynamic(self, file: File, on_progress: DynamicProgressCallback):
        return await self.transcriber.transcribe_dynamic(file, on_progress=on_progress)

    async def transcribe(self, file: File, on_progress: TranscribeProgressCallback) -> Path:
        return await self.transcriber.transcribe(file=file, on_progress=on_progress)