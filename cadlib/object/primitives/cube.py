from numbers import Number

from cadlib.object import Object
from cadlib.scad import ScadObject


class Cube(Object):
    def __init__(self, size):
        if isinstance(size, Number):
            self._size = [size, size, size]
        elif len(size) == 3:
            self._size = size
        else:
            raise ValueError("Invalid size: {}".format(size))

    def __eq__(self, other):
        return isinstance(other, Cube) and other._size == self._size

    def __repr__(self):
        return f"Cube({self._size!r})"

    def to_scad(self):
        return ScadObject("cube", [self._size], None, None)