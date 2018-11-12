import math

from cadlib.util import Vector, Matrix, degree
from cadlib.scad import ScadObject
from cadlib.transform import Transform
from cadlib.util.number import to_number

class RotateAxisAngle(Transform):
    def __init__(self, axis, angle = None):
        axis = Vector.convert(axis, "axis", required_length=3)
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
        return "Rotate by {}° around {}".format(self._angle, self._axis)

    def __repr__(self):
        return f"RotateAxisAngle({self._axis!r}, {self._angle!r})"

    def inverse(self):
        return RotateAxisAngle(-self._axis, self._angle)

    def to_scad(self, target):
        children = [target] if target is not None else []
        return ScadObject("rotate", None, [("a", self._angle), ("v", list(self._axis))], children)

    def to_matrix(self):
        s = math.sin(self._angle * degree)
        c = math.cos(self._angle * degree)
        C = 1 - c
        x, y, z = self._axis.normalized()

        return Matrix.from_rows(
            [x*x*C + c  , x*y*C - z*s, x*z*C + y*s, 0],
            [y*x*C + z*s, y*y*C + c  , y*z*C - x*s, 0],
            [z*x*C - y*s, z*y*C + x*s, z*z*C + c  , 0],
            [0          , 0          , 0          , 1],
        )
