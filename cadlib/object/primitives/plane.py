from cadlib.util.vector import Vector
from cadlib import infinity as inf
from cadlib.util import Z
from cadlib.object import Object
from cadlib.object.primitives import Cuboid
from cadlib.util.number import to_number


class Plane(Object):
    def __init__(self, normal, offset):
        normal = Vector.convert(normal, "normal", required_length=3)
        if normal.is_zero:
            raise ValueError("Normal vector is zero")

        offset = to_number(offset, "offset")

        self._normal = normal
        self._offset = offset

    def __eq__(self, other):
        return (isinstance(other, Plane)
            and other._normal == self._normal
            and other._offset == self._offset)

    def __repr__(self):
        return f"Plane({self._normal!r}, {self._offset!r})"

    def __str__(self):
        return f"Plane with normal {self._normal} and offset {self._offset}"

    def to_scad(self):
        return (Cuboid([inf, inf, inf])
            .translate([-inf / 2, -inf / 2, -inf])
            .up(self._offset)
            .rotate(frm = Z, to = self._normal, ignore_ambiguity = True)
            .to_scad().comment(str(self)))
