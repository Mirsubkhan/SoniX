from core.ports.audio_extractor import AudioExtractor
from core.entities.file_dto import FileInputDTO, FileOutputDTO
from pathlib import Path
import asyncio


class FFMpegAudioExtractor(AudioExtractor):
    def __init__(self, output_dir: Path = Path("./results/audio_extracted")):
        self.output_dir = output_dir.resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def extract_audio_from_video(self, file_input: FileInputDTO) -> FileOutputDTO:
        file_output = FileOutputDTO(file_path=Path(self.output_dir.joinpath(f"{file_input.file_path.stem}.wav")))
        cmd = ["ffmpeg", "-y", "-i", str(file_input.file_path), "-vn", "-acodec", "pcm_s16le",
                "-ar", "16000", "-ac", "1", str(file_output.file_path)]

        proc = await asyncio.create_subprocess_shell(" ".join(cmd), stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL)
        await proc.communicate()

        if proc.returncode != 0:
            raise RuntimeError(f"FFmpeg failed with code {proc.returncode}")

        if not file_output.file_path.exists():
            raise FileNotFoundError(f"Expected output file not found: {file_output.file_path}")

        return file_output