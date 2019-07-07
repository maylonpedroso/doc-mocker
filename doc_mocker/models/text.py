from enum import Enum


class TextType(Enum):
    NORMAL = 1.0
    TITLE = 2.0
    SUBTITLE = 1.5


class Text:
    def __init__(self, value: str, type_: TextType = TextType.NORMAL):
        self.value = value.replace("\n", " ").replace("  ", " ")
        self.type = type_
