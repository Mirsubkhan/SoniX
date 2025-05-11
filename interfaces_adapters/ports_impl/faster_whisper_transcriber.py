import asyncio
from pathlib import Path
import aiofiles
from faster_whisper import WhisperModel
from core.ports.audio_transcriber import AudioTranscriber, DynamicProgressCallback, TranscribeProgressCallback
from core.entities.file import File
from core.entities.transcription_result import TranscriptionSegment
from datetime import timedelta

class FasterWhisperTranscriber(AudioTranscriber):
    def __init__(self, model_size="medium", compute_type="auto"):
        self.model = WhisperModel(
            model_size_or_path=model_size,
            compute_type=compute_type,
            device="cuda"
        )

    async def transcribe_dynamic(self, file: File, on_progress: DynamicProgressCallback):
        segments_raw, _ = self.model.transcribe(
            str(file.file_path),
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

            s = TranscriptionSegment(
                start=timedelta(seconds=seg.start),
                end=timedelta(seconds=seg.end),
                text=text_part
            )

            current_text += " " + text_part

            now = asyncio.get_event_loop().time()

            if now - last_time >= 2:
                await on_progress(current_text.strip())
                last_time = now


    async def transcribe(self, file: File, on_progress: TranscribeProgressCallback) -> Path:
        segments_raw, _ = self.model.transcribe(
            str(file.file_path),
            patience=1,
            beam_size=5,
            vad_filter=True
        )

        full_text = ""
        total_secs = file.file_duration.total_seconds()
        seconds_per_heart = total_secs / 10

        for seg in segments_raw:
            if not seg.text.strip():
                continue

            full_text += " " + seg.text.strip()
            filled_hearts = int(seg.end / seconds_per_heart)
            current_filled = min(filled_hearts, 10)

            try:
                await on_progress(current_filled)
            except Exception as e:
                print(f"Ошибка при вызове on_progress: {e}")

        text_path = file.file_path.with_suffix(".txt")
        async with aiofiles.open(text_path, "w") as f:
            await f.write(full_text)

        return Path(text_path)