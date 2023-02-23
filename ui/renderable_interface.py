import abc

from .geometry import Dimensions, Point


class RenderableInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'render') and
                callable(subclass.render) or
                NotImplemented)

    @abc.abstractmethod
    def render(self, point: Point):
        raise NotImplementedError
