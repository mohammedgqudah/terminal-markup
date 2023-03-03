from collections import namedtuple

from wcwidth import wcswidth


Dimensions = namedtuple('Dimensions', ['height', 'width'])
Point = namedtuple('Point', ['y', 'x'])


def ensure_value_in_range(_min, _max, value):
    """
    A function that takes min, max, and value, it returns max if value exceeds max, min
    if the value less than min, or the value.
    :param _min:
    :param _max:
    :param value:
    :return:
    """
    if value < _min:
        return _min
    elif value > _max:
        return _max
    else:
        return value


def get_text_height_and_width(text: str) -> Dimensions:
    """
    Get string height (lines) and width (number of cells)
    :param text:
    :return:
    """
    # TODO: does `expandtabs` respect terminal size
    lines = text.expandtabs().split('\n')
    return Dimensions(len(lines), max([wcswidth(line) for line in lines]))
