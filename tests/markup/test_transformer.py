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
        'attributes': {}
    }]

    markup = '<Button>"click me"</Button>'
    _list = MarkupToList().transform(parser.parse(markup))

    assert _list == [{
        'component': {
            'module': 'Button',
            'attribute': None
        },
        'children': ['click me'],
        'attributes': {}
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
        'attributes': {'classes': 'success'}
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
        }
    }]
