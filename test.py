import curses

from ui.screen import Screen
from ui.static import Static
from ui.text import Text
from ui.styles import Styles, Padding, DisplayType, Display
from ui.button import Button
from ui.line_break import LineBreak

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
            Text("2", styles=Styles(display=Display(type=DisplayType.INLINE_BLOCK))),
            Button(
                "click me! ↗",
                styles=Styles(**{**Button.styles.__dict__, 'display': Display(type=DisplayType.INLINE_BLOCK)})
            ),
            Text("3", styles=Styles(display=Display(type=DisplayType.INLINE_BLOCK))),
            LineBreak(0),
            Static([
                Text("Ayo...")
            ],
                styles=Styles(display=Display(type=DisplayType.INLINE_BLOCK))
            ),
            Static([
                Text("\tI'm nested"),
                Static([
                    Text("\t\tmore nesting\ntest"),
                    Static([
                        Text("AAAH!"),
                        Text("AY!"),
                    ])
                ], styles=Styles(min_width=40))
            ], id='second-static', styles=Styles(min_height=20, min_width=60, display=Display(type=DisplayType.INLINE_BLOCK)))
        ], id='main-static', styles=Styles(min_height=20))
    )

    screen.render()

    while True:
        pass
        screen.window.refresh()


curses.wrapper(main)
