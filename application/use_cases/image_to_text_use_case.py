import asyncio
from pathlib import Path
from core.entities.file import FileType
from core.entities.file_dto import FileInputDTO, FileOutputDTO
from core.ports.image_to_text_converter import ImageToTextConverter
from interfaces_adapters.ports_impl.easyocr_converter import EasyOCRImageToText


class ImageToTextUseCase:
    def __init__(self, converter: ImageToTextConverter):
        self.converter = converter

    async def image_to_text(self, file_input: FileInputDTO, as_file: bool = False, lang: str = "ru") -> FileOutputDTO:
        return await self.converter.image_to_text(file_input=file_input, as_file=as_file, lang=lang)


async def main():
    file = FileInputDTO(file_path=Path(
        r"C:\Users\Guest8\Downloads\photo_2025-05-13_21-29-48.jpg"),
                        file_type=FileType.PHOTO,
                        file_duration=None)

    converter = EasyOCRImageToText()
    file_out = await ImageToTextUseCase(converter=converter).image_to_text(file_input=file, lang="en")
    print(file_out.file_txt)

if __name__ == "__main__":
    asyncio.run(main())