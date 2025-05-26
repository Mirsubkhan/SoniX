import asyncio
import aiofiles
from faster_whisper import WhisperModel
from core.ports.audio_transcriber import AudioTranscriber, DynamicProgressCallback, TranscribeProgressCallback
from core.entities.file_dto import FileInputDTO, FileOutputDTO


class FasterWhisperTranscriber(AudioTranscriber):
    def __init__(self, model_size="medium", compute_type="auto"):
        self.model = WhisperModel(
            model_size_or_path=model_size,
            compute_type=compute_type,
            device="cuda"
        )

    async def transcribe_dynamic(self, file_input: FileInputDTO, on_progress: DynamicProgressCallback) -> None:
        segments_raw, _ = self.model.transcribe(
            str(file_input.file_path),
            patience=1,
            beam_size=5,
            vad_filter=True
        )

        current_text = ""
        last_time = asyncio.get_event_loop().time()

        for seg in segments_raw:
            if not seg.text.strip():
                continue

            text_part = seg.text.strip()

            current_text += " " + text_part

            now = asyncio.get_event_loop().time()

            if now - last_time >= 2.0:
                if len(current_text) <= 4096:
                    await on_progress(current_text, False)
                else:
                    current_text = text_part
                    await on_progress(current_text, True)

                last_time = now


    async def transcribe(self, file_input: FileInputDTO, on_progress: TranscribeProgressCallback) -> FileOutputDTO:
        segments_raw, _ = self.model.transcribe(
            str(file_input.file_path),
            patience=1,
            beam_size=5,
            vad_filter=True
        )

        full_text = ""
        total_secs = file_input.file_duration.total_seconds()
        seconds_per_heart = total_secs / 10
        last_update = asyncio.get_event_loop().time()

        for seg in segments_raw:
            if not seg.text.strip():
                continue

            full_text += " " + seg.text.strip()
            filled_hearts = int(seg.end / seconds_per_heart)
            current_filled = min(filled_hearts, 10)
            print(current_filled)
            now = asyncio.get_event_loop().time()
            if now - last_update >= 2:
                try:
                    await on_progress(current_filled)
                except Exception as e:
                    continue

        file_output = FileOutputDTO(file_path=file_input.file_path.with_suffix(".txt"))
        async with aiofiles.open(file_output.file_path, "w") as f:
            await f.write(full_text)

        return file_output