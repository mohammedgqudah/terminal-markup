import pickle
import codecs
import sys

import pyte
import pexpect

from ui.screen import Screen


class TerminalOutput:
    _screen = None
    _stream = None

    TERMINAL_COLS = 100
    TERMINAL_LINES = 100

    def setup_method(self):
        self._screen = pyte.Screen(self.TERMINAL_LINES, self.TERMINAL_LINES)
        self._stream = pyte.Stream(self._screen)

    def output(self, screen: Screen, as_string: bool = True) -> str:
        # TEMP
        script_location = '/Users/qudah/Desktop/personal/terminal-markup/tests/render_pickled_screen.py'

        pickled = codecs.encode(pickle.dumps(screen), "base64").decode()
        curses_output = pexpect.run(f'{sys.executable} {script_location} -p="{pickled}"')

        self._stream.feed(curses_output.decode('UTF-8'))

        if as_string:
            return "\n".join(self._screen.display)

        return self._screen.display

    def line(self, text):
        return f"{text}{' ' * (self.TERMINAL_COLS - len(text))}"

    def lines(self, number):
        return self.lines_as_string(*[self.line("") for i in range(0, number)])

    def lines_as_string(self, *lines):
        return "\n".join(lines)
