from importlib import import_module
from typing import Dict, Tuple


def partition_import_string(string: str) -> Tuple[str, str]:
    """
    Returns a tuple of module, attribute if the string is in the format "package.module:attr".
    An exception is raised otherwise.
    """
    (module, _, attribute) = string.partition(':')

    if not attribute:
        raise Exception(f"Expected an import string to be in this format: `package.module:attribute`, got: {string}")

    return module, attribute


def import_aliased_string(module: str, dotted_attribute: str = None, aliases: Dict[str, str] = None):
    """
    examples:
        >>> import_aliased_string("package.sub.module", "function_name")
        <function function_name at 0x00000>
        >>> import_aliased_string("sub.module", "function_name", {'sub': 'package.sub'})
        <function function_name at 0x00000>
        >>> import_aliased_string("function_name", aliases={'function_name': 'package.sub.module:function_name'})
        <function function_name at 0x00000>
        >>> import_aliased_string("module.function_name", "function_name", aliases={
        >>>     'module': 'sub.module:function_name',
        >>>     'sub': 'package.sub'
        >>> })
        <function function_name at 0x00000>

    :param aliases:
    :param module:
    :param dotted_attribute:
    :return:
    """
    aliases = aliases or {}

    # when `dotted_attribute` is not provided, the first argument is presumed to be an alias
    if not dotted_attribute:
        if module in aliases:
            return import_aliased_string(*partition_import_string(aliases[module]), aliases=aliases)

        raise Exception(f"`{module}` cannot be resolved, no alias found")

    if module in aliases:
        return import_aliased_string(aliases[module], dotted_attribute, aliases=aliases)

    return import_string(module, dotted_attribute)


def import_string(module: str, dotted_attribute: str) -> object:
    """
    example :
        >>> import_string("package.module", "function_name")
        <function function_name at 0x00000>

    :param module:
    :param dotted_attribute:
    :return:
    """
    if not dotted_attribute:
        raise Exception(f"No attribute was specified for module `{module}`")

    module = import_module(module)
    attribute = module

    for attr in dotted_attribute.split('.'):
        attribute = getattr(attribute, attr)

    return attribute
