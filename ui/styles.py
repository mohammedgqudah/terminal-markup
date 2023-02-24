import typing
from enum import Enum
from dataclasses import dataclass


class DisplayType(Enum):
    FLEX = 1
    INLINE = 2
    INLINE_BLOCK = 3


class OverflowType(Enum):
    HIDDEN = 1
    SCROLL = 2


@dataclass
class Display:
    type: DisplayType


@dataclass
class Padding:
    top: int = 0
    bottom: int = 0
    left: int = 0
    right: int = 0


@dataclass
class Styles:
    display: Display = Display(type=DisplayType.INLINE_BLOCK)
    max_height: typing.Optional[int] = None
    min_height: typing.Optional[int] = None
    max_width: typing.Optional[int] = None
    min_width: typing.Optional[int] = None
    overflow: OverflowType = OverflowType.SCROLL
    padding: Padding = Padding()

    def get(self, key, default=None):
        return getattr(self, key) or default
