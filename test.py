import curses


from ui.screen import Screen
from ui.static import Static
from ui.text import Text


def main(std_scr):
    screen = Screen(std_scr).append(
        Static([
            Text("1-2-3-4-5-6-7-8-9-10-11-12-13-14-15-16-17heyhesdf"),
            Text("Hiiiiii")
        ]),
        Static([
            Text("11111111112")
        ]),
        Static([
            Text("222"),
            Text("222ayayay"),
        ])
    )

    screen.render()

    while True:
        pass


curses.wrapper(main)
