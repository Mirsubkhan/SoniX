import asyncio
import warnings
from concurrent.futures.thread import ThreadPoolExecutor
from pathlib import Path
from PIL import Image
from exceptiongroup import catch

from core.entities.file_dto import FileInputDTO, FileOutputDTO
from core.ports.bg_remover import BgRemover
import torch
from transformers import AutoModelForImageSegmentation
from torchvision import transforms
import tensorflow as tf

class BiRefNETRemover(BgRemover):
    def __init__(self, output_dir: Path = Path("./bg_removed")):
        self.output_dir = output_dir.resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.executor = ThreadPoolExecutor(max_workers=4)

        tf.get_logger().setLevel('ERROR')
        tf.autograph.set_verbosity(0)
        warnings.filterwarnings("ignore", module="tensorflow")

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

    async def remove_bg(self, file: FileInputDTO) -> FileOutputDTO:
        im = await asyncio.to_thread(
            lambda: Image.open(file.file_path).convert("RGB")
        )

        res = await asyncio.get_event_loop().run_in_executor(
            self.executor,
            self._process_image_sync,
            im,
            file.file_path.stem
        )

        return FileOutputDTO(file_path=res)

    def _process_image_sync(self, im: Image.Image, stem: str) -> Path:
        try:
            im_size = im.size

            input_tensor = self.transform_image(im).unsqueeze(0).to("cuda")

            with torch.no_grad():
                preds = self.model(input_tensor)[-1].sigmoid().cpu()

            mask = transforms.ToPILImage()(preds[0].squeeze()).resize(im_size)
            im.putalpha(mask)

            output_path = self.output_dir / f"{stem}_nobg.png"
            im.save(output_path)

            return output_path
        except Exception as e:
            raise RuntimeError(f"Image processing failed: {str(e)}")
