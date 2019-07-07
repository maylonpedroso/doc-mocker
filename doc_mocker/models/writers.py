from pathlib import Path
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont

from doc_mocker.fonts import Font
from .text import Text


def points_to_millimeters(points: float) -> int:
    return int(points * 0.352778)


def millimeters_to_points(millimeters: float) -> int:
    return int(millimeters * 2.83465)


class PageImageWriter:
    def write_text(
        self, position: Tuple[int, int], window: Tuple[int, int], text: str, font: Font
    ) -> Tuple[int, int]:
        """
        Draw the supplied text with given font at given position
        :param position: position to draw text at
        :param window: size of the window the text must fit in
        :param text: string to draw in the image
        :param font: font info to generate text
        :return: None
        """
        raise NotImplementedError()

    def write_image(self, position: Tuple[int, int], image: object) -> Tuple[int, int]:
        raise NotImplementedError()

    def apply_filter(self, filter_: object) -> None:
        raise NotImplementedError()

    def save(self, path: Path) -> None:
        raise NotImplementedError()


class PILWriter(PageImageWriter):
    def __init__(self, height: int, width: int, resolution: float) -> None:
        self.image = Image.new("L", (width, height), 255)
        self.resolution: float = resolution

    def scale(self, value: int) -> int:
        return round(value * self.resolution)

    def unscale(self, value: int) -> int:
        return round(value / self.resolution)

    @staticmethod
    def _split_text(text: str, font: FreeTypeFont, window: Tuple[int, int]) -> str:
        right, bottom = window
        words = text.split()
        text = ""
        while words:
            starts = 0
            ends = len(words)
            while starts != ends:
                count = (starts + ends) // 2 + 1
                phrase = " ".join(words[:count])
                next_text = f"{text}\n{phrase}".strip()
                width, height = font.getsize_multiline(next_text)
                if height > bottom:
                    return text
                if width > right:
                    ends = count - 1
                else:
                    starts = count
            phrase = " ".join(words[:starts])
            text = f"{text}\n{phrase}".strip()
            words = words[starts + 1 :]  # noqa E203
        return text

    def write_text(
        self, position: Tuple[int, int], window: Tuple[int, int], text: Text, font: Font
    ) -> Tuple[int, int]:
        draw = ImageDraw.Draw(self.image)

        # Resize text based on its type
        font_size = millimeters_to_points(font.size * text.type.value)

        # TODO: Investigate how to include `italic`, `bold` and `underlined`
        # probably using multiple font files
        true_font = ImageFont.truetype(f"{font}", font_size)

        window = tuple(map(self.scale, window))
        position = tuple(map(self.scale, position))

        text_ = self._split_text(text.value, true_font, window)
        draw.multiline_text(position, text_, font=true_font)

        # Add a padding below the text
        box = tuple(map(self.unscale, true_font.getsize_multiline(text_)))
        return box[0], box[1] + int(font.size * text.type.value * 0.3)

    def write_image(self, position: Tuple[int, int], image: object):
        """
        Paste the supplied image at the given position
        :param position: Tuple(x, y) to paste the image a
        :param image: object to paste
        :return: None
        """
        self.image.paste(image, tuple(map(self.scale, position)))

    def apply_filter(self, filter_: object) -> None:
        if hasattr(filter_, "apply") and callable(filter_.apply):
            filter_.apply(self.image)
        else:
            raise TypeError(f"{type(filter_)} must implement `apply` method")

    def save(self, path: Path, name: str) -> None:
        self.image.save(path / Path(f"{name}.png"))
