from application.use_cases.file_handler_use_case import FileHandlerUseCase
from core.entities.file_dto import FileInputDTO, FileOutputDTO
from core.ports.bg_remover import BgRemover
from pathlib import Path


class BgRemoverUseCase:
    def __init__(self, remover: BgRemover, f_handler: FileHandlerUseCase):
        self.output_dir = Path("./results/removed_bgs").resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.remover = remover
        self.f_handler = f_handler

    async def remove_bg(self, f_input: FileInputDTO) -> FileOutputDTO:
        image = await self.f_handler.open_img(f_input.file_path)

        no_bg_img = await self.remover.remove_bg(image=image)

        return await self.f_handler.save_img(image=no_bg_img, fpath=self.output_dir.joinpath(f_input.file_path.stem + ".png"))