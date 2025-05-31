from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from core.ports.image_text_extractor import ImageTextExtractor
from concurrent.futures.thread import ThreadPoolExecutor
from core.entities.file_dto import FileOutputDTO
from PIL.Image import Image
from pathlib import Path
import asyncio


class TrImageTextExtractor(ImageTextExtractor):
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)

        self.h_processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten').to("cuda")
        self.h_model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten').to("cuda")

        self.p_processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-printed').to("cuda")
        self.p_model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-printed').to("cuda")

    async def image_to_text_handwritten(
            self,
            image: Image,
            fpath: Path
    ) -> str:
        return await asyncio.get_event_loop().run_in_executor(
            self.executor,
            self._process_handwritten,
            image
        )

    async def image_to_text_printed(
            self,
            image: Image,
            fpath: Path
    ) -> str:
        return await asyncio.get_event_loop().run_in_executor(
            self.executor,
            self._process_printed,
            image
        )

    def _process_handwritten(self, image: Image) -> str:
        pixel_values = self.h_processor(images=image, return_tensors="pt").pixel_values

        generated_ids = self.h_model.generate(pixel_values)
        generated_text = self.h_processor.batch_deocde(generated_ids, skip_special_tokens=False)[0]

        return generated_text

    def _process_printed(self, image: Image) -> str:
        pixel_values = self.p_processor(images=image, return_tensors="pt").pixel_values

        generated_ids = self.p_model.generate(pixel_values)
        generated_text = self.p_processor.batch_deocde(generated_ids, skip_special_tokens=False)[0]

        return generated_text
