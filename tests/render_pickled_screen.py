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
parser.add_argument("--terminal_height", required=True)
parser.add_argument("--terminal_width", required=True)

args = parser.parse_args()

screen: Screen = pickle.loads(codecs.decode(args.pickle.encode(), "base64"))

config.terminal_height = int(args.terminal_height)
config.terminal_width = int(args.terminal_width)


def main(std_scr):
    curses.init_color(10, 153, 255, 51)  # TEMP
    screen.render(std_scr)


curses.wrapper(main)
