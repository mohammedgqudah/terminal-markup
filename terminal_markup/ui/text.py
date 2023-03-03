from .geometry import get_text_height_and_width, Dimensions, Point, wcswidth
from .renderable import Renderable
from .styles import Styles


class Text(Renderable):
    """
    A component responsible for rendering text within a window.

    Notes:
        `addstr` will advance the cursor automatically to the next line when it reaches the end of the window,
        which fails because the window height has already been calculated. to overcome this a hidden space is added
        and the end of the string, so that when the file character fails, it will catch the exception and ignore it
        because the space isn't meant to be rendered.
    """
    def __init__(self, text: str, styles: Styles = None):
        self.text = text
        self.dimensions = self.get_min_height_and_width()
        self.styles = styles or self.styles
        self._addstr_args = []

    def get_min_height_and_width(self) -> Dimensions:
        y, x = get_text_height_and_width(self.text)

        return Dimensions(y, x)

    def render(self, point: Point):
        self.position = point
        _text = self.text
        _, parent_width = self.parent.get_min_height_and_width()
        height, _ = self.get_min_height_and_width()
        lines = _text.split("\n")

        # if wcswidth(lines[-1]) == parent_width:
        #     lines[-1] = lines[-1] + " "

        for idx, line in enumerate(lines):
            try:
                # `addstr` by defaults advances the cursor to the next line,
                # to avoid this, ~~an extra space was added~~, which is meant to not be rendered
                # because curses will return ERR and the cursor position will not change then.
                # it is not the best solution, but that's because the python wrapper doesn't export `addchstr`
                self.parent.window.addstr(point.y + idx, point.x, line, *self._addstr_args)
            except:
                pass

    def post_calculating_parent_dimensions_hook(self):
        pass

    def __repr__(self):
        return f"{__class__.__name__}(text={self.text})"
