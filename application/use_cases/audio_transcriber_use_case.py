from core.ports.audio_transcriber import AudioTranscriber, DynamicSSTCallback, STTCallback
from application.use_cases.audio_extractor_use_case import AudioExtractorUseCase
from application.use_cases.file_handler_use_case import FileHandlerUseCase
from core.entities.file_dto import FileInputDTO, FileOutputDTO
from core.entities.file import FileType
from pathlib import Path
from typing import Union


class AudioTranscriberUseCase:
    def __init__(self, transcriber: AudioTranscriber, extractor: AudioExtractorUseCase, f_handler: FileHandlerUseCase):
        self.output_dir = Path("./results/transcribed_audio").resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.transcriber = transcriber
        self.extractor = extractor
        self.f_handler = f_handler

    async def transcribe_dynamic(
            self,
            file_input: FileInputDTO,
            on_progress: DynamicSSTCallback
    ) -> None:
        file_input.file_path = await self._extract_audio(file_input=file_input)
        await self.transcriber.transcribe_dynamic(file_input=file_input, on_progress=on_progress)

    async def transcribe(
            self,
            file_input: FileInputDTO,
            on_progress: Union[STTCallback, None]
    ) -> FileOutputDTO:
        file_input.file_path = await self._extract_audio(file_input=file_input)
        result_text = await self.transcriber.transcribe(file_input=file_input, on_progress=on_progress)
        output_path = self.output_dir.joinpath(file_input.file_path.stem + ".txt")

        return await self.f_handler.save_as_txt(fpath=output_path, text=result_text)

    async def _extract_audio(self, file_input: FileInputDTO) -> Path:
        if file_input.file_type == FileType.VIDEO:
            file_output = await self.extractor.extract(file_input=file_input)
            file_input.file_path = file_output.file_path

        return file_input.file_path