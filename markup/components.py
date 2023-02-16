from utils.importer import import_aliased_string, import_string

DEFAULT_ALIASES = {
    'Footer': 'textual.widgets:Footer',
    'widgets': 'textual.widgets',
    'Container': 'textual.containers:Container',
    'Button': 'widgets:Button'
}


def import_component(name_or_module: str, attribute: str = None, use_alias: bool = True):
    if not use_alias:
        return import_string(name_or_module, attribute)

    return import_aliased_string(name_or_module, attribute, aliases=DEFAULT_ALIASES)
