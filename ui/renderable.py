import abc
import typing
if typing.TYPE_CHECKING:
    from ui.screen import Screen
    from ui.static import Static, _Region

from .geometry import Dimensions, Point
from .styles import Styles


class Renderable(metaclass=abc.ABCMeta):
    """
    Attributes:
    """
    id: typing.Optional[str] = None
    position: typing.Optional[Point] = None
    dimensions: typing.Optional[Dimensions] = None
    screen: typing.Optional['Screen'] = None
    parent: typing.Optional[typing.Union['Screen', 'Static']] = None
    styles: Styles = Styles()

    _region: '_Region' = None
    _needs_parent_dimensions: bool = False

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
                hasattr(subclass, 'get_min_height_and_width') and
                callable(subclass.get_min_height_and_width) and
                hasattr(subclass, 'render') and
                callable(subclass.render)
                or NotImplemented
        )

    @abc.abstractmethod
    def get_min_height_and_width(self) -> Dimensions:
        raise NotImplementedError

    def get_max_height_and_width(self):
        return self.get_min_height_and_width()

    @abc.abstractmethod
    def render(self, position: Point):
        raise NotImplementedError

    def post_calculating_parent_dimensions_hook(self):
        pass

    def __debug_repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, position={self.position}, dimensions={self.get_min_height_and_width()})"
