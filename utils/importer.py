from importlib import import_module


def import_string(name: str) -> object:
    """
    example:
        >>> import_string("package.module:function_name")
        <function function_name at 0x00000>

    :param name:
    :return:
    """
    (module_str, colon, attributes_str) = name.partition(':')

    if not colon or not attributes_str:
        raise Exception("Component must be in this format `package.module:attribute")

    module = import_module(module_str)
    attribute = module

    for attr in attributes_str.split('.'):
        attribute = getattr(attribute, attr)

    return attribute
