from numbers import Number
from warnings import warn

from cadlib.object import Object
from cadlib.scad import ScadObject
from cadlib.util import number


class Cuboid(Object):
    def __init__(self, x, y, z):
        x = number.convert(x, "x")
        y = number.convert(y, "y")
        z = number.convert(z, "z")

        if x == 0: warn("x size is 0")
        if y == 0: warn("y size is 0")
        if z == 0: warn("z size is 0")

        self._size = [x, y, z]

    def __eq__(self, other):
        return (isinstance(other, Cuboid)
            and other._size == self._size)

    def __repr__(self):
        x, y, z = self._size
        return f"Cuboid({x!r}, {y!r}, {z!r})"

    def __str__(self):
        w, d, h = self._size
        if w == d == h:
            return f"Cube with size {w}"
        else:
            return f"Cuboid with width {w}, depth {d}, and height {h}"

    def to_scad(self):
        # In OpenSCAD, it's called "cube" - even if the sides are not equal.
        return ScadObject("cube", [self._size], None, None)
