import asyncio
from pathlib import Path

from core.ports.image_to_ascii import ImageToASCII
from PIL import Image, ImageFont, ImageDraw
import numpy as np
from core.entities.file_dto import FileInputDTO, FileOutputDTO

ASCII_CHARS = r"$@B%8&WM#*oahkbdpqwmZ0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]

class AsciiConverter(ImageToASCII):
    def __init__(self, chars: str=ASCII_CHARS):
        self.ascii_chars = chars
        self.font =ImageFont.load_default()
        self.char_width, self.char_height = self._get_char_dimensions()

    async def map_pixels_to_ascii(self, image: Image, add_color=False) -> Image:
        pixels = np.array(image)
        width, height = image.size

        output_size = (width * self.char_width, height * self.char_height)

        ascii_image = Image.new("RGB", output_size, color=(0, 0, 0))
        draw = ImageDraw.Draw(ascii_image)

        for y in range(height):
            for x in range(width):
                r, g, b = pixels[y, x][:3]
                char = await self._brightness_to_ascii(r, g, b)
                draw.text(
                    (x * self.char_width, y * self.char_height),
                    char,
                    fill=(r, g, b),
                    font=self.font
                )

        return ascii_image

    async def convert_image_to_ascii(self, file_input: FileInputDTO, add_color: bool = False) -> FileOutputDTO:
        image = Image.open(file_input.file_path).convert("RGB")
        resized_image = await self._resize_image(image)

        ascii_img = await self.map_pixels_to_ascii(resized_image, add_color)

        output_path: Path = file_input.file_path.with_stem(
            file_input.file_path.stem + "_ascii"
        ).with_suffix(".png")

        ascii_img.save(output_path)

        return FileOutputDTO(file_path=output_path)

    async def _get_char_dimensions(self) -> tuple[int, int]:
        bbox = self.font.getbbox("A")
        return int(bbox[2] - bbox[0]), int(bbox[3] - bbox[1])

    async def _brightness_to_ascii(self, r: int, g: int, b: int) -> str:
        brightness = int(0.299 * r + 0.587 * g + 0.114 * b)
        index = brightness * len(self.ascii_chars) // 256
        return self.ascii_chars[index]

    async def _resize_image(self, image: Image.Image, target_char_width: int = 260) -> Image.Image:
        aspect_ratio = image.height / image.width
        new_width = target_char_width
        new_height = int(aspect_ratio * new_width * (self.char_width / self.char_height))
        return await asyncio.to_thread(lambda: image.resize((new_width, new_height)))