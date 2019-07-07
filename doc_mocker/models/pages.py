import json
from pathlib import Path
from typing import Optional, Tuple
from uuid import uuid4

from ..fonts import Font
from ..utils import FunctionBindDescriptor
from .text import Text
from .writers import PILWriter


def _to_inches(millimeters: float) -> float:
    return millimeters / 25.4


def _to_millimeters(inches: float) -> float:
    return inches * 25.4


class Page:

    height_inches = FunctionBindDescriptor("height", _to_inches, _to_millimeters)
    width_inches = FunctionBindDescriptor("width", _to_inches, _to_millimeters)
    resolution = FunctionBindDescriptor("dpi", _to_inches, _to_millimeters)

    def __init__(self, height: int, width: int, dpi: int, columns=1) -> None:
        self.height = height
        self.width = width
        self.dpi = dpi
        self.margin_top = 20
        self.margin_left = 20
        self.content = []

        # TODO: Fix this for multiple columns
        self.column_with = self.width - 2 * self.margin_left / columns

        self.pointer = (self.margin_left, self.margin_top)

        # TODO: Inject this dependency as an abstraction
        self.writer = PILWriter(
            int(self.height_inches * self.dpi),
            int(self.width_inches * self.dpi),
            self.resolution,
        )

    @property
    def is_full(self) -> bool:
        return self.pointer[0] >= self.width - self.margin_left

    def write(self, text: Text, font: Font) -> None:
        # Calculate available window to write text
        window = (
            self.width - self.margin_left - self.pointer[0],
            self.height - self.margin_top - self.pointer[1],
        )

        # Write text and get dimensions
        width, height = self.writer.write_text(self.pointer, window, text, font)

        self.content.append(
            {
                "text": {
                    "value": text.value,
                    "x": self.pointer[0],
                    "y": self.pointer[1],
                    "width": width,
                    "height": height,
                }
            }
        )

        # Recalculate pointer position
        self.pointer = (self.pointer[0], self.pointer[1] + height)
        if self.pointer[1] > self.height - self.margin_top:
            self.pointer = (self.pointer[0] + self.column_with, self.margin_top)

    def paint(self, image: object, position: Optional[Tuple[int, int]]) -> None:
        self.writer.write_image(position or self.pointer, image)

    def save(self, path: Path):
        name = str(uuid4())
        (path / Path(f"{name}.json")).write_text(
            json.dumps(
                {
                    "height": self.height,
                    "width": self.width,
                    "dpi": self.dpi,
                    "content": self.content,
                }
            )
        )
        self.writer.save(path, name)
