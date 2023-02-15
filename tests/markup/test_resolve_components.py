import pytest

from utils.importer import import_string
from textual.widgets import Button


def test_it_raises_an_exception_if_the_format_is_invalid():
    with pytest.raises(Exception):
        import_string("invalid")


def test_it_imports_an_object():
    assert Button == import_string("textual.widgets:Button")


def test_it_imports_a_nested_attribute_string():
    assert Button.DEFAULT_CSS == import_string("textual.widgets:Button.DEFAULT_CSS")


def test_it_raises_an_exception_if_the_module_is_invalid():
    with pytest.raises(ImportError):
        import_string("doesnt.exist:Button")


def test_it_raises_an_exception_if_the_attribute_is_invalid():
    with pytest.raises(Exception):
        import_string("textual.widgets:xyz")
