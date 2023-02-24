import abc
import typing
if typing.TYPE_CHECKING:
    from ui.screen import Screen
    from ui.static import Static

from .geometry import Dimensions, Point
from .styles import Styles


class Renderable(metaclass=abc.ABCMeta):
    id: typing.Optional[str] = None
    position: typing.Optional[Point] = None
    dimensions: typing.Optional[Dimensions] = None
    screen: typing.Optional['Screen'] = None
    parent: typing.Optional[typing.Union['Screen', 'Static']] = None
    styles: Styles = Styles()

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
                hasattr(subclass, 'get_height_and_width') and
                callable(subclass.get_height_and_width) and
                hasattr(subclass, 'render') and
                callable(subclass.render)
                or NotImplemented
        )

    @abc.abstractmethod
    def get_height_and_width(self) -> Dimensions:
        raise NotImplementedError

    @abc.abstractmethod
    def render(self, position: Point):
        raise NotImplementedError

    def __debug_repr__(self):
        return f"{__class__.__name__}(id={self.id}, position={self.position}, dimensions={self.get_height_and_width()})"
