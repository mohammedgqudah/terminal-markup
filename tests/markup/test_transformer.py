from textual.widgets import Button, Footer
from textual.containers import Container

from markup.transformer import MarkupToList
from markup.parser import parser

from utils.importer import import_string, import_aliased_string


def test_it_transforms_a_single_component():
    markup = '<Button></Button>'
    _list = MarkupToList().transform(parser.parse(markup))

    assert _list == [{
        'component': Button,
        'children': [],
        'attributes': {},
        'callable_attributes': {}
    }]

    markup = '<Button>"click me"</Button>'
    _list = MarkupToList().transform(parser.parse(markup))

    assert _list == [{
        'component': Button,
        'children': ['click me'],
        'attributes': {},
        'callable_attributes': {}
    }]


def test_it_transforms_attributes():
    markup = '<Button classes="success">"click me"</Button>'

    _list = MarkupToList().transform(parser.parse(markup))

    assert _list == [{
        'component': Button,
        'children': ['click me'],
        'attributes': {'classes': 'success'},
        'callable_attributes': {}
    }]

    markup = '<Button classes="success" id="primary-btn">"click me"</Button>'
    _list = MarkupToList().transform(parser.parse(markup))

    assert _list == [{
        'component': Button,
        'children': ['click me'],
        'attributes': {
            'classes': 'success',
            'id': 'primary-btn'
        },
        'callable_attributes': {}
    }]


def test_it_transforms_callable_attributes():
    markup = '<Button @click=utils.importer:import_string>"click me"</Button>'

    _list = MarkupToList().transform(parser.parse(markup))

    assert _list == [{
        'component': Button,
        'children': ['click me'],
        'attributes': {},
        'callable_attributes': {
            'click': import_string
        }
    }]


def test_it_transforms_callable_attributes_in_a_self_closing_attribute():
    markup = '<Button @click=utils.importer:import_string/>'
    _list = MarkupToList().transform(parser.parse(markup))

    assert _list == [{
        'component': Button,
        'children': None,
        'attributes': {},
        'callable_attributes': {
            'click': import_string
        }
    }]

    markup = '<Button @click=utils.importer:import_string classes="success"/>'
    _list = MarkupToList().transform(parser.parse(markup))

    assert _list == [{
        'component': Button,
        'children': None,
        'attributes': {
            'classes': 'success'
        },
        'callable_attributes': {
            'click': import_string
        }
    }]


def test_it_parses_nested_elements_attributes():
    markup = '''
        <textual.widgets:Button/>
        <Footer/>
        <Container @click=utils.importer:import_string>
            <textual.widgets:Button classes="success" @click=utils.importer:import_aliased_string>"activate"</textual.widgets:Button>
            <textual.widgets:Button classes="failure">"delete"</textual.widgets:Button>
        </Container>
    '''

    _list = MarkupToList().transform(parser.parse(markup))

    assert _list == [
        {
            'component': Button,
            'children': None,
            'attributes': {},
            'callable_attributes': {}
        },
        {
            'component': Footer,
            'children': None,
            'attributes': {},
            'callable_attributes': {}
        },
        {
            'component': Container,
            'children': [
                {
                    'component': Button,
                    'children': ["activate"],
                    'attributes': {
                        'classes': "success"
                    },
                    'callable_attributes': {
                        'click': import_aliased_string
                    }
                },
                {
                    'component': Button,
                    'children': ["delete"],
                    'attributes': {
                        'classes': "failure"
                    },
                    'callable_attributes': {}
                },
            ],
            'attributes': {},
            'callable_attributes': {
                'click': import_string
            }
        }
    ]


def test_it_transforms_an_import_path():
    markup = '<widgets:Button></widgets:Button>'
    _list = MarkupToList().transform(parser.parse(markup))

    assert _list == [{
        'component': Button,
        'children': [],
        'attributes': {},
        'callable_attributes': {}
    }]
