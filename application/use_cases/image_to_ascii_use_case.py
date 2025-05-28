from core.ports.image_to_ascii import ImageToASCII
from core.entities.file_dto import FileInputDTO, FileOutputDTO

class AsciiConverterUseCase:
    def __init__(self, converter: ImageToASCII):
        self.converter = converter

    async def convert(self, file_input: FileInputDTO, add_color: bool=False) -> FileOutputDTO:
        return await self.converter.convert_image_to_ascii(file_input, add_color)