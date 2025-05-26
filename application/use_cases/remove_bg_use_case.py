from core.entities.file_dto import FileInputDTO, FileOutputDTO
from core.ports.background_remover import BackgroundRemover


class BgRemoverUseCase:
    def __init__(self, remover: BackgroundRemover):
        self.remover = remover

    async def remove_bg(self, file: FileInputDTO) -> FileOutputDTO:
        return await self.remover.remove_bg(file=file)



