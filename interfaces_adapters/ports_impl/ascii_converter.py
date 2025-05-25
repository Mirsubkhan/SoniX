from core.ports.photo_style_converter import PhotoStyleConverter
from PIL import Image, ImageFont, ImageDraw
import numpy as np
from core.entities.file_dto import FileInputDTO, FileOutputDTO

ASCII_CHARS = r"$@B%8&WM#*oahkbdpqwmZ0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]

class AsciiConverter(PhotoStyleConverter):
    def __init__(self, chars: str=ASCII_CHARS):
        self.ascii_chars = chars
        self.font =ImageFont.load_default()

    async def map_pixels_to_ascii(self, image: Image, add_color=False) -> Image:
        pixels = np.array(image)
        width, height = image.size

        bbox = self.font.getbbox("A")
        char_width = bbox[2] - bbox[0]
        char_height = bbox[3] - bbox[1]

        output_width = width * char_width
        output_height = height * char_height

        bg_color = (255, 255, 255) if not add_color else (0, 0, 0)
        text_color = lambda r, g, b: (r, g, b) if add_color else (0, 0, 0)

        ascii_image = Image.new("RGB", (output_width, output_height), color=bg_color)
        draw = ImageDraw.Draw(ascii_image)

        for y in range(height):
            for x in range(width):
                r, g, b = pixels[y, x][:3]
                brightness = int(0.299 * r + 0.587 * g + 0.114 * b)
                char = ASCII_CHARS[brightness * len(ASCII_CHARS) // 256]
                draw.text((x * char_width, y * char_height), char, fill=text_color(r, g, b), font=self.font)

        return ascii_image

    async def convert_image_to_ascii(self, file_input: FileInputDTO, add_color: bool = False) -> FileOutputDTO:
        image = Image.open(file_input.file_path).convert("RGB")

        target_char_width = 260
        bbox = self.font.getbbox("A")
        char_width = bbox[2] - bbox[0]
        char_height = bbox[3] - bbox[1]

        new_width = target_char_width
        new_height = int((image.height / image.width) * new_width * (char_width / char_height))
        image = image.resize((new_width, new_height))

        ascii_img = await self.map_pixels_to_ascii(image, add_color)

        file_output = FileOutputDTO(file_path = file_input.file_path.with_stem(file_input.file_path.stem + "_ascii").with_suffix(".png"))
        ascii_img.save(file_output.file_path)

        return file_output
