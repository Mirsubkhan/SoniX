from core.entities.file import File
from core.ports.photo_style_converter import PhotoStyleConverter
from pathlib import Path

class AsciiConverterUseCase:
    def __init__(self, converter: PhotoStyleConverter):
        self.converter = converter

    async def convert(self, file: File, add_color: bool=False) -> Path:
        return await self.converter.convert_image_to_ascii(file, add_color)