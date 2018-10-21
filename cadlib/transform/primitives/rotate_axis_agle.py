from cadlib.util import Vector
from cadlib.scad.scad import ScadObject
from cadlib.transform.transform import Transform
from cadlib.util.number import to_number


class RotateAxisAngle(Transform):
    def __init__(self, axis, angle = None):
        axis = Vector.convert(axis, "axis", 3)
        if axis.is_zero:
            raise ValueError("axis may not be zero-length")

        self._axis  = axis
        self._angle = to_number(angle, self._axis.length, "angle")

    def __eq__(self, other):
        if isinstance(other, RotateAxisAngle):
            return self._axis == other._axis and self._angle == other._angle
        else:
            return False

    def __str__(self):
        return "Rotate by {} degrees around {}".format(self._angle, self._axis)

    def to_scad(self, target):
        children = [target] if target is not None else []
        return ScadObject("rotate", None, [("a", self._angle), ("v", list(self._axis))], children)