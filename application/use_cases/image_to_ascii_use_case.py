from core.ports.image_to_ascii import ImageToASCII
from core.entities.file_dto import FileInputDTO, FileOutputDTO

class AsciiConverterUseCase:
    def __init__(self, converter: ImageToASCII):
        self.converter = converter

    async def convert(self, file_input: FileInputDTO, char_width: int=300) -> FileOutputDTO:
        return await self.converter.convert_image_to_ascii(file_input, char_width)