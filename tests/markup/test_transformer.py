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
