from application.use_cases.file_handler_use_case import FileHandlerUseCase
from core.entities.file_dto import FileInputDTO, FileOutputDTO
from core.ports.image_text_extractor import ImageTextExtractor
from pathlib import Path


class ImageTextExtractorUseCase:
    def __init__(self, converter: ImageTextExtractor, file_handler: FileHandlerUseCase):
        self.output_dir = Path("./results/image_to_text").resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.converter = converter
        self.file_handler = file_handler

    async def image_to_text(self, f_input: FileInputDTO, is_handwritten: bool) -> FileOutputDTO:
        image = await self.file_handler.open_img(f_input.file_path)

        if is_handwritten:
            output_text = await self.converter.image_to_text_handwritten(fpath=f_input.file_path, image=image)
        else:
            output_text = await self.converter.image_to_text_printed(fpath=f_input.file_path, image=image)

        return await self.file_handler.save_as_txt(fpath=self.output_dir / f"{f_input.file_path.stem}.txt", text=output_text)