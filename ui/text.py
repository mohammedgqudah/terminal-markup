from ui.geometry import get_text_height_and_width, Dimensions, Point
from .plane_interface import PlaneInterface
from .renderable_interface import RenderableInterface


class Text(PlaneInterface, RenderableInterface):
    def __init__(self, text: str):
        self.text = text
        self.screen = None
        self.parent = None

    def get_height_and_width(self) -> Dimensions:
        y, x = get_text_height_and_width(self.text)
        return Dimensions(y, x + 1)

    def render(self, point: Point):
        self.parent.window.addstr(*point, self.text)
