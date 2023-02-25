from .terminal_output import TerminalOutput
from ui.screen import Screen
from ui.styles import Styles, Display, Padding, DisplayType
from ui.static import Static
from ui.text import Text
from ui.button import Button
from ui.line_break import LineBreak


class TestUI(TerminalOutput):
    def test_rendering_complex_ui(self):
        screen = Screen().append(
            Static([
                Text("Title"),
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
                ], id='second-static',
                    styles=Styles(min_height=20, min_width=60, display=Display(type=DisplayType.INLINE_BLOCK)))
            ], id='main-static', styles=Styles(min_height=20))
        )

        # TODO: last height x width isn't showing, check pyte config.
        expected = """Title                                                                                               
2click me! ↗3                                                                                       
Ayo7x1        I'm nested                                                                            
                      more nesting                                                                  
      test                                                                                          
      AAAH!                                                                                         
      AY6x2                              40x4                                                       
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                            60x20"""
        assert expected == self.output(screen=screen).strip()
