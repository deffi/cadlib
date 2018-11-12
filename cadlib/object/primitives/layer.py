from warnings import warn

from cadlib.util.vector import Vector
from cadlib import infinity as inf
from cadlib.util import Z
from cadlib.object import Object
from cadlib.object.primitives import Cuboid
from cadlib.util.number import to_number


class Layer(Object):
    def __init__(self, normal, offset1, offset2):
        normal = Vector.convert(normal, "normal", required_length=3)
        if normal.is_zero:
            raise ValueError("Normal vector is zero")

        offset1 = to_number(offset1, "offset1")
        offset2 = to_number(offset2, "offset2")

        if offset1 == offset2: warn("offsets are equal")

        self._normal = normal
        self._offset1 = offset1
        self._offset2 = offset2

    def __eq__(self, other):
        if not isinstance(other, Layer): return False

        return other._normal == self._normal \
           and other._offset1 == self._offset1 \
           and other._offset2 == self._offset2

    def __repr__(self):
        return(f"Layer({self._normal!r}, {self._offset1!r}, {self._offset2!r})")

    def __str__(self):
        return f"Layer with normal {self._normal} from {self._offset1} to {self._offset2}"

    def to_scad(self):
        o1 = min(self._offset1, self._offset2)
        o2 = max(self._offset1, self._offset2)

        return Cuboid([inf, inf, o2 - o1]) \
            .translate([-inf / 2, -inf / 2, 0]) \
            .up(o1) \
            .rotate(frm = Z, to = self._normal, ignore_ambiguity = True) \
            .to_scad().comment(str(self))