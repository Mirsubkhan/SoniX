from core.entities.file_dto import FileInputDTO, FileOutputDTO
from core.ports.bg_remover import BgRemover


class BgRemoverUseCase:
    def __init__(self, remover: BgRemover):
        self.remover = remover

    async def remove_bg(self, file: FileInputDTO) -> FileOutputDTO:
        return await self.remover.remove_bg(file=file)



