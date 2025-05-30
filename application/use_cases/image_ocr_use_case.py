from application.use_cases.file_handler_use_case import FileHandlerUseCase
from core.entities.file_dto import FileInputDTO, FileOutputDTO
from core.ports.image_ocr import ImageOCR


class ImageOCRUseCase:
    def __init__(self, converter: ImageOCR, file_handler: FileHandlerUseCase):
        self.converter = converter
        self.file_handler = file_handler

    async def image_to_text(self, file_input: FileInputDTO, as_file: bool, is_handwritten: bool) -> FileOutputDTO:
        image = await self.file_handler.open_img(file_input.file_path)

        if is_handwritten:
            output = await self.converter.image_to_text_handwritten(fpath=file_input.file_path, image=image)
        else:
            output = await self.converter.image_to_text_handwritten(fpath=file_input.file_path, image=image)

        if as_file:
            return await self.file_handler.save_as_txt(fpath=output.file_path, text=output.file_txt)

        return output