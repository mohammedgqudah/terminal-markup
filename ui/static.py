import typing
import logging
import random
from itertools import cycle

import curses

from .geometry import Dimensions, Point
from .renderable import Renderable
from .styles import Styles, DisplayType

COLOR_GREY = 10


colors = [
    (3, COLOR_GREY),
    (5, curses.COLOR_CYAN),
    (4, curses.COLOR_MAGENTA),
    (1, curses.COLOR_RED),
]

colors = cycle(colors)


class Static(Renderable):
    """
    A Static is a container that can render a list of renderable children
    including other Statics.
    """
    def __init__(
            self,
            children: typing.List[Renderable],
            id: str = None,
            styles: typing.Optional[Styles] = None
    ):
        self.children = children
        self.id = id
        self.window = None
        self.styles = styles or self.styles

    def render(self, position: Point):
        self.parent.window.refresh()

        self.position = position
        self.window = curses.newwin(*self.get_height_and_width(), *self.position)

        logging.debug(f"window created for {self.__debug_repr__()}")

        # --- TEMP ---
        c = next(colors)
        curses.init_pair(c[0], curses.COLOR_YELLOW, c[1])
        # self.window.bkgd(curses.color_pair(c[0]))
        # --- TEMP ---

        current_line = 0
        current_column = 0
        previous_child = None

        for child in self.children:
            # if the previous child was displayed inline, current child can be rendered right next to it
            # only if it's styled to be rendered inline, otherwise, the current column will be reset
            # and the line will increment based in the previous child height.
            if previous_child and previous_child.styles.display.type == DisplayType.INLINE_BLOCK and child.styles.display.type != DisplayType.INLINE_BLOCK:
                current_column = 0
                current_line += previous_child.get_height_and_width().height

            child_y = current_line
            child_x = current_column
            logging.debug(f"\trendering child {child.__debug_repr__()} at Y={child_y}")

            child.screen = self.screen
            child.parent = self

            if type(child) is Static:
                # Static windows position is relevant to the main screen and not the parent
                # to simulate rendering a static within another static, child XY will be
                # increased by the parent XY (position).
                logging.debug(f"child is Static. Y={child_y+child.parent.position.y} X={child_x+child.parent.position.x}")
                child_y += child.parent.position.y
                child_x += child.parent.position.x

            # if the current child is styled for inline rendering, current column will be incremented
            # to allow the next child to also be displayed inline if it supports it.
            # Otherwise, current_line will be incremented by the child height and current column will be reset
            if child.styles.display.type == DisplayType.INLINE_BLOCK:
                current_column += child.get_height_and_width().width - 1
            else:
                current_line += child.get_height_and_width().height
                current_column = 0

            child.render(Point(child_y, child_x))
            previous_child = child

        # self.debug_dimensions()

        self.window.refresh()

    def debug_dimensions(self):
        height, width = self.get_height_and_width()
        label = f"{width}x{height}"
        if (width - 1) - len(label) < 0:
            return

        self.window.addstr(
            height - 1,
            (width - 1) - len(label),
            label,
            curses.A_BOLD | curses.A_UNDERLINE
        )

    def get_height_and_width(self) -> Dimensions:
        # example layout:
        #   ------ ------
        #   ---------------
        # the first line consists of two inline elements
        # both having the same width (6)
        # and the second is a single element, width: (15)
        # the following loop will generate this list
        # [[True, 12], [False, 15]]
        cumulative_line_widths = []

        for child in self.children:
            # if the current child is inline and the previous is also inline
            # increment the previous child width
            if cumulative_line_widths and \
                    cumulative_line_widths[len(cumulative_line_widths) - 1][0]\
                    and child.styles.display.type == DisplayType.INLINE_BLOCK:
                cumulative_line_widths[len(cumulative_line_widths) - 1][1] += child.get_height_and_width().width
                continue

            # if the child is inline add its width
            # and set the first element to True
            # so the next iteration increases its width
            # instead of appending a new entry
            cumulative_line_widths.append([
                    child.styles.display.type == DisplayType.INLINE_BLOCK,
                    child.get_height_and_width().width
            ])

        logging.debug(f"`{self.id}`: {cumulative_line_widths}")
        height = sum([child.get_height_and_width().height for child in self.children])
        width = max(cumulative_line_widths, key=lambda w: w[1])[1]

        height = max(height, self.styles.get('min_height', height))
        width = max(width, self.styles.get('min_width', width))

        return Dimensions(height, width)

    def __repr__(self):
        return f"Static(id={self.id}, children={self.children})"
