from .geometry import get_text_height_and_width, Dimensions, Point
from .renderable import Renderable
from .styles import Styles


class Text(Renderable):
    def __init__(self, text: str, styles: Styles = None):
        self.text = text
        self.styles = styles or self.styles
        self._addstr_args = []

    def get_height_and_width(self) -> Dimensions:
        y, x = get_text_height_and_width(self.text)

        # x + 1 is a temporary solution until i figure how to prevent curses
        # from progressing the cursor to a new line at the end of a sentence.
        return Dimensions(y, x + 1)

    def render(self, point: Point):
        self.position = point

        for idx, line in enumerate(self.text.split('\n')):
            self.parent.window.addstr(point.y + idx, point.x, line, *self._addstr_args)

    def __repr__(self):
        return f"{__class__.__name__}(text={self.text})"
