import asyncio
from pathlib import Path
from typing import List

import aiofiles
from aiogram.types import Message
from faster_whisper import WhisperModel
from domain.repositories.transcriber import ITranscriber
from domain.entities.file import File
from domain.entities.transcription_result import TranscriptionResult, TranscriptionSegment
from datetime import timedelta


class FasterWhisperTranscriber(ITranscriber):
    def __init__(self, model_size="medium", compute_type="auto"):
        self.model = WhisperModel(
            model_size_or_path=model_size,
            compute_type=compute_type,
            device="cuda"
        )

    async def transcribe(self, file: File, message: Message = None, mid: int = None, rafile: bool = False):
        segments_raw, _ = self.model.transcribe(
            str(file.file_path),
            patience=1,
            beam_size=5,
            vad_filter=True
        )

        segments: List[TranscriptionSegment] = []
        all_text_parts: List[str] = []

        if not rafile:
            chat_id = message.chat.id
            current_text = ""
            last_update_time = asyncio.get_event_loop().time()
            await message.bot.delete_message(chat_id=chat_id, message_id=mid)
            sent_msg = await message.bot.send_message(chat_id=chat_id, text="⏳ Начинаю транскрибацию...")
            message_id = sent_msg.message_id

            for seg in segments_raw:
                if not seg.text.strip():
                    continue

                text_part = seg.text.strip()
                all_text_parts.append(text_part)

                s = TranscriptionSegment(
                    start=timedelta(seconds=seg.start),
                    end=timedelta(seconds=seg.end),
                    text=text_part
                )
                segments.append(s)
                current_text += " " + text_part

                try:
                    now = asyncio.get_event_loop().time()

                    if now - last_update_time >= 3:
                        await message.bot.edit_message_text(
                            chat_id=chat_id,
                            message_id=message_id,
                            text=current_text.strip()
                        )
                        last_update_time = now
                except Exception as e:
                    current_text = " "  + text_part
                    sent = await message.bot.send_message(chat_id=chat_id, text=current_text)
                    last_update_time = asyncio.get_event_loop().time()
                    message_id = sent.message_id
                    continue

            return None

        else:
            full_text = ""
            total_secs = file.file_duration.total_seconds()
            seconds_per_heart = total_secs / 10  # Правильно

            progress_message = await message.bot.send_message(
                chat_id=message.chat.id,
                text="🔄 Транскрибирую:\n🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍"
            )
            progress_msg_id = progress_message.message_id

            progress_bar_template = lambda filled: "💚" * filled + "🤍" * (10 - filled)
            last_update_time = asyncio.get_event_loop().time()
            current_filled = 0

            for seg in segments_raw:
                if not seg.text.strip():
                    continue

                full_text += " " + seg.text.strip()

                filled_hearts = int(seg.end / seconds_per_heart)
                if filled_hearts > current_filled:
                    current_filled = min(filled_hearts, 10)
                    progress_bar = progress_bar_template(current_filled)
                    now = asyncio.get_event_loop().time()
                    if now - last_update_time >= 3:
                        try:
                            await message.bot.edit_message_text(
                                chat_id=message.chat.id,
                                message_id=progress_msg_id,
                                text=f"🔄 Транскрибирую:\n{progress_bar}"
                            )
                            last_update_time = now
                        except Exception as e:
                            print(f"Ошибка редактирования прогресса: {e}")

            await message.bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=progress_msg_id,
                text="✅ Готово! Расшифровка завершена.\n💚💚💚💚💚💚💚💚💚💚"
            )

            text_path = file.file_path.with_suffix(".txt")
            async with aiofiles.open(text_path, "w") as f:
                await f.write(full_text)

            return Path(text_path)