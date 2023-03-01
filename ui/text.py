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
        self.text = text + " "
        self.styles = styles or self.styles
        self._addstr_args = []

    def get_min_height_and_width(self) -> Dimensions:
        y, x = get_text_height_and_width(self.text)

        # -1 because the extra space is hidden and will not be part of the final rendered text.
        # TODO: only if it's required, but the problem is that the parent will calculate the width based on the children.

        return Dimensions(y, x - 1)

    def render(self, point: Point):
        self.position = point
        _, parent_width = self.parent.get_min_height_and_width()
        lines, _ = self.get_min_height_and_width()

        for idx, line in enumerate(self.text.split('\n')):
            # sometimes adding an extra space is not necessary
            # because the parent window is bigger and curses won't
            # advance the cursor, so if it's the last line and the parent
            # is bigger, remove the hidden space.
            if idx == (lines - 1) and wcswidth(line) < parent_width:
                line = line[:-1]

            try:
                # `addstr` by defaults advances the cursor to the next line,
                # to avoid this, an extra space was added, which is meant to not be rendered
                # because curses will return ERR and the cursor position will not change then.
                # it is not the best solution, but that's because the python wrapper doesn't export `addchstr`
                self.parent.window.addstr(point.y + idx, point.x, line, *self._addstr_args)
            except:
                pass

    def __repr__(self):
        return f"{__class__.__name__}(text={self.text})"
