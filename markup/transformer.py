from lark import Transformer, v_args
from textual.widget import Widget

import inspect
from collections import namedtuple
from typing import Any


from markup.components import import_component

ImportableAttribute = namedtuple('ImportableAttribute', ['attribute', 'importable'])


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
        return import_component(module, attribute)

    def component(self, _object: Any):
        if not inspect.isclass(_object):
            raise Exception(f"A component must be a class, got: {_object}")
        if not issubclass(_object, Widget):
            raise Exception(f"A component must be of type {Widget}, got: {_object}")
        return _object

    def import_absolute_path(self, module, attribute):
        return import_component(module, attribute, use_alias=False)

    def start(self, *args):
        return list(args)

    def full_element(self, opening, *rest):
        (attributes, body, closing) = rest

        return {
            'component': opening,
            'children': body,
            **attributes
        }

    def self_closing_element(self, opening, attributes=None):
        attributes = attributes or {}

        return {
            'component': opening,
            'children': None,
            **attributes
        }

    def raw_attribute(self, name, value):
        return name, value

    def importable_attribute(self, name, importable):
        return ImportableAttribute(name, importable)

    def attributes(self, *attrs):
        # TODO: partition list, or rewrite the grammar to automatically separate
        importable_attributes = (attr for attr in attrs if isinstance(attr, ImportableAttribute))
        raw_attributes = (attr for attr in attrs if not isinstance(attr, ImportableAttribute))
        return {
            'attributes': dict(raw_attributes),
            'importable_attributes': dict(importable_attributes)
        }
