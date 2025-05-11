import asyncio
import subprocess
from core.ports.audio_separator import AudioSeparator, ProgressCallback
from core.entities.file import File
from pathlib import Path

class DemucsSeparator(AudioSeparator):
    def __init__(self, output_dir: Path = Path("./separated")):
        self.output_dir = output_dir.resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def separate(self, file: File, on_progress: ProgressCallback) -> Path:
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

        while True:
            line = await process.stdout.readline()
            if not line:
                break

            decoded = line.decode().strip()

            if "100%|" in decoded:
                progress_bars_completed += 1
                total_progress_percent = progress_bars_completed * 25
                total_progress_percent = min(total_progress_percent, 100)

                try:
                    await on_progress(total_progress_percent)
                except Exception as e:
                    print(f"Ошибка при вызове on_progress: {e}")

        await process.wait()

        input_stem = Path(file.file_path).stem
        result_dir = self.output_dir / "mdx_extra" / input_stem

        if not result_dir.exists():
            raise ValueError(f"Demucs не создал папку с результатами: {result_dir}")

        return result_dir
