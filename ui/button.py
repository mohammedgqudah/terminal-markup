import curses

from .text import Text
from .geometry import Point, get_text_height_and_width
from .styles import Styles, Padding


class Button(Text):

    def __init__(self, label: str, id: str = None, styles: Styles = None):
        default_styles = Styles(
            padding=Padding(top=1, bottom=1, left=3, right=3)
        )
        self.label = label
        self.styles = default_styles.merge(styles)
        text = self.build_text()

        super().__init__(text=text, styles=self.styles)

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

        # if the label has multiple lines, each line should be padded
        label = "\n".join([
            f"{left_padding_text}{line}{right_padding_text}"
            for line in self.label.split('\n')
        ])

        return (
                f"{top_padding_text}" +
                self.styles.padding.top * '\n' +
                label +
                self.styles.padding.bottom * '\n' +
                f"{bottom_padding_text}"
        )

    def render(self, point: Point):
        self._addstr_args = (curses.A_BOLD | curses.color_pair(1),)

        super().render(point)

    # TODO: to be implemented.
    def on_click(self):
        # highlight text
        pass
