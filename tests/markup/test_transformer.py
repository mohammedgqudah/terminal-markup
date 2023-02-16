from markup.transformer import MarkupToList
from markup.parser import parser


def test_it_transforms_a_single_component():
    markup = '<Button></Button>'
    _list = MarkupToList().transform(parser.parse(markup))

    assert _list == [{
        'component': {
            'module': 'Button',
            'attribute': None
        },
        'children': [],
        'attributes': {},
        'callable_attributes': {}
    }]

    markup = '<Button>"click me"</Button>'
    _list = MarkupToList().transform(parser.parse(markup))

    assert _list == [{
        'component': {
            'module': 'Button',
            'attribute': None
        },
        'children': ['click me'],
        'attributes': {},
        'callable_attributes': {}
    }]


def test_it_transforms_attributes():
    markup = '<Button classes="success">"click me"</Button>'

    _list = MarkupToList().transform(parser.parse(markup))

    assert _list == [{
        'component': {
            'module': 'Button',
            'attribute': None
        },
        'children': ['click me'],
        'attributes': {'classes': 'success'},
        'callable_attributes': {}
    }]

    markup = '<Button classes="success" id="primary-btn">"click me"</Button>'
    _list = MarkupToList().transform(parser.parse(markup))

    assert _list == [{
        'component': {
            'module': 'Button',
            'attribute': None
        },
        'children': ['click me'],
        'attributes': {
            'classes': 'success',
            'id': 'primary-btn'
        },
        'callable_attributes': {}
    }]


def test_it_transforms_callable_attributes():
    markup = '<Button @click=myapp.functions:onclick>"click me"</Button>'

    _list = MarkupToList().transform(parser.parse(markup))

    assert _list == [{
        'component': {
            'module': 'Button',
            'attribute': None
        },
        'children': ['click me'],
        'attributes': {},
        'callable_attributes': {
            'click': {
                'module': 'myapp.functions',
                'attribute': 'onclick'
            }
        }
    }]


def test_it_transforms_callable_attributes_in_a_self_closing_attribute():
    markup = '<Button @click=myapp.functions:onclick/>'
    _list = MarkupToList().transform(parser.parse(markup))

    assert _list == [{
        'component': {
            'module': 'Button',
            'attribute': None
        },
        'children': None,
        'attributes': {},
        'callable_attributes': {
            'click': {
                'module': 'myapp.functions',
                'attribute': 'onclick'
            }
        }
    }]

    markup = '<Button @click=myapp.functions:onclick classes="success"/>'
    _list = MarkupToList().transform(parser.parse(markup))

    assert _list == [{
        'component': {
            'module': 'Button',
            'attribute': None
        },
        'children': None,
        'attributes': {
            'classes': 'success'
        },
        'callable_attributes': {
            'click': {
                'module': 'myapp.functions',
                'attribute': 'onclick'
            }
        }
    }]


def test_it_parses_nested_elements_attributes():
    markup = '''
        <textual.widgets:Button/>
        <Footer/>
        <Container @click=module:func1>
            <textual.widgets:Button classes="success" @click=module:func2>"activate"</textual.widgets:Button>
            <textual.widgets:Button classes="failure">"delete"</textual.widgets:Button>
        </Container>
    '''

    _list = MarkupToList().transform(parser.parse(markup))

    assert _list == [
        {
            'component': {
                'module': 'textual.widgets',
                'attribute': 'Button'
            },
            'children': None,
            'attributes': {},
            'callable_attributes': {}
        },
        {
            'component': {
                'module': 'Footer',
                'attribute': None
            },
            'children': None,
            'attributes': {},
            'callable_attributes': {}
        },
        {
            'component': {
                'module': 'Container',
                'attribute': None
            },
            'children': [
                {
                    'component': {
                        'module': 'textual.widgets',
                        'attribute': 'Button'
                    },
                    'children': ["activate"],
                    'attributes': {
                        'classes': "success"
                    },
                    'callable_attributes': {
                        'click': {
                            'module': 'module',
                            'attribute': 'func2'
                        }
                    }
                },
                {
                    'component': {
                        'module': 'textual.widgets',
                        'attribute': 'Button'
                    },
                    'children': ["delete"],
                    'attributes': {
                        'classes': "failure"
                    },
                    'callable_attributes': {}
                },
            ],
            'attributes': {},
            'callable_attributes': {
                'click': {
                    'module': 'module',
                    'attribute': 'func1'
                }
            }
        }
    ]
