import curses

from ui.screen import Screen
from ui.static import Static
from ui.text import Text
from ui.styles import Styles, Padding
from ui.button import Button

import argparse
import logging

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")

args = parser.parse_args()
if args.verbose:
    logging.basicConfig(level=logging.DEBUG, filename=__import__('pathlib').Path(__file__).parent.joinpath('lang'))


def main(std_scr):
    curses.init_color(10, 153, 255, 51)

    screen = Screen(std_scr).append(
        Static([
            Text("1"),
            Text("2"),
            Button(
                "click me! ↗",
                # styles=Styles(padding=Padding(top=0, bottom=0, right=1, left=1))
            ),
            Static([
                Text("Ayo")
            ]),
            Static([
                Text("\tI'm nested"),
                Static([
                    Text("\t\tmore nesting\ntest"),
                    Static([
                        Text("\t\t\tAAAH!"),
                        Text("\t\t\tAY!"),
                    ])
                ], styles=Styles(min_width=40))
            ], id='second-static', styles=Styles(min_height=20, min_width=60))
        ], id='main-static', styles=Styles(min_height=20, min_width=80))
    )

    screen.render()

    while True:
        pass
        screen.window.refresh()


curses.wrapper(main)
