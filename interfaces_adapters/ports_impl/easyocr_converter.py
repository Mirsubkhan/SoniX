import asyncio
from pathlib import Path

import aiofiles

from core.entities.file_dto import FileInputDTO, FileOutputDTO
from core.ports.image_to_text_converter import ImageToTextConverter
from easyocr import easyocr

class EasyOCRImageToText(ImageToTextConverter):
    def __init__(self, output_dir: Path = Path("./image_to_text")):
        self.output_dir = output_dir.resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)


    async def image_to_text(self, file_input: FileInputDTO, as_file: bool, lang: str) -> FileOutputDTO:
        reader = easyocr.Reader(['ru', 'en'], gpu=True)
        result = await asyncio.to_thread(reader.readtext,str(file_input.file_path))
        extracted_text = ' '.join(item[1] for item in result)

        output_path = self.output_dir / f"{file_input.file_path.stem}.txt"
        file_output = FileOutputDTO(file_path=output_path, file_txt=extracted_text)

        if as_file:
            async with aiofiles.open(file_output.file_path, "w") as f:
                await f.write(file_output.file_txt)

        return file_output