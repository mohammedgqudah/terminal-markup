import typing
import logging
import random
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
class _LayoutPlaceholder:
    """
    A LayoutPlaceholder is used internally to calculate layouts before displaying them, for example
    a layout consisting of 3 elements, 2 inline and 1 block:
    --------   --------
    -------------------

    will be converted into a list of Placeholders:
        [Placeholder(width=16, height=1), Placeholder(width=19, height=1)]

    which makes dealing with the layout easier.
    """
    height: int
    width: int
    is_inline: bool


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
                current_line += previous_child._layout_placeholder.height

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
                current_column += child.get_height_and_width().width
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
        cumulative_children: typing.List[_LayoutPlaceholder] = []

        for child in self.children:
            # if the current child is inline and the previous is also inline
            # increment the previous child width
            if (
                    cumulative_children and
                    cumulative_children[len(cumulative_children) - 1].is_inline
                    and child.styles.display.type == DisplayType.INLINE_BLOCK
            ):
                last_placeholder = cumulative_children[len(cumulative_children) - 1]
                child._layout_placeholder = last_placeholder
                last_placeholder.width += child.get_height_and_width().width
                last_placeholder.height = max(child.get_height_and_width().height, last_placeholder.height)
                continue

            # if the child is inline add its width
            # and set the first element to True
            # so the next iteration increases its width
            # instead of appending a new entry
            placeholder = _LayoutPlaceholder(
                is_inline=child.styles.display.type == DisplayType.INLINE_BLOCK,
                width=child.get_height_and_width().width,
                height=child.get_height_and_width().height
            )
            cumulative_children.append(placeholder)
            child._layout_placeholder = placeholder

        logging.debug(f"`{self.id}`: {cumulative_children}")

        height = sum([child.height for child in cumulative_children])
        width = max(cumulative_children, key=lambda w: w.width).width

        height = max(height, self.styles.get('min_height', height))
        width = max(width, self.styles.get('min_width', width))

        return Dimensions(height, width)

    def __repr__(self):
        return f"Static(id={self.id}, children={self.children})"
