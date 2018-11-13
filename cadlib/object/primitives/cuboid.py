from numbers import Number
from warnings import warn

from cadlib.object import Object
from cadlib.scad import ScadObject


class Cuboid(Object):
    def __init__(self, size):
        if isinstance(size, Number):
            if size == 0:
                warn("size is 0")
            self._size = [size, size, size]
        elif len(size) == 3:
            if size[0] == 0: warn("x size is 0")
            if size[1] == 0: warn("y size is 0")
            if size[2] == 0: warn("z size is 0")
            self._size = size
        else:
            raise ValueError("Invalid size: {}".format(size))

    def __eq__(self, other):
        return (isinstance(other, Cuboid)
            and other._size == self._size)

    def __repr__(self):
        return f"Cuboid({self._size!r})"

    def __str__(self):
        w, d, h = self._size
        if w == d == h:
            return f"Cube with size {w}"
        else:
            return f"Cuboid with width {w}, depth {d}, and height {h}"

    def to_scad(self):
        # In OpenSCAD, it's called "cube" - even if the sides are not equal.
        return ScadObject("cube", [self._size], None, None)
