from application.use_cases.file_handler_use_case import FileHandlerUseCase
from core.entities.file_dto import FileInputDTO, FileOutputDTO
from core.ports.ascii_converter import ASCIIConverter
from pathlib import Path


class ASCIIConverterUseCase:
    def __init__(self, converter: ASCIIConverter, file_handler: FileHandlerUseCase):
        self.output_dir = Path("./results/ascii_converted").resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.converter = converter
        self.file_handler = file_handler

    async def convert(self, f_input: FileInputDTO, char_width: int=300) -> FileOutputDTO:
        image = await self.file_handler.open_img(f_input.file_path)

        output_img = await self.converter.image_to_ascii(image=image, fpath=f_input.file_path, char_width=char_width)
        output_path = self.output_dir.joinpath(f_input.file_path.stem + "_ascii.png")

        return await self.file_handler.save_img(image=output_img, fpath=output_path)