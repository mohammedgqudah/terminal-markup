from typing import List, Union
import random

import curses

from .geometry import Dimensions, Point
from .plane_interface import PlaneInterface
from .renderable_interface import RenderableInterface

colors = [
    (1, curses.COLOR_RED),
    (3, curses.COLOR_CYAN),
    (4, curses.COLOR_MAGENTA)
]

colors = iter(random.sample(colors, 3))


class Static(PlaneInterface):
    def __init__(self, children: List[Union[PlaneInterface, RenderableInterface]]):
        self.screen = None
        self.parent = None
        self.children = children
        self.position = None
        self.window = None

    def render(self, point: Point):
        self.position = point
        self.window = curses.newwin(*self.get_height_and_width(), *self.position)

        # --- TEMP ---
        c = next(colors)
        curses.init_pair(c[0], curses.COLOR_YELLOW, c[1])
        self.window.bkgd(curses.color_pair(c[0]))
        # --- TEMP ---

        last_height = 0
        for child in self.children:
            child.screen = self.screen
            child.parent = self
            child.render(Point(last_height, 0))
            last_height += child.get_height_and_width().height

        self.window.refresh()

    def get_height_and_width(self) -> Dimensions:
        [child.get_height_and_width() for child in self.children]
        height = sum([child.get_height_and_width().height for child in self.children])
        width = max([child.get_height_and_width().width for child in self.children])

        return Dimensions(height, width)
