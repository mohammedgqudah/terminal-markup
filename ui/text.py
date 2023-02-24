from ui.geometry import get_text_height_and_width, Dimensions, Point
from ui.renderable import Renderable


class Text(Renderable):
    def __init__(self, text: str):
        self.text = text

    def get_height_and_width(self) -> Dimensions:
        y, x = get_text_height_and_width(self.text)

        # x + 1 is a temporary solution until i figure how to prevent curses
        # from progressing the cursor to a new line at the end of a sentence.
        return Dimensions(y, x + 1)

    def render(self, point: Point):
        self.position = point

        self.parent.window.addstr(*point, self.text)

    def __repr__(self):
        return f"Text(text={self.text})"
