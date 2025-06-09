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

    async def image_to_text(self, f_input: FileInputDTO) -> FileOutputDTO:
        output_list = await self.converter.image_to_text(fpath=f_input.file_path)
        output_text = ' '.join(item[1] for item in output_list)

        if not output_text.strip():
            output_text = "П-У-С-Т-О-Т-А"

        return await self.file_handler.save_as_txt(fpath=self.output_dir / f"{f_input.file_path.stem}.txt", text=output_text)