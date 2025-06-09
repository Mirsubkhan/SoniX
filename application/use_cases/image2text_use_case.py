from application.use_cases.file_handler_use_case import FileHandlerUseCase
from core.entities.file_dto import FileInputDTO, FileOutputDTO
from core.ports.image2text import Image2Text
from pathlib import Path


class Image2TextUseCase:
    def __init__(self, converter: Image2Text, file_handler: FileHandlerUseCase):
        self.output_dir = Path("./results/image_to_text").resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.converter = converter
        self.file_handler = file_handler

    async def image_to_text(self, f_input: FileInputDTO) -> FileOutputDTO:
        extracted_text = await self.converter.image_to_text(fpath=f_input.file_path)

        return await self.file_handler.save_as_txt(
            fpath=self.output_dir / f"{f_input.file_path.stem}.txt",
            text=extracted_text
        )