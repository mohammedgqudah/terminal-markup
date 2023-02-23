from .geometry import Point


class Screen:
    def __init__(self, std_screen):
        self.window = std_screen
        self.children = []

    def render(self):
        # commit added windows/pads
        self.window.refresh()

        last_y = 0

        for child in self.children:
            child.parent = self
            child.render(Point(last_y, 0))
            last_y += child.get_height_and_width().height

        self.window.refresh()

    def append(self, *items):
        for item in items:
            item.parent = self
            item.screen = self

        self.children += items

        return self
