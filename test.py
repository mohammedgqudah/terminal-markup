import curses


from ui.screen import Screen
from ui.static import Static
from ui.text import Text

import argparse
import logging

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")

args = parser.parse_args()
if args.verbose:
    logging.basicConfig(level=logging.DEBUG, filename=__import__('pathlib').Path(__file__).parent.joinpath('lang'))


def main(std_scr):
    curses.init_color(10, 153,255,51)

    screen = Screen(std_scr).append(
        Static([
            Text("1"),
            Text("2"),
            Static([
                Text("I'm nested"),
                Static([
                    Text("more nesting\ntest"),
                    Static([
                        Text("AAAH!"),
                        Text("AY!"),
                    ])
                ])
            ], id='second-static')
        ], id='main-static')
    )

    screen.render()

    while True:
        pass
        screen.window.refresh()


curses.wrapper(main)