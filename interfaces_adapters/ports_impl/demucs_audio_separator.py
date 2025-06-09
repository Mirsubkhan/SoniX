from core.ports.audio_separator import AudioSeparator, SeparatorProgressCallback
from core.entities.file_dto import FileInputDTO, FileOutputDTO
from typing import Union
from pathlib import Path
import subprocess
import asyncio
import sys


class DemucsAudioSeparator(AudioSeparator):
    def __init__(self, output_dir: Path = Path("./results/separated")):
        self.output_dir = output_dir.resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def separate(
            self,
            file_input: FileInputDTO,
            on_progress: Union[SeparatorProgressCallback, None]
    ) -> FileOutputDTO:
        cmd = [
            sys.executable, "-m", "demucs.separate",
            "--mp3",
            "--two-stems", "vocals",
            "-n", "mdx_extra",
            "-d", "cuda",
            "-o", str(self.output_dir),
            str(file_input.file_path)
        ]

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        if on_progress is not None:
            progress_bars_completed = 0
            last_update = asyncio.get_event_loop().time()

            while True:
                line = await process.stdout.readline()
                if not line:
                    break

                decoded = line.decode().strip()

                if "100%|" in decoded:
                    progress_bars_completed += 1
                    total_progress_percent = progress_bars_completed * 25
                    total_progress_percent = min(total_progress_percent, 100)

                    now = asyncio.get_event_loop().time()
                    if now - last_update >= 2:
                        try:
                            await on_progress(total_progress_percent)
                            last_update = now
                        except Exception as e:
                            pass

        await process.wait()

        if process.returncode != 0:
            raise RuntimeError(f"Demucs failed with code: {process.returncode}")

        result_dir = FileOutputDTO(file_path=self.output_dir / file_input.file_path.stem)
        if not result_dir.file_path.exists():
            raise ValueError(f"Demucs didn't create the dir with results: {result_dir.file_path}")

        return result_dir
