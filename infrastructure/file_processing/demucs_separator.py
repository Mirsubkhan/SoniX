import asyncio
import os
import shutil
import subprocess
import uuid

from aiogram.types import Message

from domain.repositories.separator import ISeparator
from domain.entities.file import File
from pathlib import Path
import demucs.separate

class DemucsSeparator(ISeparator):
    def __init__(self, output_dir: Path = Path("./separated")):
        self.output_dir = output_dir.resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def separate(self, file: File, message: Message) -> Path:
        cmd = [
            "python", "-m", "demucs.separate",
            "--mp3",
            "--two-stems", "vocals",
            "-n", "mdx_extra",
            "-d", "cuda",
            "-o", str(self.output_dir),
            str(file.file_path)
        ]

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        progress_bars_completed = 0
        last_progress = ""
        edit_msg = await message.answer("Минуточку...")
        last_time = asyncio.get_event_loop().time()
        while True:
            line = await process.stdout.readline()
            if not line:
                print("not line")
                break
            decoded = line.decode().strip()
            print(decoded)

            if "100%|" in decoded:
                progress_bars_completed += 1

            total_progress_percent = progress_bars_completed * 25
            heart_count = total_progress_percent // 10
            hearts = "💚" * heart_count + "🤍" * (10 - heart_count)

            if hearts != last_progress:
                last_progress = hearts

                try:
                    now = asyncio.get_event_loop().time()
                    if now - last_time >= 2:
                        await message.bot.edit_message_text(text=f"🎧 Обработка аудио...\nПрогресс: {hearts}",
                                                            message_id=edit_msg.message_id,
                                                            chat_id=message.chat.id)
                        last_time = now

                except Exception as e:
                    print(f"Не удалось обновить сообщение: {e}")


        await process.wait()

        input_stem = Path(file.file_path).stem
        result_dir = self.output_dir / "mdx_extra" / input_stem

        if not result_dir.exists():
            raise ValueError(f"Demucs не создал папку с результатами: {result_dir}")

        return result_dir
