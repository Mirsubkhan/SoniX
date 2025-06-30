from core.ports.audio_transcriber import AudioTranscriber, DynamicSSTCallback, STTCallback
from core.entities.file_dto import FileInputDTO
from faster_whisper import WhisperModel
from typing import Union
import asyncio


class FWhisperAudioTranscriber(AudioTranscriber):
    def __init__(self, model_size="large-v3", compute_type="auto"):
        self.model = WhisperModel(
            model_size_or_path=model_size,
            compute_type=compute_type,
            device="cuda"
        )

    async def transcribe_dynamic(
            self,
            file_input: FileInputDTO,
            on_progress: DynamicSSTCallback
    ) -> None:
        segments, _ = self._transcribe_segments(file_input)
        current_text = ""

        last_text_part = ""
        last_time = asyncio.get_event_loop().time()

        for seg in segments:
            text_part = seg.text.strip()
            if not text_part:
                continue

            current_text += f"{text_part} "

            now = asyncio.get_event_loop().time()
            if now - last_time >= 2.0:
                msg = current_text if len(current_text) <= 4096 else text_part
                if msg != last_text_part:
                    await on_progress(msg, len(current_text) > 4096)
                    last_text_part = msg
                current_text = current_text if len(current_text) <= 4096 else text_part
                last_time = now


        if current_text:
            msg = current_text if len(current_text) <= 4096 else current_text[-4096:]
            if msg != last_text_part and msg.strip() != "":
                await on_progress(msg, len(current_text) > 4096)

    async def transcribe(
            self,
            file_input: FileInputDTO,
            on_progress: Union[STTCallback, None]
    ) -> str:
        segments, _ = self._transcribe_segments(file_input)
        full_text = ""

        progress_tracker = None
        if on_progress is not None:
            total_secs = file_input.file_duration.total_seconds()
            seconds_per_heart = total_secs / 10
            last_update = asyncio.get_event_loop().time()
            progress_tracker = (seconds_per_heart, last_update)

        for seg in segments:
            text_part = seg.text.strip()
            if not text_part:
                continue

            full_text += f"{text_part} "

            if progress_tracker is None:
                continue

            seconds_per_heart, last_update = progress_tracker
            filled_hearts = int(seg.end / seconds_per_heart)
            current_filled = min(filled_hearts, 10)

            now = asyncio.get_event_loop().time()
            if now - last_update < 2.0:
                continue

            try:
                await on_progress(current_filled)
            except Exception:
                pass

            progress_tracker = (seconds_per_heart, now)

        return full_text.strip()

    def _transcribe_segments(self, file_input: FileInputDTO):
        return self.model.transcribe(
            str(file_input.file_path),
            patience=1,
            beam_size=5,
            vad_filter=True
        )