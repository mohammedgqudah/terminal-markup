from functools import reduce
from lark import Transformer, v_args


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
            'attributes': attributes
        }

    def self_closing_element(self, opening):
        return {
            'component': opening,
            'children': None
        }

    def attribute(self, *attrs):
        return tuple(attrs)

    def attributes(self, *attrs):
        return dict(attrs)
