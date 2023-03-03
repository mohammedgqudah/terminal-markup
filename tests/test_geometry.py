from terminal_markup.ui.geometry import ensure_value_in_range, get_text_height_and_width


def test_ensure_value_in_range():
    assert 2 == ensure_value_in_range(0, 5, value=2)
    assert 0 == ensure_value_in_range(0, 5, value=-1)
    assert 5 == ensure_value_in_range(0, 5, value=6)


def test_get_text_height_and_width():
    text = (
        "This is line one, it is uhhhh short\n"
        "this is line two, is is much longer. the next line include Japanese\n"
        "コンニチハ"
    )

    assert (3, 67) == get_text_height_and_width(text)

    text = (
        "Line one\n"
        "123456789コンニチハ"
    )

    assert (2, 19) == get_text_height_and_width(text)

