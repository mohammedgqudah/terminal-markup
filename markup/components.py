from importlib import import_module

DEFAULT_COMPONENTS = {
    'Footer': 'textual.widgets.'
}


def resolve_component(name: str) -> object:
    (module_str, colon, attributes_str) = name.partition(':')

    if not colon or not attributes_str:
        raise Exception("Component must be in this format `package.module:attribute")

    module = import_module(module_str)
    attribute = module

    for attr in attributes_str.split('.'):
        attribute = getattr(attribute, attr)

    return attribute
