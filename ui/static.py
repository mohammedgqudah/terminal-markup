from typing import List
import logging
import random
from itertools import cycle

import curses

from .geometry import Dimensions, Point
from ui.interfaces.renderable import Renderable

COLOR_GREY = 10


colors = [
    (1, curses.COLOR_RED),
    (3, COLOR_GREY),
    (4, curses.COLOR_MAGENTA),
    (5, curses.COLOR_CYAN)
]

colors = cycle(random.sample(colors, 4))


class Static(Renderable):
    """
    A Static is a container that can render a list of renderable children
    including other Statics.
    """
    def __init__(
            self,
            children: List[Renderable],
            id: str = None
    ):
        self.children = children
        self.id = id
        self.window = None

    def render(self, position: Point):
        self.parent.window.refresh()

        self.position = position
        self.window = curses.newwin(*self.get_height_and_width(), *self.position)

        logging.debug(f"window created for {self.__debug_repr__()}")

        # --- TEMP ---
        c = next(colors)
        curses.init_pair(c[0], curses.COLOR_YELLOW, c[1])
        self.window.bkgd(curses.color_pair(c[0]))
        # --- TEMP ---

        current_line = 0

        for child in self.children:
            child_y = current_line
            logging.debug(f"\trendering child {child.__debug_repr__()} at Y={child_y}")

            child.screen = self.screen
            child.parent = self

            if type(child) is Static:
                # Static windows position is relevant to the main screen and not the parent
                # to simulate rendering a static within another static, child Y will be
                # increased by the parent Y position.
                logging.debug(f"child is a Static. Y={child_y+child.parent.position.y}")
                child_y += child.parent.position.y

            child.render(Point(child_y, 0))

            # increment current_line by the current child height
            # so the next child gets rendered under it.
            current_line += child.get_height_and_width().height

        self.window.refresh()

    def get_height_and_width(self) -> Dimensions:
        [child.get_height_and_width() for child in self.children]
        height = sum([child.get_height_and_width().height for child in self.children])
        width = max([child.get_height_and_width().width for child in self.children])

        return Dimensions(height, width)

    def __repr__(self):
        return f"Static(id={self.id}, children={self.children})"
