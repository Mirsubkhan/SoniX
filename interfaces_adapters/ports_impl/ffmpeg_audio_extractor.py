import asyncio
import os
from core.ports.audio_extractor import AudioExtractor
from core.entities.file_dto import FileInputDTO, FileOutputDTO
from pathlib import Path

class FFMpegAudioExtractor(AudioExtractor):
    def __init__(self, output_dir="./temp/audio_extracted"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    async def extract_audio_from_video(self, file_input: FileInputDTO) -> FileOutputDTO:
        file_output = FileOutputDTO(file_path=Path(os.path.join(self.output_dir, f"{file_input.file_path.stem}.wav")))
        cmd = f'ffmpeg -y -i "{file_input.file_path}" -vn -acodec pcm_s16le -ar 16000 -ac 1 "{file_output}"'

        proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL)
        await proc.communicate()

        return file_output