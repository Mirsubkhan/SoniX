from concurrent.futures.thread import ThreadPoolExecutor
from core.ports.image2text import Image2Text
from pathlib import Path
import easyocr
import asyncio
import re

class EasyOCRImage2Text(Image2Text):
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.reader = easyocr.Reader(['en', 'ru'], gpu=True)

    async def image_to_text(self, fpath: Path) -> str:
        result = await asyncio.to_thread(
            lambda: self.reader.readtext(
                str(fpath),
                decoder='beamsearch',
                beamWidth=100,
                paragraph=False
            )
        )
        extracted_text = await self._format_result(result)

        return "П-У-С-Т-О / E-M-P-T-Y" if not extracted_text else extracted_text

    @staticmethod
    async def _format_result(result):
        if not result:
            return ""

        first_item = result[0]
        has_confidence = len(first_item) == 3

        heights = []
        for item in result:
            box = item[0]
            y_coords = [point[1] for point in box]
            heights.append(max(y_coords) - min(y_coords))

        avg_height = sum(heights) / len(heights) if heights else 0
        lines = []
        current_line = []
        y_center_prev = None

        sorted_result = sorted(result, key=lambda x: min(x[0][0][1], x[0][1][1]))

        for item in sorted_result:
            box = item[0]
            text = item[1]

            y_min = min(point[1] for point in box)
            y_max = max(point[1] for point in box)
            y_center = (y_min + y_max) / 2

            if y_center_prev is None or abs(y_center - y_center_prev) < avg_height * 0.6:
                current_line.append((min(point[0] for point in box), text))
            else:
                if current_line:
                    lines.append(current_line)
                current_line = [(min(point[0] for point in box), text)]
            y_center_prev = y_center

        if current_line:
            lines.append(current_line)

        output_lines = []
        for line in lines:
            sorted_line = sorted(line, key=lambda x: x[0])
            output_lines.append(" ".join(text for _, text in sorted_line))

        return "\n\n".join(output_lines)