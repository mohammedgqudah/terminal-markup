import typing
import logging
from itertools import cycle
from dataclasses import dataclass

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


@dataclass
class _Region:
    """
    A Region is used internally to calculate layouts before displaying them, for example
    a layout consisting of 3 elements, 2 inline and 1 block:
    --------   --------
    -------------------

    will be converted into a list of Regions:
        [Region(width=16, height=1, is_inline=True), Region(width=19, height=1, is_inline=False)]

    which makes dealing with the layout easier.
    """
    height: int
    width: int
    is_inline: bool
    parent: Renderable

    def available_area_width(self):
        return self.parent.get_max_height_and_width().width - self.width

    def is_available(self, renderable: Renderable):
        return self.is_inline and self.available_area_width() >= renderable.get_min_height_and_width().width

    def append(self, renderable: Renderable):
        renderable._region = self

        self.width += renderable.get_min_height_and_width().width
        self.height = max(renderable.get_min_height_and_width().height, self.height)


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

        for child in self.children:
            child.screen = self.screen
            child.parent = self

    def render(self, position: Point):
        self.parent.window.refresh()

        self.position = position
        self.window = curses.newwin(*self.get_min_height_and_width(), *self.position)

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
            if (
                    previous_child and
                    previous_child._region.is_inline and
                    previous_child._region != child._region
            ):
                current_column = 0
                """The previous child height is not used to increment `current_line`, because the current child
                could be rendered after two inline elements, where the first element is the highest,
                so if the previous height was used, the current child could overwrite
                the first child. Example:

                -child1- --------
                -------- -child2-
                -------- --------
                -child1-
                -----------------
                --current child--
                -----------------

                In the example above you can see that child1 is 4 lines, where child2 (rendered next to it)
                is only 3 lines, if we only increment current_line by 3, we will end up with something like:
 
                -child1- --------
                -------- -child2-
                -------- --------
                xxxxxxx----------
                --current child--
                -----------------

                `xxxxxxx` represents what was overwritten.

                Luckily, a layout placeholder object is attached to the child, which has the correct height.
                """
                current_line += previous_child._region.height

            child_y = current_line
            child_x = current_column
            logging.debug(f"\trendering child {child.__debug_repr__()} at Y={child_y}")

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
                current_column += child.get_min_height_and_width().width
            else:
                current_line += child.get_min_height_and_width().height
                current_column = 0

            child.render(Point(child_y, child_x))
            previous_child = child

        # self.debug_dimensions()

        self.window.refresh()

    def debug_dimensions(self):
        height, width = self.get_min_height_and_width()
        label = f"{width}x{height}"
        if (width - 1) - len(label) < 0:
            return

        self.window.addstr(
            height - 1,
            (width - 1) - len(label),
            label,
            curses.A_BOLD | curses.A_UNDERLINE
        )

    def get_max_height_and_width(self) -> Dimensions:
        return self.parent.get_max_height_and_width()

    def get_min_height_and_width(self) -> Dimensions:
        regions: typing.List[_Region] = []

        for child in self.children:
            if child.styles.display.type == DisplayType.INLINE_BLOCK and regions and regions[-1].is_available(child):
                previous_region = regions[-1]
                previous_region.append(child)
                continue

            # if the child couldn't join the previous region
            # create a new one.
            new_region = _Region(
                parent=self,
                is_inline=child.styles.display.type == DisplayType.INLINE_BLOCK,
                width=child.get_min_height_and_width().width,
                height=child.get_min_height_and_width().height
            )
            regions.append(new_region)
            child._region = new_region

        height = sum([child.height for child in regions])
        width = max(regions, key=lambda w: w.width).width

        height = max(height, self.styles.get('min_height', height))
        width = max(width, self.styles.get('min_width', width))

        return Dimensions(height, width)

    def __repr__(self):
        return f"Static(id={self.id}, children={self.children})"
