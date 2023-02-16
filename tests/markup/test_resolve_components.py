import pytest

from utils.importer import import_string, import_aliased_string
from textual.widgets import Button


def test_it_raises_an_exception_if_the_format_is_invalid():
    with pytest.raises(Exception):
        import_string("invalid", 'invalid')


def test_it_imports_an_object():
    assert Button == import_string("textual.widgets", "Button")


def test_it_accepts_attribute_as_a_second_argument():
    assert Button == import_string("textual.widgets", "Button")


def test_it_imports_a_nested_attribute_string():
    assert Button.DEFAULT_CSS == import_string("textual.widgets", "Button.DEFAULT_CSS")


def test_it_raises_an_exception_if_the_module_is_invalid():
    with pytest.raises(ImportError):
        import_string("doesnt.exist", "Button")


def test_it_raises_an_exception_if_the_attribute_is_invalid():
    with pytest.raises(Exception):
        import_string("textual.widgets", "xyz")


def test_it_aliases_a_module():
    assert Button == import_aliased_string("widgets", "Button", aliases={
        'widgets': 'textual.widgets'
    })


def test_it_aliases_an_attribute():
    assert Button == import_aliased_string("Button", aliases={
        'Button': 'textual.widgets:Button'
    })


def test_it_allows_using_other_aliases_in_an_alias():
    assert Button == import_aliased_string("widgets_y", "Button", aliases={
        'Button': 'widgets_y:Button',
        'x': 'textual.widgets',
        'widgets_y': 'x'
    })


def test_it_raises_an_exception_if_attribute_is_not_specified():
    with pytest.raises(Exception,
                       match='`textual.widgets` cannot be resolved, no alias found'):
        import_aliased_string("textual.widgets")


def test_it_raises_an_exception_if_attribute_is_m():
    with pytest.raises(Exception,
                       match='`textual` cannot be resolved, no alias found'):
        import_aliased_string("textual")
