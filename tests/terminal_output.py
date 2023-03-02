import pickle
import codecs
import sys

import pyte
import pexpect

from ui.screen import Screen
from ui.geometry import Dimensions
from . import config


class TerminalOutput:
    _screen = None
    _stream = None

    def set_screen_size(self, dimensions: Dimensions):
        config.terminal['terminal_lines'] = dimensions.height
        config.terminal['terminal_cols'] = dimensions.width

    def output(self, screen: Screen, as_string: bool = True) -> str:
        self._screen = pyte.Screen(config.terminal['terminal_cols'], config.terminal['terminal_lines'])
        self._stream = pyte.Stream(self._screen)

        # TEMP
        script_location = '/Users/qudah/Desktop/personal/terminal-markup/tests/render_pickled_screen.py'

        pickled = codecs.encode(pickle.dumps(screen), "base64").decode()
        curses_output = pexpect.run(f'{sys.executable} {script_location} -p="{pickled}" --terminal_cols={config.terminal["terminal_cols"]} --terminal_lines={config.terminal["terminal_lines"]}')

        self._stream.feed(curses_output.decode('UTF-8'))

        if as_string:
            return "\n".join(self._screen.display)

        return self._screen.display

    def line(self, text):
        return f"{text}{' ' * (config.terminal['terminal_cols'] - len(text))}"

    def lines(self, number):
        return self.lines_as_string(*[self.line("") for i in range(0, number)])

    def lines_as_string(self, *lines):
        return "\n".join(lines)
