from .terminal_output import TerminalOutput
from terminal_markup.ui.screen import Screen
from terminal_markup.ui.styles import Styles, Display, Padding, DisplayType
from terminal_markup.ui.static import Static
from terminal_markup.ui.button import Button


class TestButton(TerminalOutput):
    def test_it_renders_inline_buttons(self):
        screen = Screen([
            Static([
                Button("Activate", styles=Styles(display=Display(type=DisplayType.INLINE_BLOCK))),
                Button("Activate!", styles=Styles(display=Display(type=DisplayType.INLINE_BLOCK))),
                Button("Deactivate", styles=Styles(display=Display(type=DisplayType.BLOCK))),
            ])
        ])

        expected = """
▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔                                                                       
   Activate      Activate!                                                                          
▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁                                                                       
▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔                                                                                    
   Deactivate                                                                                       
▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁"""

        assert expected.strip() == self.output(screen).strip()

    def test_it_renders_a_single_button(self):
        screen = Screen([
            Static([
                Button("Activate"),
            ])
        ])

        expected = self.lines_as_string(
            self.line('▔▔▔▔▔▔▔▔▔▔▔▔▔▔'),
            self.line('   Activate   '),
            self.line('▁▁▁▁▁▁▁▁▁▁▁▁▁▁')
        )
        assert expected.strip() == self.output(screen).strip()

    def test_it_renders_a_button_with_zero_padding(self):
        screen = Screen([
            Static([
                Button("Activate", styles=Styles(padding=Padding())),
            ])
        ])
        assert """Activate""" == self.output(screen).strip()

    def test_it_renders_a_button_with_custom_padding(self):
        screen = Screen([
            Static([
                Button("Activate", styles=Styles(padding=Padding(top=1, bottom=1, left=0, right=0))),
            ])
        ])
        expected = self.lines_as_string(
            self.line('▔▔▔▔▔▔▔▔'),
            self.line('Activate'),
            self.line('▁▁▁▁▁▁▁▁')
        )
        assert expected.strip() == self.output(screen).strip()

        screen = Screen([
            Static([
                Button("Activate", styles=Styles(padding=Padding(top=1, bottom=1, left=1, right=1))),
            ])
        ])
        expected = self.lines_as_string(
            self.line('▔▔▔▔▔▔▔▔▔▔'),
            self.line(' Activate '),
            self.line('▁▁▁▁▁▁▁▁▁▁')
        )
        assert expected.strip() == self.output(screen).strip()

        screen = Screen([
            Static([
                Button("Activate", styles=Styles(padding=Padding(top=1, bottom=1, left=1, right=0))),
            ])
        ])
        expected = self.lines_as_string(
            self.line('▔▔▔▔▔▔▔▔▔'),
            self.line(' Activate'),
            self.line('▁▁▁▁▁▁▁▁▁')
        )
        assert expected.strip() == self.output(screen).strip()

        screen = Screen([
            Static([
                Button("Activate", styles=Styles(padding=Padding(top=1, bottom=0, left=1, right=0))),
            ])
        ])
        expected = self.lines_as_string(
            self.line('▔▔▔▔▔▔▔▔▔'),
            self.line(' Activate'),
        )
        assert expected.strip() == self.output(screen).strip()
