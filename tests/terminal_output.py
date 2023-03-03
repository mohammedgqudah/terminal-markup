import pickle
import codecs
import sys

import pyte
import pexpect
from wcwidth import wcswidth

from terminal_markup.ui.screen import Screen
from terminal_markup.ui.geometry import Dimensions
from . import config
from terminal_markup.config import root_dir


class TerminalOutput:
    _screen = None
    _stream = None

    def set_screen_size(self, dimensions: Dimensions):
        config.terminal_height = dimensions.height
        config.terminal_width = dimensions.width

    def output(self, screen: Screen, as_string: bool = True) -> str:
        self._screen = pyte.Screen(config.terminal_width, config.terminal_height)
        self._stream = pyte.Stream(self._screen)

        script_location = root_dir.joinpath('tests', 'render_pickled_screen.py')

        pickled = codecs.encode(pickle.dumps(screen), "base64").decode()
        curses_output = pexpect.run(
            f'{sys.executable} {script_location} -p="{pickled}" '
            f'--terminal_width={config.terminal_width} --terminal_height={config.terminal_height}'
        )

        self._stream.feed(curses_output.decode('UTF-8'))

        if as_string:
            return "\n".join(self._screen.display)

        return self._screen.display

    def line(self, text):
        return f"{text}{' ' * (config.terminal_width - wcswidth(text))}"

    def lines(self, number):
        return self.lines_as_string(*[self.line("") for i in range(0, number)])

    def lines_as_string(self, *lines):
        return "\n".join(lines)
