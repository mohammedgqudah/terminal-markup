from enum import Enum
from dataclasses import dataclass


class DisplayType(Enum):
    FLEX = 1
    INLINE = 2
    INLINE_BLOCK = 3


@dataclass
class Display:
    type: DisplayType


class Styles:
    def __init__(self):
        self.display: Display = Display(type=DisplayType.INLINE_BLOCK)
        