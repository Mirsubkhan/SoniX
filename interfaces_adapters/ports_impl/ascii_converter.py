from core.ports.art_converter import ArtConverter
from PIL import Image, ImageFont, ImageDraw
from pathlib import Path
import numpy as np
import asyncio


class ASCIIConverter(ArtConverter):
    def __init__(self):
        self.ascii_chars = r"$@B%8&WM#*oahkbdpqwmZ0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]
        self.font_path = Path(r"C:\Users\Guest8\Desktop\GAR8S\Programming\Python\SoniX\Montserrat-ExtraBold.ttf")
        self.font = ImageFont.truetype(str(self.font_path))
        self.char_width, self.char_height = self._get_char_dimensions()

    async def image_to_ascii(self, image: Image.Image, char_width: int = 300) -> Image.Image:
        resized_image = await self._resize_image(image, target_char_width=char_width)
        ascii_img = await self._map_pixels_to_ascii(resized_image)

        return ascii_img

    async def _map_pixels_to_ascii(self, image: Image.Image) -> Image.Image:
        pixels = np.array(image)
        width, height = image.size

        output_size = (width * self.char_width, height * self.char_height)

        ascii_image = Image.new("RGB", output_size, color=(0, 0, 0))
        draw = ImageDraw.Draw(ascii_image)

        for y in range(height):
            for x in range(width):
                r, g, b = pixels[y, x][:3]
                char = self._brightness_to_ascii(r, g, b)

                draw.text(
                    (x * self.char_width, y * self.char_height),
                    char,
                    fill=(r, g, b),
                    font=self.font
                )

        return ascii_image

    async def _resize_image(self, image: Image.Image, target_char_width: int = 300) -> Image.Image:
        aspect_ratio = image.height / image.width
        new_width = target_char_width
        new_height = int(aspect_ratio * new_width * (self.char_width / self.char_height))
        return await asyncio.to_thread(lambda: image.resize((new_width, new_height)))

    def _get_char_dimensions(self) -> tuple[int, int]:
        bbox = self.font.getbbox("A")
        return int(bbox[2] - bbox[0]), int(bbox[3] - bbox[1])

    def _brightness_to_ascii(self, r: int, g: int, b: int) -> str:
        brightness = int(0.299 * r + 0.587 * g + 0.114 * b)
        index = brightness * len(self.ascii_chars) // 256
        return self.ascii_chars[index]


