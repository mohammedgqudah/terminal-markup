from functools import reduce
from lark import Transformer, v_args
from collections import namedtuple

CallableAttribute = namedtuple('CallableAttribute', ['attribute', 'callable'])

@v_args(inline=True)
class MarkupToList(Transformer):
    atom = str
    str = str
    CNAME = str

    def ESCAPED_STRING(self, string):
        return string[1:-1]

    def element_body(self, *children):
        return list(children)

    def dotted_name(self, left, right):
        return f"{left}.{right}"

    def import_path(self, module, attribute):
        return {
            'module': module,
            'attribute': str(attribute) if attribute else None
        }

    def start(self, *args):
        return list(args)

    def full_element(self, opening, *rest):
        (attributes, body, closing) = rest

        return {
            'component': opening,
            'children': body,
            **attributes
        }

    def self_closing_element(self, opening):
        return {
            'component': opening,
            'children': None
        }

    def raw_attribute(self, name, value):
        return name, value

    def callable_attribute(self, name, _callable):
        return CallableAttribute(name, _callable)

    def attributes(self, *attrs):
        # TODO: partition list, or rewrite the grammar to automatically separate
        callable_attributes = (attr for attr in attrs if isinstance(attr, CallableAttribute))
        raw_attributes = (attr for attr in attrs if not isinstance(attr, CallableAttribute))
        return {
            'attributes': dict(raw_attributes),
            'callable_attributes': dict(callable_attributes)
        }
