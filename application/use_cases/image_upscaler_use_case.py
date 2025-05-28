from core.entities.file_dto import FileInputDTO, FileOutputDTO
from core.ports.image_upscaler import ImageUpscaler

class UpscalerUseCase:
    def __init__(self, upscaler: ImageUpscaler):
        self.upscaler = upscaler

    async def upscale(self, file: FileInputDTO) -> FileOutputDTO:
        return await self.upscaler.upscale_image(file_input=file)



