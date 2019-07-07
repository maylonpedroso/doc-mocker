from enum import Enum

from .pages import Page  # noqa: F401
from .text import Text, TextType  # noqa: F401


class PageType(Enum):
    A4 = (292, 210)
