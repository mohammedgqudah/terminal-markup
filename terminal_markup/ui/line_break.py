from .geometry import Dimensions, Point
from .renderable import Renderable


class LineBreak(Renderable):
    def __init__(self, lines: int = 1):
        self.lines = lines

    def get_min_height_and_width(self) -> Dimensions:
        return Dimensions(self.lines, 0)

    def render(self, point: Point):
        pass

    def __repr__(self):
        return f"{__class__.__name__}(lines={self.lines})"
