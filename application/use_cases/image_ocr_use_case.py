from core.entities.file_dto import FileInputDTO, FileOutputDTO
from core.ports.image_ocr import ImageOCR


class ImageOCRUseCase:
    def __init__(self, converter: ImageOCR):
        self.converter = converter

    async def image_to_text(self, file_input: FileInputDTO, as_file: bool = False, lang: str = "ru") -> FileOutputDTO:
        return await self.converter.image_to_text(file_input=file_input, as_file=as_file, lang=lang)