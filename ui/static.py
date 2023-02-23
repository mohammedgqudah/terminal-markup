from typing import List, Union
import logging
import random
from itertools import cycle

import curses

from .geometry import Dimensions, Point
from .plane_interface import PlaneInterface
from .renderable_interface import RenderableInterface

COLOR_GREY = 10


colors = [
    (1, curses.COLOR_RED),
    (3, COLOR_GREY),
    (4, curses.COLOR_MAGENTA),
    (5, curses.COLOR_CYAN)
]

colors = cycle(random.sample(colors, 4))


class Static(PlaneInterface):
    def __init__(self, children: List[Union[PlaneInterface, RenderableInterface]], id: str = None):
        self.screen = None
        self.parent = None
        self.children = children
        self.position = None
        self.window = None
        self.id = id

    def render(self, point: Point):
        # I have to refresh the parent window before adding more windows
        self.parent.window.refresh()

        self.position = point
        self.window = curses.newwin(*self.get_height_and_width(), *self.position)

        logging.debug(f"rendering: {self}")

        # --- TEMP ---
        c = next(colors)
        curses.init_pair(c[0], curses.COLOR_YELLOW, c[1])
        self.window.bkgd(curses.color_pair(c[0]))
        # --- TEMP ---

        last_height = 0
        for child in self.children:
            y = last_height

            logging.debug(f"y={y}")

            child.screen = self.screen
            child.parent = self

            if type(child) is Static:
                logging.debug(f"static found {child}, y={y+child.parent.position.y}")
                y += child.parent.position.y

            child.render(Point(y, 0))
            last_height += child.get_height_and_width().height

        self.window.refresh()

    def get_height_and_width(self) -> Dimensions:
        [child.get_height_and_width() for child in self.children]
        height = sum([child.get_height_and_width().height for child in self.children])
        width = max([child.get_height_and_width().width for child in self.children])

        return Dimensions(height, width)

    def __repr__(self):
        return f"Static(id={self.id}, position={self.position}, dimensions={self.get_height_and_width()})"
