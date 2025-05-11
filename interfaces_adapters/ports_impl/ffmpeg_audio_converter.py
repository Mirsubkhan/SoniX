import asyncio
import os
import uuid
from core.ports.audio_converter import AudioConverter
from core.entities.file import File
from pathlib import Path

class FFMpegAudioConverter(AudioConverter):
    def __init__(self, output_dir="./temp/audio_extracted"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    async def convert_to_wav(self, file: File) -> Path:
        output_path = os.path.join(self.output_dir, f"{uuid.uuid4().hex}.wav")
        cmd = f'ffmpeg -y -i "{file.file_path}" -acodec pcm_s16le -ar 16000 -ac 1 "{output_path}"'

        proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL)
        await proc.communicate()

        return Path(output_path)