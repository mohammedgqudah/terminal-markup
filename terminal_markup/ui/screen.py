import os
from .geometry import Point, Dimensions


class Screen:
    dimensions: Dimensions

    def __init__(self, children: list = None):
        self.window = None
        self.children = children or []

        for child in self.children:
            child.parent = self

    def render(self, std_scr):
        self.window = std_scr
        # commit added windows/pads
        self.window.refresh()
        self.dimensions = self.get_height_and_width()

        last_y = 0

        for child in self.children:
            child.render(Point(last_y, 0))
            last_y += child.get_min_height_and_width().height

        self.window.refresh()

    def get_height_and_width(self) -> Dimensions:
        if "PYTEST_CURRENT_TEST" in os.environ:
            from tests import config
            columns, lines = config.terminal_width, config.terminal_height
        else:
            columns, lines = os.get_terminal_size()

        return Dimensions(lines, columns)

    def get_min_height_and_width(self) -> Dimensions:
        return self.get_height_and_width()

    def get_max_height_and_width(self) -> Dimensions:
        return self.get_height_and_width()

    def append(self, *items):
        for item in items:
            item.parent = self
            item.screen = self

        self.children += items

        return self
