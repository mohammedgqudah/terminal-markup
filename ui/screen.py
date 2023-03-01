from .geometry import Point, Dimensions


class Screen:
    def __init__(self, children: list = None):
        self.window = None
        self.children = children or []

    def render(self, std_scr):
        self.window = std_scr
        # commit added windows/pads
        self.window.refresh()

        last_y = 0

        for child in self.children:
            child.parent = self
            child.render(Point(last_y, 0))
            last_y += child.get_min_height_and_width().height

        self.window.refresh()

    def get_height_and_width(self) -> Dimensions:
        y, x = self.window.getmaxyx()

        return Dimensions(y + 1, x + 1)

    def get_min_height_and_width(self) -> Dimensions:
        return self.get_height_and_width()

    def append(self, *items):
        for item in items:
            item.parent = self
            item.screen = self

        self.children += items

        return self
