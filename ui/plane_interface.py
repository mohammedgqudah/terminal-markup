import abc

from .geometry import Dimensions


class PlaneInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_height_and_width') and
                callable(subclass.get_height_and_width) or
                NotImplemented)

    @abc.abstractmethod
    def get_height_and_width(self) -> Dimensions:
        raise NotImplementedError
