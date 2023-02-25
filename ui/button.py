import curses

from .text import Text
from .geometry import Point, get_text_height_and_width
from .styles import Styles, Padding


class Button(Text):
    # styles = Styles(
    #     padding=Padding(top=1, bottom=1, left=3, right=3)
    # )

    def __init__(self, label: str, id: str = None, styles: Styles = None):
        self.label = label

        if not styles:
            self.styles.padding.top = self.styles.padding.bottom = 1
            self.styles.padding.left = self.styles.padding.right = 3

        self.styles = styles or self.styles

        text = self.build_text()

        super().__init__(text=text)

    def render(self, point: Point):
        self.position = point

        self.parent.window.addstr(*point, self.text, curses.A_BOLD | curses.color_pair(1))

    def build_text(self):
        label_height, label_width = get_text_height_and_width(self.label)

        left_padding_text = " " * self.styles.padding.left
        right_padding_text = " " * self.styles.padding.right

        top_padding_text = (
            "▔" * (label_width + self.styles.padding.left + self.styles.padding.right)
            if self.styles.padding.top
            else ''
        )
        bottom_padding_text = (
            "▁" * (label_width + self.styles.padding.left + self.styles.padding.right)
            if self.styles.padding.bottom
            else ''
        )

        return (
                f"{top_padding_text}" +
                self.styles.padding.top * '\n' +
                f"{left_padding_text}{self.label}{right_padding_text}" +
                self.styles.padding.bottom * '\n' +
                f"{bottom_padding_text}"
        )

    # TODO: to be implemented.
    def on_click(self):
        # highlight text
        pass
