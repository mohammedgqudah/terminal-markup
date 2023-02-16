from markup.parser import parser


def test_it_parses_a_single_empty_full_element():
    markup = '''<Button></Button>'''

    parser.parse(markup)


def test_it_parses_a_self_closing_element():
    markup = '''<Button/>'''

    parser.parse(markup)


def test_it_parses_multiple_top_level_full_elements():
    markup = '''
    <Button></Button>
    <Footer></Footer>
    '''

    parser.parse(markup)


def test_it_parses_nested_elements():
    markup = '''
    <Container>
        <Button></Button>
        <Button></Button>
    </Container>
    '''

    parser.parse(markup)


def test_it_accepts_escaped_strings_in_elements():
    markup = '''<Button>"click me"</Button>'''

    parser.parse(markup)


def test_it_accepts_a_primary_as_a_component():
    markup = '''<textual.widgets:Button>"click me"</textual.widgets:Button>'''

    parser.parse(markup)


def test_it_accepts_attributes_in_an_opening_tag():
    parser.parse('''
        <Button on_click="run">"click me"</Button>
    ''')
    parser.parse('''
        <Button on_click="run" classes="success">"click me"</Button>
   ''')


def test_it_accepts_attributes_in_a_self_closing_tag():
    parser.parse('''
        <Header @click=app:button_click />
    ''')
    parser.parse('''
        <Header on_click="run" classes="success"/>
   ''')
