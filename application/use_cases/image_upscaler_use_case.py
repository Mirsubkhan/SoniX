from application.use_cases.file_handler_use_case import FileHandlerUseCase
from core.entities.file_dto import FileInputDTO, FileOutputDTO
from core.ports.image_upscaler import ImageUpscaler
from pathlib import Path


class ImageUpscalerUseCase:
    def __init__(self, upscaler: ImageUpscaler, file_handler: FileHandlerUseCase):
        self.output_dir = Path("./results/upscaled_images").resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.upscaler = upscaler
        self.file_handler = file_handler

    async def upscale(self, file: FileInputDTO) -> FileOutputDTO:
        image = await self.file_handler.open_img_with_cv2(fpath=file.file_path)

        output = await self.upscaler.upscale_image(image=image, fpath=file.file_path)

        output_dir = self.output_dir.joinpath(file.file_path.stem + ".png")

        return await self.file_handler.save_img_with_cv2(fpath=output_dir, image=output)

