from core.entities.file import File
from core.ports.photo_style_converter import PhotoStyleConverter
from pathlib import Path
from core.entities.file_dto import FileInputDTO, FileOutputDTO

class AsciiConverterUseCase:
    def __init__(self, converter: PhotoStyleConverter):
        self.converter = converter

    async def convert(self, file_input: FileInputDTO, add_color: bool=False) -> FileOutputDTO:
        return await self.converter.convert_image_to_ascii(file_input, add_color)