from .terminal_output import TerminalOutput
from terminal_markup.ui.screen import Screen
from terminal_markup.ui.static import Static
from terminal_markup.ui.text import Text
from terminal_markup.ui.button import Button


class TestText(TerminalOutput):
    def test_it_renders_text_and_calculates_dimensions_correctly(self):
        text = Text("Hello world")
        static = Static([text])
        screen = Screen([static])

        assert "Hello world" == self.output(screen=screen).strip()
        assert static.get_min_height_and_width().width == 11
        assert static.get_min_height_and_width().height == 1

        text = Text("Hello world\nline")
        static = Static([text])
        screen = Screen([static])

        assert self.lines_as_string(
            self.line("Hello world"),
            self.line('line')
        ).strip() == self.output(screen=screen).strip()
        assert static.get_min_height_and_width().width == 11
        assert static.get_min_height_and_width().height == 2

        text = Text("Hello world\nHello world")
        static = Static([text])
        screen = Screen([static])

        assert self.lines_as_string(
            self.line("Hello world"),
            self.line('Hello world')
        ).strip() == self.output(screen=screen).strip()
        assert static.get_min_height_and_width().width == 11
        assert static.get_min_height_and_width().height == 2
