from pathlib import Path

from application.use_cases.file_handler_use_case import FileHandlerUseCase
from core.ports.image_to_ascii import ImageToASCII
from core.entities.file_dto import FileInputDTO, FileOutputDTO

class AsciiConverterUseCase:
    def __init__(self, converter: ImageToASCII, file_handler: FileHandlerUseCase):
        self.converter = converter
        self.file_handler = file_handler

    async def convert(self, file_input: FileInputDTO, char_width: int=300) -> FileOutputDTO:
        image = await self.file_handler.open_img(file_input.file_path)

        output_img = await self.converter.image_to_ascii(image=image, fpath=file_input.file_path, char_width=char_width)
        output_path: Path = file_input.file_path.with_stem(file_input.file_path.stem + "_ascii").with_suffix(".png")
        output = await self.file_handler.save_img(image=output_img, fpath=output_path)

        return output