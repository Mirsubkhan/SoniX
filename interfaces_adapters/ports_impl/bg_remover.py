import asyncio
from pathlib import Path
from PIL import Image
from core.entities.file_dto import FileInputDTO, FileOutputDTO
from core.ports.background_remover import BackgroundRemover
import torch
from transformers import AutoModelForImageSegmentation
from torchvision import transforms
from torchvision.transforms._functional_tensor import rgb_to_grayscale

class BgRemover(BackgroundRemover):
    def __init__(self, output_dir: Path = Path("./bg_removed_imgs")):
        self.output_dir = output_dir.resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def remove_bg(self, file: FileInputDTO) -> FileOutputDTO:
        torch.set_float32_matmul_precision("high")
        birefnet = AutoModelForImageSegmentation.from_pretrained(
            "ZhengPeng7/BiRefNet", trust_remote_code=True
        )
        birefnet.to("cuda")
        transform_image = transforms.Compose([
            transforms.Resize((1024, 1024)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ])

        im = Image.open(file.file_path).convert("RGB")
        image_size = im.size

        input_tensor = transform_image(im).unsqueeze(0).to("cuda")

        with torch.no_grad():
            preds = birefnet(input_tensor)[-1].sigmoid().cpu()
        mask = transforms.ToPILImage()(preds[0].squeeze()).resize(image_size)

        im.putalpha(mask)

        output = FileOutputDTO(file_path=self.output_dir / (file.file_path.stem + "_nobg.png"))

        im.save(output.file_path)

        return output
