from aiogram.types import Message

from domain.entities.file import File, FileType
from domain.repositories.transcriber import ITranscriber
from domain.repositories.converter import IAudioConverter
from domain.repositories.audio_extractor import IAudioExtractor
from domain.entities.transcription_result import TranscriptionResult

class TranscribeAudioUseCase:
    def __init__(self, transcriber: ITranscriber, audio_extractor: IAudioExtractor = None, converter: IAudioConverter = None):
        self.transcriber = transcriber
        # self.audio_extractor = audio_extractor
        # self.converter = converter

    async def transcribe(self, file: File, message: Message = None, mid: int = None, rafile: bool = False):
        result = await self.transcriber.transcribe(file, message=message, mid=mid, rafile=rafile)

        return result