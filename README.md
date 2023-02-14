# Terminal (Textual) Markup
A markup language to build `Textualize\Textual` components.

> ⚠️ This project is purely an experiment and shouldn't be
> used for normal usage.


The language grammar is defined in markup/grammar.lark


```python
markup = '<textual.widgets:Button classes="success" id="primary-btn">"click me"</textual.widgets:Button>'
_list = MarkupToList().transform(parser.parse(markup))

assert _list == [{
    'component': {
        'module': 'textual.widgets',
        'attribute': 'Button'
    },
    'children': ['click me'],
    'attributes': {
        'classes': 'success',
        'id': 'primary-btn'
    }
}]
```

Language Grammar
```lark
// STARTING RULES
// ==============
start: element+
?element: full_element
    | self_closing_element

// ELEMENTS
// ========
full_element: _op_tag element_body _cl_tag
self_closing_element: "<" import_path attributes "/>"

element_body: (element | atom)*

atom: ESCAPED_STRING
    | NUMBER


// IMPORTS
// =======
?dotted_name: CNAME -> str
    | dotted_name "." CNAME

import_path: dotted_name [":" dotted_name]

// TAGS
// ====
_op_tag: "<" import_path attributes">"
_cl_tag: "</" import_path ">"

// ATTRIBUTES
// ==========
attributes: attribute*
?attribute: CNAME "=" attribute_value
    | "@" CNAME "=" import_path -> callback_attribute

?attribute_value: atom

// LARK IMPORTS
// ==========

%import common.CNAME
%import common.ESCAPED_STRING
%import common.WS
%import common.NUMBER
%ignore WS
```