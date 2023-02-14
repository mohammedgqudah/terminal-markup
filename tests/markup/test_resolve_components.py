import pytest

from markup.components import resolve_component
from textual.widgets import Button


def test_it_raises_an_exception_if_the_format_is_invalid():
    with pytest.raises(Exception):
        resolve_component("invalid")


def test_it_imports_an_object():
    assert Button == resolve_component("textual.widgets:Button")


def test_it_imports_a_nested_attribute_string():
    assert Button.DEFAULT_CSS == resolve_component("textual.widgets:Button.DEFAULT_CSS")


def test_it_raises_an_exception_if_the_module_is_invalid():
    with pytest.raises(ImportError):
        resolve_component("doesnt.exist:Button")


def test_it_raises_an_exception_if_the_attribute_is_invalid():
    with pytest.raises(Exception):
        resolve_component("textual.widgets:xyz")
