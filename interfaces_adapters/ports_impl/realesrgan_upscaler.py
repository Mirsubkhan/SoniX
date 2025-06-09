from core.ports.image_upscaler import ImageUpscaler
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer
from numpy import ndarray
from pathlib import Path
import asyncio
import torch


class RealERSGANUpscaler(ImageUpscaler):
    def __init__(self):
        model_path = r"C:\Users\Guest8\Desktop\GAR8S\Programming\Python\SoniX\RealESRGAN_x4plus.pth"
        state_dict = torch.load(model_path, map_location=torch.device("cuda"))['params_ema']

        self.model = RRDBNet(num_in_ch=3, num_out_ch=3, scale=4)
        self.model.load_state_dict(state_dict=state_dict, strict=True)

        self.up_sampler = RealESRGANer(scale=4, model_path=model_path, model=self.model, tile=0, pre_pad=0, half=True, tile_pad=10)

    async def upscale_image(self, image: ndarray, fpath: Path) -> ndarray:
        height = image.shape[0]
        width = image.shape[1]
        outscale = 2 if height and width > 2400 else 4

        output, _ = await asyncio.to_thread(
            lambda: self.up_sampler.enhance(img=image, outscale=outscale)
        )

        return output

