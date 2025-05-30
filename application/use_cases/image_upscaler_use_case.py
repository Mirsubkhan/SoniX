from application.use_cases.file_handler_use_case import FileHandlerUseCase
from core.entities.file_dto import FileInputDTO, FileOutputDTO
from core.ports.image_upscaler import ImageUpscaler

class UpscalerUseCase:
    def __init__(self, upscaler: ImageUpscaler, file_handler: FileHandlerUseCase):
        self.upscaler = upscaler
        self.file_handler = file_handler

    async def upscale(self, file: FileInputDTO) -> FileOutputDTO:
        image = await self.file_handler.open_img_with_cv2(fpath=file.file_path)

        return await self.upscaler.upscale_image(image=image, fpath=file.file_path)

        # await self.file_handler.save_img_with_cv2(fpath=output.file_path, image=)


