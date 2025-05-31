import asyncio
from pathlib import Path

import cv2
import torch
from basicsr.archs.rrdbnet_arch import RRDBNet
from numpy import ndarray
from core.ports.image_upscaler import ImageUpscaler
from core.entities.file_dto import FileInputDTO, FileOutputDTO
from realesrgan import RealESRGANer

model_path = r"C:\Users\Guest8\Desktop\GAR8S\Programming\Python\SoniX\RealESRGAN_x4plus.pth"
state_dict = torch.load(model_path, map_location=torch.device("cuda"))['params_ema']

class RealERSGANUpscaler(ImageUpscaler):
    def __init__(self):
        self.model = RRDBNet(num_in_ch=3, num_out_ch=3, scale=4)
        self.model.load_state_dict(state_dict=state_dict, strict=True)

        self.up_sampler = RealESRGANer(scale=4, model_path=model_path, model=self.model, tile=0, pre_pad=0, half=True, tile_pad=10)

    async def upscale_image(self, image: ndarray, fpath: Path) -> ndarray:
        output, _ = await asyncio.to_thread(
            self.up_sampler.enhance, img=image, outscale=4
        )

        return output

