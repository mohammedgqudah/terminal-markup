"""
Accepts a base64 encoded pickled screen and initializes a curses application.

Usage:
    python render_pickled_screen.py -p="base64...."

Used by tests to get the curses application output and feed a virtual terminal emulator.
"""
import argparse
import pickle
import curses
import codecs

from ui.screen import Screen
from tests import config

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--pickle", required=True)
parser.add_argument("--terminal_lines", required=True)
parser.add_argument("--terminal_cols", required=True)

args = parser.parse_args()

screen: Screen = pickle.loads(codecs.decode(args.pickle.encode(), "base64"))

config.terminal['terminal_lines'] = int(args.terminal_lines)
config.terminal['terminal_cols'] = int(args.terminal_cols)


def main(std_scr):
    curses.init_color(10, 153, 255, 51)  # TEMP
    screen.render(std_scr)


curses.wrapper(main)
