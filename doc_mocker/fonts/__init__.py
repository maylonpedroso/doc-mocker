from pathlib import Path


class Font:
    filename: Path = "undefined"
    italic = False
    bold = False
    underlined = False

    def __init__(self, size):
        self.size = size

    def __str__(self):
        return str(Path(__file__).parent / f"files/{self.filename}")


class Arial(Font):
    filename = "arial.ttf"


class TimesNewRoman(Font):
    filename = "times-new-roman.ttf"
