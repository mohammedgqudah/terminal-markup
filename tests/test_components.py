import pytest

from textual.widgets import Button
from markup.components import import_component


def test_it_imports_components_using_full_path():
    assert Button == import_component("textual.widgets", "Button")


def test_it_imports_components_using_an_alias():
    assert Button == import_component("widgets", "Button")


def test_it_has_an_option_to_not_use_aliases():
    with pytest.raises(Exception):
        import_component("widgets", "Button", use_alias=False)
