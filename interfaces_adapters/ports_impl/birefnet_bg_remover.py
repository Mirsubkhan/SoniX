import asyncio
import warnings
from concurrent.futures.thread import ThreadPoolExecutor
from pathlib import Path
from PIL.Image import Image
from core.entities.file_dto import FileInputDTO, FileOutputDTO
from core.ports.bg_remover import BgRemover
import torch
from transformers import AutoModelForImageSegmentation
from torchvision import transforms
import tensorflow as tf

class BiRefNETBgRemover(BgRemover):
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)

        torch.set_float32_matmul_precision("high")
        self.model = AutoModelForImageSegmentation.from_pretrained(
            "ZhengPeng7/BiRefNet",
            trust_remote_code=True
        ).to("cuda")

        self.transform_image = transforms.Compose([
            transforms.Resize((1024, 1024)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            ),
        ])

    async def remove_bg(self, image: Image) -> Image:
        return await asyncio.get_event_loop().run_in_executor(
            self.executor,
            self._process_image_sync,
            image
        )

    def _process_image_sync(self, image: Image) -> Image:
        try:
            im_size = image.size

            input_tensor = self.transform_image(image).unsqueeze(0).to("cuda")

            with torch.no_grad():
                preds = self.model(input_tensor)[-1].sigmoid().cpu()

            mask = transforms.ToPILImage()(preds[0].squeeze()).resize(im_size)
            image.putalpha(mask)

            return image
        except Exception as e:
            raise RuntimeError(f"Image processing failed: {str(e)}")
