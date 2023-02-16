from utils.importer import import_aliased_string

DEFAULT_ALIASES = {
    'Footer': 'textual.widgets:Footer',
    'widgets': 'textual.widgets',
    'Container': 'textual.containers:Container',
    'Button': 'widgets:Button'
}

# TODO: use_alias


def import_component(name_or_module: str, attribute: str = None, use_alias: bool = True):
    return import_aliased_string(name_or_module, attribute, aliases=DEFAULT_ALIASES)
